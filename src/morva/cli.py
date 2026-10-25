"""MORVA command-line pipeline.

    morva [--synthetic] synth | manifest FILE | ingest | clean | windows | baselines | plot-tracks

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

from morva.config import load_config, project_path


class Workspace:
    def __init__(self, synthetic: bool, data_cfg: dict, exp_cfg: dict | None = None):
        def resolve(rel: str) -> Path:
            return project_path(rel) / "_synthetic" if synthetic else project_path(rel)

        from morva.ingestion.sources import sources

        p = data_cfg["paths"]
        self.synthetic = synthetic
        # One raw folder per data source (V1/V2: the DMA folder only)
        self.raw_dirs = {name: resolve(s["raw"]) for name, s in sources(data_cfg).items()}
        self.raw = next(iter(self.raw_dirs.values()))
        self.interim = resolve(p["interim"])
        self.processed, self.manifests = resolve(p["processed"]), resolve(p["manifests"])
        # Each study version writes to its own results tree, so V2 never overwrites V1 tables and figures
        self.results = resolve((exp_cfg or {}).get("results_dir", "results"))


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


def _eval_mask(meta: pl.DataFrame, args) -> tuple[np.ndarray, str]:
    """Windows of `--split`, optionally restricted to one `--region`; returns (mask, run-name suffix)."""
    mask = meta["split"] == args.split
    if getattr(args, "region", None):
        if "region" not in meta.columns:
            sys.exit("--region needs windows built with region tags; rerun `clean` and `windows`")
        mask &= meta["region"] == args.region
    return mask.to_numpy(), f"_{args.region}" if getattr(args, "region", None) else ""


def _check_test_lock(args) -> None:
    from morva.evaluation.splits import LOCKED_SPLITS

    if args.split in LOCKED_SPLITS and not args.confirm_test:
        sys.exit(f"Split '{args.split}' is locked. Freeze hypotheses first, then pass --confirm-test (one final run).")


def cmd_synth(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.ingestion.synthetic import generate, generate_marinecadastre

    if not ws.synthetic:
        sys.exit("synth only writes to the synthetic workspace: run `morva --synthetic synth`")
    out = generate(ws.raw / "SYNTHETIC_aisdk-2025-01-01.csv")
    print(f"wrote {out.relative_to(project_path('.'))}")
    if "marinecadastre" in ws.raw_dirs:  # V3 config: also a synthetic US day
        out = generate_marinecadastre(ws.raw_dirs["marinecadastre"] / "SYNTHETIC_ais-2025-01-01.csv.zst")
        print(f"wrote {out.relative_to(project_path('.'))}")


def cmd_manifest(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.ingestion.manifest import write_manifest
    from morva.ingestion.sources import sources

    all_sources = sources(data_cfg)
    name = args.source or next(iter(all_sources))
    if name not in all_sources:
        sys.exit(f"unknown source '{name}'; configured: {sorted(all_sources)}")
    src = all_sources[name]
    for f in map(Path, args.files):
        if (ws.manifests / f"{f.name}.json").exists() and not args.force:
            print(f"{f.name}: manifest exists")
            continue
        out = write_manifest(f, ws.manifests, src["provider"], src["url"], args.notes)
        print(f"wrote {out.relative_to(project_path('.'))}")


RAW_SUFFIXES = {"dma": (".zip", ".csv"), "marinecadastre_2025": (".zst", ".csv")}


def _raw_files(raw_dir: Path, fmt: str) -> list[Path]:
    """One file per day: prefer an extracted .csv over its compressed original."""
    by_stem: dict[str, Path] = {}
    for p in sorted(raw_dir.iterdir()) if raw_dir.exists() else []:
        stem = p.name.split(".")[0]
        if p.is_file() or p.is_symlink():
            if p.name.endswith(RAW_SUFFIXES[fmt]) and (stem not in by_stem or p.suffix == ".csv"):
                by_stem[stem] = p
    return list(by_stem.values())


def cmd_ingest(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.ingestion import dma, marinecadastre
    from morva.ingestion.sources import regions, sources

    readers = {"dma": dma.ingest_file, "marinecadastre_2025": marinecadastre.ingest_file}
    log_path = ws.results / "tables" / "ingest_log.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {}
    n_files = 0
    for name, src in sources(data_cfg).items():
        boxes = [r for r in regions(data_cfg) if r["source"] == name]
        if not boxes:
            continue
        files = [Path(f) for f in args.files] if args.files else _raw_files(ws.raw_dirs[name], src["format"])
        n_files += len(files)
        for f in files:
            if (ws.interim / f"{f.name.split('.')[0]}.parquet").exists() and f.name in log and not args.force:
                print(f"{f.name}: already ingested (use --force to redo)")
                continue
            rec = readers[src["format"]](f, ws.interim, src, boxes)
            log[f.name] = rec
            print(f"{f.name}: {rec['rows_in_aoi']:,} rows in AOIs {rec['rows_written_by_region']}, "
                  f"{rec['exact_duplicates_removed']:,} exact duplicates removed")
        if args.files:
            break  # explicit files belong to the first source
    if not n_files:
        sys.exit(f"no raw files in {sorted(str(d) for d in ws.raw_dirs.values())}")
    _write_json(dict(sorted(log.items())), log_path)


# Columns used downstream; loading only these keeps multi-week runs within laptop memory
CLEAN_COLUMNS = ["t", "mmsi", "lat", "lon", "sog", "cog", "heading", "nav_status",
                 "ship_type", "length", "width", "draught", "region"]


def _calendar_of(data_cfg: dict) -> dict[str, str]:
    """Region -> split calendar (V3 configs only)."""
    from morva.ingestion.sources import regions

    return {r["name"]: r["calendar"] for r in regions(data_cfg)}


def _map_periods(ws: Workspace, data_cfg, exp_cfg, meta: pl.DataFrame) -> dict[str, tuple]:
    """Region -> (start, end) of the period whose traffic builds its flow map: the training block of its calendar
    (V3), or everything before the train/val boundary (V1/V2)."""
    from morva.evaluation.splits import resolve_boundaries, resolve_calendars
    from morva.ingestion.sources import regions

    split_cfg = exp_cfg["split"]
    if "calendars" in split_cfg:
        bounds = resolve_calendars(meta, split_cfg, _calendar_of(data_cfg), synthetic=ws.synthetic)
        return {r: (b["train_start"], b["train_end"]) for r, b in bounds.items()}
    if ws.synthetic:
        split_cfg = {**split_cfg, "train_end": None, "val_end": None, "test_end": None}
    train_end, _, _ = resolve_boundaries(meta, split_cfg)
    return {r["name"]: (None, train_end) for r in regions(data_cfg)}


def _region_names(data_cfg: dict) -> list[str]:
    from morva.ingestion.sources import regions

    return [r["name"] for r in regions(data_cfg)]


def _track_files(ws: Workspace) -> list[Path]:
    files = sorted((ws.processed / "tracks").glob("*.parquet"))
    if not files:
        sys.exit(f"no track files in {ws.processed / 'tracks'}; run `clean`")
    return files


def cmd_clean(ws: Workspace, data_cfg, exp_cfg, args):
    """Quality flags and segmentation, one region at a time so peak memory stays at one area's size.

    Writes tracks/<region>.parquet (segment ids unique across regions), vessels.parquet keyed by (mmsi, region),
    and points_clean.parquet for the home AOI only (used by the V1 `sensitivity` analysis).
    """
    from morva.quality.checks import FLAG_COLS, HARD_FLAGS, add_flags, normalize_sentinels, quality_report
    from morva.trajectories.segment import segment_tracks, vessel_table

    interim = sorted(ws.interim.glob("*.parquet"))
    q, s = data_cfg["quality"], data_cfg["segmentation"]
    home = data_cfg["aoi"]["name"]
    track_dir = ws.processed / "tracks"
    track_dir.mkdir(parents=True, exist_ok=True)
    for old in track_dir.glob("*.parquet"):
        old.unlink()
    reports, vessels, next_segment = {}, [], 0
    for region in _region_names(data_cfg):
        raw = pl.scan_parquet(interim).filter(pl.col("region") == region).select(CLEAN_COLUMNS).collect()
        if raw.is_empty():
            print(f"{region}: no rows")
            continue
        flagged = add_flags(normalize_sentinels(raw), q["max_implied_speed_kn"], q["max_plausible_sog_kn"])
        report = quality_report(raw, flagged)
        del raw
        if region == home:  # pre-segmentation clean points, so `sensitivity` can vary segmentation thresholds
            flagged.filter(~pl.any_horizontal(HARD_FLAGS)).drop(FLAG_COLS).write_parquet(
                ws.processed / "points_clean.parquet")
        tracks = segment_tracks(flagged, s["gap_s"], s["min_points"], s["min_duration_s"])
        del flagged
        tracks = tracks.with_columns(pl.col("segment_id").rank("dense").cast(pl.Int64) - 1 + next_segment)
        next_segment = int(tracks["segment_id"].max()) + 1 if len(tracks) else next_segment
        report["segmentation"] = {
            **s,
            "segments": tracks["segment_id"].n_unique(),
            "vessels_with_segments": tracks["mmsi"].n_unique(),
            "rows_in_segments": len(tracks),
        }
        tracks.write_parquet(track_dir / f"{region}.parquet")
        vessels.append(vessel_table(tracks).with_columns(region=pl.lit(region)))
        reports[region] = report
        seg = report["segmentation"]
        print(f"{region}: {seg['segments']} segments from {seg['vessels_with_segments']} vessels; "
              f"flags {report['flags']}")
        del tracks
    pl.concat(vessels, how="diagonal").write_parquet(ws.processed / "vessels.parquet")
    # Home report at top level (same keys as V1); transfer waterways reported separately
    out = {**reports.get(home, {}), "transfer_regions": {r: v for r, v in reports.items() if r != home}}
    _write_json(out, ws.results / "tables" / "quality_report.json")


def cmd_windows(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.evaluation.splits import (
        assign_calendar_split,
        assign_split,
        resolve_boundaries,
        resolve_calendars,
        split_summary,
    )
    from morva.features.windows import build_windows

    w = exp_cfg["windows"]
    parts = []
    for f in _track_files(ws):  # one region at a time; segments never cross regions
        try:
            parts.append(build_windows(pl.read_parquet(f), w))
        except ValueError:
            print(f"{f.stem}: no valid windows")
    hist = np.concatenate([p[0] for p in parts])
    fut = np.concatenate([p[1] for p in parts])
    meta = pl.concat([p[2] for p in parts]).with_columns(sample_id=pl.int_range(pl.len(), dtype=pl.Int64))
    split_cfg = exp_cfg["split"]
    home = data_cfg["aoi"]["name"]
    if "calendars" in split_cfg:  # V3: each region follows its own calendar, with a calibration block
        bounds = resolve_calendars(meta, split_cfg, _calendar_of(data_cfg), synthetic=ws.synthetic)
        meta = assign_calendar_split(meta, bounds, home, w["step_s"], w["obs_steps"], w["future_steps"])
        summary_args = {"boundaries": bounds}
        source = "synthetic fractions (PROVISIONAL)" if ws.synthetic else "calendars"
    else:
        if ws.synthetic:  # synthetic data has its own dates: always use proportional blocks
            split_cfg = {**split_cfg, "train_end": None, "val_end": None, "test_end": None}
        train_end, val_end, test_end = resolve_boundaries(meta, split_cfg)
        meta = assign_split(meta, train_end, val_end, w["step_s"], w["obs_steps"], w["future_steps"],
                            test_end=test_end, home_region=home)
        summary_args = {"train_end": train_end, "val_end": val_end, "test_end": test_end}
        source = "explicit" if split_cfg.get("train_end") else "auto_fractions (PROVISIONAL)"
    vessels = pl.read_parquet(ws.processed / "vessels.parquet").drop("n_points")
    meta = meta.join(vessels, on=["mmsi", "region"], how="left", maintain_order="left")

    np.savez_compressed(ws.processed / "windows.npz", hist=hist, fut=fut, sample_id=meta["sample_id"].to_numpy())
    meta.write_parquet(ws.processed / "windows_meta.parquet")
    summary = split_summary(meta, **summary_args)
    summary["boundaries_source"] = source
    _write_json(summary, ws.results / "tables" / "split_summary.json")
    print(json.dumps(summary["counts"], indent=2))


def cmd_fairway(ws: Workspace, data_cfg, exp_cfg, args):
    """V2: build traffic-flow maps per region from the training period and fairway features for every window."""
    from morva.features.fairway import FlowMaps, fairway_feature_names, fairway_features
    from morva.ingestion.sources import regions

    f_cfg, w = exp_cfg["fairway"], exp_cfg["windows"]
    hist = np.load(ws.processed / "windows.npz")["hist"]
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    periods = _map_periods(ws, data_cfg, exp_cfg, meta)
    parts = []
    if "calendars" in exp_cfg["split"]:
        summary = {"map_periods_utc": {r: [str(a), str(b)] for r, (a, b) in periods.items()}, "config": f_cfg,
                   "regions": {}}
    else:  # V2 layout, unchanged
        summary = {"map_period_end_utc": str(next(iter(periods.values()))[1]), "config": f_cfg, "regions": {}}
    for box in regions(data_cfg):
        path = ws.processed / "tracks" / f"{box['name']}.parquet"
        sel = (meta["region"] == box["name"]).to_numpy()
        if not path.exists() or not sel.any() or box["name"] not in periods:
            continue
        map_start, map_end = periods[box["name"]]
        in_period = pl.col("t") < map_end
        if map_start is not None:
            in_period &= pl.col("t") >= map_start
        points = pl.read_parquet(path, columns=["t", "mmsi", "lat", "lon", "sog", "cog"]).filter(in_period)
        maps = FlowMaps.build(points, box, f_cfg)
        m = meta.filter(pl.Series(sel))
        feats = fairway_features(hist[sel], m["t0"], maps, w["step_s"], w["future_steps"], f_cfg)
        df = pl.DataFrame({"sample_id": m["sample_id"], **feats})
        parts.append(df)
        cover = df.with_columns(split=m["split"]).group_by("split").agg(
            windows=pl.len(), with_flow=pl.col("flow_hdg_0").is_not_nan().sum(),
            median_abs_offset_m=pl.col("flow_offset_0").abs().median(),
            median_abs_hdg_deg=pl.col("flow_hdg_0").abs().median()).sort("split")
        summary["regions"][box["name"]] = {"map_points": maps.n_points, "map_days": len(maps.by_day),
                                           "grid": [maps.nx, maps.ny, maps.nb], "by_split": cover.to_dicts()}
        print(f"{box['name']}: {maps.n_points:,} map points over {len(maps.by_day)} days")
        print(cover)
        del maps
    out = pl.concat(parts).sort("sample_id")
    assert out.columns[1:] == fairway_feature_names(f_cfg["ahead_min"])
    out.write_parquet(ws.processed / "fairway_features.parquet")
    _write_json(summary, ws.results / "tables" / "fairway_summary.json")


def cmd_baselines(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.evaluation.metrics import per_sample_metrics, step_errors_m, summarize
    from morva.models import baselines
    from morva.viz.plots import plot_error_vs_horizon

    _check_test_lock(args)
    w, b, ev = exp_cfg["windows"], exp_cfg["baselines"], exp_cfg["evaluation"]
    arrays = np.load(ws.processed / "windows.npz")
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    mask, run_name = _eval_mask(meta, args)
    run_name = f"{args.split}{run_name}"
    if not mask.any():
        sys.exit(f"no windows in '{run_name}'")
    hist, fut, m = arrays["hist"][mask], arrays["fut"][mask], meta.filter(pl.Series(mask))
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
    kf = lambda h, q: baselines.kalman_cv(h, w["future_steps"], w["step_s"], q)  # noqa: E731
    kf_tuning = {str(q): float(step_errors_m(kf(h_tr, q), f_tr).mean()) for q in b["kalman_q_grid"]}
    best_q = float(min(kf_tuning, key=kf_tuning.get))
    print(f"Kalman-CV q tuned on train: ADE by q {kf_tuning} -> q={best_q:g}")

    models = {
        "persistence": lambda h: baselines.persistence(h, w["future_steps"], w["step_s"]),
        "cv": lambda h: baselines.cv(h, w["future_steps"], w["step_s"]),
        "ctrv": lambda h: baselines.ctrv(h, w["future_steps"], w["step_s"], b["ctrv_turn_window_steps"],
                                         b["ctrv_max_turn_rate_deg_s"], b["ctrv_min_sog_kn"]),
        "ctrv_damped": lambda h: damped(h, best_tau),
        "kalman_cv": lambda h: kf(h, best_q),
    }
    run_dir = ws.results / "runs" / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}_baselines_{run_name}"
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
    _write_json({"split": args.split, "region": args.region, "git": _git_hash(), "config": exp_cfg, "metrics": summary,
                 "paired_vs_cv": paired, "ctrv_damped_tuning": {"ade_by_tau_train": tuning, "best_tau_s": best_tau},
                 "kalman_tuning": {"ade_by_q_train": kf_tuning, "best_q": best_q}},
                run_dir / "summary.json")

    lines = ["| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |", "|---|---|---|---|---|---|"]
    for name, mets in summary.items():
        for k, s in mets.items():
            lines.append(f"| {name} | {k} | {s['mean']:.0f} ({s['ci95_lo']:.0f}–{s['ci95_hi']:.0f}) | "
                         f"{s['median']:.0f} | {s['p90']:.0f} | {s['n_samples']} / {s['n_vessels']} vessels |")
    lines += ["", f"Paired difference vs CV on identical windows (model − CV, m; negative = better). "
              f"Damped-CTRV tau = {best_tau:g} s, Kalman q = {best_q:g} m²/s³, both tuned on train.", "",
              "| model | ΔADE (95% CI) | ΔFDE (95% CI) |", "|---|---|---|"]
    for name, d in paired.items():
        a, f = d["ade_m"], d["fde_m"]
        lines.append(f"| {name} | {a['mean']:+.0f} ({a['ci95_lo']:+.0f} to {a['ci95_hi']:+.0f}) | "
                     f"{f['mean']:+.0f} ({f['ci95_lo']:+.0f} to {f['ci95_hi']:+.0f}) |")
    table = ws.results / "tables" / f"baselines_{run_name}.md"
    table.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    fig = plot_error_vs_horizon(step_err, w["step_s"], ws.results / "figures" / f"baselines_error_{run_name}.png",
                                f"Baseline error vs lead time ({run_name}{', SYNTHETIC' if ws.synthetic else ''})")
    print(f"wrote {fig.relative_to(project_path('.'))}")


def cmd_plot_tracks(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.viz.plots import plot_tracks

    tracks = pl.read_parquet(ws.processed / "tracks" / f"{data_cfg['aoi']['name']}.parquet")
    title = f"{data_cfg['aoi']['name']}{' (SYNTHETIC)' if ws.synthetic else ''}"
    out = plot_tracks(tracks, ws.results / "figures" / "tracks_overview.png", title)
    print(f"wrote {out.relative_to(project_path('.'))}")


def cmd_regime_eda(ws: Workspace, data_cfg, exp_cfg, args):
    from morva.viz.regime_eda import regime_eda

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
    from morva.features.windows import build_windows
    from morva.trajectories.segment import segment_tracks

    s, w = data_cfg["segmentation"], exp_cfg["windows"]
    points = pl.read_parquet(ws.processed / "points_clean.parquet")  # home AOI only
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


def _load_meta(ws: Workspace, feature_groups: list[str]) -> pl.DataFrame:
    """Window metadata, with the precomputed fairway features joined when a feature set needs them."""
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    if "fairway" in feature_groups:
        path = ws.processed / "fairway_features.parquet"
        if not path.exists():
            sys.exit("feature sets use 'fairway': run `morva fairway` first")
        meta = meta.join(pl.read_parquet(path), on="sample_id", how="left", maintain_order="left")
    return meta


def cmd_intervals(ws: Workspace, data_cfg, exp_cfg, args):
    """V3: quantile residual model + split-conformal calibration; interval coverage and width.

    Trains once on home `train` windows. By default, calibrates on home `calib` windows (or, with
    --local-calibration, on the evaluated region's own `transfer_calib` windows) and evaluates `--split` (optionally
    one `--region`). With --sweep, the same fitted model is evaluated on the home `--split` windows and on every
    transfer region's `transfer_<split>` windows, each with home calibration and, for transfer regions, also with
    local calibration.
    """
    from morva.evaluation.conformal import box_scores, conformal_offset, coverage, half_widths
    from morva.evaluation.metrics import summarize
    from morva.features.motion import build_features
    from morva.models.quantile import QuantileResidualGBM, residual_truth

    _check_test_lock(args)
    if "uncertainty" not in exp_cfg:
        sys.exit("`intervals` needs an `uncertainty` section (V3 config: --exp-config configs/v3/experiment.yaml)")
    if args.sweep and (args.region or args.local_calibration or args.split.startswith("transfer_")):
        sys.exit("--sweep takes a home split (val or test) and covers every region and calibration itself")
    w, g, u, ev = exp_cfg["windows"], exp_cfg["gbm"], exp_cfg["uncertainty"], exp_cfg["evaluation"]
    step = w["step_s"]
    knots_min = list(g["knots_min"])
    knots = [int(k * 60 / step) for k in knots_min]
    sets = g["feature_sets"][args.feature_set]
    arrays = np.load(ws.processed / "windows.npz")
    hist_all, fut_all = arrays["hist"], arrays["fut"]
    meta = _load_meta(ws, sets)
    split, region = meta["split"], meta["region"]
    home_cal = (split == "calib").to_numpy()

    # Evaluation targets: (name, evaluated windows, calibration windows, calibration label, region)
    if args.sweep:
        targets = [(args.split, (split == args.split).to_numpy(), home_cal, "home calib", None)]
        for r in sorted(set(region.filter(split == f"transfer_{args.split}"))):
            ev_r = ((split == f"transfer_{args.split}") & (region == r)).to_numpy()
            local = ((split == "transfer_calib") & (region == r)).to_numpy()
            targets.append((f"transfer_{args.split}_{r}", ev_r, home_cal, "home calib", r))
            targets.append((f"transfer_{args.split}_{r}_localcal", ev_r, local, "local transfer_calib", r))
    else:
        ev_mask, suffix = _eval_mask(meta, args)
        if args.local_calibration:
            if not args.region:
                sys.exit("--local-calibration needs --region")
            targets = [(f"{args.split}{suffix}_localcal", ev_mask,
                        ((split == "transfer_calib") & (region == args.region)).to_numpy(),
                        "local transfer_calib", args.region)]
        else:
            targets = [(f"{args.split}{suffix}", ev_mask, home_cal, "home calib", args.region)]
    tr = (split == "train").to_numpy()
    if args.sweep:  # a region without local calibration windows only loses its secondary analysis
        skipped = [t[0] for t in targets if t[3].startswith("local") and not t[2].any()]
        for name in skipped:
            print(f"{name}: no transfer_calib windows in this region; local calibration skipped")
        targets = [t for t in targets if t[0] not in skipped]
    empty = [t[0] for t in targets if not (t[1].any() and t[2].any())]
    if not tr.any() or empty:
        sys.exit(f"empty blocks: {int(tr.sum())} train windows; targets without evaluated or calibration windows: "
                 f"{empty}")

    def X(mask):
        return build_features(hist_all[mask], meta.filter(pl.Series(mask)), step, sets)

    X_tr, cols = X(tr)
    keep = ~np.isnan(X_tr).all(axis=0)  # a feature with no training values cannot be used
    cols = [c for c, k in zip(cols, keep, strict=True) if k]
    cat = [c == "ship_group" for c in cols] if "ship_group" in cols else None
    model = QuantileResidualGBM(knots, u["quantiles"], categorical=cat, seed=g["seed"]).fit(
        X_tr[:, keep], hist_all[tr], fut_all[tr], step)
    print(f"fitted {len(model.models)} quantile models on {int(tr.sum()):,} train windows")
    stamp = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    cache: dict[int, tuple] = {}

    def predict(mask):  # each block is predicted once, even when it serves several targets
        key = hash(mask.tobytes())
        if key not in cache:
            cache[key] = (model.predict(X(mask)[0][:, keep]), residual_truth(hist_all[mask], fut_all[mask], step,
                                                                              knots))
        return cache[key]

    for name, ev_mask, cal, cal_label, reg in targets:
        p_cal, y_cal = predict(cal)
        p_ev, y_ev = predict(ev_mask)
        groups = meta.filter(pl.Series(ev_mask))["mmsi"].to_numpy()
        results = {}
        for level in u["interval_levels"]:
            lo_c, hi_c = model.interval(p_cal, level)
            offset = conformal_offset(box_scores(lo_c, hi_c, y_cal), level)
            lo, hi = model.interval(p_ev, level)
            inside = box_scores(lo, hi, y_ev) <= offset[None, :]
            raw = coverage(lo, hi, y_ev, np.zeros_like(offset))
            hw = half_widths(lo, hi, offset)
            per_knot = {}
            for i, h in enumerate(knots_min):
                c = summarize(inside[:, i].astype(float), groups, ev["n_bootstrap"], ev["seed"])
                per_knot[str(h)] = {"coverage": c["mean"], "ci95_lo": c["ci95_lo"], "ci95_hi": c["ci95_hi"],
                                    "uncalibrated_coverage": float(raw[i]), "offset_m": float(offset[i]),
                                    "half_width_along_m": float(hw[i, 0]), "half_width_cross_m": float(hw[i, 1])}
            results[str(level)] = per_knot
        counts = {"train": int(tr.sum()), "calibration": int(cal.sum()), "evaluated": int(ev_mask.sum()),
                  "evaluated_vessels": int(len(np.unique(groups)))}
        run_dir = ws.results / "runs" / f"{stamp}_intervals_{args.feature_set}_{name}"
        _write_json({"split": args.split, "target": name, "region": reg, "feature_set": args.feature_set,
                     "calibration": cal_label, "git": _git_hash(),
                     "config": {"uncertainty": u, "gbm_seed": g["seed"], "knots_min": knots_min},
                     "windows": counts, "features": cols, "n_iter": model.n_iter(), "intervals": results},
                    run_dir / "summary.json")
        lines = [f"# Conformal prediction boxes ({args.feature_set}; {name}; calibration: {cal_label})", "",
                 f"{counts['train']:,} train / {counts['calibration']:,} calibration / {counts['evaluated']:,} "
                 f"evaluated windows ({counts['evaluated_vessels']} vessels). Coverage = share of windows whose true "
                 "position lies inside the 2-D box (95% CI, vessel bootstrap).", "",
                 "| level | horizon (min) | coverage | uncalibrated | half-width along (m) | half-width cross (m) |",
                 "|---|---|---|---|---|---|"]
        for level, per_knot in results.items():
            for h, r in per_knot.items():
                lines.append(f"| {float(level):.0%} | {h} | {r['coverage']:.3f} ({r['ci95_lo']:.3f}–"
                             f"{r['ci95_hi']:.3f}) | {r['uncalibrated_coverage']:.3f} | "
                             f"{r['half_width_along_m']:.0f} | {r['half_width_cross_m']:.0f} |")
        out = ws.results / "tables" / f"intervals_{args.feature_set}_{name}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n")
        print("\n".join(lines[:1] + lines[4:]))


def cmd_gbm(ws: Workspace, data_cfg, exp_cfg, args):
    """E3/E4: residual GBM with feature-set ablation. Trains on train, evaluates on `--split` (val by default)."""
    import time

    from morva.evaluation.metrics import paired_summaries, per_sample_metrics, step_errors_m, summarize
    from morva.features.motion import SHIP_GROUP_CODES, build_features
    from morva.models import baselines
    from morva.models.gbm import ResidualGBM
    from morva.viz.regime_eda import TURN_BINS, past_turn_rate_deg_min

    _check_test_lock(args)
    w, g, ev = exp_cfg["windows"], exp_cfg["gbm"], exp_cfg["evaluation"]
    step, n_fut = w["step_s"], w["future_steps"]
    knots = [int(k * 60 / step) for k in g["knots_min"]]
    arrays = np.load(ws.processed / "windows.npz")
    meta = _load_meta(ws, [s for sets in g["feature_sets"].values() for s in sets])
    tr = (meta["split"] == "train").to_numpy()
    ev_mask, suffix = _eval_mask(meta, args)
    if args.holdout_eval_vessels:  # train only on vessels that never appear in the evaluated windows
        ev_vessels = meta.filter(pl.Series(ev_mask))["mmsi"].unique().implode()
        n_before = int(tr.sum())
        tr &= ~meta["mmsi"].is_in(ev_vessels).to_numpy()
        suffix += "_vesselheldout"
        print(f"vessel-held-out: train windows {n_before:,} -> {int(tr.sum()):,}")
    if args.train_subsample and args.train_subsample < tr.sum():  # size control for the held-out comparison
        keep_idx = np.random.default_rng(ev["seed"]).choice(np.flatnonzero(tr), args.train_subsample, replace=False)
        tr = np.zeros_like(tr)
        tr[keep_idx] = True
        suffix += f"_sub{args.train_subsample}"
        print(f"random train subsample: {args.train_subsample:,} windows")
    hist_all, fut_all = arrays["hist"], arrays["fut"]
    if not tr.any() or not ev_mask.any():
        sys.exit(f"empty split: {tr.sum()} train / {ev_mask.sum()} {args.split} windows; rerun `windows`")
    m_ev, h_ev, f_ev = meta.filter(pl.Series(ev_mask)), hist_all[ev_mask], fut_all[ev_mask]
    groups = m_ev["mmsi"].to_numpy()
    seeds = args.seeds or [g["seed"]]

    def fit_sets(tr_m, ev_m, seeds):
        """Fit every feature set on tr_m windows and return step errors on ev_m windows."""
        h_tr, f_tr, m_tr = hist_all[tr_m], fut_all[tr_m], meta.filter(pl.Series(tr_m))
        h_e, f_e, m_e = hist_all[ev_m], fut_all[ev_m], meta.filter(pl.Series(ev_m))
        out, info, sfde = {}, {}, {}
        for name, sets in g["feature_sets"].items():
            X_tr, cols = build_features(h_tr, m_tr, step, sets)
            X_e, _ = build_features(h_e, m_e, step, sets)
            keep = ~np.isnan(X_tr).all(axis=0)  # a feature with no training values cannot be used
            dropped = [c for c, k in zip(cols, keep, strict=True) if not k]
            X_tr, X_e, cols = X_tr[:, keep], X_e[:, keep], [c for c, k in zip(cols, keep, strict=True) if k]
            if dropped:
                print(f"{name}: dropped all-missing features {dropped}")
            cat = [c == "ship_group" for c in cols] if "ship_group" in cols else None
            sfde[name] = {}
            for seed in seeds:  # tables use the first seed; the spread across seeds is reported separately
                t0 = time.time()
                model = ResidualGBM(knots, categorical=cat, seed=seed).fit(X_tr, h_tr, f_tr, step)
                e = step_errors_m(model.predict(X_e, h_e, step, n_fut), f_e)
                sfde[name][seed] = float(e[:, -1].mean())
                if seed == seeds[0]:
                    out[name] = e
                    info[name] = {"features": cols, "dropped_all_missing": dropped, "train_windows": int(tr_m.sum()),
                                  "fit_s": round(time.time() - t0, 1), "n_iter": model.n_iter()}
                print(f"{name} seed {seed}: fitted in {time.time() - t0:.0f} s on {int(tr_m.sum()):,} windows, "
                      f"ADE {e.mean():.0f} m, FDE {e[:, -1].mean():.0f} m (n={int(ev_m.sum()):,})")
        return out, info, sfde

    errs = {"cv": step_errors_m(baselines.cv(h_ev, n_fut, step), f_ev)}
    if args.spatial_holdout:
        sp = g["spatial"]
        edges, buf = np.asarray(sp["lon_edges"], float), sp["buffer_deg"]
        lons = np.concatenate([hist_all[..., 1], fut_all[..., 1]], axis=1)
        lon_min, lon_max = np.nanmin(lons, axis=1), np.nanmax(lons, axis=1)
        band = np.clip(np.digitize(hist_all[:, -1, 1], edges[1:-1]), 0, len(edges) - 2)  # anchor band
        ev_idx = np.flatnonzero(ev_mask)
        for name in g["feature_sets"]:
            errs[name] = np.full((len(ev_idx), n_fut), np.nan)
        fit_info, seed_fde = {"folds": []}, {}
        for b in range(len(edges) - 1):
            lo, hi = edges[b], edges[b + 1]
            ev_b = ev_mask & (band == b)
            tr_b = tr & ((lon_max < lo - buf) | (lon_min >= hi + buf))
            if not ev_b.any() or not tr_b.any():
                continue
            print(f"spatial fold {b}: hold out lon [{lo}, {hi}); train {int(tr_b.sum()):,} / eval {int(ev_b.sum()):,}")
            out, info, _ = fit_sets(tr_b, ev_b, seeds[:1])
            pos = ev_b[ev_idx]
            for name, e in out.items():
                errs[name][pos] = e
            fit_info["folds"].append({"lon": [float(lo), float(hi)], "train_windows": int(tr_b.sum()),
                                      "eval_windows": int(ev_b.sum()), "models": info})
        suffix += "_spatialheldout"
        tr_report = int(np.mean([f["train_windows"] for f in fit_info["folds"]]))
    else:
        out, fit_info, seed_fde = fit_sets(tr, ev_mask, seeds)
        errs.update(out)
        tr_report = int(tr.sum())
    m_tr = meta.filter(pl.Series(tr))

    per = {k: per_sample_metrics(e, step, w["horizons_min"]) for k, e in errs.items()}
    summary = {k: {mk: summarize(v, groups, ev["n_bootstrap"], ev["seed"]) for mk, v in p.items()}
               for k, p in per.items()}

    def paired(a, b):  # ADE, final error and every reported horizon
        return paired_summaries(per[b], per[a], groups, ev["n_bootstrap"], ev["seed"])

    names = list(g["feature_sets"])
    comparisons = {f"{n} - cv": paired("cv", n) for n in names}
    comparisons.update({f"{n} - A_motion": paired("A_motion", n) for n in names if n != "A_motion"})

    turn = past_turn_rate_deg_min(h_ev, step)
    group_names = {v: k for k, v in SHIP_GROUP_CODES.items()}
    sg, _ = build_features(h_ev, m_ev, step, ["vessel"])
    turn_idx = np.digitize(np.nan_to_num(turn), TURN_BINS[1:-1])  # 0 .. len(TURN_BINS) - 2
    strata = pl.DataFrame({
        "turn_bin": [f"{TURN_BINS[i]:g}–{TURN_BINS[i + 1]:g}" for i in turn_idx],
        "_order": turn_idx,
        "ship_group": [group_names.get(c, "unknown") if not np.isnan(c) else "unknown" for c in sg[:, 0]],
        **{k: e[:, -1] for k, e in errs.items()},
    })
    by_turn = (strata.group_by("turn_bin", "_order").agg(n=pl.len(), **{k: pl.col(k).mean() for k in errs})
               .sort("_order").drop("_order"))
    by_group = strata.group_by("ship_group").agg(n=pl.len(), **{k: pl.col(k).mean() for k in errs}).sort("n",
                                                                                                    descending=True)
    # Vessel novelty: are gains generalisation or recognition of vessels already seen in training?
    seen = m_ev["mmsi"].is_in(m_tr["mmsi"].unique().implode()).to_numpy()
    novelty = {}
    for label, mask in (("unseen_vessels", ~seen), ("seen_vessels", seen)):
        if mask.any():
            novelty[label] = {"windows": int(mask.sum()), "vessels": int(len(np.unique(groups[mask]))),
                              **{f"{n} - A_motion": summarize(per[n]["fde_m"][mask] - per["A_motion"]["fde_m"][mask],
                                                              groups[mask], ev["n_bootstrap"], ev["seed"])
                                 for n in names if n != "A_motion"},
                              "A_motion - cv": summarize(per["A_motion"]["fde_m"][mask] - per["cv"]["fde_m"][mask],
                                                         groups[mask], ev["n_bootstrap"], ev["seed"])}
    run_dir = ws.results / "runs" / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}_gbm_{args.split}{suffix}"
    run_dir.mkdir(parents=True, exist_ok=True)
    per_sample = pl.DataFrame({"sample_id": m_ev["sample_id"], **{f"fde_{k}": e[:, -1] for k, e in errs.items()},
                               **{f"ade_{k}": e.mean(axis=1) for k, e in errs.items()},
                               **{f"err{h}_{k}": p[f"err_{h}min_m"] for k, p in per.items()
                                  for h in w["horizons_min"] if f"err_{h}min_m" in p}})
    per_sample.write_parquet(run_dir / "per_sample.parquet")
    _write_json({"split": args.split, "region": args.region, "git": _git_hash(), "config": exp_cfg["gbm"],
                 "fit": fit_info,
                 "metrics": summary, "paired": comparisons, "fde_by_turn_bin": by_turn.to_dicts(),
                 "fde_by_ship_group": by_group.to_dicts(), "vessel_novelty": novelty,
                 "holdout_eval_vessels": bool(args.holdout_eval_vessels), "train_windows": tr_report,
                 "spatial_holdout": bool(args.spatial_holdout),
                 "seed_fde": seed_fde}, run_dir / "summary.json")

    fmt = lambda s: f"{s['mean']:+.0f} ({s['ci95_lo']:+.0f} to {s['ci95_hi']:+.0f})"  # noqa: E731
    H = n_fut * step // 60  # noqa: N806  (final horizon, minutes)
    inner = [h for h in w["horizons_min"] if h < H]
    title = args.split + (f", {args.region}" if args.region else "") + (
        ", vessel-held-out" if args.holdout_eval_vessels else "") + (
        ", spatially held-out (longitude bands)" if args.spatial_holdout else "") + (
        f", random train subsample {args.train_subsample:,}" if args.train_subsample else "")
    lines = [f"# Residual GBM context ablation ({title}; {tr_report:,} train windows"
             f"{' (mean per fold)' if args.spatial_holdout else ''})", "",
             f"| model | ADE m (95% CI) | FDE@{H} m (95% CI) | " + " | ".join(f"err@{h}" for h in inner) + " |",
             "|---|---|---|" + "---|" * len(inner)]
    for k, s in summary.items():
        lines.append(f"| {k} | {s['ade_m']['mean']:.0f} ({s['ade_m']['ci95_lo']:.0f}–{s['ade_m']['ci95_hi']:.0f}) | "
                     f"{s['fde_m']['mean']:.0f} ({s['fde_m']['ci95_lo']:.0f}–{s['fde_m']['ci95_hi']:.0f}) | "
                     + " | ".join(f"{s[f'err_{h}min_m']['mean']:.0f}" for h in inner) + " |")
    lines += ["", "Paired differences on identical windows (m, negative = first model better), vessel bootstrap:", "",
              "| comparison | ΔADE | ΔFDE |", "|---|---|---|"]
    lines += [f"| {c} | {fmt(d['ade_m'])} | {fmt(d['fde_m'])} |" for c, d in comparisons.items()]
    if inner:
        lines += ["", "Paired error differences at earlier horizons (m, 95% CI, vessel bootstrap):", "",
                  "| comparison | " + " | ".join(f"Δerr@{h}" for h in inner) + " |", "|---|" + "---|" * len(inner)]
        lines += [f"| {c} | " + " | ".join(fmt(d[f"err_{h}min_m"]) for h in inner) + " |"
                  for c, d in comparisons.items()]
    for title, tab in (("past turn rate (°/min)", by_turn), ("ship group", by_group)):
        lines += ["", f"Mean FDE@{H} min (m) by {title}:", "", "| " + " | ".join(tab.columns) + " |",
                  "|" + "---|" * len(tab.columns)]
        lines += ["| " + " | ".join(f"{v:.0f}" if isinstance(v, float) else str(v) for v in r) + " |"
                  for r in tab.iter_rows()]
    lines += ["", f"ΔFDE@{H} min (m) for vessels NOT seen in training vs vessels seen in training:", "",
              "| comparison | " + " | ".join(f"{k} ({v['vessels']} vessels)" for k, v in novelty.items()) + " |",
              "|---|" + "---|" * len(novelty)]
    comps = [c for c in next(iter(novelty.values())) if " - " in c]
    lines += [f"| {c} | " + " | ".join(fmt(v[c]) for v in novelty.values()) + " |" for c in comps]
    if len(seeds) > 1:
        lines += ["", f"FDE@{H} min (m) across seeds {seeds}:", "",
                  "| model | mean | sd | min | max |", "|---|---|---|---|---|"]
        for n, d in seed_fde.items():
            v = np.array(list(d.values()))
            lines.append(f"| {n} | {v.mean():.0f} | {v.std(ddof=1):.1f} | {v.min():.0f} | {v.max():.0f} |")
    out = ws.results / "tables" / f"gbm_ablation_{args.split}{suffix}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def regime_comparisons(sets: list[str]) -> list[tuple[str, str]]:
    """Paired contrasts reported by regime: motion-only vs CV, then every other feature set vs motion-only."""
    return [("A_motion", "cv")] + [(n, "A_motion") for n in sets if n != "A_motion"]


def cmd_regime_report(ws: Workspace, data_cfg, exp_cfg, args):
    """Results by past-only manoeuvring regime, with threshold sensitivity, for every configured feature set.

    Reads the stored per-sample runs for `--split` (and `--region`). The vessel-held-out and longitude-band sections
    are included when those runs exist; longitude bands only apply to the home area.
    """
    from dataclasses import replace

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from morva.evaluation.metrics import summarize
    from morva.features.regimes import (
        REGIMES,
        SENSITIVITY,
        RegimeParams,
        assign_regimes,
        regime_variables,
        turn_label_reliable,
    )

    _check_test_lock(args)
    w, ev = exp_cfg["windows"], exp_cfg["evaluation"]
    H = w["future_steps"] * w["step_s"] // 60  # noqa: N806  (final horizon, minutes)
    gbm_sets = list(exp_cfg["gbm"]["feature_sets"])
    meta = pl.read_parquet(ws.processed / "windows_meta.parquet")
    mask, run_name = _eval_mask(meta, args)
    run_name = f"{args.split}{run_name}"
    hist, m = np.load(ws.processed / "windows.npz")["hist"][mask], meta.filter(pl.Series(mask))

    def latest(pattern, required=True):
        runs = sorted((ws.results / "runs").glob(pattern))
        if not runs:
            if required:
                sys.exit(f"no run matching {pattern}; run it first")
            return None, None
        df = pl.read_parquet(runs[-1] / "per_sample.parquet")
        missing = [n for n in gbm_sets if "_gbm_" in pattern and f"fde_{n}" not in df.columns]
        if missing:
            sys.exit(f"{runs[-1].name} lacks feature sets {missing}; re-run it with the current config")
        return df, runs[-1].name

    BASE = ("persistence", "ctrv", "ctrv_damped", "kalman_cv")  # noqa: N806
    gbm, gbm_run = latest(f"*_gbm_{run_name}")
    base, base_run = latest(f"*_baselines_{run_name}")
    held, held_run = latest(f"*_gbm_{run_name}_vesselheldout", required=False)
    spat, spat_run = latest(f"*_gbm_{run_name}_spatialheldout", required=False)
    base_w = base.pivot(on="model", index="sample_id", values="fde_m")
    fde = (m.select("sample_id", "mmsi")
           .join(gbm.select("sample_id", *[f"fde_{n}" for n in ("cv", *gbm_sets)]), on="sample_id")
           .join(base_w.select("sample_id", *BASE).rename({c: f"fde_{c}" for c in BASE}), on="sample_id"))
    held_out = []
    for title, pre, df in ((f"Vessel-held-out training (all {run_name} vessels unseen)", "held_", held),
                           ("Spatially held-out (longitude band unseen in training, 0.05° buffer)", "spat_", spat)):
        if df is not None:
            fde = fde.join(df.select("sample_id", *[pl.col(f"fde_{n}").alias(f"{pre}{n}") for n in gbm_sets]),
                           on="sample_id")
            held_out.append((title, pre))
    assert len(fde) == len(m), f"per-sample results do not cover all {run_name} windows"
    groups = fde["mmsi"].to_numpy()
    col = lambda c: fde[c].to_numpy()  # noqa: E731

    p0 = RegimeParams()
    v = regime_variables(hist, w["step_s"], p0.lookback_min)
    reg = assign_regimes(v, p0)
    reliable = turn_label_reliable(v, p0)
    ws.processed.mkdir(parents=True, exist_ok=True)
    pl.DataFrame({"sample_id": m["sample_id"], "regime": reg, "turn_label_reliable": reliable, **v}).write_parquet(
        ws.processed / f"regimes_{run_name}.parquet")

    models = ["persistence", "cv", "ctrv", "ctrv_damped", "kalman_cv", *gbm_sets]
    comps = regime_comparisons(gbm_sets)
    fmt = lambda s: f"{s['mean']:+.0f} ({s['ci95_lo']:+.0f} to {s['ci95_hi']:+.0f})"  # noqa: E731

    def paired(prefix_b, b, prefix_a, a, sel):
        pa = "fde_" if a == "cv" else prefix_a  # CV is the same forecast in every training setting
        return summarize(col(f"{prefix_b}{b}")[sel] - col(f"{pa}{a}")[sel], groups[sel], ev["n_bootstrap"],
                         ev["seed"])

    runs_used = ", ".join(f"`{r}`" for r in (gbm_run, held_run, spat_run, base_run) if r)
    lines = [f"# Results by past-only manoeuvring regime ({run_name})", "",
             f"Regime parameters: {p0.label()}. Runs: {runs_used}.", "",
             f"## Mean FDE@{H} min (m)", "",
             "| regime | windows | share | vessels | turn label reliable | " + " | ".join(models) + " |",
             "|---|---|---|---|---|" + "---|" * len(models)]
    rows = []
    for r in REGIMES:
        sel = reg == r
        if not sel.any():
            continue
        rows.append({"regime": r, **{mm: float(col(f"fde_{mm}")[sel].mean()) for mm in models}})
        rel = f"{reliable[sel].mean():.0%}" if r != "low_speed" else "n/a"
        lines.append(f"| {r} | {sel.sum():,} | {sel.mean():.1%} | {len(np.unique(groups[sel]))} | {rel} | "
                     + " | ".join(f"{rows[-1][mm]:.0f}" for mm in models) + " |")

    header = "| regime | " + " | ".join(f"{b} − {a}" for b, a in comps) + " |"
    lines += ["", f"## Paired ΔFDE@{H} min by regime (m, 95% CI, vessel bootstrap; negative = first model better)",
              "",
              header, "|---|" + "---|" * len(comps)]
    for r in REGIMES:
        sel = reg == r
        if sel.any():
            lines.append(f"| {r} | " + " | ".join(fmt(paired("fde_", b, "fde_", a, sel)) for b, a in comps) + " |")

    for title, pre in held_out:
        lines += ["", f"## {title}: paired ΔFDE@{H} min by regime", "", header, "|---|" + "---|" * len(comps)]
        for r in REGIMES:
            sel = reg == r
            if sel.any():
                lines.append(f"| {r} | " + " | ".join(fmt(paired(pre, b, pre, a, sel)) for b, a in comps) + " |")

    # Threshold sensitivity: vary one parameter at a time; also 'sustained turning'
    configs = [("primary", p0, False)] + [(f"{k}={x:g}", replace(p0, **{k: type(getattr(p0, k))(x)}), False)
                                          for k, x in SENSITIVITY] + [("sustained turning (>=70% same sign)", p0, True)]
    sens = []
    for name, p, sustained in configs:
        vv = v if p.lookback_min == p0.lookback_min else regime_variables(hist, w["step_s"], p.lookback_min)
        rr = assign_regimes(vv, p, sustained)
        for r in REGIMES:
            sel = rr == r
            if sel.sum() < 30:
                continue
            row = {"config": name, "regime": r, "windows": int(sel.sum()), "share": float(sel.mean()),
                   **{f"fde_{mm}": float(col(f"fde_{mm}")[sel].mean()) for mm in ("cv", *gbm_sets)}}
            for b, a in comps:
                d = paired("fde_", b, "fde_", a, sel)
                row[f"d_{b}_vs_{a}"], row[f"d_{b}_vs_{a}_lo"], row[f"d_{b}_vs_{a}_hi"] = d["mean"], d["ci95_lo"], d[
                    "ci95_hi"]
            sens.append(row)
    sens_df = pl.DataFrame(sens)
    sens_df.write_csv(ws.results / "tables" / f"regime_sensitivity_{run_name}.csv")
    lines += ["", f"## Threshold sensitivity (`regime_sensitivity_{run_name}.csv`)", ""]
    if sens_df.is_empty():
        lines.append("No regime × configuration cell has the 30 windows needed for a sensitivity estimate.")
    else:
        lines += [f"{len(configs)} configurations (primary, one-at-a-time changes, sustained turning), "
                  f"{sens_df.height} regime×config cells. Cells where the 95% CI lies entirely below 0 (first model "
                  "better) / entirely above 0 (first model worse):", "",
                  "| comparison | CI below 0 | CI above 0 |", "|---|---|---|"]
        for b, a in comps:
            hi, lo = sens_df[f"d_{b}_vs_{a}_hi"], sens_df[f"d_{b}_vs_{a}_lo"]
            lines.append(f"| {b} − {a} | {int((hi < 0).sum())} | {int((lo > 0).sum())} |")
        key = [c for c in ("C_location", "E_fairway") if c in gbm_sets]
        lines += ["", "| config | " + " | ".join(REGIMES) + " |", "|---|" + "---|" * len(REGIMES)]
        for name, *_ in configs:
            sub = {r["regime"]: r for r in sens_df.filter(pl.col("config") == name).to_dicts()}
            lines.append(f"| {name} | " + " | ".join(
                (f"n={sub[r]['windows']:,}, " + ", ".join(f"{k[0]}−A {sub[r][f'd_{k}_vs_A_motion']:+.0f}" for k in key))
                if r in sub else "–" for r in REGIMES) + " |")

    out = ws.results / "tables" / f"regimes_{run_name}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    show = ["cv", *gbm_sets]
    width = 0.8 / len(show)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = np.arange(len(rows))
    for i, mm in enumerate(show):
        ax.bar(x + (i - (len(show) - 1) / 2) * width, [r[mm] for r in rows], width=width, label=mm)
    counts = {r: int((reg == r).sum()) for r in REGIMES}
    ax.set_xticks(x, [f"{r['regime']}\n(n={counts[r['regime']]:,})" for r in rows], fontsize=8)
    ax.set_ylabel(f"Mean FDE at {H} min (m)")
    ax.set_title(f"Prediction error by past-only manoeuvring regime ({run_name})")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ws.results / "figures" / f"regime_fde_{run_name}.png", dpi=150)
    plt.close(fig)


def cmd_summary_figure(ws: Workspace, data_cfg, exp_cfg, args):
    """Three-panel generalisation figure (in-area / unseen vessels / unseen waters) from stored runs."""
    from morva.viz.plots import plot_generalisation_panels

    def metrics(pattern):
        runs = sorted((ws.results / "runs").glob(pattern))
        if not runs:
            sys.exit(f"no run matching {pattern}")
        mets = json.loads((runs[-1] / "summary.json").read_text())["metrics"]
        return {m: v["fde_m"] for m, v in mets.items()}

    sp = args.split
    label = "test split, single post-freeze run" if sp == "test" else "validation"
    if args.v2:  # V2: raw location vs fairway context, in-area, unseen bands and the independent waterways
        from morva.viz.plots import CONTEXT_COLOURS

        panels = {"Home": metrics(f"*_gbm_{sp}"), "Home: held-out bands": metrics(f"*_gbm_{sp}_spatialheldout"),
                  "Independent: Bornholm": metrics(f"*_gbm_transfer_{sp}_bornholm"),
                  "Independent: Skagen": metrics(f"*_gbm_transfer_{sp}_skagen")}
        models = [("A_motion", "A  motion"), ("C_location", "C  + raw location"), ("E_fairway", "E  + fairway")]
        out = plot_generalisation_panels(panels, ws.results / "figures" / f"transfer_{sp}.png",
                                         f"Raw location vs fairway context, constant velocity dashed ({label})",
                                         models=models, colours=CONTEXT_COLOURS)
    else:
        panels = {"In-area": metrics(f"*_gbm_{sp}"), "Unseen vessels": metrics(f"*_gbm_{sp}_vesselheldout"),
                  "Unseen waters": metrics(f"*_gbm_{sp}_spatialheldout")}
        out = plot_generalisation_panels(panels, ws.results / "figures" / f"generalisation_{sp}.png",
                                         f"Learned residual model vs constant velocity (dashed), {label}")
    print(f"wrote {out.relative_to(project_path('.'))}")


def main(argv=None):
    from morva.evaluation.splits import EVAL_SPLITS

    # --region choices come from the data config actually in use
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--data-config", default="configs/data.yaml")
    region_names = _region_names(load_config(pre.parse_known_args(argv)[0].data_config))

    ap = argparse.ArgumentParser(prog="morva")
    ap.add_argument("--synthetic", action="store_true", help="use the isolated synthetic workspace")
    ap.add_argument("--data-config", default="configs/data.yaml")
    ap.add_argument("--exp-config", default="configs/experiment.yaml")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("synth", help="generate synthetic DMA-format AIS (smoke tests only)")
    p = sub.add_parser("manifest", help="record provenance + checksum of raw files")
    p.add_argument("files", nargs="+")
    p.add_argument("--source", help="configured data source name (default: the first)")
    p.add_argument("--notes", default="")
    p.add_argument("--force", action="store_true", help="overwrite existing manifests")
    p = sub.add_parser("ingest", help="raw zip/csv -> AOI-filtered, de-duplicated interim parquet")
    p.add_argument("files", nargs="*")
    p.add_argument("--force", action="store_true", help="re-ingest files already in the ingest log")
    sub.add_parser("clean", help="quality flags, report, segmentation")
    sub.add_parser("windows", help="build prediction windows and time-block split")
    sub.add_parser("fairway", help="V2: traffic-flow maps (training period) and fairway features per window")
    p = sub.add_parser("baselines", help="evaluate persistence / CV / CTRV")
    p.add_argument("--split", default="val", choices=["train", *EVAL_SPLITS])
    p.add_argument("--confirm-test", action="store_true")
    p.add_argument("--region", choices=region_names, help="evaluate one region only (default: all in the split)")
    sub.add_parser("plot-tracks", help="overview map of segmented tracks")
    p = sub.add_parser("gbm", help="E3/E4: residual GBM context ablation (train -> val)")
    p.add_argument("--split", default="val", choices=list(EVAL_SPLITS))
    p.add_argument("--confirm-test", action="store_true")
    p.add_argument("--region", choices=region_names, help="evaluate one region only (default: all in the split)")
    p.add_argument("--holdout-eval-vessels", action="store_true",
                   help="exclude every vessel of the evaluated split from training")
    p.add_argument("--seeds", type=int, nargs="+", help="seeds to train (default: config seed)")
    p.add_argument("--train-subsample", type=int, help="random subsample of training windows (size control)")
    p.add_argument("--spatial-holdout", action="store_true", help="hold out one longitude band at a time (H4)")
    p = sub.add_parser("intervals", help="V3: quantile model + conformal calibration; interval coverage on --split")
    p.add_argument("--split", default="val", choices=list(EVAL_SPLITS))
    p.add_argument("--region", choices=region_names, help="evaluate one region only (default: all in the split)")
    p.add_argument("--feature-set", default="E_fairway", help="feature set from the gbm config (default E_fairway)")
    p.add_argument("--local-calibration", action="store_true",
                   help="calibrate on the region's own transfer_calib windows (secondary analysis)")
    p.add_argument("--sweep", action="store_true",
                   help="fit once; evaluate the home split and every transfer region (home and local calibration)")
    p.add_argument("--confirm-test", action="store_true")
    p = sub.add_parser("sensitivity", help="E0: retained data under different gap thresholds")
    p.add_argument("--gap-s", type=int, nargs="+", default=[600, 1200, 1800])
    p.add_argument("--window-gap-s", type=int, nargs="+", default=[120, 180, 300])
    p = sub.add_parser("summary-figure", help="3-panel generalisation figure from stored runs")
    p.add_argument("--split", default="test", choices=["val", "test"])
    p.add_argument("--v2", action="store_true", help="V2 figure: raw location vs fairway context across waterways")
    p = sub.add_parser("regime-report", help="results by past-only manoeuvring regime + threshold sensitivity")
    p.add_argument("--split", default="val", choices=list(EVAL_SPLITS))
    p.add_argument("--region", choices=region_names, help="report one region only (default: all in the split)")
    p.add_argument("--confirm-test", action="store_true")
    sub.add_parser("regime-eda", help="figures supporting the manoeuvring-regime definition (train+val only)")

    args = ap.parse_args(argv)
    data_cfg, exp_cfg = load_config(args.data_config), load_config(args.exp_config)
    ws = Workspace(args.synthetic, data_cfg, exp_cfg)
    handlers = {
        "synth": cmd_synth, "manifest": cmd_manifest, "ingest": cmd_ingest, "clean": cmd_clean,
        "windows": cmd_windows, "fairway": cmd_fairway, "baselines": cmd_baselines, "plot-tracks": cmd_plot_tracks,
        "regime-eda": cmd_regime_eda, "sensitivity": cmd_sensitivity, "gbm": cmd_gbm,
        "regime-report": cmd_regime_report, "intervals": cmd_intervals, "summary-figure": cmd_summary_figure,
    }
    handlers[args.cmd](ws, data_cfg, exp_cfg, args)


if __name__ == "__main__":
    main()
