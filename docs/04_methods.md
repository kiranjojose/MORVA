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

## Manoeuvring regimes (frozen 11 Oct 2026; `src/vesselmind/features/regimes.py`)
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
