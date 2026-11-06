# Deviation screening (H_wind_current; val; alpha 0.05)

376,524 train / 68,219 calibration / 78,568 evaluated windows (638 vessels), anchor speed >= 5.0 kn. Deviations start 10 min into the forecast. First flag = first horizon with p <= 0.05 / 7; per-horizon columns use p <= 0.05.

| deviation | detector | false alarms, first flag | detected, first flag | median delay (min) | detected at 20 min | detected at 60 min |
|---|---|---:|---:|---:|---:|---:|
| none | model_box | 0.020 | 0.016 | 5 | 0.048 | 0.049 |
| none | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| none | turn | 0.030 | 0.025 | 10 | 0.046 | 0.052 |
| none | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_15 | model_box | 0.020 | 0.052 | 10 | 0.146 | 0.156 |
| turn_15 | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| turn_15 | turn | 0.030 | 0.012 | 5 | 0.030 | 0.016 |
| turn_15 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_30 | model_box | 0.020 | 0.086 | 10 | 0.258 | 0.250 |
| turn_30 | cv_distance | 0.017 | 0.015 | 0 | 0.046 | 0.049 |
| turn_30 | turn | 0.030 | 0.010 | 0 | 0.026 | 0.013 |
| turn_30 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_60 | model_box | 0.020 | 0.138 | 10 | 0.365 | 0.354 |
| turn_60 | cv_distance | 0.017 | 0.017 | 5 | 0.047 | 0.047 |
| turn_60 | turn | 0.030 | 0.009 | 0 | 0.023 | 0.007 |
| turn_60 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| turn_90 | model_box | 0.020 | 0.164 | 10 | 0.402 | 0.398 |
| turn_90 | cv_distance | 0.017 | 0.019 | 10 | 0.045 | 0.048 |
| turn_90 | turn | 0.030 | 0.010 | 0 | 0.027 | 0.009 |
| turn_90 | speed | 0.018 | 0.015 | 0 | 0.048 | 0.051 |
| stop | model_box | 0.020 | 0.135 | 10 | 0.393 | 0.376 |
| stop | cv_distance | 0.017 | 0.007 | 0 | 0.039 | 0.038 |
| stop | turn | 0.030 | 0.007 | 0 | 0.015 | 0.001 |
| stop | speed | 0.018 | 0.019 | 5 | 0.069 | 0.054 |
| slow_50pct | model_box | 0.020 | 0.065 | 5 | 0.306 | 0.273 |
| slow_50pct | cv_distance | 0.017 | 0.009 | 0 | 0.037 | 0.032 |
| slow_50pct | turn | 0.030 | 0.025 | 10 | 0.045 | 0.052 |
| slow_50pct | speed | 0.018 | 0.015 | 0 | 0.050 | 0.050 |
| slow_75pct | model_box | 0.020 | 0.035 | 10 | 0.149 | 0.128 |
| slow_75pct | cv_distance | 0.017 | 0.012 | 0 | 0.040 | 0.042 |
| slow_75pct | turn | 0.030 | 0.025 | 10 | 0.046 | 0.052 |
| slow_75pct | speed | 0.018 | 0.015 | 0 | 0.048 | 0.049 |
| fast_125pct | model_box | 0.020 | 0.034 | 10 | 0.161 | 0.131 |
| fast_125pct | cv_distance | 0.017 | 0.018 | 5 | 0.055 | 0.057 |
| fast_125pct | turn | 0.030 | 0.025 | 10 | 0.047 | 0.052 |
| fast_125pct | speed | 0.018 | 0.018 | 0 | 0.052 | 0.057 |
| fast_150pct | model_box | 0.020 | 0.065 | 5 | 0.340 | 0.291 |
| fast_150pct | cv_distance | 0.017 | 0.025 | 10 | 0.065 | 0.069 |
| fast_150pct | turn | 0.030 | 0.025 | 10 | 0.047 | 0.052 |
| fast_150pct | speed | 0.018 | 0.021 | 0 | 0.058 | 0.064 |
| jump_200m | model_box | 0.020 | 0.028 | 0 | 0.087 | 0.071 |
| jump_200m | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| jump_200m | turn | 0.030 | 0.026 | 10 | 0.048 | 0.052 |
| jump_200m | speed | 0.018 | 0.014 | 0 | 0.049 | 0.052 |
| jump_500m | model_box | 0.020 | 0.064 | 0 | 0.313 | 0.204 |
| jump_500m | cv_distance | 0.017 | 0.015 | 0 | 0.047 | 0.050 |
| jump_500m | turn | 0.030 | 0.028 | 10 | 0.053 | 0.052 |
| jump_500m | speed | 0.018 | 0.016 | 0 | 0.054 | 0.055 |
| jump_1000m | model_box | 0.020 | 0.247 | 0 | 0.527 | 0.426 |
| jump_1000m | cv_distance | 0.017 | 0.015 | 0 | 0.048 | 0.050 |
| jump_1000m | turn | 0.030 | 0.031 | 5 | 0.057 | 0.053 |
| jump_1000m | speed | 0.018 | 0.268 | 0 | 0.692 | 0.584 |
