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

**Status: experimentally complete (test run 21 Oct 2026).** Fairway context from historical traffic (model E) improved
on motion-only prediction at home and in both independent waterways, and raw coordinates made prediction worse in both
(V2-H1 and V2-H2 supported; `docs/06_results.md`). The plan as written before V2 follows.

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

**Status: split set (2026-10-18).** New locked test period 7–15 Oct 2026. Independent waterways: Bornholm
(Bornholmsgat) and Skagen. See `docs/05_protocol.md`, "V2 split".

## Next directions after V2

- Junction and route-choice representation, so diverging branches are not averaged.
- Port, berth and anchorage context, and low-speed or harbour-specific modelling.
- Chart-based context that does not need traffic history: bathymetry and coastline constraints.
- Other countries, seasons and waterway types, including waters with sparse traffic history.
- Uncertainty, longer horizons and transfer to another country (V3 below).

## V3 — Reliable forecasts in new waters (planned 22 Oct 2026)

V2 showed that fairway context makes forecasts *better* in waters the model has never seen. V3 asks whether they are
*trustworthy* there: honest uncertainty, longer horizons and transfer to another country. These are research
questions in their own right and also the questions behind any later product decision. The study stays
research-led, with the V1/V2 discipline: a split set before data are inspected, hypotheses frozen before the test,
and one test run.

### Scope

- **In:** calibrated prediction intervals; horizons up to 60 minutes; transfer to another country (USA: Salish Sea,
  optionally Houston); how much traffic history a flow map needs; junction ambiguity (exploratory).
- **Out (later versions):** neighbouring-vessel interaction moves to V4; behaviour-deviation screening moves to V5.
  Finland is deferred: its open data (Digitraffic, CC BY 4.0) has no historical archive and would need weeks of live
  recording, so it is a possible V3b.

### Research questions

| | Question | Why |
|---|---|---|
| RQ1 | Can the residual model give calibrated 80% and 90% prediction intervals, and do they stay calibrated in independent waterways and another country? | A forecast without honest uncertainty cannot support a decision |
| RQ2 | Does fairway context's advantage over motion-only grow with horizon (20 → 60 min)? | Lane knowledge should matter more the further ahead the forecast goes |
| RQ3 | Does a model trained in Denmark, using the US waterway's own flow map, improve on motion-only in the USA? | Transfer across countries, traffic cultures and receiver networks |
| RQ4 | How many days of traffic history does a flow map need (1, 3, 7, all map days)? | How quickly a new area can be supported |
| RQ5 (exploratory) | Near junctions, do features describing several same-direction branches improve on the averaged flow? | The known weakness of V2 |

### Data and split (historical, time runs forward)

All test periods are untouched: their files are **not downloaded until the V3 hypotheses are frozen**. Models are
trained in the Danish home area only.

| Region | Map history / training | Validation | Test (locked) |
|---|---|---|---|
| Denmark: home (training area) | 19 Sep–6 Oct 2026 (train) | 7–15 Oct 2026 (spent V2 test days) | 16–29 Oct 2026 |
| Denmark: Bornholm, Skagen | 19 Sep–6 Oct 2026 (map only) | 7–15 Oct 2026 | 16–29 Oct 2026 |
| USA: Salish Sea | 19 Sep–6 Oct 2025 (map only) | 7–15 Oct 2025 | 16–29 Oct 2025 |
| USA: Houston (optional) | 19 Sep–6 Oct 2025 (map only) | 7–15 Oct 2025 | 16–29 Oct 2025 |
| Norway: Bergen/Fedje (optional) | as Denmark, if Kystverket HAIS data are recent enough | | |

- **Validation days are used for two separate purposes:** 7–11 Oct for model selection, and 12–15 Oct as the
  calibration set for the prediction intervals. The two must not overlap.
- **USA data:** NOAA/BOEM Marine Cadastre daily files for 2025 (`ais-2025-MM-DD.csv.zst`, about 230 MB each, already
  sampled at one minute). The catalogue lists no access constraints; the stated use is "coastal and ocean planning,
  not for navigation", and the data are provided as is. That is sufficient for research. Commercial use is not
  addressed explicitly and must be confirmed with NOAA before any product use.
