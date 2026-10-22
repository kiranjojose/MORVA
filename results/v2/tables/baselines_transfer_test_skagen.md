| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2667 (2521–2829) | 2855 | 4333 | 97396 / 1011 vessels |
| persistence | fde_m | 5012 (4746–5318) | 5376 | 8213 | 97396 / 1011 vessels |
| persistence | err_5min_m | 1294 (1222–1375) | 1383 | 2086 | 97396 / 1011 vessels |
| persistence | err_10min_m | 2559 (2418–2717) | 2742 | 4148 | 97396 / 1011 vessels |
| persistence | err_20min_m | 5012 (4746–5318) | 5376 | 8213 | 97396 / 1011 vessels |
| cv | ade_m | 348 (297–417) | 110 | 920 | 97396 / 1011 vessels |
| cv | fde_m | 846 (720–1009) | 257 | 2380 | 97396 / 1011 vessels |
| cv | err_5min_m | 96 (82–114) | 31 | 212 | 97396 / 1011 vessels |
| cv | err_10min_m | 280 (239–336) | 84 | 710 | 97396 / 1011 vessels |
| cv | err_20min_m | 846 (720–1009) | 257 | 2380 | 97396 / 1011 vessels |
| ctrv | ade_m | 467 (407–547) | 183 | 1218 | 97396 / 1011 vessels |
| ctrv | fde_m | 1136 (1004–1313) | 466 | 3057 | 97396 / 1011 vessels |
| ctrv | err_5min_m | 124 (105–151) | 42 | 277 | 97396 / 1011 vessels |
| ctrv | err_10min_m | 375 (322–447) | 132 | 946 | 97396 / 1011 vessels |
| ctrv | err_20min_m | 1136 (1004–1313) | 466 | 3057 | 97396 / 1011 vessels |
| ctrv_damped | ade_m | 351 (298–420) | 113 | 922 | 97396 / 1011 vessels |
| ctrv_damped | fde_m | 847 (721–1012) | 262 | 2370 | 97396 / 1011 vessels |
| ctrv_damped | err_5min_m | 98 (83–118) | 33 | 217 | 97396 / 1011 vessels |
| ctrv_damped | err_10min_m | 283 (241–340) | 87 | 711 | 97396 / 1011 vessels |
| ctrv_damped | err_20min_m | 847 (721–1012) | 262 | 2370 | 97396 / 1011 vessels |
| kalman_cv | ade_m | 348 (297–416) | 110 | 921 | 97396 / 1011 vessels |
| kalman_cv | fde_m | 845 (720–1009) | 256 | 2380 | 97396 / 1011 vessels |
| kalman_cv | err_5min_m | 96 (82–114) | 31 | 212 | 97396 / 1011 vessels |
| kalman_cv | err_10min_m | 280 (239–336) | 84 | 710 | 97396 / 1011 vessels |
| kalman_cv | err_20min_m | 845 (720–1009) | 256 | 2380 | 97396 / 1011 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2318 (+2170 to +2469) | +4166 (+3875 to +4459) |
| ctrv | +118 (+108 to +130) | +290 (+273 to +308) |
| ctrv_damped | +2 (+1 to +4) | +2 (-1 to +4) |
| kalman_cv | -0 (-0 to -0) | -0 (-0 to -0) |
