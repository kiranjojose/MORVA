| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 6524 (6030–7066) | 6811 | 11667 | 59505 / 748 vessels |
| persistence | fde_m | 12410 (11436–13472) | 12680 | 22721 | 59505 / 748 vessels |
| persistence | err_5min_m | 1150 (1063–1246) | 1226 | 1974 | 59505 / 748 vessels |
| persistence | err_10min_m | 2273 (2100–2463) | 2423 | 3932 | 59505 / 748 vessels |
| persistence | err_20min_m | 4443 (4108–4816) | 4724 | 7795 | 59505 / 748 vessels |
| persistence | err_30min_m | 6526 (6044–7068) | 6908 | 11586 | 59505 / 748 vessels |
| persistence | err_45min_m | 9527 (8801–10322) | 9956 | 17193 | 59505 / 748 vessels |
| persistence | err_60min_m | 12410 (11436–13472) | 12680 | 22721 | 59505 / 748 vessels |
| cv | ade_m | 1802 (1562–2127) | 649 | 4880 | 59505 / 748 vessels |
| cv | fde_m | 4481 (3946–5198) | 1715 | 12136 | 59505 / 748 vessels |
| cv | err_5min_m | 90 (76–107) | 27 | 196 | 59505 / 748 vessels |
| cv | err_10min_m | 267 (226–323) | 76 | 661 | 59505 / 748 vessels |
| cv | err_20min_m | 813 (689–983) | 239 | 2249 | 59505 / 748 vessels |
| cv | err_30min_m | 1545 (1321–1854) | 481 | 4319 | 59505 / 748 vessels |
| cv | err_45min_m | 2891 (2508–3413) | 986 | 8012 | 59505 / 748 vessels |
| cv | err_60min_m | 4481 (3946–5198) | 1715 | 12136 | 59505 / 748 vessels |
| ctrv | ade_m | 2316 (2112–2589) | 1264 | 5880 | 59505 / 748 vessels |
| ctrv | fde_m | 5695 (5280–6265) | 3424 | 14086 | 59505 / 748 vessels |
| ctrv | err_5min_m | 116 (96–143) | 36 | 253 | 59505 / 748 vessels |
| ctrv | err_10min_m | 351 (298–424) | 119 | 869 | 59505 / 748 vessels |
| ctrv | err_20min_m | 1063 (930–1237) | 429 | 2799 | 59505 / 748 vessels |
| ctrv | err_30min_m | 2003 (1795–2277) | 924 | 5280 | 59505 / 748 vessels |
| ctrv | err_45min_m | 3712 (3400–4143) | 1998 | 9548 | 59505 / 748 vessels |
| ctrv | err_60min_m | 5695 (5280–6265) | 3424 | 14086 | 59505 / 748 vessels |
| ctrv_damped | ade_m | 1800 (1560–2125) | 657 | 4866 | 59505 / 748 vessels |
| ctrv_damped | fde_m | 4472 (3938–5190) | 1718 | 12091 | 59505 / 748 vessels |
| ctrv_damped | err_5min_m | 92 (77–110) | 28 | 201 | 59505 / 748 vessels |
| ctrv_damped | err_10min_m | 269 (227–326) | 79 | 661 | 59505 / 748 vessels |
| ctrv_damped | err_20min_m | 814 (690–983) | 244 | 2233 | 59505 / 748 vessels |
| ctrv_damped | err_30min_m | 1544 (1319–1851) | 488 | 4303 | 59505 / 748 vessels |
| ctrv_damped | err_45min_m | 2887 (2504–3408) | 999 | 7968 | 59505 / 748 vessels |
| ctrv_damped | err_60min_m | 4472 (3938–5190) | 1718 | 12091 | 59505 / 748 vessels |
| kalman_cv | ade_m | 1802 (1562–2126) | 648 | 4882 | 59505 / 748 vessels |
| kalman_cv | fde_m | 4481 (3946–5198) | 1714 | 12136 | 59505 / 748 vessels |
| kalman_cv | err_5min_m | 90 (76–107) | 27 | 196 | 59505 / 748 vessels |
| kalman_cv | err_10min_m | 267 (226–323) | 76 | 661 | 59505 / 748 vessels |
| kalman_cv | err_20min_m | 813 (689–982) | 238 | 2250 | 59505 / 748 vessels |
| kalman_cv | err_30min_m | 1545 (1320–1854) | 481 | 4317 | 59505 / 748 vessels |
| kalman_cv | err_45min_m | 2891 (2507–3412) | 985 | 8010 | 59505 / 748 vessels |
| kalman_cv | err_60min_m | 4481 (3946–5198) | 1714 | 12136 | 59505 / 748 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +4722 (+4222 to +5260) | +7929 (+6873 to +9015) |
| ctrv | +514 (+425 to +590) | +1214 (+913 to +1474) |
| ctrv_damped | -2 (-4 to -0) | -9 (-13 to -6) |
| kalman_cv | -0 (-1 to -0) | -1 (-1 to -0) |
