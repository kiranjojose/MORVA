# MORVA

**Context-aware vessel manoeuvre prediction from AIS, with reproducible baselines, manoeuvring-regime analysis and
explicit generalisation tests.**

MORVA (Maritime Operational Reasoning and Vessel Analytics) is an independent maritime machine-learning research project. It asks a focused question:

> When do vessel and geographic context improve 5–20-minute trajectory prediction beyond constant-motion and
> motion-only learned baselines, and do those improvements transfer to unseen vessels and unseen waters?

The project combines AIS data engineering, geospatial processing, interpretable kinematic models, residual machine
learning and leakage-aware evaluation. It is an offline research prototype, not a real-time or safety-certified
navigation system.

## Why this problem matters

AIS reports where a vessel is, how fast it is moving and its course over ground. It does not directly reveal why the
vessel is manoeuvring or when the manoeuvre will end. A turn can continue, settle onto a new course, follow a fairway
bend or lead into a terminal approach.

This creates a useful modelling question. Recent motion provides a strong short-term baseline, while vessel type,
dimensions and location may contain additional information. Those same variables can also create shortcuts: vessel
attributes may identify recurring services, and raw coordinates may let a model memorise local routes. MORVA
therefore evaluates both predictive accuracy and transfer.

## Study at a glance

| Item | Design |
|---|---|
| Data | Danish Maritime Authority historical shore-based AIS |
| Study period | 19 September–6 October 2026 |
| Study area | Great Belt, Øresund and southern Kattegat |
| Population | Class A AIS transmitters |
| Prediction task | 20-minute history → 20-minute future at one-minute resolution |
| Dataset | 359,738 gap-safe windows from 1,971 vessels |
| Split | 12 training days, 3 validation days, 3 locked test days |
| Baselines | Persistence, CV, CTRV, damped CTRV, CV Kalman filter |
| Learned model | Gradient-boosted residual correction to constant velocity |
| Context ablation | Motion; + vessel attributes; + raw location; all features |
| Generalisation | Later time period, unseen vessels and spatially held-out longitude bands |
| Metrics | ADE, FDE and horizon errors with vessel-grouped bootstrap intervals |

## Main result

![Test FDE at 20 minutes in three evaluation settings](results/figures/generalisation_test.png)

Mean final displacement error at 20 minutes on the 57,068-window test period:

| Model | In-area | Unseen vessels | Unseen waters |
|---|---:|---:|---:|
| Constant velocity | 1,554 m | 1,554 m | 1,554 m |
| A: motion only | 1,267 m | 1,429 m | 1,465 m |
| B: + vessel attributes | 1,128 m | 1,367 m | 1,442 m |
| C: + raw location | 863 m | 1,165 m | 2,592 m |
| D: all features | **831 m** | **1,140 m** | 1,918 m |

Four conclusions define the project:

1. **Constant velocity is a strong baseline.** Ordinary CTRV is 467 m worse at 20 minutes; damped CTRV and the
   constant-velocity Kalman filter converge to approximately the CV result.
2. **Motion-only learning helps most during non-steady behaviour.** The test improvement over CV is 88 m during
   steady transit, 316 m while turning and 1,078 m during combined turning and speed change.
3. **Raw location is highly predictive inside familiar waters.** The full model reduces in-area FDE@20 by 47%, and
   the benefit survives when every test vessel is removed from training.
4. **Raw location does not transfer to unseen waters.** Spatial hold-out reverses the gain: location is 1,127 m worse
   than motion alone. The in-area model learned useful but geographically attached route corrections.

The negative transfer result is central. High in-area accuracy does not demonstrate transferable geographic
understanding.

## Research design

### Leakage-aware windows

AIS messages are irregular. MORVA segments tracks, resamples them to one-minute intervals and rejects a prediction
window if any original reporting gap inside its history or future exceeds 180 seconds. Windows never cross the
train/validation/test boundaries.

### Transparent baselines

- **Persistence:** remain at the last observed position.
- **Constant velocity (CV):** continue with the latest speed and course.
- **CTRV:** continue with the recent speed and turn rate.
- **Damped CTRV:** decay the recent turn rate over the forecast horizon.
- **CV Kalman:** estimate position and velocity using a linear Kalman filter.

Baseline parameters are selected using training data only.

### Residual prediction

The learned model starts from the CV trajectory and predicts an along-track and cross-track correction in the vessel's
local body frame. Corrections are estimated at 5, 10, 15 and 20 minutes and interpolated between those knots.

The four controlled feature sets are:

- **A — motion:** recent speed, speed change, course change, course jitter and past relative positions;
- **B — vessel:** A plus vessel group, length, beam and draught;
- **C — location:** A plus latitude, longitude and course orientation;
- **D — all:** motion, vessel and location features.

Holding the learner and samples fixed makes it possible to attribute changes to the added information rather than to a
different model architecture.

### Past-only manoeuvring regimes

Every sample is classified from the last 10 minutes of observed history:

| Regime | Past-only definition |
|---|---|
| Low-speed | Mean SOG below 5 kn |
| Steady | At least 5 kn, turn below 1°/min, speed change below 2 kn |
| Turning | At least 5 kn, turn at least 1°/min, speed change below 2 kn |
| Speed-changing | At least 5 kn, turn below 1°/min, speed change at least 2 kn |
| Combined | At least 5 kn, turn at least 1°/min, speed change at least 2 kn |

