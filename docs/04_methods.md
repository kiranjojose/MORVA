# 04 — Methods

## Preprocessing
UTC parse → schema cast → AOI + Class A filter → sentinels to null → flags (invalid position, bad MMSI, duplicate, implied-speed spike, high SOG) → segmentation at gaps > `gap_s` → minimum points/duration.

## Prediction task
1-min resampling (linear lat/lon/SOG, circular COG). History of 20 min including the anchor point, forecast of 20 min. Windows are discarded if any original AIS gap inside them exceeds 180 s, or if mean history SOG < 1 kn.

## Baselines
- **Persistence**: last position.
- **CV**: last reported SOG/COG, finite-difference fallback.
- **CTRV**: constant turn rate from the mean COG change over the last 5 min, clipped to ±3°/s, set to 0 below 1 kn.
- **Damped CTRV**: the estimated turn rate decays exponentially; the decay constant is selected on training data.
- **CV Kalman**: linear local-position/velocity state estimator; process noise is selected on training data.

## Learned residual model
The learned model uses scikit-learn's histogram gradient boosting with absolute-error loss. It begins with the CV
trajectory and predicts along-track and cross-track residuals in the vessel's body frame at 5, 10, 15 and 20 minutes.
Intermediate one-minute residuals are linearly interpolated.

Four controlled feature sets are evaluated:

- **A motion**: recent SOG statistics, speed changes, net turns, COG jitter, reported/finite-difference speed ratio and
  past positions in the body frame.
- **B vessel**: A plus ship group, length, width and draught.
- **C location**: A plus latitude, longitude and sine/cosine of anchor course.
- **D all**: motion, vessel and location features.

The learner and prediction targets remain fixed across feature sets. Seeds 0–2 are reported. The model is deterministic
and does not yet produce calibrated uncertainty.

## Generalisation settings

- **In-area chronological**: train on 19–30 September; evaluate validation 1–3 October and test 4–6 October.
- **Vessel-held-out**: remove all evaluation MMSIs from the training set; compare with a random training subset of the
  same size.
- **Spatially held-out**: divide the AOI into four longitude bands; for each band, train outside the band and a 0.05°
  buffer, then predict anchors inside the held-out band.

## Metrics
ADE, FDE and per-horizon error (m, haversine). Mean, median and p90, with 95% CI from a vessel-grouped bootstrap. Paired differences for model comparisons.

## Manoeuvring regimes (frozen 11 Oct 2026; `src/morva/features/regimes.py`)
A regime describes the vessel's observed motion state at prediction time, computed **only from the last 10 minutes of
the observation history**. No future movement, position or prediction error is used.

Variables (all kept as continuous values alongside the label): mean SOG; speed change (final SOG − SOG 10 min earlier);
turn rate = |net COG change| / 10 min (net, not mean absolute, which is dominated by COG noise); signed turn rate;
turn consistency (share of 1-min course changes with the same sign as the net turn); position-derived turn (bearing of
the first vs second half-leg) as a robustness check.

| Regime | Definition (past 10 min) | Interpretation |
|---|---|---|
| Low-speed | mean SOG < 5 kn | harbour movement, waiting, slow manoeuvring; COG less reliable |
| Steady transit | ≥ 5 kn, turn < 1°/min, \|ΔSOG\| < 2 kn | approximately straight, constant speed |
| Turning | ≥ 5 kn, turn ≥ 1°/min, \|ΔSOG\| < 2 kn | course alteration without major speed change |
| Speed-changing | ≥ 5 kn, turn < 1°/min, \|ΔSOG\| ≥ 2 kn | acceleration or deceleration |
| Combined | ≥ 5 kn, turn ≥ 1°/min, \|ΔSOG\| ≥ 2 kn | simultaneous turn and speed change |

Rationale: 1°/min ≈ 10° of net course alteration in 10 min, separating route bends from small corrections while
keeping enough samples. 2 kn in 10 min is operational acceleration rather than AIS fluctuation. 5 kn is a pragmatic
data-quality and operational boundary (COG instability; mixed harbour behaviours), not a universal ship-handling law.

**Quality safeguard:** a turning or straight label is "reliable" when ≥ 80% of COG values are valid, mean SOG ≥ 5 kn,
and the COG-based and position-based turn fall on the same side of the threshold.

**Sensitivity (one parameter at a time):** turn 0.5 / 1 / 2°/min; speed change 1 / 2 / 3 kn; low speed 3 / 5 / 7 kn;
lookback 5 / 10 / 15 min; plus "sustained turning" (≥ 70% of 1-min changes with the same sign).

Context variables (port proximity, fairway, vessel type, traffic) are deliberately **not** part of the regime, so their
contribution can be measured *within* a regime.

