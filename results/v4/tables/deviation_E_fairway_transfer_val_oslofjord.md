# Deviation screening (E_fairway; transfer_val_oslofjord; alpha 0.05)

376,524 train / 12,609 calibration / 12,999 evaluated windows (135 vessels), anchor speed >= 5.0 kn. Deviations start 10 min into the forecast. First flag = first horizon with p <= 0.05 / 7; per-horizon columns use p <= 0.05.

| deviation | detector | false alarms, first flag | detected, first flag | median delay (min) | detected at 20 min | detected at 60 min |
|---|---|---:|---:|---:|---:|---:|
| none | model_box | 0.020 | 0.015 | 0 | 0.053 | 0.049 |
| none | cv_distance | 0.015 | 0.013 | 0 | 0.055 | 0.053 |
| none | turn | 0.028 | 0.023 | 10 | 0.051 | 0.048 |
| none | speed | 0.014 | 0.010 | 0 | 0.053 | 0.058 |
| turn_15 | model_box | 0.020 | 0.017 | 5 | 0.053 | 0.055 |
| turn_15 | cv_distance | 0.015 | 0.013 | 0 | 0.055 | 0.049 |
| turn_15 | turn | 0.028 | 0.014 | 5 | 0.040 | 0.020 |
| turn_15 | speed | 0.014 | 0.010 | 0 | 0.053 | 0.058 |
| turn_30 | model_box | 0.020 | 0.020 | 5 | 0.088 | 0.067 |
| turn_30 | cv_distance | 0.015 | 0.013 | 0 | 0.060 | 0.043 |
| turn_30 | turn | 0.028 | 0.013 | 5 | 0.031 | 0.015 |
| turn_30 | speed | 0.014 | 0.010 | 0 | 0.053 | 0.058 |
| turn_60 | model_box | 0.020 | 0.025 | 5 | 0.139 | 0.119 |
| turn_60 | cv_distance | 0.015 | 0.015 | 0 | 0.069 | 0.052 |
| turn_60 | turn | 0.028 | 0.013 | 0 | 0.035 | 0.016 |
| turn_60 | speed | 0.014 | 0.010 | 0 | 0.053 | 0.058 |
| turn_90 | model_box | 0.020 | 0.028 | 10 | 0.157 | 0.141 |
| turn_90 | cv_distance | 0.015 | 0.025 | 35 | 0.079 | 0.102 |
| turn_90 | turn | 0.028 | 0.012 | 0 | 0.034 | 0.012 |
| turn_90 | speed | 0.014 | 0.010 | 0 | 0.053 | 0.058 |
| stop | model_box | 0.020 | 0.022 | 5 | 0.162 | 0.109 |
| stop | cv_distance | 0.015 | 0.010 | 0 | 0.040 | 0.024 |
| stop | turn | 0.028 | 0.009 | 0 | 0.021 | 0.001 |
| stop | speed | 0.014 | 0.011 | 0 | 0.202 | 0.157 |
| slow_50pct | model_box | 0.020 | 0.020 | 5 | 0.109 | 0.071 |
| slow_50pct | cv_distance | 0.015 | 0.011 | 0 | 0.042 | 0.020 |
| slow_50pct | turn | 0.028 | 0.022 | 10 | 0.048 | 0.046 |
| slow_50pct | speed | 0.014 | 0.010 | 0 | 0.055 | 0.056 |
| slow_75pct | model_box | 0.020 | 0.017 | 0 | 0.063 | 0.054 |
| slow_75pct | cv_distance | 0.015 | 0.012 | 0 | 0.047 | 0.024 |
| slow_75pct | turn | 0.028 | 0.022 | 10 | 0.050 | 0.047 |
| slow_75pct | speed | 0.014 | 0.010 | 0 | 0.053 | 0.053 |
| fast_125pct | model_box | 0.020 | 0.018 | 5 | 0.076 | 0.065 |
| fast_125pct | cv_distance | 0.015 | 0.015 | 0 | 0.065 | 0.094 |
| fast_125pct | turn | 0.028 | 0.023 | 10 | 0.051 | 0.048 |
| fast_125pct | speed | 0.014 | 0.014 | 0 | 0.056 | 0.064 |
| fast_150pct | model_box | 0.020 | 0.025 | 5 | 0.130 | 0.091 |
| fast_150pct | cv_distance | 0.015 | 0.018 | 5 | 0.080 | 0.124 |
| fast_150pct | turn | 0.028 | 0.023 | 10 | 0.051 | 0.048 |
| fast_150pct | speed | 0.014 | 0.020 | 5 | 0.067 | 0.083 |
| jump_200m | model_box | 0.020 | 0.016 | 0 | 0.058 | 0.052 |
| jump_200m | cv_distance | 0.015 | 0.013 | 0 | 0.055 | 0.053 |
| jump_200m | turn | 0.028 | 0.024 | 5 | 0.054 | 0.048 |
| jump_200m | speed | 0.014 | 0.011 | 0 | 0.055 | 0.059 |
| jump_500m | model_box | 0.020 | 0.022 | 0 | 0.097 | 0.064 |
| jump_500m | cv_distance | 0.015 | 0.013 | 0 | 0.058 | 0.054 |
| jump_500m | turn | 0.028 | 0.025 | 5 | 0.059 | 0.048 |
| jump_500m | speed | 0.014 | 0.016 | 0 | 0.296 | 0.274 |
| jump_1000m | model_box | 0.020 | 0.035 | 0 | 0.247 | 0.147 |
| jump_1000m | cv_distance | 0.015 | 0.014 | 0 | 0.064 | 0.055 |
| jump_1000m | turn | 0.028 | 0.027 | 5 | 0.065 | 0.048 |
| jump_1000m | speed | 0.014 | 0.688 | 0 | 0.890 | 0.886 |
