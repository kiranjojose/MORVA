# V4 decision (val)

Runs: `20261106T115415Z_gbm_transfer_val_oslofjord`, `20261106T120458Z_gbm_transfer_val_skagen`, `20261110T073136Z_intervals_E_fairway_val`, `20261110T073136Z_intervals_E_fairway_transfer_val_oslofjord_localcal`, `20261110T073136Z_intervals_E_fairway_transfer_val_skagen_localcal`, `20261106T121243Z_deviation_E_fairway_val`, `20261106T114329Z_gbm_val`

| Hypothesis | Outcome |
|---|---|
| V4-H1 | **supported** |
| V4-H2 | **supported** |
| V4-H3 | **supported** |
| V4-H4 | **supported** |
| V4-H5 | **supported** |

## V4-H1

| Check | Value | Pass |
|---|---|---|
| oslofjord: E_fairway - A_motion at 20 min, 95% CI upper < 0 | −315 m (−400 to −226) | yes |
| oslofjord: E_fairway - A_motion at 60 min, 95% CI upper < 0 | −990 m (−1,285 to −746) | yes |
| skagen: E_fairway - A_motion at 20 min, 95% CI upper < 0 | −107 m (−132 to −86) | yes |
| skagen: E_fairway - A_motion at 60 min, 95% CI upper < 0 | −714 m (−830 to −605) | yes |

## V4-H2

| Check | Value | Pass |
|---|---|---|
| oslofjord: C_location - A_motion at 20 min, 95% CI lower > 0 | +646 m (+511 to +828) | yes |
| oslofjord: C_location - A_motion at 60 min, 95% CI lower > 0 | +1,215 m (+828 to +1,718) | yes |
| skagen: C_location - A_motion at 20 min, 95% CI lower > 0 | +1,702 m (+1,503 to +1,934) | yes |
| skagen: C_location - A_motion at 60 min, 95% CI lower > 0 | +5,281 m (+4,668 to +6,007) | yes |

## V4-H3

| Check | Value | Pass |
|---|---|---|
| home: 80% box at 20 min within ±3 points | 81.8% (nominal 80%) | yes |
| home: 80% box at 60 min within ±3 points | 81.3% (nominal 80%) | yes |
| home: 90% box at 20 min within ±3 points | 90.8% (nominal 90%) | yes |
| home: 90% box at 60 min within ±3 points | 90.6% (nominal 90%) | yes |
| oslofjord: 80% box at 20 min within ±3 points | 80.6% (nominal 80%) | yes |
| oslofjord: 80% box at 60 min within ±3 points | 80.6% (nominal 80%) | yes |
| oslofjord: 90% box at 20 min within ±3 points | 90.5% (nominal 90%) | yes |
| oslofjord: 90% box at 60 min within ±3 points | 90.0% (nominal 90%) | yes |
| skagen: 80% box at 20 min within ±3 points | 80.1% (nominal 80%) | yes |
| skagen: 80% box at 60 min within ±3 points | 79.8% (nominal 80%) | yes |
| skagen: 90% box at 20 min within ±3 points | 90.3% (nominal 90%) | yes |
| skagen: 90% box at 60 min within ±3 points | 90.0% (nominal 90%) | yes |

## V4-H4

| Check | Value | Pass |
|---|---|---|
| turn_30: model − cv_distance detection at 20 min, 95% CI lower > 0 | +21.7 points (+18.6 to +25.0) | yes |
| turn_30: model − turn detection at 20 min, 95% CI lower > 0 | +23.8 points (+21.1 to +26.7) | yes |
| turn_30: model − speed detection at 20 min, 95% CI lower > 0 | +21.6 points (+17.9 to +25.5) | yes |
| turn_60: model − cv_distance detection at 20 min, 95% CI lower > 0 | +32.4 points (+28.6 to +36.1) | yes |
| turn_60: model − turn detection at 20 min, 95% CI lower > 0 | +34.8 points (+31.6 to +38.1) | yes |
| turn_60: model − speed detection at 20 min, 95% CI lower > 0 | +32.3 points (+28.2 to +36.5) | yes |
| turn_90: model − cv_distance detection at 20 min, 95% CI lower > 0 | +36.2 points (+32.3 to +40.1) | yes |
| turn_90: model − turn detection at 20 min, 95% CI lower > 0 | +38.1 points (+34.6 to +41.5) | yes |
| turn_90: model − speed detection at 20 min, 95% CI lower > 0 | +36.0 points (+31.6 to +40.3) | yes |
| stop: model − cv_distance detection at 20 min, 95% CI lower > 0 | +35.8 points (+32.0 to +39.4) | yes |
| stop: model − turn detection at 20 min, 95% CI lower > 0 | +38.2 points (+35.2 to +41.2) | yes |
| stop: model − speed detection at 20 min, 95% CI lower > 0 | +32.8 points (+28.4 to +37.0) | yes |
| slow_50pct: model − cv_distance detection at 20 min, 95% CI lower > 0 | +27.2 points (+24.3 to +30.2) | yes |
| slow_50pct: model − turn detection at 20 min, 95% CI lower > 0 | +26.4 points (+23.7 to +29.3) | yes |
| slow_50pct: model − speed detection at 20 min, 95% CI lower > 0 | +25.9 points (+22.4 to +29.4) | yes |
| fast_150pct: model − cv_distance detection at 20 min, 95% CI lower > 0 | +27.8 points (+24.5 to +31.2) | yes |
| fast_150pct: model − turn detection at 20 min, 95% CI lower > 0 | +29.6 points (+26.8 to +32.7) | yes |
| fast_150pct: model − speed detection at 20 min, 95% CI lower > 0 | +28.6 points (+24.8 to +32.3) | yes |
| control: model false alarms at 20 min within 4%–6% | 4.8% | yes |

## V4-H5

| Check | Value | Pass |
|---|---|---|
| home: H_wind_current − E_fairway at 60 min, 95% CI inside ±150 m | +3 m (−19 to +23) | yes |
