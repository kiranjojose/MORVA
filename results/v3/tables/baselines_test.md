| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 7863 (7474–8267) | 8389 | 12282 | 230570 / 1466 vessels |
| persistence | fde_m | 14647 (13761–15555) | 15987 | 23801 | 230570 / 1466 vessels |
| persistence | err_5min_m | 1431 (1379–1488) | 1489 | 2161 | 230570 / 1466 vessels |
| persistence | err_10min_m | 2816 (2709–2931) | 2943 | 4265 | 230570 / 1466 vessels |
| persistence | err_20min_m | 5465 (5243–5698) | 5741 | 8342 | 230570 / 1466 vessels |
| persistence | err_30min_m | 7954 (7598–8314) | 8446 | 12296 | 230570 / 1466 vessels |
| persistence | err_45min_m | 11425 (10824–12045) | 12330 | 18079 | 230570 / 1466 vessels |
| persistence | err_60min_m | 14647 (13761–15555) | 15987 | 23801 | 230570 / 1466 vessels |
| cv | ade_m | 3392 (3110–3664) | 2241 | 8005 | 230570 / 1466 vessels |
| cv | fde_m | 8059 (7400–8683) | 5632 | 18422 | 230570 / 1466 vessels |
| cv | err_5min_m | 161 (146–176) | 44 | 471 | 230570 / 1466 vessels |
| cv | err_10min_m | 515 (464–559) | 166 | 1496 | 230570 / 1466 vessels |
| cv | err_20min_m | 1605 (1456–1742) | 781 | 4224 | 230570 / 1466 vessels |
| cv | err_30min_m | 3025 (2745–3288) | 1839 | 7447 | 230570 / 1466 vessels |
| cv | err_45min_m | 5449 (4995–5895) | 3592 | 13061 | 230570 / 1466 vessels |
| cv | err_60min_m | 8059 (7400–8683) | 5632 | 18422 | 230570 / 1466 vessels |
| ctrv | ade_m | 4206 (3984–4417) | 2990 | 9571 | 230570 / 1466 vessels |
| ctrv | fde_m | 9649 (9106–10170) | 7127 | 21675 | 230570 / 1466 vessels |
| ctrv | err_5min_m | 214 (193–235) | 66 | 589 | 230570 / 1466 vessels |
| ctrv | err_10min_m | 684 (623–741) | 276 | 1901 | 230570 / 1466 vessels |
| ctrv | err_20min_m | 2097 (1946–2233) | 1209 | 5242 | 230570 / 1466 vessels |
| ctrv | err_30min_m | 3865 (3638–4070) | 2570 | 9239 | 230570 / 1466 vessels |
| ctrv | err_45min_m | 6716 (6358–7061) | 4727 | 15601 | 230570 / 1466 vessels |
| ctrv | err_60min_m | 9649 (9106–10170) | 7127 | 21675 | 230570 / 1466 vessels |
| ctrv_damped | ade_m | 3395 (3114–3665) | 2241 | 8006 | 230570 / 1466 vessels |
| ctrv_damped | fde_m | 8061 (7401–8682) | 5630 | 18416 | 230570 / 1466 vessels |
| ctrv_damped | err_5min_m | 164 (148–179) | 47 | 474 | 230570 / 1466 vessels |
| ctrv_damped | err_10min_m | 517 (467–564) | 173 | 1491 | 230570 / 1466 vessels |
| ctrv_damped | err_20min_m | 1607 (1457–1745) | 788 | 4223 | 230570 / 1466 vessels |
| ctrv_damped | err_30min_m | 3028 (2749–3290) | 1844 | 7439 | 230570 / 1466 vessels |
| ctrv_damped | err_45min_m | 5451 (4996–5896) | 3584 | 13052 | 230570 / 1466 vessels |
| ctrv_damped | err_60min_m | 8061 (7401–8682) | 5630 | 18416 | 230570 / 1466 vessels |
| kalman_cv | ade_m | 3392 (3110–3664) | 2242 | 8006 | 230570 / 1466 vessels |
| kalman_cv | fde_m | 8059 (7400–8683) | 5632 | 18423 | 230570 / 1466 vessels |
| kalman_cv | err_5min_m | 161 (146–176) | 44 | 471 | 230570 / 1466 vessels |
| kalman_cv | err_10min_m | 515 (464–560) | 166 | 1497 | 230570 / 1466 vessels |
| kalman_cv | err_20min_m | 1605 (1456–1742) | 781 | 4225 | 230570 / 1466 vessels |
| kalman_cv | err_30min_m | 3025 (2745–3288) | 1839 | 7447 | 230570 / 1466 vessels |
| kalman_cv | err_45min_m | 5449 (4996–5895) | 3592 | 13060 | 230570 / 1466 vessels |
| kalman_cv | err_60min_m | 8059 (7400–8683) | 5632 | 18423 | 230570 / 1466 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +4471 (+3888 to +5111) | +6588 (+5309 to +8026) |
| ctrv | +814 (+660 to +963) | +1590 (+1142 to +2058) |
| ctrv_damped | +2 (-0 to +5) | +2 (-3 to +7) |
| kalman_cv | +0 (-0 to +0) | +0 (-0 to +0) |
