# 00 — Research and development roadmap

## Objective

Develop and evaluate context-aware 5–20-minute vessel trajectory prediction from historical AIS, with emphasis on
reproducibility, interpretable baselines, manoeuvring regimes and transfer beyond familiar vessels and waters.

## V1 — Reproducible prediction study

**Status: complete.**

- Ingest and document 18 days of Danish historical AIS.
- Build quality checks, trajectory segmentation and gap-safe windows.
- Freeze chronological train, validation and test periods.
- Establish persistence, CV, CTRV, damped CTRV and Kalman baselines.
- Implement a residual gradient-boosting predictor.
- Ablate motion, vessel and raw-location information.
- Define past-only manoeuvring regimes and threshold sensitivity.
- Evaluate later-time, vessel-held-out and spatially held-out generalisation.
- Freeze hypotheses and perform a single test run.
- Publish the preliminary summary, data card, protocol, results and limitations.

## V2 — Transferable navigational context

The V1 spatial hold-out shows that raw coordinates encode useful local knowledge but transfer poorly. V2 replaces
absolute position with features whose meaning is consistent across waterways:

- fairway-relative position and heading;
- local fairway curvature and distance to upcoming bends;
- distance to coastline, port, anchorage and route junctions;
- depth and bathymetric constraints where licensing permits;
- historical traffic-flow direction and density;
- course-relative rather than absolute spatial representation.

Evaluation should include independent waterways, longer time periods and the existing in-area, vessel-held-out and
spatially held-out controls.

## V3 — Uncertainty and interaction

- Produce calibrated trajectory intervals or multiple plausible futures.
- Compare quantile, conformal and probabilistic output formulations.
- Add neighbouring-vessel features and encounter geometry.
- Evaluate calibration and route validity, not displacement error alone.
- Measure compute, latency and degradation under missing observations.

## V4 — Behaviour deviation research

Prediction residuals may support behavioural-deviation screening, but this is a separate task:

- define anomaly categories and operational relevance;
- distinguish data faults from unusual vessel behaviour;
- obtain credible labels or expert-reviewed cases;
- compare residual-based signals with transparent route, speed and turn rules;
- measure false alarms and context-dependent explanations;
- avoid interpreting an outlier as automatically unsafe or illegal.

## Engineering roadmap

- Version datasets, feature definitions and trained artifacts.
- Add experiment tracking and deterministic reproduction commands.
- Create batch inference and historical playback APIs.
- Build an interactive analysis interface for tracks, predictions and uncertainty.
- Add monitoring for data quality, model drift and unsupported operating conditions.
- Document security, retention, licensing and audit requirements before external deployment.
