| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2947 (2816–3090) | 3028 | 4548 | 167533 / 1209 vessels |
| persistence | fde_m | 5510 (5262–5778) | 5702 | 8575 | 167533 / 1209 vessels |
| persistence | err_5min_m | 1440 (1376–1509) | 1476 | 2213 | 167533 / 1209 vessels |
| persistence | err_10min_m | 2837 (2710–2973) | 2919 | 4378 | 167533 / 1209 vessels |
| persistence | err_20min_m | 5510 (5262–5778) | 5702 | 8575 | 167533 / 1209 vessels |
| cv | ade_m | 634 (576–691) | 273 | 1699 | 167533 / 1209 vessels |
| cv | fde_m | 1566 (1425–1706) | 754 | 4105 | 167533 / 1209 vessels |
| cv | err_5min_m | 158 (143–173) | 44 | 452 | 167533 / 1209 vessels |
| cv | err_10min_m | 502 (456–548) | 165 | 1443 | 167533 / 1209 vessels |
| cv | err_20min_m | 1566 (1425–1706) | 754 | 4105 | 167533 / 1209 vessels |
| ctrv | ade_m | 843 (778–907) | 428 | 2203 | 167533 / 1209 vessels |
| ctrv | fde_m | 2068 (1927–2210) | 1168 | 5145 | 167533 / 1209 vessels |
| ctrv | err_5min_m | 210 (189–231) | 66 | 568 | 167533 / 1209 vessels |
| ctrv | err_10min_m | 673 (614–731) | 272 | 1851 | 167533 / 1209 vessels |
| ctrv | err_20min_m | 2068 (1927–2210) | 1168 | 5145 | 167533 / 1209 vessels |
| ctrv_damped | ade_m | 637 (578–695) | 280 | 1701 | 167533 / 1209 vessels |
| ctrv_damped | fde_m | 1569 (1425–1709) | 760 | 4109 | 167533 / 1209 vessels |
| ctrv_damped | err_5min_m | 161 (145–176) | 47 | 454 | 167533 / 1209 vessels |
| ctrv_damped | err_10min_m | 505 (458–551) | 172 | 1442 | 167533 / 1209 vessels |
| ctrv_damped | err_20min_m | 1569 (1425–1709) | 760 | 4109 | 167533 / 1209 vessels |
| kalman_cv | ade_m | 634 (576–691) | 273 | 1699 | 167533 / 1209 vessels |
| kalman_cv | fde_m | 1566 (1425–1705) | 754 | 4105 | 167533 / 1209 vessels |
| kalman_cv | err_5min_m | 158 (143–173) | 44 | 452 | 167533 / 1209 vessels |
| kalman_cv | err_10min_m | 502 (456–547) | 164 | 1444 | 167533 / 1209 vessels |
| kalman_cv | err_20min_m | 1566 (1425–1705) | 754 | 4105 | 167533 / 1209 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2314 (+2148 to +2478) | +3944 (+3608 to +4274) |
| ctrv | +209 (+195 to +226) | +502 (+460 to +548) |
| ctrv_damped | +3 (+1 to +5) | +4 (+1 to +7) |
| kalman_cv | -0 (-0 to +0) | -0 (-1 to +0) |