## V2: fairway context from historical traffic (`src/morva/features/fairway.py`)

**Feature sets.** E = A (21 motion features) + 14 fairway features = 35 features. F = E + 4 vessel features (ship
group, length, beam, draught) = 39 features. Both use the same residual GBM, targets, hyperparameters and training
windows as A–D. E and F contain no latitude, longitude, projected coordinates or absolute bearing: every fairway
feature is measured relative to the vessel's own position and course.

**Data source.** No external chart or fairway dataset is used. Each region's flow map is built from that region's own
DMA AIS track points in the training period (19–30 Sep 2026): moving points only (SOG ≥ 3 kn), one point per vessel per
minute, so density means vessel-minutes. The map is versioned by its configuration (`fairway:` in
`configs/experiment.yaml`) and the code at the pinned commit `9491f7d`.

**Flow map.** A grid of 300 m cells × 12 course bins (30° each), in a local metric projection of the region's box. Each
(cell, bin) stores the count, the sums of sin and cos of course, and first and second moments of position within the
cell.

**Query.** For a query position and course, the map pools a 5 × 5 block of cells (1.5 km × 1.5 km) and the course bin
of the query course ± 1 bin (about ± 45°). Only same-direction traffic contributes, so the opposite lane of a traffic
separation scheme is ignored. No single fairway is selected: all same-direction traffic in the block is pooled.

**Features.** At the last observed position (the anchor):

| Feature | Meaning |
|---|---|
| `flow_logdens_0` | log(1 + same-direction vessel-minutes per map day) |
| `flow_coher_0` | mean resultant length of pooled courses (1 = one clear direction) |
| `flow_hdg_0` | flow course minus vessel course, degrees, + = flow to starboard |
| `flow_offset_0` | vessel's offset from the flow centroid along the flow's starboard axis, metres |
| `flow_width_0` | lateral standard deviation of the pooled traffic, metres |

At the constant-velocity positions 5, 10 and 20 minutes ahead (`k` = 5, 10, 20): `flow_logdens_k`, `flow_hdg_k` and
`flow_offset_k`, using the vessel's current course to select same-direction traffic. Features are computed only at the
anchor and these three points, not along the observed history.

**Junctions and multiple branches.** Where same-direction branches diverge inside the pooled block, their traffic is
averaged: the flow direction is a mixture and `flow_coher_0` falls. Coherence is the model's only signal of such
ambiguity; no branch is chosen. This is a known weakness near junctions (see limitations).

**Missing coverage.** If fewer than 10 vessel-minutes are pooled, all flow features except density are missing; a
query outside the region's box is missing entirely. The gradient-boosting model handles missing values natively. On
the test period, flow features are present for 96.5% of home, 93.4% of Bornholm and 96.1% of Skagen windows.

**Scaling.** No normalisation is applied (tree models are invariant to monotone scaling). Density is divided by the
number of days in the map.

**Leakage guard.** A window whose future falls inside the map period (a training window) receives a map built without
the day or days its future covers, so it never sees its own future path. Validation, test and independent-waterway
windows use the full training-period map, which contains none of their days.

**Use of the independent waterways.** Bornholm and Skagen were chosen on 18 Oct from a one-day traffic count on a
training-period day (24 Sep), before any model was run on them. The fairway method and all its settings were fixed
before the first evaluation and were not tuned afterwards. Validation results in the waterways (`transfer_val`) were
then inspected and informed the V2 hypotheses; their windows were never used to fit a model.

**V2 split.** Train 19–30 Sep (home windows only), validation 1–6 Oct, test 7–15 Oct (locked); window counts per
region and split are in `docs/03_data_card.md`. Hypotheses, decision rules and the primary seed (0) are in
`docs/05_protocol.md`.

## V3: 60-minute prediction, cross-country transfer and calibrated boxes

V3 is configured independently in `configs/v3/data.yaml` and `configs/v3/experiment.yaml`; the V1 and V2
configurations are unchanged. The hypotheses and one-pass test procedure were frozen in `docs/05_protocol.md` at
commit `126dda2`, using the code pinned there.

### Prediction task and windows

Each example contains 20 minutes of observed motion and 60 minutes of future motion on a one-minute grid. Point errors
are evaluated after 5, 10, 20, 30, 45 and 60 minutes, with FDE referring to the 60-minute endpoint. Residual targets
are fitted at 5, 10, 15, 20, 30, 45 and 60 minutes and interpolated linearly between those knots.

The complete history–future span must remain inside one calendar block. Windows are rejected when an original AIS gap
anywhere in the 80-minute span exceeds 180 seconds or when mean speed during the history is below 1 knot. Consecutive
anchors remain five minutes apart, so observations overlap and are not statistically independent.

