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
    from vesselmind.quality.checks import add_flags, normalize_sentinels, quality_report
    from vesselmind.trajectories.segment import segment_tracks, vessel_table

    raw = pl.read_parquet(sorted(ws.interim.glob("*.parquet")), columns=CLEAN_COLUMNS)
    q, s = data_cfg["quality"], data_cfg["segmentation"]
    flagged = add_flags(normalize_sentinels(raw), q["max_implied_speed_kn"], q["max_plausible_sog_kn"])
    report = quality_report(raw, flagged)

    tracks = segment_tracks(flagged, s["gap_s"], s["min_points"], s["min_duration_s"])
    report["segmentation"] = {
        **s,
        "segments": tracks["segment_id"].n_unique(),
        "vessels_with_segments": tracks["mmsi"].n_unique(),
        "rows_in_segments": len(tracks),
    }
    ws.processed.mkdir(parents=True, exist_ok=True)
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
    train_end, val_end = resolve_boundaries(meta, exp_cfg["split"])
    meta = assign_split(meta, train_end, val_end, w["step_s"], w["obs_steps"], w["future_steps"])
    vessels = pl.read_parquet(ws.processed / "vessels.parquet").drop("n_points")
    meta = meta.join(vessels, on="mmsi", how="left", maintain_order="left")

    np.savez_compressed(ws.processed / "windows.npz", hist=hist, fut=fut, sample_id=meta["sample_id"].to_numpy())
    meta.write_parquet(ws.processed / "windows_meta.parquet")
    summary = split_summary(meta, train_end, val_end)
    summary["boundaries_source"] = "explicit" if exp_cfg["split"].get("train_end") else "auto_fractions (PROVISIONAL)"
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

    models = {
        "persistence": lambda h: baselines.persistence(h, w["future_steps"], w["step_s"]),
        "cv": lambda h: baselines.cv(h, w["future_steps"], w["step_s"]),
        "ctrv": lambda h: baselines.ctrv(h, w["future_steps"], w["step_s"], b["ctrv_turn_window_steps"],
                                         b["ctrv_max_turn_rate_deg_s"], b["ctrv_min_sog_kn"]),
    }
    run_dir = ws.results / "runs" / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}_baselines_{args.split}"
    rows, summary, step_err = [], {}, {}
    for name, fn in models.items():
        err = step_errors_m(fn(hist), fut)
        step_err[name] = err
        per = per_sample_metrics(err, w["step_s"], w["horizons_min"])
        summary[name] = {k: summarize(v, groups, ev["n_bootstrap"], ev["seed"]) for k, v in per.items()}
        rows.append(pl.DataFrame({"sample_id": m["sample_id"], "model": name, **per}))

    run_dir.mkdir(parents=True, exist_ok=True)
    pl.concat(rows).write_parquet(run_dir / "per_sample.parquet")
    _write_json({"split": args.split, "git": _git_hash(), "config": exp_cfg, "metrics": summary},
                run_dir / "summary.json")

    lines = ["| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |", "|---|---|---|---|---|---|"]
    for name, mets in summary.items():
        for k, s in mets.items():
            lines.append(f"| {name} | {k} | {s['mean']:.0f} ({s['ci95_lo']:.0f}–{s['ci95_hi']:.0f}) | "
                         f"{s['median']:.0f} | {s['p90']:.0f} | {s['n_samples']} / {s['n_vessels']} vessels |")
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
    sub.add_parser("regime-eda", help="figures supporting the manoeuvring-regime definition (train+val only)")

    args = ap.parse_args(argv)
    data_cfg, exp_cfg = load_config(args.data_config), load_config(args.exp_config)
    ws = Workspace(args.synthetic, data_cfg)
    handlers = {
        "synth": cmd_synth, "manifest": cmd_manifest, "ingest": cmd_ingest, "clean": cmd_clean,
        "windows": cmd_windows, "baselines": cmd_baselines, "plot-tracks": cmd_plot_tracks,
        "regime-eda": cmd_regime_eda,
    }
    handlers[args.cmd](ws, data_cfg, exp_cfg, args)


if __name__ == "__main__":
    main()
