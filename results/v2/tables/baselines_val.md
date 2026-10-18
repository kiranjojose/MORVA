| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2906 (2760–3046) | 3008 | 4503 | 120412 / 1048 vessels |
| persistence | fde_m | 5428 (5142–5694) | 5664 | 8493 | 120412 / 1048 vessels |
| persistence | err_5min_m | 1422 (1352–1492) | 1469 | 2198 | 120412 / 1048 vessels |
| persistence | err_10min_m | 2798 (2660–2934) | 2900 | 4334 | 120412 / 1048 vessels |
| persistence | err_20min_m | 5428 (5142–5694) | 5664 | 8493 | 120412 / 1048 vessels |
| cv | ade_m | 633 (577–693) | 268 | 1699 | 120412 / 1048 vessels |
| cv | fde_m | 1563 (1424–1714) | 744 | 4100 | 120412 / 1048 vessels |
| cv | err_5min_m | 157 (143–173) | 42 | 453 | 120412 / 1048 vessels |
| cv | err_10min_m | 503 (457–552) | 160 | 1451 | 120412 / 1048 vessels |
| cv | err_20min_m | 1563 (1424–1714) | 744 | 4100 | 120412 / 1048 vessels |
| ctrv | ade_m | 830 (768–901) | 421 | 2180 | 120412 / 1048 vessels |
| ctrv | fde_m | 2031 (1888–2181) | 1139 | 5086 | 120412 / 1048 vessels |
| ctrv | err_5min_m | 209 (188–232) | 64 | 562 | 120412 / 1048 vessels |
| ctrv | err_10min_m | 665 (608–726) | 265 | 1829 | 120412 / 1048 vessels |
| ctrv | err_20min_m | 2031 (1888–2181) | 1139 | 5086 | 120412 / 1048 vessels |
| ctrv_damped | ade_m | 636 (578–697) | 274 | 1700 | 120412 / 1048 vessels |
| ctrv_damped | fde_m | 1566 (1426–1717) | 752 | 4096 | 120412 / 1048 vessels |
| ctrv_damped | err_5min_m | 160 (145–176) | 45 | 455 | 120412 / 1048 vessels |
| ctrv_damped | err_10min_m | 506 (459–556) | 167 | 1446 | 120412 / 1048 vessels |
| ctrv_damped | err_20min_m | 1566 (1426–1717) | 752 | 4096 | 120412 / 1048 vessels |
| kalman_cv | ade_m | 633 (577–694) | 268 | 1700 | 120412 / 1048 vessels |
| kalman_cv | fde_m | 1563 (1424–1714) | 744 | 4100 | 120412 / 1048 vessels |
| kalman_cv | err_5min_m | 157 (143–173) | 42 | 453 | 120412 / 1048 vessels |
| kalman_cv | err_10min_m | 503 (457–552) | 160 | 1451 | 120412 / 1048 vessels |
| kalman_cv | err_20min_m | 1563 (1424–1714) | 744 | 4100 | 120412 / 1048 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2272 (+2112 to +2432) | +3865 (+3540 to +4196) |
| ctrv | +197 (+183 to +213) | +468 (+427 to +510) |
| ctrv_damped | +3 (+1 to +5) | +3 (+0 to +6) |
| kalman_cv | +0 (-0 to +0) | +0 (-0 to +0) |
