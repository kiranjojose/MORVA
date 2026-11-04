# Deviation screening (E_fairway; transfer_val_salish_sea; alpha 0.05)

316,680 train / 26,704 calibration / 24,689 evaluated windows (364 vessels), anchor speed >= 5.0 kn. Deviations start 10 min into the forecast. First flag = first horizon with p <= 0.05 / 7; per-horizon columns use p <= 0.05.

| deviation | detector | false alarms, first flag | detected, first flag | median delay (min) | detected at 20 min | detected at 60 min |
|---|---|---:|---:|---:|---:|---:|
| turn_30 | model_box | 0.015 | 0.073 | 10 | 0.269 | 0.262 |
| turn_30 | cv_distance | 0.022 | 0.019 | 5 | 0.066 | 0.061 |
| turn_30 | turn | 0.036 | 0.016 | 0 | 0.043 | 0.021 |
| turn_30 | speed | 0.024 | 0.020 | 5 | 0.060 | 0.062 |
| turn_60 | model_box | 0.015 | 0.152 | 10 | 0.358 | 0.365 |
| turn_60 | cv_distance | 0.022 | 0.016 | 0 | 0.071 | 0.065 |
| turn_60 | turn | 0.036 | 0.016 | 0 | 0.042 | 0.015 |
| turn_60 | speed | 0.024 | 0.020 | 5 | 0.060 | 0.062 |
| stop | model_box | 0.015 | 0.149 | 10 | 0.363 | 0.356 |
| stop | cv_distance | 0.022 | 0.009 | 0 | 0.062 | 0.051 |
| stop | turn | 0.036 | 0.011 | 0 | 0.024 | 0.002 |
| stop | speed | 0.024 | 0.026 | 5 | 0.117 | 0.085 |
| slow_50pct | model_box | 0.015 | 0.040 | 5 | 0.271 | 0.245 |
| slow_50pct | cv_distance | 0.022 | 0.011 | 0 | 0.057 | 0.046 |
| slow_50pct | turn | 0.036 | 0.030 | 10 | 0.057 | 0.055 |
| slow_50pct | speed | 0.024 | 0.020 | 5 | 0.066 | 0.059 |
| fast_150pct | model_box | 0.015 | 0.052 | 5 | 0.326 | 0.312 |
| fast_150pct | cv_distance | 0.022 | 0.030 | 10 | 0.077 | 0.082 |
| fast_150pct | turn | 0.036 | 0.031 | 10 | 0.062 | 0.058 |
| fast_150pct | speed | 0.024 | 0.026 | 5 | 0.077 | 0.088 |
| jump_500m | model_box | 0.015 | 0.057 | 0 | 0.286 | 0.244 |
| jump_500m | cv_distance | 0.022 | 0.021 | 5 | 0.062 | 0.060 |
| jump_500m | turn | 0.036 | 0.042 | 5 | 0.092 | 0.058 |
| jump_500m | speed | 0.024 | 0.020 | 5 | 0.082 | 0.071 |
