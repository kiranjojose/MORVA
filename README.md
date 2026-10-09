# VesselMind

**Context-aware vessel behaviour modelling from historical AIS: reproducible baselines, prediction and anomaly analysis.**

> **Status:** V1 research prototype, work in progress (started 9 Oct 2026). No results yet.
> Everything in this repository is historical research playback. It is not a real-time or safety-certified system.

## Research question

Does vessel context (vessel type, size, and later local traffic) improve 5/10/20-minute trajectory prediction
compared with transparent kinematic baselines, and does any improvement depend on the manoeuvring regime
(open-water transit vs. turning / port approach)?

See [docs/01_problem.md](docs/01_problem.md) and [docs/05_protocol.md](docs/05_protocol.md).

## Quick start

```bash
uv sync                                   # Python 3.12 environment
uv run pytest                             # unit tests
make smoke                                # full pipeline on SYNTHETIC data (isolated workspace)
```

Real data (Danish Maritime Authority historical AIS):

```bash
# 1. Download a daily file into data/raw/ (see data/README.md), then:
uv run vesselmind manifest data/raw/aisdk-YYYY-MM-DD.zip --notes "first sample day"
make pipeline                             # ingest -> clean -> windows -> baselines (validation split)
```

## Pipeline

```
raw zip/CSV (immutable, checksummed manifest)
  -> ingest:    AOI + Class A filter, schema cast          data/interim/*.parquet
  -> clean:     sentinels -> null, quality flags, segments  data/processed/tracks.parquet, vessels.parquet
  -> windows:   1-min resampling, 20-min history / 20-min future, gap-safe windows, time-block split
  -> models:    persistence, constant velocity, CTRV  (learned models next)
  -> evaluate:  one shared evaluator: ADE/FDE, per-horizon error, vessel-grouped bootstrap CIs
```

## Repository layout

| Path | Contents |
|---|---|
| `src/vesselmind/` | `ingestion/ quality/ trajectories/ features/ models/ anomaly/ evaluation/ viz/`, `cli.py` |
| `configs/` | `data.yaml` (source, AOI, quality, segmentation), `experiment.yaml` (windows, split, baselines) |
| `data/` | `raw/ interim/ processed/` (git-ignored), `manifests/` (committed provenance) |
| `docs/` | problem, literature, data card, methods, protocol, results, limitations, research log |
| `results/` | `tables/`, `figures/`, `runs/<timestamp>/summary.json` |
| `tests/` | unit tests for geodesy, quality flags, segmentation, windows, split and metrics |

## Principles

- Raw data is never modified. Suspicious points are flagged, not silently deleted.
- Splits are by time block. No window crosses a split boundary, and transforms are fit on training data only.
- The test split is locked (`--confirm-test`) and run once, after hypotheses are frozen.
- Negative results are reported. Synthetic anomaly labels are always labelled as synthetic.

## Acknowledgement of tools

Implementation was assisted by an AI coding assistant (Claude). Research questions, protocol decisions,
interpretation and writing are the author's own.