### Sources and canonical schema

Two providers feed the same internal schema through `src/morva/ingestion/sources.py`:

- Danish data use the DMA adapter established in V1.
- US data use NOAA/BOEM Marine Cadastre 2025 daily `.csv.zst` files and
  `src/morva/ingestion/marinecadastre.py`. Provider fields for time, MMSI, position, SOG, COG, heading, dimensions,
  draught and identity metadata are renamed to the DMA-compatible columns. Transceiver value `A` becomes `Class A`
  and only that class is retained. Numeric AIS vessel-type codes are converted to common labels—including 70–79 as
  cargo, 80–89 as tanker, 52 as tug and 31–32 as towing—before the shared ship-group mapping is applied. Numeric
  navigational-status codes are likewise converted to their AIS text meanings; unrecognised values are retained as
  strings rather than silently assigned a known status.

### Regions and calendars

The five regions are the Danish home area, Bornholm and Skagen on the 2026 calendar, plus the Salish Sea and Houston
on the 2025 calendar. Each calendar contains four non-overlapping blocks:

| Purpose | Dates | Home label | Transfer-region label |
|---|---|---|---|
| Model fitting and flow-map history | 19 Sep–6 Oct | `train` | `transfer_context` |
| Model selection | 7–11 Oct | `val` | `transfer_val` |
| Interval calibration | 12–15 Oct | `calib` | `transfer_calib` |
| Locked evaluation | 16–29 Oct | `test` | `transfer_test` |

Only home `train` windows fit model parameters. Transfer-region history constructs the region's flow map but never
fits the forecasting model. A window receives a label only when its entire 80-minute span lies within that block.

### Point models and V3 fairway features

Feature sets A–F retain the V2 learner and hyperparameters, with seed 0 prespecified. Each region's flow map is built
from its own context block. The anchor contributes density, coherence, heading difference, lateral offset and lane
width. Density, heading difference and lateral offset are then queried at the constant-velocity positions 5, 10, 20,
30, 45 and 60 minutes ahead. This produces 23 fairway features rather than V2's 14. Model E therefore contains 21
motion plus 23 fairway features (44 total); model F adds four vessel features (48 total).

### Quantile prediction boxes and conformal adjustment

For every one of the seven target knots and both body-frame axes, four histogram-gradient-boosting models estimate the
0.05, 0.10, 0.90 and 0.95 residual quantiles. Model E therefore fits 7 × 2 × 4 = 56 quantile regressors. Predicted
quantiles are sorted along the quantile dimension before interval construction, preventing independently fitted
quantiles from crossing. The central 80% box uses the 0.10 and 0.90 estimates on both axes; the 90% box uses 0.05 and
0.95.

Split-conformal calibration then applies a common per-knot adjustment to both axes. For calibration window `i`, knot
`h` and axes `a` in {along, cross}, the nonconformity score is

`s[i,h] = max_a(max(lower[i,h,a] − truth[i,h,a], truth[i,h,a] − upper[i,h,a]))`.

For target coverage `p` and `n` calibration windows, `k = ceil((n + 1) × p)` and `q[h]` is the `k`-th smallest
score at knot `h` (or infinity if `k > n`). The adjusted box is

`[lower[i,h,a] − q[h], upper[i,h,a] + q[h]]`.

Because the score takes the worse axis, the target is joint two-dimensional coverage of the future position, not
separate marginal coverage of along- and cross-track coordinates. Under exchangeability, the construction provides a
finite-sample marginal guarantee; overlapping windows from the same vessel weaken the literal independence premise,
so held-out empirical coverage and vessel-grouped uncertainty are still reported. Although `q[h]` is normally a
positive widening, the implementation treats it as a general conformal adjustment because an already conservative
raw box can yield a negative score quantile.

### Calibration and evaluation

Home calibration uses `calib` windows from the Danish home area. Local calibration instead uses `transfer_calib`
windows from the evaluated region, without changing model weights. Both versions are evaluated on identical target
windows. In the validation study, calibration dates follow the model-selection dates; in the locked test study,
calibration precedes evaluation, matching the intended deployment order.

Point forecasts report mean, median and 90th-percentile displacement error at every horizon. Model contrasts are
paired on identical windows and receive vessel-grouped bootstrap 95% confidence intervals with 1,000 resamples.
Interval evaluation reports joint-box coverage with the same grouped interval and the mean along- and cross-track
half-widths. Coverage is aggregate over all windows in a setting; it is not conditional coverage within a vessel type,
regime or location. The pre-written `scripts/v3_decide.py` reads saved summaries and applies the frozen hypothesis
rules mechanically; it neither fits a model nor selects a threshold.
