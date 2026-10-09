# 04 — Methods

## Preprocessing
UTC parse → schema cast → AOI + Class A filter → sentinels to null → flags (invalid position, bad MMSI, duplicate, implied-speed spike, high SOG) → segmentation at gaps > `gap_s` → minimum points/duration.

## Prediction task
1-min resampling (linear lat/lon/SOG, circular COG). History of 20 min including the anchor point, forecast of 20 min. Windows are discarded if any original AIS gap inside them exceeds 180 s, or if mean history SOG < 1 kn.

## Baselines
- **Persistence**: last position.
- **CV**: last reported SOG/COG, finite-difference fallback.
- **CTRV**: constant turn rate from the mean COG change over the last 5 min, clipped to ±3°/s, set to 0 below 1 kn.

## Learned models (next)
GBM on displacement targets; small GRU (A: motion-only, B: + vessel type/size). Three seeds each, with Gaussian output for uncertainty.

## Metrics
ADE, FDE and per-horizon error (m, haversine). Mean, median and p90, with 95% CI from a vessel-grouped bootstrap. Paired differences for model comparisons.
