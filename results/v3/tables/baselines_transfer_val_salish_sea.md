| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 6503 (6003–7093) | 6091 | 12255 | 34247 / 375 vessels |
| persistence | fde_m | 11308 (10286–12541) | 10624 | 22790 | 34247 / 375 vessels |
| persistence | err_5min_m | 1313 (1225–1411) | 1245 | 2468 | 34247 / 375 vessels |
| persistence | err_10min_m | 2534 (2363–2730) | 2385 | 4776 | 34247 / 375 vessels |
| persistence | err_20min_m | 4791 (4440–5177) | 4515 | 9021 | 34247 / 375 vessels |
| persistence | err_30min_m | 6778 (6251–7370) | 6303 | 12903 | 34247 / 375 vessels |
| persistence | err_45min_m | 9317 (8570–10195) | 8769 | 18140 | 34247 / 375 vessels |
| persistence | err_60min_m | 11308 (10286–12541) | 10624 | 22790 | 34247 / 375 vessels |
| cv | ade_m | 5130 (4401–5869) | 3179 | 12121 | 34247 / 375 vessels |
| cv | fde_m | 11347 (9838–12901) | 7257 | 26974 | 34247 / 375 vessels |
| cv | err_5min_m | 308 (256–363) | 82 | 897 | 34247 / 375 vessels |
| cv | err_10min_m | 951 (799–1101) | 341 | 2671 | 34247 / 375 vessels |
| cv | err_20min_m | 2716 (2303–3116) | 1466 | 6788 | 34247 / 375 vessels |
| cv | err_30min_m | 4783 (4078–5526) | 2948 | 11525 | 34247 / 375 vessels |
| cv | err_45min_m | 8131 (6981–9335) | 5114 | 19241 | 34247 / 375 vessels |
| cv | err_60min_m | 11347 (9838–12901) | 7257 | 26974 | 34247 / 375 vessels |
| ctrv | ade_m | 4917 (4420–5458) | 3424 | 11212 | 34247 / 375 vessels |
| ctrv | fde_m | 9889 (8988–10864) | 6861 | 22863 | 34247 / 375 vessels |
| ctrv | err_5min_m | 408 (333–482) | 113 | 1158 | 34247 / 375 vessels |
| ctrv | err_10min_m | 1176 (986–1369) | 478 | 3252 | 34247 / 375 vessels |
| ctrv | err_20min_m | 3023 (2600–3443) | 1770 | 7410 | 34247 / 375 vessels |
| ctrv | err_30min_m | 4905 (4316–5520) | 3263 | 11712 | 34247 / 375 vessels |
| ctrv | err_45min_m | 7556 (6802–8372) | 5202 | 17482 | 34247 / 375 vessels |
| ctrv | err_60min_m | 9889 (8988–10864) | 6861 | 22863 | 34247 / 375 vessels |
| ctrv_damped | ade_m | 5136 (4403–5882) | 3169 | 12148 | 34247 / 375 vessels |
| ctrv_damped | fde_m | 11336 (9829–12886) | 7235 | 27007 | 34247 / 375 vessels |
| ctrv_damped | err_5min_m | 315 (260–373) | 86 | 903 | 34247 / 375 vessels |
| ctrv_damped | err_10min_m | 962 (805–1117) | 343 | 2677 | 34247 / 375 vessels |
| ctrv_damped | err_20min_m | 2732 (2309–3139) | 1471 | 6819 | 34247 / 375 vessels |
| ctrv_damped | err_30min_m | 4798 (4080–5552) | 2937 | 11557 | 34247 / 375 vessels |
| ctrv_damped | err_45min_m | 8130 (6972–9331) | 5101 | 19285 | 34247 / 375 vessels |
| ctrv_damped | err_60min_m | 11336 (9829–12886) | 7235 | 27007 | 34247 / 375 vessels |
| kalman_cv | ade_m | 5129 (4400–5868) | 3180 | 12124 | 34247 / 375 vessels |
| kalman_cv | fde_m | 11345 (9837–12899) | 7256 | 26978 | 34247 / 375 vessels |
| kalman_cv | err_5min_m | 308 (256–363) | 82 | 897 | 34247 / 375 vessels |
| kalman_cv | err_10min_m | 951 (799–1101) | 340 | 2671 | 34247 / 375 vessels |
| kalman_cv | err_20min_m | 2715 (2303–3115) | 1467 | 6788 | 34247 / 375 vessels |
| kalman_cv | err_30min_m | 4783 (4078–5525) | 2949 | 11526 | 34247 / 375 vessels |
| kalman_cv | err_45min_m | 8130 (6980–9333) | 5113 | 19243 | 34247 / 375 vessels |
| kalman_cv | err_60min_m | 11345 (9837–12899) | 7256 | 26978 | 34247 / 375 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +1373 (+631 to +2285) | -39 (-1788 to +1951) |
| ctrv | -213 (-567 to +168) | -1457 (-2472 to -379) |
| ctrv_damped | +6 (-1 to +14) | -11 (-21 to -0) |
| kalman_cv | -1 (-1 to -0) | -2 (-2 to -1) |
