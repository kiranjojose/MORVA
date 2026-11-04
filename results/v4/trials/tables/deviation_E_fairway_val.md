# Deviation screening (E_fairway; val; alpha 0.05)

316,680 train / 57,134 calibration / 68,952 evaluated windows (734 vessels), anchor speed >= 5.0 kn. Deviations start 10 min into the forecast. First flag = first horizon with p <= 0.05 / 7; per-horizon columns use p <= 0.05.

| deviation | detector | false alarms, first flag | detected, first flag | median delay (min) | detected at 20 min | detected at 60 min |
|---|---|---:|---:|---:|---:|---:|
| turn_30 | model_box | 0.014 | 0.179 | 10 | 0.539 | 0.546 |
| turn_30 | cv_distance | 0.015 | 0.015 | 5 | 0.062 | 0.065 |
| turn_30 | turn | 0.030 | 0.013 | 0 | 0.053 | 0.016 |
| turn_30 | speed | 0.017 | 0.015 | 5 | 0.046 | 0.051 |
| turn_60 | model_box | 0.014 | 0.348 | 10 | 0.668 | 0.688 |
| turn_60 | cv_distance | 0.015 | 0.018 | 10 | 0.083 | 0.132 |
| turn_60 | turn | 0.030 | 0.013 | 0 | 0.063 | 0.010 |
| turn_60 | speed | 0.017 | 0.015 | 5 | 0.046 | 0.051 |
| stop | model_box | 0.014 | 0.369 | 5 | 0.675 | 0.678 |
| stop | cv_distance | 0.015 | 0.011 | 0 | 0.044 | 0.073 |
| stop | turn | 0.030 | 0.009 | 0 | 0.024 | 0.002 |
| stop | speed | 0.017 | 0.034 | 5 | 0.501 | 0.265 |
| slow_50pct | model_box | 0.014 | 0.148 | 5 | 0.581 | 0.555 |
| slow_50pct | cv_distance | 0.015 | 0.012 | 0 | 0.042 | 0.035 |
| slow_50pct | turn | 0.030 | 0.026 | 10 | 0.049 | 0.048 |
| slow_50pct | speed | 0.017 | 0.015 | 0 | 0.058 | 0.053 |
| fast_150pct | model_box | 0.014 | 0.157 | 5 | 0.613 | 0.587 |
| fast_150pct | cv_distance | 0.015 | 0.020 | 5 | 0.073 | 0.079 |
| fast_150pct | turn | 0.030 | 0.027 | 10 | 0.054 | 0.049 |
| fast_150pct | speed | 0.017 | 0.021 | 0 | 0.078 | 0.082 |
| jump_500m | model_box | 0.014 | 0.117 | 0 | 0.559 | 0.469 |
| jump_500m | cv_distance | 0.015 | 0.014 | 5 | 0.051 | 0.050 |
| jump_500m | turn | 0.030 | 0.054 | 0 | 0.173 | 0.049 |
| jump_500m | speed | 0.017 | 0.091 | 0 | 0.488 | 0.402 |