The regime analysis includes alternative thresholds and a position-derived turn check. Context variables are not part
of the regime definition, so their contribution can be measured within each motion state.

### Generalisation tests

- **Chronological test:** later whole-day time block.
- **Vessel-held-out:** every evaluation vessel is removed from training, with a same-size random-subset control.
- **Spatially held-out:** each longitude band is predicted by a model trained outside that band with a buffer.
- **Multiple seeds:** learned models are repeated with seeds 0–2.

Paired error differences use identical windows. Confidence intervals resample whole vessels because overlapping
windows from one vessel are not independent.

## Reproducible pipeline

```text
raw DMA ZIP/CSV + checksummed manifests
  → ingest: AOI and Class A filtering, schema conversion, exact de-duplication
  → quality: sentinel normalisation, flags and quality report
  → tracks: gap-based segmentation and vessel metadata
  → windows: one-minute resampling, gap-safe histories/futures, chronological split
  → baselines: persistence, CV, CTRV, damped CTRV and CV Kalman
  → learning: residual GBM with motion/vessel/location ablations
  → evaluation: horizon metrics, paired differences, grouped confidence intervals
  → analysis: regimes, vessel hold-out, spatial hold-out and sensitivity tests
```

Raw data are not committed. Manifests record filenames, checksums and provenance; derived aggregate tables and figures
are versioned.

## Quick start

Requirements: Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
make smoke
```

`make smoke` runs the complete pipeline in an isolated synthetic workspace, so synthetic artifacts cannot be mixed
with real experiment outputs.

To process DMA data:

```bash
uv run morva manifest data/raw/aisdk-YYYY-MM-DD.zip --notes "..."
make pipeline
uv run morva gbm
```

The test split is deliberately protected by `--confirm-test`. It has already been used for the recorded V1 test run
and must not be used for further model development.

## Technology

- **Python 3.12**
- **Polars, PyArrow and Parquet** for large tabular AIS processing
- **NumPy** for trajectory tensors, geometry and vectorised baselines
- **scikit-learn** for histogram gradient boosting
- **DuckDB** for local analytical queries
- **Matplotlib** for research figures
- **PyYAML** for configuration-driven experiments
- **pytest** and **Ruff** for verification and static checks
- Optional **PyTorch** dependency for future sequence-model experiments

## Repository structure

| Path | Purpose |
|---|---|
| `src/morva/ingestion/` | DMA ingestion, manifests and synthetic data |
| `src/morva/quality/` | Sentinel normalisation and quality flags |
| `src/morva/trajectories/` | Track segmentation and vessel metadata |
| `src/morva/features/` | Windows, motion features and regimes |
| `src/morva/models/` | Kinematic baselines, Kalman filter and residual GBM |
| `src/morva/evaluation/` | Splits, metrics and grouped uncertainty |
| `src/morva/viz/` | Maps and result visualisations |
| `configs/` | Data and experiment configuration |
| `docs/` | Problem, literature, methods, protocol, results and limitations |
| `paper/` | Preliminary research summary |
| `results/` | Versioned tables, figures and run summaries |
| `tests/` | Geodesy, quality, segmentation, window, model and regime tests |

## Documentation

- [Problem statement and motivation](docs/01_problem.md)
- [Literature position](docs/02_literature.md)
- [Data card and terms](docs/03_data_card.md)
- [Methods](docs/04_methods.md)
- [Protocol and hypothesis provenance](docs/05_protocol.md)
- [Validation and test results](docs/06_results.md)
- [Limitations](docs/07_limitations.md)
- [Research log](docs/08_research_log.md)
- [Preliminary research summary](paper/preliminary_summary.md)

## Scope and limitations

The results cover 18 days, one Danish study area and Class A traffic. The spatial folds are bands within that area,
not independent waterways. The learned comparison uses one model family and deterministic outputs. AIS omits control
commands, route intent and several environmental and interaction variables.

MORVA does not provide collision avoidance, infer intent, certify anomalies or replace radar, bridge judgement or
VTS procedures. See the full [limitations](docs/07_limitations.md).

## Next research steps

1. Replace raw coordinates with transferable features: fairway-relative position and bearing, local curvature,
   coastline and bathymetry constraints, port proximity and historical traffic-flow fields.
2. Evaluate geographic transfer on independent waterways and longer time periods.
3. Add calibrated uncertainty and multiple plausible future trajectories.
4. Model surrounding-vessel interactions under the same controlled evaluation.
5. Evaluate prediction residuals for anomaly screening only after defining credible labels and operational criteria.

## Data access

Historical AIS files are available from the
[Danish Maritime Authority](https://www.dma.dk/safety-at-sea/navigational-information/ais-data). Raw files are not
redistributed here. The [data card](docs/03_data_card.md) records the study selection, observed quality, source terms
and known biases.

## Licence

Code is released under the [MIT License](LICENSE). DMA AIS data is not included and remains subject to the provider's
terms.

## Acknowledgement of tools

Implementation was assisted by an AI coding assistant (Claude). Research questions, protocol decisions,
interpretation and writing are the author's own.
