"""VesselMind command-line pipeline.

    vesselmind [--synthetic] synth | manifest FILE | ingest | clean | windows | baselines | plot-tracks

`--synthetic` redirects all data and results to data/_synthetic and results/_synthetic so
smoke-test artefacts can never mix with real experiment outputs.
"""

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import polars as pl

from vesselmind.config import load_config, project_path


class Workspace:
    def __init__(self, synthetic: bool, data_cfg: dict):
        def resolve(rel: str) -> Path:
            return project_path(rel) / "_synthetic" if synthetic else project_path(rel)

        p = data_cfg["paths"]
        self.synthetic = synthetic
        self.raw, self.interim = resolve(p["raw"]), resolve(p["interim"])
        self.processed, self.manifests = resolve(p["processed"]), resolve(p["manifests"])
        self.results = resolve("results")


def _git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=project_path("."),
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "uncommitted"


def _write_json(obj: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str) + "\n")
    print(f"wrote {path.relative_to(project_path('.'))}")


def cmd_synth(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.ingestion.synthetic import generate

    if not ws.synthetic:
        sys.exit("synth only writes to the synthetic workspace: run `vesselmind --synthetic synth`")
    out = generate(ws.raw / "SYNTHETIC_aisdk-2025-01-01.csv")
    print(f"wrote {out.relative_to(project_path('.'))}")


def cmd_manifest(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.ingestion.manifest import write_manifest

    src = data_cfg["source"]
    for f in map(Path, args.files):
        if (ws.manifests / f"{f.name}.json").exists() and not args.force:
            print(f"{f.name}: manifest exists")
            continue
        out = write_manifest(f, ws.manifests, src["provider"], src["url"], args.notes)
        print(f"wrote {out.relative_to(project_path('.'))}")


def cmd_ingest(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.ingestion.dma import ingest_file

    if args.files:
        files = [Path(f) for f in args.files]
    else:
        # One file per day: if both aisdk-X.zip and its extracted aisdk-X.csv exist, read the CSV
        by_stem: dict[str, Path] = {}
        for p in sorted(ws.raw.iterdir()):
            if p.suffix in (".zip", ".csv") and (p.stem not in by_stem or p.suffix == ".csv"):
                by_stem[p.stem] = p
        files = list(by_stem.values())
    if not files:
        sys.exit(f"no .zip/.csv files in {ws.raw}")
    log_path = ws.results / "tables" / "ingest_log.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {}
    for f in files:
        if (ws.interim / f"{f.name.split('.')[0]}.parquet").exists() and f.name in log and not args.force:
            print(f"{f.name}: already ingested (use --force to redo)")
            continue
        rec = ingest_file(f, ws.interim, data_cfg)
        log[f.name] = rec
        print(f"{f.name}: {rec['rows_in_aoi']:,} rows in AOI, "
              f"{rec['exact_duplicates_removed']:,} exact duplicates removed")
    _write_json(dict(sorted(log.items())), log_path)


# Columns used downstream; loading only these keeps multi-week runs within laptop memory
CLEAN_COLUMNS = ["t", "mmsi", "lat", "lon", "sog", "cog", "heading", "nav_status",
                 "ship_type", "length", "width", "draught"]


def cmd_clean(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.quality.checks import FLAG_COLS, HARD_FLAGS, add_flags, normalize_sentinels, quality_report
    from vesselmind.trajectories.segment import segment_tracks, vessel_table

    raw = pl.read_parquet(sorted(ws.interim.glob("*.parquet")), columns=CLEAN_COLUMNS)
    q, s = data_cfg["quality"], data_cfg["segmentation"]
    flagged = add_flags(normalize_sentinels(raw), q["max_implied_speed_kn"], q["max_plausible_sog_kn"])
    report = quality_report(raw, flagged)

    ws.processed.mkdir(parents=True, exist_ok=True)
    # Pre-segmentation clean points, kept so segmentation thresholds can be varied in `sensitivity`
    flagged.filter(~pl.any_horizontal(HARD_FLAGS)).drop(FLAG_COLS).write_parquet(ws.processed / "points_clean.parquet")
    tracks = segment_tracks(flagged, s["gap_s"], s["min_points"], s["min_duration_s"])
    report["segmentation"] = {
        **s,
        "segments": tracks["segment_id"].n_unique(),
        "vessels_with_segments": tracks["mmsi"].n_unique(),
        "rows_in_segments": len(tracks),
    }
    tracks.write_parquet(ws.processed / "tracks.parquet")
    vessel_table(tracks).write_parquet(ws.processed / "vessels.parquet")
    _write_json(report, ws.results / "tables" / "quality_report.json")
    print(json.dumps(report["flags"], indent=2))
    seg = report["segmentation"]
    print(f"{seg['segments']} segments from {seg['vessels_with_segments']} vessels")


def cmd_windows(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.evaluation.splits import assign_split, resolve_boundaries, split_summary
    from vesselmind.features.windows import build_windows

    w = exp_cfg["windows"]
    tracks = pl.read_parquet(ws.processed / "tracks.parquet")
    hist, fut, meta = build_windows(tracks, w)
    split_cfg = exp_cfg["split"]
    if ws.synthetic:  # synthetic data has its own dates: always use proportional blocks
        split_cfg = {**split_cfg, "train_end": None, "val_end": None}
    train_end, val_end = resolve_boundaries(meta, split_cfg)
    meta = assign_split(meta, train_end, val_end, w["step_s"], w["obs_steps"], w["future_steps"])
    vessels = pl.read_parquet(ws.processed / "vessels.parquet").drop("n_points")
    meta = meta.join(vessels, on="mmsi", how="left", maintain_order="left")

    np.savez_compressed(ws.processed / "windows.npz", hist=hist, fut=fut, sample_id=meta["sample_id"].to_numpy())
    meta.write_parquet(ws.processed / "windows_meta.parquet")
    summary = split_summary(meta, train_end, val_end)
    summary["boundaries_source"] = "explicit" if split_cfg.get("train_end") else "auto_fractions (PROVISIONAL)"
    _write_json(summary, ws.results / "tables" / "split_summary.json")
    print(json.dumps(summary["counts"], indent=2))


def cmd_baselines(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.evaluation.metrics import per_sample_metrics, step_errors_m, summarize
    from vesselmind.models import baselines
    from vesselmind.viz.plots import plot_error_vs_horizon

    if args.split == "test" and not args.confirm_test:
        sys.exit("Test split is locked. Freeze hypotheses first, then pass --confirm-test (one final run).")
    w, b, ev = exp_cfg["windows"], exp_cfg["baselines"], exp_cfg["evaluation"]
    arrays = np.load(ws.processed / "windows.npz")
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    mask = (meta["split"] == args.split).to_numpy()
    if not mask.any():
        sys.exit(f"no windows in split '{args.split}'")
    hist, fut, m = arrays["hist"][mask], arrays["fut"][mask], meta.filter(pl.col("split") == args.split)
    groups = m["mmsi"].to_numpy()

    # Tune the damped-CTRV time constant on TRAIN windows only (never on the split being evaluated)
    train_idx = np.flatnonzero((meta["split"] == "train").to_numpy())
    rng = np.random.default_rng(ev["seed"])
    train_idx = rng.choice(train_idx, size=min(len(train_idx), b["tuning_max_windows"]), replace=False)
    h_tr, f_tr = arrays["hist"][train_idx], arrays["fut"][train_idx]
    damped = lambda h, tau: baselines.ctrv_damped(  # noqa: E731
        h, w["future_steps"], w["step_s"], tau, b["ctrv_turn_window_steps"], b["ctrv_max_turn_rate_deg_s"],
        b["ctrv_min_sog_kn"])
    tuning = {str(tau): float(step_errors_m(damped(h_tr, tau), f_tr).mean()) for tau in b["ctrv_damped_tau_grid_s"]}
    best_tau = float(min(tuning, key=tuning.get))
    print(f"damped CTRV tau tuned on {len(train_idx):,} train windows: ADE by tau {tuning} -> tau={best_tau:g}s")

    models = {
        "persistence": lambda h: baselines.persistence(h, w["future_steps"], w["step_s"]),
        "cv": lambda h: baselines.cv(h, w["future_steps"], w["step_s"]),
        "ctrv": lambda h: baselines.ctrv(h, w["future_steps"], w["step_s"], b["ctrv_turn_window_steps"],
                                         b["ctrv_max_turn_rate_deg_s"], b["ctrv_min_sog_kn"]),
        "ctrv_damped": lambda h: damped(h, best_tau),
    }
    run_dir = ws.results / "runs" / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}_baselines_{args.split}"
    rows, summary, step_err = [], {}, {}
    for name, fn in models.items():
        err = step_errors_m(fn(hist), fut)
        step_err[name] = err
        per = per_sample_metrics(err, w["step_s"], w["horizons_min"])
        summary[name] = {k: summarize(v, groups, ev["n_bootstrap"], ev["seed"]) for k, v in per.items()}
        rows.append(pl.DataFrame({"sample_id": m["sample_id"], "model": name, **per}))

    # Paired differences vs CV on identical windows (negative = better than CV), vessel-grouped bootstrap
    by_model = {r["model"][0]: r for r in rows}
    paired = {
        name: {k: summarize(by_model[name][k].to_numpy() - by_model["cv"][k].to_numpy(), groups,
                            ev["n_bootstrap"], ev["seed"]) for k in ("ade_m", "fde_m")}
        for name in by_model if name != "cv"
    }

    run_dir.mkdir(parents=True, exist_ok=True)
    pl.concat(rows).write_parquet(run_dir / "per_sample.parquet")
    _write_json({"split": args.split, "git": _git_hash(), "config": exp_cfg, "metrics": summary,
                 "paired_vs_cv": paired, "ctrv_damped_tuning": {"ade_by_tau_train": tuning, "best_tau_s": best_tau}},
                run_dir / "summary.json")

    lines = ["| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |", "|---|---|---|---|---|---|"]
    for name, mets in summary.items():
        for k, s in mets.items():
            lines.append(f"| {name} | {k} | {s['mean']:.0f} ({s['ci95_lo']:.0f}–{s['ci95_hi']:.0f}) | "
                         f"{s['median']:.0f} | {s['p90']:.0f} | {s['n_samples']} / {s['n_vessels']} vessels |")
    lines += ["", f"Paired difference vs CV on identical windows (model − CV, m; negative = better). "
              f"Damped-CTRV tau = {best_tau:g} s, tuned on train.", "",
              "| model | ΔADE (95% CI) | ΔFDE (95% CI) |", "|---|---|---|"]
    for name, d in paired.items():
        a, f = d["ade_m"], d["fde_m"]
        lines.append(f"| {name} | {a['mean']:+.0f} ({a['ci95_lo']:+.0f} to {a['ci95_hi']:+.0f}) | "
                     f"{f['mean']:+.0f} ({f['ci95_lo']:+.0f} to {f['ci95_hi']:+.0f}) |")
    table = ws.results / "tables" / f"baselines_{args.split}.md"
    table.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    fig = plot_error_vs_horizon(step_err, w["step_s"], ws.results / "figures" / f"baselines_error_{args.split}.png",
                                f"Baseline error vs lead time ({args.split}{', SYNTHETIC' if ws.synthetic else ''})")
    print(f"wrote {fig.relative_to(project_path('.'))}")


def cmd_plot_tracks(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.viz.plots import plot_tracks

    tracks = pl.read_parquet(ws.processed / "tracks.parquet")
    title = f"{data_cfg['aoi']['name']}{' (SYNTHETIC)' if ws.synthetic else ''}"
    out = plot_tracks(tracks, ws.results / "figures" / "tracks_overview.png", title)
    print(f"wrote {out.relative_to(project_path('.'))}")


def cmd_regime_eda(ws: Workspace, data_cfg, exp_cfg, args):
    from vesselmind.viz.regime_eda import regime_eda

    w = exp_cfg["windows"]
    hist = np.load(ws.processed / "windows.npz")["hist"]
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    runs = sorted((ws.results / "runs").glob("*_baselines_val"))
    per_sample = pl.read_parquet(runs[-1] / "per_sample.parquet") if runs else None
    summary = regime_eda(hist, meta, per_sample, w["step_s"], ws.results / "figures")
    _write_json(summary, ws.results / "tables" / "regime_eda.json")
    print(json.dumps(summary, indent=2, default=str))


def cmd_sensitivity(ws: Workspace, data_cfg, exp_cfg, args):
    """E0: how segmentation gap and window gap thresholds change retained data (counts only, no model fitting)."""
    from vesselmind.features.windows import build_windows
    from vesselmind.trajectories.segment import segment_tracks

    s, w = data_cfg["segmentation"], exp_cfg["windows"]
    points = pl.read_parquet(ws.processed / "points_clean.parquet")
    rows = []
    for gap_s in args.gap_s:
        tracks = segment_tracks(points, gap_s, s["min_points"], s["min_duration_s"])
        for max_gap in args.window_gap_s:
            _, _, meta = build_windows(tracks, {**w, "max_gap_s": max_gap})
            rows.append({"segment_gap_s": gap_s, "window_max_gap_s": max_gap,
                         "segments": tracks["segment_id"].n_unique(), "vessels": tracks["mmsi"].n_unique(),
                         "points_in_segments": len(tracks), "windows": len(meta),
                         "window_vessels": meta["mmsi"].n_unique()})
            print(rows[-1])
    df = pl.DataFrame(rows)
    df.write_csv(ws.results / "tables" / "sensitivity_gaps.csv")
    print(f"wrote {(ws.results / 'tables' / 'sensitivity_gaps.csv').relative_to(project_path('.'))}")


def cmd_gbm(ws: Workspace, data_cfg, exp_cfg, args):
    """E3/E4: residual GBM with feature-set ablation. Trains on train, evaluates on `--split` (val by default)."""
    import time

    from vesselmind.evaluation.metrics import per_sample_metrics, step_errors_m, summarize
    from vesselmind.features.motion import SHIP_GROUP_CODES, build_features
    from vesselmind.models import baselines
    from vesselmind.models.gbm import ResidualGBM
    from vesselmind.viz.regime_eda import TURN_BINS, past_turn_rate_deg_min

    if args.split == "test" and not args.confirm_test:
        sys.exit("Test split is locked. Freeze hypotheses first, then pass --confirm-test (one final run).")
    w, g, ev = exp_cfg["windows"], exp_cfg["gbm"], exp_cfg["evaluation"]
    step, n_fut = w["step_s"], w["future_steps"]
    knots = [int(k * 60 / step) for k in g["knots_min"]]
    arrays = np.load(ws.processed / "windows.npz")
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    tr = (meta["split"] == "train").to_numpy()
    ev_mask = (meta["split"] == args.split).to_numpy()
    h_tr, f_tr, m_tr = arrays["hist"][tr], arrays["fut"][tr], meta.filter(pl.col("split") == "train")
    h_ev, f_ev, m_ev = arrays["hist"][ev_mask], arrays["fut"][ev_mask], meta.filter(pl.col("split") == args.split)
    if not tr.any() or not ev_mask.any():
        sys.exit(f"empty split: {tr.sum()} train / {ev_mask.sum()} {args.split} windows; rerun `windows`")
    groups = m_ev["mmsi"].to_numpy()

    errs = {"cv": step_errors_m(baselines.cv(h_ev, n_fut, step), f_ev)}
    fit_info = {}
    for name, sets in g["feature_sets"].items():
        X_tr, cols = build_features(h_tr, m_tr, step, sets)
        X_ev, _ = build_features(h_ev, m_ev, step, sets)
        keep = ~np.isnan(X_tr).all(axis=0)  # a feature with no training values cannot be used
        dropped = [c for c, k in zip(cols, keep, strict=True) if not k]
        X_tr, X_ev, cols = X_tr[:, keep], X_ev[:, keep], [c for c, k in zip(cols, keep, strict=True) if k]
        if dropped:
            print(f"{name}: dropped all-missing features {dropped}")
        cat = [c == "ship_group" for c in cols] if "ship_group" in cols else None
        t0 = time.time()
        model = ResidualGBM(knots, categorical=cat, seed=g["seed"]).fit(X_tr, h_tr, f_tr, step)
        errs[name] = step_errors_m(model.predict(X_ev, h_ev, step, n_fut), f_ev)
        fit_info[name] = {"features": cols, "dropped_all_missing": dropped,
                          "fit_s": round(time.time() - t0, 1), "n_iter": model.n_iter()}
        print(f"{name}: fitted in {fit_info[name]['fit_s']} s, {args.split} ADE {errs[name].mean():.0f} m, "
              f"FDE {errs[name][:, -1].mean():.0f} m")

    per = {k: per_sample_metrics(e, step, w["horizons_min"]) for k, e in errs.items()}
    summary = {k: {mk: summarize(v, groups, ev["n_bootstrap"], ev["seed"]) for mk, v in p.items()}
               for k, p in per.items()}

    def paired(a, b):
        return {mk: summarize(per[b][mk] - per[a][mk], groups, ev["n_bootstrap"], ev["seed"])
                for mk in ("ade_m", "fde_m")}

    names = list(g["feature_sets"])
    comparisons = {f"{n} - cv": paired("cv", n) for n in names}
    comparisons.update({f"{n} - A_motion": paired("A_motion", n) for n in names if n != "A_motion"})

    turn = past_turn_rate_deg_min(h_ev, step)
    group_names = {v: k for k, v in SHIP_GROUP_CODES.items()}
    sg, _ = build_features(h_ev, m_ev, step, ["vessel"])
    strata = pl.DataFrame({
        "turn_bin": pl.Series(turn).cut(TURN_BINS[1:-1], left_closed=True).cast(pl.String),
        "ship_group": [group_names.get(c, "unknown") if not np.isnan(c) else "unknown" for c in sg[:, 0]],
        **{k: e[:, -1] for k, e in errs.items()},
    })
    by_turn = strata.group_by("turn_bin").agg(n=pl.len(), **{k: pl.col(k).mean() for k in errs}).sort("turn_bin")
    by_group = strata.group_by("ship_group").agg(n=pl.len(), **{k: pl.col(k).mean() for k in errs}).sort("n",
                                                                                                    descending=True)
    run_dir = ws.results / "runs" / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}_gbm_{args.split}"
    run_dir.mkdir(parents=True, exist_ok=True)
    per_sample = pl.DataFrame({"sample_id": m_ev["sample_id"], **{f"fde_{k}": e[:, -1] for k, e in errs.items()},
                               **{f"ade_{k}": e.mean(axis=1) for k, e in errs.items()}})
    per_sample.write_parquet(run_dir / "per_sample.parquet")
    _write_json({"split": args.split, "git": _git_hash(), "config": exp_cfg["gbm"], "fit": fit_info,
                 "metrics": summary, "paired": comparisons, "fde_by_turn_bin": by_turn.to_dicts(),
                 "fde_by_ship_group": by_group.to_dicts()}, run_dir / "summary.json")

    fmt = lambda s: f"{s['mean']:+.0f} ({s['ci95_lo']:+.0f} to {s['ci95_hi']:+.0f})"  # noqa: E731
    lines = [f"# Residual GBM context ablation ({args.split})", "",
             "| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |", "|---|---|---|---|---|"]
    for k, s in summary.items():
        lines.append(f"| {k} | {s['ade_m']['mean']:.0f} ({s['ade_m']['ci95_lo']:.0f}–{s['ade_m']['ci95_hi']:.0f}) | "
                     f"{s['fde_m']['mean']:.0f} ({s['fde_m']['ci95_lo']:.0f}–{s['fde_m']['ci95_hi']:.0f}) | "
                     f"{s['err_5min_m']['mean']:.0f} | {s['err_10min_m']['mean']:.0f} |")
    lines += ["", "Paired differences on identical windows (m, negative = first model better), vessel bootstrap:", "",
              "| comparison | ΔADE | ΔFDE |", "|---|---|---|"]
    lines += [f"| {c} | {fmt(d['ade_m'])} | {fmt(d['fde_m'])} |" for c, d in comparisons.items()]
    for title, tab in (("past turn rate (°/min)", by_turn), ("ship group", by_group)):
        lines += ["", f"Mean FDE@20 min (m) by {title}:", "", "| " + " | ".join(tab.columns) + " |",
                  "|" + "---|" * len(tab.columns)]
        lines += ["| " + " | ".join(f"{v:.0f}" if isinstance(v, float) else str(v) for v in r) + " |"
                  for r in tab.iter_rows()]
    out = ws.results / "tables" / f"gbm_ablation_{args.split}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vesselmind")
    ap.add_argument("--synthetic", action="store_true", help="use the isolated synthetic workspace")
    ap.add_argument("--data-config", default="configs/data.yaml")
    ap.add_argument("--exp-config", default="configs/experiment.yaml")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("synth", help="generate synthetic DMA-format AIS (smoke tests only)")
    p = sub.add_parser("manifest", help="record provenance + checksum of raw files")
    p.add_argument("files", nargs="+")
    p.add_argument("--notes", default="")
    p.add_argument("--force", action="store_true", help="overwrite existing manifests")
    p = sub.add_parser("ingest", help="raw zip/csv -> AOI-filtered, de-duplicated interim parquet")
    p.add_argument("files", nargs="*")
    p.add_argument("--force", action="store_true", help="re-ingest files already in the ingest log")
    sub.add_parser("clean", help="quality flags, report, segmentation")
    sub.add_parser("windows", help="build prediction windows and time-block split")
    p = sub.add_parser("baselines", help="evaluate persistence / CV / CTRV")
    p.add_argument("--split", default="val", choices=["train", "val", "test"])
    p.add_argument("--confirm-test", action="store_true")
    sub.add_parser("plot-tracks", help="overview map of segmented tracks")
    p = sub.add_parser("gbm", help="E3/E4: residual GBM context ablation (train -> val)")
    p.add_argument("--split", default="val", choices=["val", "test"])
    p.add_argument("--confirm-test", action="store_true")
    p = sub.add_parser("sensitivity", help="E0: retained data under different gap thresholds")
    p.add_argument("--gap-s", type=int, nargs="+", default=[600, 1200, 1800])
    p.add_argument("--window-gap-s", type=int, nargs="+", default=[120, 180, 300])
    sub.add_parser("regime-eda", help="figures supporting the manoeuvring-regime definition (train+val only)")

    args = ap.parse_args(argv)
    data_cfg, exp_cfg = load_config(args.data_config), load_config(args.exp_config)
    ws = Workspace(args.synthetic, data_cfg)
    handlers = {
        "synth": cmd_synth, "manifest": cmd_manifest, "ingest": cmd_ingest, "clean": cmd_clean,
        "windows": cmd_windows, "baselines": cmd_baselines, "plot-tracks": cmd_plot_tracks,
        "regime-eda": cmd_regime_eda, "sensitivity": cmd_sensitivity, "gbm": cmd_gbm,
    }
    handlers[args.cmd](ws, data_cfg, exp_cfg, args)


if __name__ == "__main__":
    main()
