| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 9517 (9198–9804) | 9703 | 13056 | 76694 / 1228 vessels |
| persistence | fde_m | 18577 (17932–19155) | 19018 | 25508 | 76694 / 1228 vessels |
| persistence | err_5min_m | 1591 (1540–1640) | 1605 | 2174 | 76694 / 1228 vessels |
| persistence | err_10min_m | 3171 (3070–3266) | 3204 | 4328 | 76694 / 1228 vessels |
| persistence | err_20min_m | 6301 (6095–6490) | 6389 | 8621 | 76694 / 1228 vessels |
| persistence | err_30min_m | 9398 (9086–9681) | 9563 | 12886 | 76694 / 1228 vessels |
| persistence | err_45min_m | 14003 (13516–14432) | 14306 | 19234 | 76694 / 1228 vessels |
| persistence | err_60min_m | 18577 (17932–19155) | 19018 | 25508 | 76694 / 1228 vessels |
| cv | ade_m | 1220 (1102–1389) | 469 | 3184 | 76694 / 1228 vessels |
| cv | fde_m | 3126 (2829–3540) | 1218 | 8117 | 76694 / 1228 vessels |
| cv | err_5min_m | 64 (56–74) | 26 | 113 | 76694 / 1228 vessels |
| cv | err_10min_m | 181 (158–210) | 65 | 365 | 76694 / 1228 vessels |
| cv | err_20min_m | 535 (472–614) | 183 | 1363 | 76694 / 1228 vessels |
| cv | err_30min_m | 1016 (910–1159) | 350 | 2741 | 76694 / 1228 vessels |
| cv | err_45min_m | 1954 (1769–2215) | 698 | 5271 | 76694 / 1228 vessels |
| cv | err_60min_m | 3126 (2829–3540) | 1218 | 8117 | 76694 / 1228 vessels |
| ctrv | ade_m | 1983 (1879–2128) | 1076 | 4667 | 76694 / 1228 vessels |
| ctrv | fde_m | 5192 (4928–5570) | 3033 | 12299 | 76694 / 1228 vessels |
| ctrv | err_5min_m | 84 (73–98) | 34 | 164 | 76694 / 1228 vessels |
| ctrv | err_10min_m | 253 (228–285) | 103 | 572 | 76694 / 1228 vessels |
| ctrv | err_20min_m | 809 (755–882) | 356 | 1973 | 76694 / 1228 vessels |
| ctrv | err_30min_m | 1617 (1527–1740) | 770 | 3909 | 76694 / 1228 vessels |
| ctrv | err_45min_m | 3216 (3053–3449) | 1720 | 7669 | 76694 / 1228 vessels |
| ctrv | err_60min_m | 5192 (4928–5570) | 3033 | 12299 | 76694 / 1228 vessels |
| ctrv_damped | ade_m | 1221 (1102–1389) | 477 | 3167 | 76694 / 1228 vessels |
| ctrv_damped | fde_m | 3124 (2829–3537) | 1229 | 8088 | 76694 / 1228 vessels |
| ctrv_damped | err_5min_m | 66 (57–76) | 27 | 117 | 76694 / 1228 vessels |
| ctrv_damped | err_10min_m | 183 (159–212) | 67 | 365 | 76694 / 1228 vessels |
| ctrv_damped | err_20min_m | 536 (473–616) | 187 | 1350 | 76694 / 1228 vessels |
| ctrv_damped | err_30min_m | 1017 (911–1160) | 357 | 2720 | 76694 / 1228 vessels |
| ctrv_damped | err_45min_m | 1954 (1769–2212) | 712 | 5251 | 76694 / 1228 vessels |
| ctrv_damped | err_60min_m | 3124 (2829–3537) | 1229 | 8088 | 76694 / 1228 vessels |
| kalman_cv | ade_m | 1219 (1101–1389) | 468 | 3182 | 76694 / 1228 vessels |
| kalman_cv | fde_m | 3125 (2828–3539) | 1216 | 8120 | 76694 / 1228 vessels |
| kalman_cv | err_5min_m | 64 (56–74) | 26 | 113 | 76694 / 1228 vessels |
| kalman_cv | err_10min_m | 181 (158–210) | 65 | 365 | 76694 / 1228 vessels |
| kalman_cv | err_20min_m | 534 (471–614) | 183 | 1363 | 76694 / 1228 vessels |
| kalman_cv | err_30min_m | 1015 (910–1158) | 349 | 2741 | 76694 / 1228 vessels |
| kalman_cv | err_45min_m | 1953 (1768–2214) | 697 | 5271 | 76694 / 1228 vessels |
| kalman_cv | err_60min_m | 3125 (2828–3539) | 1216 | 8120 | 76694 / 1228 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +8297 (+7907 to +8622) | +15451 (+14652 to +16139) |
| ctrv | +762 (+700 to +816) | +2066 (+1896 to +2214) |
| ctrv_damped | +1 (-1 to +2) | -2 (-4 to +1) |
| kalman_cv | -1 (-1 to -0) | -1 (-1 to -1) |
