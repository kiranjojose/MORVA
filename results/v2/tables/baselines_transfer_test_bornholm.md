| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 3472 (3329–3617) | 3434 | 4817 | 55561 / 904 vessels |
| persistence | fde_m | 6587 (6318–6858) | 6533 | 9135 | 55561 / 904 vessels |
| persistence | err_5min_m | 1663 (1596–1734) | 1640 | 2310 | 55561 / 904 vessels |
| persistence | err_10min_m | 3315 (3180–3454) | 3275 | 4600 | 55561 / 904 vessels |
| persistence | err_20min_m | 6587 (6318–6858) | 6533 | 9135 | 55561 / 904 vessels |
| cv | ade_m | 233 (203–271) | 74 | 568 | 55561 / 904 vessels |
| cv | fde_m | 569 (498–661) | 170 | 1552 | 55561 / 904 vessels |
| cv | err_5min_m | 63 (55–74) | 23 | 111 | 55561 / 904 vessels |
| cv | err_10min_m | 186 (160–217) | 58 | 401 | 55561 / 904 vessels |
| cv | err_20min_m | 569 (498–661) | 170 | 1552 | 55561 / 904 vessels |
| ctrv | ade_m | 337 (301–386) | 126 | 831 | 55561 / 904 vessels |
| ctrv | fde_m | 852 (771–970) | 322 | 2180 | 55561 / 904 vessels |
| ctrv | err_5min_m | 84 (72–98) | 30 | 167 | 55561 / 904 vessels |
| ctrv | err_10min_m | 261 (229–302) | 90 | 619 | 55561 / 904 vessels |
| ctrv | err_20min_m | 852 (771–970) | 322 | 2180 | 55561 / 904 vessels |
| ctrv_damped | ade_m | 234 (204–272) | 76 | 562 | 55561 / 904 vessels |
| ctrv_damped | fde_m | 570 (500–662) | 175 | 1535 | 55561 / 904 vessels |
| ctrv_damped | err_5min_m | 65 (56–76) | 24 | 115 | 55561 / 904 vessels |
| ctrv_damped | err_10min_m | 188 (162–220) | 60 | 400 | 55561 / 904 vessels |
| ctrv_damped | err_20min_m | 570 (500–662) | 175 | 1535 | 55561 / 904 vessels |
| kalman_cv | ade_m | 232 (203–271) | 74 | 567 | 55561 / 904 vessels |
| kalman_cv | fde_m | 569 (498–661) | 170 | 1552 | 55561 / 904 vessels |
| kalman_cv | err_5min_m | 63 (54–74) | 23 | 111 | 55561 / 904 vessels |
| kalman_cv | err_10min_m | 185 (160–217) | 58 | 400 | 55561 / 904 vessels |
| kalman_cv | err_20min_m | 569 (498–661) | 170 | 1552 | 55561 / 904 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +3240 (+3087 to +3378) | +6018 (+5725 to +6284) |
| ctrv | +104 (+92 to +119) | +283 (+252 to +320) |
| ctrv_damped | +2 (+1 to +2) | +1 (+0 to +2) |
| kalman_cv | -0 (-0 to -0) | -0 (-0 to -0) |
