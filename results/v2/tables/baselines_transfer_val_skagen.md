| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2682 (2535–2822) | 2842 | 4310 | 67809 / 797 vessels |
| persistence | fde_m | 5034 (4763–5300) | 5349 | 8145 | 67809 / 797 vessels |
| persistence | err_5min_m | 1304 (1234–1371) | 1377 | 2078 | 67809 / 797 vessels |
| persistence | err_10min_m | 2576 (2434–2711) | 2730 | 4130 | 67809 / 797 vessels |
| persistence | err_20min_m | 5034 (4763–5300) | 5349 | 8145 | 67809 / 797 vessels |
| cv | ade_m | 361 (304–441) | 111 | 956 | 67809 / 797 vessels |
| cv | fde_m | 877 (740–1070) | 261 | 2451 | 67809 / 797 vessels |
| cv | err_5min_m | 98 (83–120) | 31 | 216 | 67809 / 797 vessels |
| cv | err_10min_m | 290 (244–354) | 84 | 734 | 67809 / 797 vessels |
| cv | err_20min_m | 877 (740–1070) | 261 | 2451 | 67809 / 797 vessels |
| ctrv | ade_m | 478 (411–570) | 184 | 1232 | 67809 / 797 vessels |
| ctrv | fde_m | 1158 (1013–1356) | 467 | 3108 | 67809 / 797 vessels |
| ctrv | err_5min_m | 128 (106–159) | 42 | 285 | 67809 / 797 vessels |
| ctrv | err_10min_m | 385 (326–468) | 132 | 967 | 67809 / 797 vessels |
| ctrv | err_20min_m | 1158 (1013–1356) | 467 | 3108 | 67809 / 797 vessels |
| ctrv_damped | ade_m | 363 (305–444) | 114 | 958 | 67809 / 797 vessels |
| ctrv_damped | fde_m | 878 (740–1072) | 266 | 2443 | 67809 / 797 vessels |
| ctrv_damped | err_5min_m | 100 (84–124) | 32 | 221 | 67809 / 797 vessels |
| ctrv_damped | err_10min_m | 292 (245–359) | 87 | 739 | 67809 / 797 vessels |
| ctrv_damped | err_20min_m | 878 (740–1072) | 266 | 2443 | 67809 / 797 vessels |
| kalman_cv | ade_m | 361 (304–441) | 111 | 956 | 67809 / 797 vessels |
| kalman_cv | fde_m | 876 (739–1069) | 261 | 2451 | 67809 / 797 vessels |
| kalman_cv | err_5min_m | 98 (83–120) | 31 | 215 | 67809 / 797 vessels |
| kalman_cv | err_10min_m | 289 (244–354) | 84 | 734 | 67809 / 797 vessels |
| kalman_cv | err_20min_m | 876 (739–1069) | 261 | 2451 | 67809 / 797 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2321 (+2179 to +2476) | +4158 (+3869 to +4471) |
| ctrv | +117 (+106 to +130) | +282 (+265 to +300) |
| ctrv_damped | +2 (+1 to +4) | +1 (-0 to +3) |
| kalman_cv | -0 (-0 to -0) | -0 (-0 to -0) |
