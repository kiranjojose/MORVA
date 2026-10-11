| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2911 (2768–3069) | 3008 | 4460 | 57068 / 622 vessels |
| persistence | fde_m | 5439 (5167–5743) | 5660 | 8422 | 57068 / 622 vessels |
| persistence | err_5min_m | 1424 (1355–1498) | 1467 | 2172 | 57068 / 622 vessels |
| persistence | err_10min_m | 2803 (2667–2952) | 2899 | 4287 | 57068 / 622 vessels |
| persistence | err_20min_m | 5439 (5167–5743) | 5660 | 8422 | 57068 / 622 vessels |
| cv | ade_m | 627 (565–684) | 267 | 1667 | 57068 / 622 vessels |
| cv | fde_m | 1554 (1400–1694) | 746 | 4045 | 57068 / 622 vessels |
| cv | err_5min_m | 155 (138–169) | 43 | 443 | 57068 / 622 vessels |
| cv | err_10min_m | 496 (446–542) | 161 | 1422 | 57068 / 622 vessels |
| cv | err_20min_m | 1554 (1400–1694) | 746 | 4045 | 57068 / 622 vessels |
| ctrv | ade_m | 824 (754–891) | 421 | 2147 | 57068 / 622 vessels |
| ctrv | fde_m | 2021 (1863–2173) | 1146 | 5019 | 57068 / 622 vessels |
| ctrv | err_5min_m | 206 (183–226) | 64 | 552 | 57068 / 622 vessels |
| ctrv | err_10min_m | 658 (595–717) | 267 | 1800 | 57068 / 622 vessels |
| ctrv | err_20min_m | 2021 (1863–2173) | 1146 | 5019 | 57068 / 622 vessels |
| ctrv_damped | ade_m | 630 (567–687) | 273 | 1664 | 57068 / 622 vessels |
| ctrv_damped | fde_m | 1556 (1403–1696) | 754 | 4044 | 57068 / 622 vessels |
| ctrv_damped | err_5min_m | 157 (140–173) | 46 | 444 | 57068 / 622 vessels |
| ctrv_damped | err_10min_m | 499 (447–547) | 168 | 1417 | 57068 / 622 vessels |
| ctrv_damped | err_20min_m | 1556 (1403–1696) | 754 | 4044 | 57068 / 622 vessels |
| kalman_cv | ade_m | 627 (565–684) | 267 | 1668 | 57068 / 622 vessels |
| kalman_cv | fde_m | 1554 (1400–1694) | 746 | 4046 | 57068 / 622 vessels |
| kalman_cv | err_5min_m | 155 (138–169) | 43 | 443 | 57068 / 622 vessels |
| kalman_cv | err_10min_m | 496 (446–542) | 161 | 1422 | 57068 / 622 vessels |
| kalman_cv | err_20min_m | 1554 (1400–1694) | 746 | 4046 | 57068 / 622 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2284 (+2121 to +2464) | +3885 (+3558 to +4244) |
| ctrv | +197 (+182 to +213) | +467 (+424 to +510) |
| ctrv_damped | +3 (+1 to +5) | +2 (-1 to +5) |
| kalman_cv | +0 (+0 to +0) | +0 (+0 to +0) |
