# Deviation screening (E_fairway; val; alpha 0.05)

376,524 train / 68,219 calibration / 78,568 evaluated windows (638 vessels), anchor speed >= 5.0 kn. Deviations start 10 min into the forecast. First flag = first horizon with p <= 0.05 / 7; per-horizon columns use p <= 0.05.

| deviation | detector | false alarms, first flag | detected, first flag | median delay (min) | detected at 20 min | detected at 60 min |
|---|---|---:|---:|---:|---:|---:|
| none | model_box | 0.017 | 0.015 | 5 | 0.048 | 0.051 |
| none | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| none | turn | 0.030 | 0.025 | 10 | 0.046 | 0.052 |
| none | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_15 | model_box | 0.017 | 0.054 | 10 | 0.149 | 0.167 |
| turn_15 | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| turn_15 | turn | 0.030 | 0.012 | 5 | 0.030 | 0.016 |
| turn_15 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_30 | model_box | 0.017 | 0.088 | 10 | 0.264 | 0.267 |
| turn_30 | cv_distance | 0.017 | 0.015 | 0 | 0.046 | 0.049 |
| turn_30 | turn | 0.030 | 0.010 | 0 | 0.026 | 0.013 |
| turn_30 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_60 | model_box | 0.017 | 0.145 | 10 | 0.371 | 0.374 |
| turn_60 | cv_distance | 0.017 | 0.017 | 5 | 0.047 | 0.047 |
| turn_60 | turn | 0.030 | 0.009 | 0 | 0.023 | 0.007 |
| turn_60 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_90 | model_box | 0.017 | 0.176 | 10 | 0.408 | 0.421 |
| turn_90 | cv_distance | 0.017 | 0.019 | 10 | 0.045 | 0.048 |
| turn_90 | turn | 0.030 | 0.010 | 0 | 0.027 | 0.009 |
| turn_90 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| stop | model_box | 0.017 | 0.146 | 10 | 0.397 | 0.392 |
| stop | cv_distance | 0.017 | 0.007 | 0 | 0.039 | 0.038 |
| stop | turn | 0.030 | 0.007 | 0 | 0.015 | 0.001 |
| stop | speed | 0.018 | 0.019 | 5 | 0.069 | 0.054 |
| slow_50pct | model_box | 0.017 | 0.068 | 5 | 0.309 | 0.288 |
| slow_50pct | cv_distance | 0.017 | 0.009 | 0 | 0.037 | 0.032 |
| slow_50pct | turn | 0.030 | 0.025 | 10 | 0.045 | 0.052 |
| slow_50pct | speed | 0.018 | 0.015 | 0 | 0.050 | 0.050 |
| slow_75pct | model_box | 0.017 | 0.036 | 10 | 0.155 | 0.142 |
| slow_75pct | cv_distance | 0.017 | 0.012 | 0 | 0.040 | 0.042 |
| slow_75pct | turn | 0.030 | 0.025 | 10 | 0.046 | 0.052 |
| slow_75pct | speed | 0.018 | 0.015 | 0 | 0.048 | 0.049 |
| fast_125pct | model_box | 0.017 | 0.035 | 10 | 0.163 | 0.146 |
| fast_125pct | cv_distance | 0.017 | 0.018 | 5 | 0.055 | 0.057 |
| fast_125pct | turn | 0.030 | 0.025 | 10 | 0.047 | 0.052 |
| fast_125pct | speed | 0.018 | 0.018 | 0 | 0.052 | 0.057 |
| fast_150pct | model_box | 0.017 | 0.068 | 5 | 0.343 | 0.310 |
| fast_150pct | cv_distance | 0.017 | 0.025 | 10 | 0.065 | 0.069 |
| fast_150pct | turn | 0.030 | 0.025 | 10 | 0.047 | 0.052 |
| fast_150pct | speed | 0.018 | 0.021 | 0 | 0.058 | 0.064 |
| jump_200m | model_box | 0.017 | 0.028 | 5 | 0.087 | 0.075 |
| jump_200m | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| jump_200m | turn | 0.030 | 0.026 | 10 | 0.048 | 0.052 |
| jump_200m | speed | 0.018 | 0.014 | 0 | 0.049 | 0.052 |
| jump_500m | model_box | 0.017 | 0.057 | 0 | 0.318 | 0.227 |
| jump_500m | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| jump_500m | turn | 0.030 | 0.028 | 10 | 0.053 | 0.052 |
| jump_500m | speed | 0.018 | 0.016 | 0 | 0.054 | 0.055 |
| jump_1000m | model_box | 0.017 | 0.220 | 0 | 0.532 | 0.446 |
| jump_1000m | cv_distance | 0.017 | 0.015 | 0 | 0.048 | 0.050 |
| jump_1000m | turn | 0.030 | 0.031 | 5 | 0.057 | 0.053 |
| jump_1000m | speed | 0.018 | 0.268 | 0 | 0.692 | 0.584 |

Paired detection gap at 20 min, model minus each rule (percentage points, 95% CI, vessel bootstrap):

| deviation | cv_distance | turn | speed |
|---|---:|---:|---:|
| none | +0.1 (-1.5 to +1.8) | +0.1 (-1.1 to +1.6) | +0.0 (-2.2 to +2.1) |
| turn_15 | +10.1 (+7.7 to +12.8) | +11.9 (+9.8 to +14.1) | +10.1 (+6.8 to +13.4) |
| turn_30 | +21.7 (+18.6 to +25.0) | +23.8 (+21.1 to +26.7) | +21.6 (+17.9 to +25.5) |
| turn_60 | +32.4 (+28.6 to +36.1) | +34.8 (+31.6 to +38.1) | +32.3 (+28.2 to +36.5) |
| turn_90 | +36.2 (+32.3 to +40.1) | +38.1 (+34.6 to +41.5) | +36.0 (+31.6 to +40.3) |
| stop | +35.8 (+32.0 to +39.4) | +38.2 (+35.2 to +41.2) | +32.8 (+28.4 to +37.0) |
| slow_50pct | +27.2 (+24.3 to +30.2) | +26.4 (+23.7 to +29.3) | +25.9 (+22.4 to +29.4) |
| slow_75pct | +11.5 (+9.2 to +13.9) | +10.9 (+8.9 to +13.1) | +10.7 (+7.9 to +13.5) |
| fast_125pct | +10.8 (+8.3 to +13.2) | +11.6 (+9.5 to +13.9) | +11.2 (+8.3 to +14.2) |
| fast_150pct | +27.8 (+24.5 to +31.2) | +29.6 (+26.8 to +32.7) | +28.6 (+24.8 to +32.3) |
| jump_200m | +4.0 (+1.9 to +6.4) | +3.9 (+2.4 to +5.6) | +3.9 (+1.1 to +6.6) |
| jump_500m | +27.1 (+23.8 to +30.4) | +26.6 (+23.9 to +29.3) | +26.5 (+22.6 to +30.1) |
| jump_1000m | +48.4 (+44.2 to +52.5) | +47.6 (+43.9 to +51.1) | -16.0 (-20.1 to -11.5) |
