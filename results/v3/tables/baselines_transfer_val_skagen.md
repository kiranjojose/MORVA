| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 7390 (6953–7859) | 7991 | 11940 | 44871 / 659 vessels |
| persistence | fde_m | 14078 (13203–15017) | 15249 | 23294 | 44871 / 659 vessels |
| persistence | err_5min_m | 1297 (1225–1372) | 1401 | 2031 | 44871 / 659 vessels |
| persistence | err_10min_m | 2564 (2427–2714) | 2782 | 4035 | 44871 / 659 vessels |
| persistence | err_20min_m | 5022 (4744–5318) | 5467 | 7983 | 44871 / 659 vessels |
| persistence | err_30min_m | 7387 (6960–7848) | 8023 | 11853 | 44871 / 659 vessels |
| persistence | err_45min_m | 10801 (10150–11496) | 11719 | 17626 | 44871 / 659 vessels |
| persistence | err_60min_m | 14078 (13203–15017) | 15249 | 23294 | 44871 / 659 vessels |
| cv | ade_m | 1982 (1696–2337) | 726 | 5486 | 44871 / 659 vessels |
| cv | fde_m | 4940 (4283–5714) | 1929 | 13465 | 44871 / 659 vessels |
| cv | err_5min_m | 100 (84–120) | 32 | 227 | 44871 / 659 vessels |
| cv | err_10min_m | 295 (246–354) | 88 | 764 | 44871 / 659 vessels |
| cv | err_20min_m | 891 (741–1077) | 270 | 2538 | 44871 / 659 vessels |
| cv | err_30min_m | 1694 (1419–2033) | 537 | 4879 | 44871 / 659 vessels |
| cv | err_45min_m | 3182 (2721–3749) | 1096 | 8948 | 44871 / 659 vessels |
| cv | err_60min_m | 4940 (4283–5714) | 1929 | 13465 | 44871 / 659 vessels |
| ctrv | ade_m | 2596 (2364–2871) | 1453 | 6628 | 44871 / 659 vessels |
| ctrv | fde_m | 6375 (5913–6891) | 3953 | 15690 | 44871 / 659 vessels |
| ctrv | err_5min_m | 132 (108–160) | 44 | 302 | 44871 / 659 vessels |
| ctrv | err_10min_m | 397 (333–474) | 139 | 1023 | 44871 / 659 vessels |
| ctrv | err_20min_m | 1197 (1040–1390) | 490 | 3253 | 44871 / 659 vessels |
| ctrv | err_30min_m | 2250 (2002–2553) | 1051 | 6104 | 44871 / 659 vessels |
| ctrv | err_45min_m | 4155 (3807–4572) | 2295 | 10666 | 44871 / 659 vessels |
| ctrv | err_60min_m | 6375 (5913–6891) | 3953 | 15690 | 44871 / 659 vessels |
| ctrv_damped | ade_m | 1981 (1695–2336) | 734 | 5478 | 44871 / 659 vessels |
| ctrv_damped | fde_m | 4932 (4274–5702) | 1938 | 13424 | 44871 / 659 vessels |
| ctrv_damped | err_5min_m | 103 (86–124) | 34 | 235 | 44871 / 659 vessels |
| ctrv_damped | err_10min_m | 298 (248–360) | 91 | 771 | 44871 / 659 vessels |
| ctrv_damped | err_20min_m | 892 (743–1075) | 276 | 2535 | 44871 / 659 vessels |
| ctrv_damped | err_30min_m | 1694 (1417–2033) | 544 | 4869 | 44871 / 659 vessels |
| ctrv_damped | err_45min_m | 3178 (2717–3741) | 1107 | 8918 | 44871 / 659 vessels |
| ctrv_damped | err_60min_m | 4932 (4274–5702) | 1938 | 13424 | 44871 / 659 vessels |
| kalman_cv | ade_m | 1982 (1695–2337) | 725 | 5489 | 44871 / 659 vessels |
| kalman_cv | fde_m | 4939 (4282–5713) | 1924 | 13462 | 44871 / 659 vessels |
| kalman_cv | err_5min_m | 100 (84–120) | 32 | 227 | 44871 / 659 vessels |
| kalman_cv | err_10min_m | 295 (245–354) | 88 | 764 | 44871 / 659 vessels |
| kalman_cv | err_20min_m | 890 (740–1076) | 270 | 2538 | 44871 / 659 vessels |
| kalman_cv | err_30min_m | 1693 (1418–2033) | 536 | 4882 | 44871 / 659 vessels |
| kalman_cv | err_45min_m | 3181 (2720–3748) | 1094 | 8944 | 44871 / 659 vessels |
| kalman_cv | err_60min_m | 4939 (4282–5713) | 1924 | 13462 | 44871 / 659 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +5408 (+4894 to +5973) | +9138 (+8002 to +10324) |
| ctrv | +613 (+512 to +706) | +1434 (+1093 to +1722) |
| ctrv_damped | -1 (-4 to +2) | -9 (-13 to -5) |
| kalman_cv | -1 (-1 to -0) | -1 (-1 to -1) |
