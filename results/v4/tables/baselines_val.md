| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 6277 (5894–6722) | 6347 | 11098 | 101559 / 655 vessels |
| persistence | fde_m | 10526 (9621–11462) | 10486 | 20712 | 101559 / 655 vessels |
| persistence | err_5min_m | 1330 (1259–1402) | 1372 | 2294 | 101559 / 655 vessels |
| persistence | err_10min_m | 2579 (2440–2719) | 2656 | 4397 | 101559 / 655 vessels |
| persistence | err_20min_m | 4814 (4541–5085) | 4995 | 8105 | 101559 / 655 vessels |
| persistence | err_30min_m | 6666 (6286–7083) | 6972 | 11500 | 101559 / 655 vessels |
| persistence | err_45min_m | 8869 (8280–9529) | 9181 | 16389 | 101559 / 655 vessels |
| persistence | err_60min_m | 10526 (9621–11462) | 10486 | 20712 | 101559 / 655 vessels |
| cv | ade_m | 5339 (4787–5905) | 3559 | 12860 | 101559 / 655 vessels |
| cv | fde_m | 11674 (10417–12913) | 7877 | 28400 | 101559 / 655 vessels |
| cv | err_5min_m | 328 (291–368) | 84 | 957 | 101559 / 655 vessels |
| cv | err_10min_m | 986 (886–1088) | 370 | 2702 | 101559 / 655 vessels |
| cv | err_20min_m | 2819 (2530–3098) | 1669 | 7079 | 101559 / 655 vessels |
| cv | err_30min_m | 5026 (4506–5562) | 3243 | 12598 | 101559 / 655 vessels |
| cv | err_45min_m | 8482 (7578–9387) | 5573 | 20959 | 101559 / 655 vessels |
| cv | err_60min_m | 11674 (10417–12913) | 7877 | 28400 | 101559 / 655 vessels |
| ctrv | ade_m | 5293 (4807–5789) | 3867 | 11971 | 101559 / 655 vessels |
| ctrv | fde_m | 10506 (9565–11453) | 7327 | 25186 | 101559 / 655 vessels |
| ctrv | err_5min_m | 435 (387–485) | 129 | 1261 | 101559 / 655 vessels |
| ctrv | err_10min_m | 1239 (1112–1372) | 558 | 3295 | 101559 / 655 vessels |
| ctrv | err_20min_m | 3229 (2913–3543) | 2075 | 7675 | 101559 / 655 vessels |
| ctrv | err_30min_m | 5341 (4817–5870) | 3808 | 12492 | 101559 / 655 vessels |
| ctrv | err_45min_m | 8163 (7385–8967) | 5620 | 19522 | 101559 / 655 vessels |
| ctrv | err_60min_m | 10506 (9565–11453) | 7327 | 25186 | 101559 / 655 vessels |
| ctrv_damped | ade_m | 5344 (4792–5911) | 3542 | 12887 | 101559 / 655 vessels |
| ctrv_damped | fde_m | 11678 (10420–12918) | 7865 | 28405 | 101559 / 655 vessels |
| ctrv_damped | err_5min_m | 335 (297–376) | 90 | 968 | 101559 / 655 vessels |
| ctrv_damped | err_10min_m | 997 (895–1100) | 383 | 2708 | 101559 / 655 vessels |
| ctrv_damped | err_20min_m | 2827 (2538–3111) | 1669 | 7104 | 101559 / 655 vessels |
| ctrv_damped | err_30min_m | 5029 (4510–5568) | 3233 | 12618 | 101559 / 655 vessels |
| ctrv_damped | err_45min_m | 8485 (7587–9392) | 5532 | 21003 | 101559 / 655 vessels |
| ctrv_damped | err_60min_m | 11678 (10420–12918) | 7865 | 28405 | 101559 / 655 vessels |
| kalman_cv | ade_m | 5338 (4787–5904) | 3559 | 12861 | 101559 / 655 vessels |
| kalman_cv | fde_m | 11670 (10413–12909) | 7879 | 28399 | 101559 / 655 vessels |
| kalman_cv | err_5min_m | 328 (291–368) | 84 | 958 | 101559 / 655 vessels |
| kalman_cv | err_10min_m | 986 (886–1088) | 370 | 2702 | 101559 / 655 vessels |
| kalman_cv | err_20min_m | 2818 (2529–3098) | 1668 | 7081 | 101559 / 655 vessels |
| kalman_cv | err_30min_m | 5025 (4506–5563) | 3244 | 12600 | 101559 / 655 vessels |
| kalman_cv | err_45min_m | 8480 (7577–9385) | 5573 | 20960 | 101559 / 655 vessels |
| kalman_cv | err_60min_m | 11670 (10413–12909) | 7879 | 28399 | 101559 / 655 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +938 (+319 to +1588) | -1147 (-2666 to +448) |
| ctrv | -46 (-259 to +177) | -1168 (-1787 to -546) |
| ctrv_damped | +5 (-1 to +11) | +4 (-4 to +13) |
| kalman_cv | -2 (-5 to +0) | -3 (-11 to +0) |
