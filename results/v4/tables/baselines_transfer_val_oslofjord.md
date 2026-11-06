| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 4846 (4128–5746) | 3911 | 10635 | 21329 / 140 vessels |
| persistence | fde_m | 8204 (6848–10120) | 5690 | 20325 | 21329 / 140 vessels |
| persistence | err_5min_m | 1008 (889–1137) | 890 | 2080 | 21329 / 140 vessels |
| persistence | err_10min_m | 1939 (1698–2195) | 1607 | 4088 | 21329 / 140 vessels |
| persistence | err_20min_m | 3641 (3144–4171) | 2875 | 7705 | 21329 / 140 vessels |
| persistence | err_30min_m | 5119 (4375–5935) | 4043 | 10714 | 21329 / 140 vessels |
| persistence | err_45min_m | 6898 (5849–8237) | 5563 | 15613 | 21329 / 140 vessels |
| persistence | err_60min_m | 8204 (6848–10120) | 5690 | 20325 | 21329 / 140 vessels |
| cv | ade_m | 4350 (3523–5200) | 3531 | 9625 | 21329 / 140 vessels |
| cv | fde_m | 9486 (7636–11399) | 7402 | 24539 | 21329 / 140 vessels |
| cv | err_5min_m | 271 (230–306) | 104 | 732 | 21329 / 140 vessels |
| cv | err_10min_m | 804 (685–918) | 455 | 1998 | 21329 / 140 vessels |
| cv | err_20min_m | 2298 (1900–2699) | 1857 | 5331 | 21329 / 140 vessels |
| cv | err_30min_m | 4099 (3328–4901) | 3219 | 9091 | 21329 / 140 vessels |
| cv | err_45min_m | 6905 (5501–8346) | 5584 | 15880 | 21329 / 140 vessels |
| cv | err_60min_m | 9486 (7636–11399) | 7402 | 24539 | 21329 / 140 vessels |
| ctrv | ade_m | 3861 (3135–4607) | 2445 | 8987 | 21329 / 140 vessels |
| ctrv | fde_m | 7419 (6069–8771) | 4251 | 19980 | 21329 / 140 vessels |
| ctrv | err_5min_m | 350 (299–398) | 155 | 869 | 21329 / 140 vessels |
| ctrv | err_10min_m | 942 (798–1084) | 560 | 2239 | 21329 / 140 vessels |
| ctrv | err_20min_m | 2435 (1980–2906) | 1813 | 5792 | 21329 / 140 vessels |
| ctrv | err_30min_m | 3932 (3139–4757) | 2617 | 9375 | 21329 / 140 vessels |
| ctrv | err_45min_m | 5941 (4724–7173) | 3438 | 14668 | 21329 / 140 vessels |
| ctrv | err_60min_m | 7419 (6069–8771) | 4251 | 19980 | 21329 / 140 vessels |
| ctrv_damped | ade_m | 4351 (3523–5202) | 3524 | 9726 | 21329 / 140 vessels |
| ctrv_damped | fde_m | 9478 (7636–11387) | 7408 | 24547 | 21329 / 140 vessels |
| ctrv_damped | err_5min_m | 277 (235–312) | 105 | 744 | 21329 / 140 vessels |
| ctrv_damped | err_10min_m | 809 (689–923) | 453 | 2006 | 21329 / 140 vessels |
| ctrv_damped | err_20min_m | 2300 (1904–2700) | 1813 | 5330 | 21329 / 140 vessels |
| ctrv_damped | err_30min_m | 4104 (3330–4914) | 3204 | 9158 | 21329 / 140 vessels |
| ctrv_damped | err_45min_m | 6907 (5493–8360) | 5572 | 15936 | 21329 / 140 vessels |
| ctrv_damped | err_60min_m | 9478 (7636–11387) | 7408 | 24547 | 21329 / 140 vessels |
| kalman_cv | ade_m | 4349 (3522–5200) | 3532 | 9626 | 21329 / 140 vessels |
| kalman_cv | fde_m | 9485 (7635–11399) | 7402 | 24536 | 21329 / 140 vessels |
| kalman_cv | err_5min_m | 271 (230–306) | 104 | 732 | 21329 / 140 vessels |
| kalman_cv | err_10min_m | 804 (685–918) | 455 | 1999 | 21329 / 140 vessels |
| kalman_cv | err_20min_m | 2298 (1900–2700) | 1857 | 5329 | 21329 / 140 vessels |
| kalman_cv | err_30min_m | 4099 (3327–4901) | 3218 | 9091 | 21329 / 140 vessels |
| kalman_cv | err_45min_m | 6904 (5501–8347) | 5586 | 15885 | 21329 / 140 vessels |
| kalman_cv | err_60min_m | 9485 (7635–11399) | 7402 | 24536 | 21329 / 140 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +496 (-447 to +1657) | -1282 (-3579 to +1329) |
| ctrv | -489 (-796 to -94) | -2067 (-3053 to -878) |
| ctrv_damped | +2 (-7 to +11) | -8 (-15 to -1) |
| kalman_cv | -0 (-2 to +0) | -1 (-4 to +1) |
