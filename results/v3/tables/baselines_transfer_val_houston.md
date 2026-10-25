| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 4421 (4250–4600) | 4487 | 8533 | 54432 / 776 vessels |
| persistence | fde_m | 8017 (7648–8400) | 8159 | 16140 | 54432 / 776 vessels |
| persistence | err_5min_m | 874 (841–911) | 876 | 1612 | 54432 / 776 vessels |
| persistence | err_10min_m | 1684 (1620–1751) | 1701 | 3156 | 54432 / 776 vessels |
| persistence | err_20min_m | 3172 (3054–3291) | 3225 | 6015 | 54432 / 776 vessels |
| persistence | err_30min_m | 4521 (4353–4694) | 4583 | 8728 | 54432 / 776 vessels |
| persistence | err_45min_m | 6348 (6085–6624) | 6480 | 12519 | 54432 / 776 vessels |
| persistence | err_60min_m | 8017 (7648–8400) | 8159 | 16140 | 54432 / 776 vessels |
| cv | ade_m | 2747 (2479–3054) | 1882 | 5945 | 54432 / 776 vessels |
| cv | fde_m | 6086 (5571–6709) | 4208 | 13205 | 54432 / 776 vessels |
| cv | err_5min_m | 188 (165–215) | 78 | 467 | 54432 / 776 vessels |
| cv | err_10min_m | 552 (488–626) | 270 | 1356 | 54432 / 776 vessels |
| cv | err_20min_m | 1509 (1342–1699) | 899 | 3526 | 54432 / 776 vessels |
| cv | err_30min_m | 2574 (2301–2880) | 1672 | 5706 | 54432 / 776 vessels |
| cv | err_45min_m | 4290 (3882–4764) | 2888 | 9380 | 54432 / 776 vessels |
| cv | err_60min_m | 6086 (5571–6709) | 4208 | 13205 | 54432 / 776 vessels |
| ctrv | ade_m | 3093 (2931–3277) | 2284 | 6700 | 54432 / 776 vessels |
| ctrv | fde_m | 6489 (6225–6788) | 4953 | 14016 | 54432 / 776 vessels |
| ctrv | err_5min_m | 227 (197–261) | 98 | 566 | 54432 / 776 vessels |
| ctrv | err_10min_m | 666 (596–745) | 330 | 1722 | 54432 / 776 vessels |
| ctrv | err_20min_m | 1815 (1671–1984) | 1109 | 4408 | 54432 / 776 vessels |
| ctrv | err_30min_m | 3023 (2831–3245) | 2078 | 7013 | 54432 / 776 vessels |
| ctrv | err_45min_m | 4788 (4562–5048) | 3490 | 10583 | 54432 / 776 vessels |
| ctrv | err_60min_m | 6489 (6225–6788) | 4953 | 14016 | 54432 / 776 vessels |
| ctrv_damped | ade_m | 2752 (2484–3059) | 1886 | 5969 | 54432 / 776 vessels |
| ctrv_damped | fde_m | 6099 (5585–6721) | 4217 | 13248 | 54432 / 776 vessels |
| ctrv_damped | err_5min_m | 188 (164–215) | 79 | 465 | 54432 / 776 vessels |
| ctrv_damped | err_10min_m | 551 (487–625) | 268 | 1363 | 54432 / 776 vessels |
| ctrv_damped | err_20min_m | 1511 (1344–1699) | 890 | 3555 | 54432 / 776 vessels |
| ctrv_damped | err_30min_m | 2580 (2307–2884) | 1670 | 5735 | 54432 / 776 vessels |
| ctrv_damped | err_45min_m | 4299 (3891–4773) | 2896 | 9406 | 54432 / 776 vessels |
| ctrv_damped | err_60min_m | 6099 (5585–6721) | 4217 | 13248 | 54432 / 776 vessels |
| kalman_cv | ade_m | 2746 (2478–3053) | 1882 | 5945 | 54432 / 776 vessels |
| kalman_cv | fde_m | 6084 (5570–6707) | 4208 | 13209 | 54432 / 776 vessels |
| kalman_cv | err_5min_m | 188 (165–215) | 78 | 468 | 54432 / 776 vessels |
| kalman_cv | err_10min_m | 552 (488–626) | 270 | 1356 | 54432 / 776 vessels |
| kalman_cv | err_20min_m | 1509 (1342–1698) | 898 | 3526 | 54432 / 776 vessels |
| kalman_cv | err_30min_m | 2573 (2301–2879) | 1671 | 5707 | 54432 / 776 vessels |
| kalman_cv | err_45min_m | 4289 (3881–4762) | 2887 | 9381 | 54432 / 776 vessels |
| kalman_cv | err_60min_m | 6084 (5570–6707) | 4208 | 13209 | 54432 / 776 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +1674 (+1322 to +2015) | +1932 (+1133 to +2654) |
| ctrv | +346 (+175 to +506) | +404 (-77 to +833) |
| ctrv_damped | +5 (+4 to +7) | +13 (+10 to +16) |
| kalman_cv | -1 (-1 to -0) | -2 (-3 to -1) |
