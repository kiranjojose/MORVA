| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 9796 (9363–10190) | 9912 | 13554 | 25021 / 558 vessels |
| persistence | fde_m | 19121 (18232–19918) | 19457 | 26475 | 25021 / 558 vessels |
| persistence | err_5min_m | 1640 (1572–1702) | 1635 | 2259 | 25021 / 558 vessels |
| persistence | err_10min_m | 3267 (3132–3393) | 3265 | 4499 | 25021 / 558 vessels |
| persistence | err_20min_m | 6489 (6209–6743) | 6522 | 8962 | 25021 / 558 vessels |
| persistence | err_30min_m | 9674 (9249–10063) | 9764 | 13377 | 25021 / 558 vessels |
| persistence | err_45min_m | 14409 (13746–14999) | 14619 | 19968 | 25021 / 558 vessels |
| persistence | err_60min_m | 19121 (18232–19918) | 19457 | 26475 | 25021 / 558 vessels |
| cv | ade_m | 1261 (1138–1430) | 458 | 3374 | 25021 / 558 vessels |
| cv | fde_m | 3283 (2950–3752) | 1218 | 8697 | 25021 / 558 vessels |
| cv | err_5min_m | 60 (54–69) | 23 | 109 | 25021 / 558 vessels |
| cv | err_10min_m | 175 (156–199) | 59 | 377 | 25021 / 558 vessels |
| cv | err_20min_m | 531 (477–601) | 169 | 1422 | 25021 / 558 vessels |
| cv | err_30min_m | 1034 (933–1170) | 331 | 2888 | 25021 / 558 vessels |
| cv | err_45min_m | 2031 (1833–2307) | 677 | 5584 | 25021 / 558 vessels |
| cv | err_60min_m | 3283 (2950–3752) | 1218 | 8697 | 25021 / 558 vessels |
| ctrv | ade_m | 2032 (1894–2207) | 1018 | 5023 | 25021 / 558 vessels |
| ctrv | fde_m | 5338 (4968–5776) | 2913 | 13108 | 25021 / 558 vessels |
| ctrv | err_5min_m | 79 (70–90) | 31 | 163 | 25021 / 558 vessels |
| ctrv | err_10min_m | 247 (224–276) | 92 | 595 | 25021 / 558 vessels |
| ctrv | err_20min_m | 814 (755–892) | 324 | 2094 | 25021 / 558 vessels |
| ctrv | err_30min_m | 1654 (1539–1799) | 716 | 4185 | 25021 / 558 vessels |
| ctrv | err_45min_m | 3309 (3078–3588) | 1621 | 8246 | 25021 / 558 vessels |
| ctrv | err_60min_m | 5338 (4968–5776) | 2913 | 13108 | 25021 / 558 vessels |
| ctrv_damped | ade_m | 1260 (1137–1429) | 465 | 3360 | 25021 / 558 vessels |
| ctrv_damped | fde_m | 3278 (2945–3743) | 1228 | 8659 | 25021 / 558 vessels |
| ctrv_damped | err_5min_m | 62 (55–70) | 24 | 113 | 25021 / 558 vessels |
| ctrv_damped | err_10min_m | 177 (157–201) | 61 | 375 | 25021 / 558 vessels |
| ctrv_damped | err_20min_m | 532 (478–603) | 174 | 1406 | 25021 / 558 vessels |
| ctrv_damped | err_30min_m | 1034 (933–1170) | 337 | 2862 | 25021 / 558 vessels |
| ctrv_damped | err_45min_m | 2028 (1830–2306) | 684 | 5555 | 25021 / 558 vessels |
| ctrv_damped | err_60min_m | 3278 (2945–3743) | 1228 | 8659 | 25021 / 558 vessels |
| kalman_cv | ade_m | 1260 (1137–1430) | 457 | 3375 | 25021 / 558 vessels |
| kalman_cv | fde_m | 3282 (2949–3751) | 1217 | 8699 | 25021 / 558 vessels |
| kalman_cv | err_5min_m | 60 (53–68) | 23 | 109 | 25021 / 558 vessels |
| kalman_cv | err_10min_m | 175 (155–198) | 59 | 375 | 25021 / 558 vessels |
| kalman_cv | err_20min_m | 531 (476–601) | 169 | 1419 | 25021 / 558 vessels |
| kalman_cv | err_30min_m | 1033 (933–1169) | 330 | 2886 | 25021 / 558 vessels |
| kalman_cv | err_45min_m | 2030 (1833–2307) | 677 | 5583 | 25021 / 558 vessels |
| kalman_cv | err_60min_m | 3282 (2949–3751) | 1217 | 8699 | 25021 / 558 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +8535 (+8063 to +8957) | +15838 (+14868 to +16690) |
| ctrv | +772 (+707 to +833) | +2055 (+1884 to +2218) |
| ctrv_damped | -1 (-3 to +2) | -5 (-9 to -1) |
| kalman_cv | -0 (-1 to -0) | -1 (-1 to -0) |
