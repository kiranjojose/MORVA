| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 7769 (7330–8225) | 8249 | 12327 | 80145 / 742 vessels |
| persistence | fde_m | 14447 (13489–15440) | 15679 | 23861 | 80145 / 742 vessels |
| persistence | err_5min_m | 1418 (1350–1486) | 1463 | 2173 | 80145 / 742 vessels |
| persistence | err_10min_m | 2790 (2656–2926) | 2891 | 4288 | 80145 / 742 vessels |
| persistence | err_20min_m | 5410 (5149–5682) | 5640 | 8385 | 80145 / 742 vessels |
| persistence | err_30min_m | 7867 (7465–8290) | 8286 | 12351 | 80145 / 742 vessels |
| persistence | err_45min_m | 11280 (10617–11972) | 12132 | 18150 | 80145 / 742 vessels |
| persistence | err_60min_m | 14447 (13489–15440) | 15679 | 23861 | 80145 / 742 vessels |
| cv | ade_m | 3362 (3068–3660) | 2235 | 7903 | 80145 / 742 vessels |
| cv | fde_m | 7983 (7284–8720) | 5550 | 18257 | 80145 / 742 vessels |
| cv | err_5min_m | 158 (144–172) | 44 | 460 | 80145 / 742 vessels |
| cv | err_10min_m | 506 (461–553) | 168 | 1462 | 80145 / 742 vessels |
| cv | err_20min_m | 1589 (1447–1733) | 785 | 4138 | 80145 / 742 vessels |
| cv | err_30min_m | 2999 (2729–3266) | 1835 | 7301 | 80145 / 742 vessels |
| cv | err_45min_m | 5405 (4924–5890) | 3561 | 12917 | 80145 / 742 vessels |
| cv | err_60min_m | 7983 (7284–8720) | 5550 | 18257 | 80145 / 742 vessels |
| ctrv | ade_m | 4165 (3925–4424) | 2963 | 9438 | 80145 / 742 vessels |
| ctrv | fde_m | 9552 (8978–10184) | 7041 | 21384 | 80145 / 742 vessels |
| ctrv | err_5min_m | 211 (191–233) | 67 | 580 | 80145 / 742 vessels |
| ctrv | err_10min_m | 677 (619–735) | 280 | 1871 | 80145 / 742 vessels |
| ctrv | err_20min_m | 2080 (1927–2229) | 1209 | 5147 | 80145 / 742 vessels |
| ctrv | err_30min_m | 3828 (3584–4065) | 2548 | 9106 | 80145 / 742 vessels |
| ctrv | err_45min_m | 6647 (6258–7055) | 4686 | 15387 | 80145 / 742 vessels |
| ctrv | err_60min_m | 9552 (8978–10184) | 7041 | 21384 | 80145 / 742 vessels |
| ctrv_damped | ade_m | 3364 (3072–3664) | 2238 | 7911 | 80145 / 742 vessels |
| ctrv_damped | fde_m | 7984 (7289–8720) | 5547 | 18256 | 80145 / 742 vessels |
| ctrv_damped | err_5min_m | 161 (146–176) | 48 | 462 | 80145 / 742 vessels |
| ctrv_damped | err_10min_m | 510 (463–557) | 177 | 1463 | 80145 / 742 vessels |
| ctrv_damped | err_20min_m | 1592 (1449–1738) | 794 | 4132 | 80145 / 742 vessels |
| ctrv_damped | err_30min_m | 3002 (2732–3269) | 1842 | 7292 | 80145 / 742 vessels |
| ctrv_damped | err_45min_m | 5406 (4928–5891) | 3562 | 12922 | 80145 / 742 vessels |
| ctrv_damped | err_60min_m | 7984 (7289–8720) | 5547 | 18256 | 80145 / 742 vessels |
| kalman_cv | ade_m | 3362 (3068–3660) | 2235 | 7903 | 80145 / 742 vessels |
| kalman_cv | fde_m | 7983 (7284–8720) | 5549 | 18257 | 80145 / 742 vessels |
| kalman_cv | err_5min_m | 158 (144–172) | 44 | 460 | 80145 / 742 vessels |
| kalman_cv | err_10min_m | 507 (461–553) | 168 | 1463 | 80145 / 742 vessels |
| kalman_cv | err_20min_m | 1589 (1447–1733) | 784 | 4139 | 80145 / 742 vessels |
| kalman_cv | err_30min_m | 2999 (2729–3266) | 1835 | 7303 | 80145 / 742 vessels |
| kalman_cv | err_45min_m | 5405 (4924–5890) | 3562 | 12923 | 80145 / 742 vessels |
| kalman_cv | err_60min_m | 7983 (7284–8720) | 5549 | 18257 | 80145 / 742 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +4407 (+3840 to +4973) | +6465 (+5214 to +7728) |
| ctrv | +803 (+648 to +955) | +1569 (+1126 to +2002) |
| ctrv_damped | +2 (-1 to +5) | +1 (-5 to +7) |
| kalman_cv | +0 (-0 to +0) | +0 (-0 to +0) |