- **USA boxes (set 23 Oct 2026 from a one-day traffic count on 24 Sep 2025, a map-period day, before any model was
  run; Class A, moving = SOG > 5 kn, counted in vessel-minutes because US data are one-minute sampled):**

  | Area | Box | Moving vessels | Moving vessel-minutes | Merchant (cargo + tanker) vessels |
  |---|---|---:|---:|---:|
  | Salish Sea (primary) | 47.0–48.8° N, 124.7–122.2° W | 256 | 50,958 | 56 |
  | Houston (optional) | 28.9–29.8° N, 95.3–94.3° W | 488 | 74,220 | 97 |
  | For comparison, same calendar day in 2026: Bornholm | | 201 | 43,983 | 155 |
  | Skagen | | 262 | 50,179 | 141 |

  The Salish Sea box covers the Strait of Juan de Fuca, Admiralty Inlet, Puget Sound and parts of Haro and Rosario
  Straits: traffic separation schemes, the Washington State Ferries network and merchant approaches. Coverage continues
  across the Canadian border, so the box is not cut by it. A first box limited to Puget Sound (47.0–48.3° N,
  123.2–122.2° W) was rejected: 133 moving vessels, 21,480 vessel-minutes and only 17 merchant vessels. Houston covers
  the Houston Ship Channel, Galveston Bay and the offshore fairway. About two-thirds of its moving traffic is tugs and
  towboats, so Houston is reported both overall and for merchant vessels only. US merchant traffic is thinner than
  Danish, so all US results are also reported by ship group.
- **Year difference:** US data are from 2025 and Danish data from 2026. Each region uses its own forward-in-time split
  and its own flow map, so the comparison stays internally consistent; the difference is reported as a limitation.
- **Norway** joins only if a small test order from Kystverket HAIS shows data for the same 2026 periods and terms
  that allow research use.

### Models

- **Point forecasts:** A, C, E and F as in V2 (same learner and hyperparameters), as references.
- **Uncertainty:** the residual model trained for quantiles of the along-track and cross-track corrections at each
  horizon point, then conformal calibration on the calibration days, so interval coverage is honest whenever new data
  resemble the calibration data. Whether that holds in new waters is RQ1. Primary analysis uses the Danish
  calibration only; recalibration on a few local validation days is a descriptive secondary analysis.
- **Junction features (exploratory):** number of distinct same-direction flow directions ahead and the angle between
  them.

### Prediction task

20-minute history and 60-minute future at one-minute resolution (V2 used 20 minutes). Errors are reported at 5, 10,
20, 30, 45 and 60 minutes. Windows need gap-safe 60-minute futures, so there will be fewer windows than in V2.

### Metrics

| Kind | Metrics |
|---|---|
| Accuracy | ADE; FDE at 5, 10, 20, 30, 45 and 60 min; median, 90th and 99th percentile |
| Uncertainty | Coverage of the 80% and 90% intervals; interval width; pinball loss |
| Plausibility | Share of forecast points in cells with no historical traffic (off-lane rate) |
| Data needs | E's error as a function of map history (1, 3, 7, all days) |
| Cost | Flow-map build time; prediction time per 1,000 windows |

All confidence intervals remain paired and vessel-grouped.

### Draft hypotheses (to be refined on validation, then frozen before the test)

- **V3-H1 (calibration):** conformal 80% and 90% intervals have coverage within 3 percentage points of nominal at 20 and
  60 minutes in the home area, Bornholm and Skagen.
- **V3-H2 (cross-country transfer):** E improves on A in the Salish Sea at 20 and 60 minutes.
- **V3-H3 (horizon):** in the independent waterways (Bornholm, Skagen, Salish Sea), E's relative improvement over A
  is larger at 60 minutes than at 20.
- **Descriptive:** interval coverage in the Salish Sea with and without local recalibration; Houston (overall and
  merchant-only) and Norway if included; map-history curve; junction features.

### Engineering needed

1. Windows with 60-minute futures and multi-horizon reporting.
2. A source adapter for Marine Cadastre CSV (field names, numeric vessel-type codes mapped to ship groups,
   transceiver class, `.zst` files), and one for Kystverket HAIS if Norway is included.
3. A quantile residual model and a conformal-calibration module.
4. Coverage, interval-width and off-lane metrics in run summaries, tables and figures.
5. A configurable map-history window for RQ4.
6. Processing one region at a time, as in V2, to keep memory in bounds.

### Order of work

1. **Data feasibility:** download US map-period and validation days only; one-day traffic count to confirm the boxes
   (done 23 Oct); Norway test order (by the author).
2. **Set the V3 split** in the configuration before any validation analysis.
3. **Infrastructure:** 60-minute windows, the US adapter, quantile model and calibration; tests and synthetic smoke run.
4. **Validation:** point and interval results in Denmark and the USA; map-history curve; junction features.
5. **Freeze V3 hypotheses**, with decision rules, primary seed and exact test commands, as in V2.
6. **Download the test periods and run the single test pass**; record every run.
7. **Write-up and product decision point:** does the model transfer to another country, are its intervals honest, and
   is the gain large enough at 30–60 minutes to matter for a real use, such as estimating a vessel's position when
   its AIS is stale?

## V4 — Neighbouring vessels and interaction

- Add neighbouring-vessel features and encounter geometry without future leakage.
- Evaluate whether interaction context improves forecasts in close-quarters situations.
- Measure compute, latency and degradation under missing observations.

## V5 — Behaviour deviation research

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
