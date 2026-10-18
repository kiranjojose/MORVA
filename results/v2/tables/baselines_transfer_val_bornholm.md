| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 3373 (3192–3545) | 3401 | 4716 | 41675 / 752 vessels |
| persistence | fde_m | 6398 (6055–6723) | 6470 | 8960 | 41675 / 752 vessels |
| persistence | err_5min_m | 1616 (1529–1699) | 1624 | 2261 | 41675 / 752 vessels |
| persistence | err_10min_m | 3220 (3046–3384) | 3242 | 4500 | 41675 / 752 vessels |
| persistence | err_20min_m | 6398 (6055–6723) | 6470 | 8960 | 41675 / 752 vessels |
| cv | ade_m | 243 (199–297) | 64 | 573 | 41675 / 752 vessels |
| cv | fde_m | 583 (491–695) | 148 | 1538 | 41675 / 752 vessels |
| cv | err_5min_m | 69 (53–92) | 19 | 107 | 41675 / 752 vessels |
| cv | err_10min_m | 197 (158–246) | 49 | 410 | 41675 / 752 vessels |
| cv | err_20min_m | 583 (491–695) | 148 | 1538 | 41675 / 752 vessels |
| ctrv | ade_m | 333 (288–389) | 107 | 818 | 41675 / 752 vessels |
| ctrv | fde_m | 827 (735–945) | 278 | 2112 | 41675 / 752 vessels |
| ctrv | err_5min_m | 88 (69–111) | 25 | 160 | 41675 / 752 vessels |
| ctrv | err_10min_m | 262 (220–314) | 76 | 609 | 41675 / 752 vessels |
| ctrv | err_20min_m | 827 (735–945) | 278 | 2112 | 41675 / 752 vessels |
| ctrv_damped | ade_m | 244 (200–298) | 66 | 566 | 41675 / 752 vessels |
| ctrv_damped | fde_m | 583 (491–696) | 152 | 1520 | 41675 / 752 vessels |
| ctrv_damped | err_5min_m | 71 (54–93) | 20 | 109 | 41675 / 752 vessels |
| ctrv_damped | err_10min_m | 198 (159–248) | 51 | 407 | 41675 / 752 vessels |
| ctrv_damped | err_20min_m | 583 (491–696) | 152 | 1520 | 41675 / 752 vessels |
| kalman_cv | ade_m | 242 (199–296) | 64 | 573 | 41675 / 752 vessels |
| kalman_cv | fde_m | 582 (491–692) | 148 | 1538 | 41675 / 752 vessels |
| kalman_cv | err_5min_m | 69 (53–91) | 19 | 106 | 41675 / 752 vessels |
| kalman_cv | err_10min_m | 196 (158–245) | 49 | 410 | 41675 / 752 vessels |
| kalman_cv | err_20min_m | 582 (491–692) | 148 | 1538 | 41675 / 752 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +3130 (+2937 to +3317) | +5815 (+5446 to +6166) |
| ctrv | +90 (+81 to +101) | +244 (+217 to +274) |
| ctrv_damped | +1 (+0 to +1) | +0 (-0 to +1) |
| kalman_cv | -1 (-1 to -0) | -1 (-3 to -0) |
