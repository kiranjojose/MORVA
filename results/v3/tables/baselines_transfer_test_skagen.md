| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 6713 (6361–7113) | 6896 | 11541 | 146955 / 1372 vessels |
| persistence | fde_m | 12738 (12047–13507) | 12978 | 22437 | 146955 / 1372 vessels |
| persistence | err_5min_m | 1185 (1126–1247) | 1234 | 1968 | 146955 / 1372 vessels |
| persistence | err_10min_m | 2342 (2224–2465) | 2443 | 3914 | 146955 / 1372 vessels |
| persistence | err_20min_m | 4578 (4341–4830) | 4779 | 7746 | 146955 / 1372 vessels |
| persistence | err_30min_m | 6723 (6371–7109) | 6992 | 11500 | 146955 / 1372 vessels |
| persistence | err_45min_m | 9801 (9278–10392) | 10095 | 17017 | 146955 / 1372 vessels |
| persistence | err_60min_m | 12738 (12047–13507) | 12978 | 22437 | 146955 / 1372 vessels |
| cv | ade_m | 1889 (1659–2179) | 717 | 5196 | 146955 / 1372 vessels |
| cv | fde_m | 4719 (4206–5349) | 1914 | 12801 | 146955 / 1372 vessels |
| cv | err_5min_m | 94 (80–111) | 30 | 206 | 146955 / 1372 vessels |
| cv | err_10min_m | 278 (238–330) | 83 | 702 | 146955 / 1372 vessels |
| cv | err_20min_m | 843 (725–997) | 259 | 2371 | 146955 / 1372 vessels |
| cv | err_30min_m | 1609 (1392–1888) | 526 | 4590 | 146955 / 1372 vessels |
| cv | err_45min_m | 3034 (2666–3498) | 1096 | 8509 | 146955 / 1372 vessels |
| cv | err_60min_m | 4719 (4206–5349) | 1914 | 12801 | 146955 / 1372 vessels |
| ctrv | ade_m | 2409 (2226–2634) | 1341 | 6155 | 146955 / 1372 vessels |
| ctrv | fde_m | 5904 (5553–6304) | 3646 | 14397 | 146955 / 1372 vessels |
| ctrv | err_5min_m | 121 (102–146) | 40 | 274 | 146955 / 1372 vessels |
| ctrv | err_10min_m | 367 (315–433) | 128 | 928 | 146955 / 1372 vessels |
| ctrv | err_20min_m | 1111 (986–1269) | 457 | 3005 | 146955 / 1372 vessels |
| ctrv | err_30min_m | 2091 (1898–2331) | 982 | 5622 | 146955 / 1372 vessels |
| ctrv | err_45min_m | 3858 (3583–4195) | 2124 | 9859 | 146955 / 1372 vessels |
| ctrv | err_60min_m | 5904 (5553–6304) | 3646 | 14397 | 146955 / 1372 vessels |
| ctrv_damped | ade_m | 1886 (1656–2177) | 724 | 5178 | 146955 / 1372 vessels |
| ctrv_damped | fde_m | 4709 (4196–5338) | 1918 | 12751 | 146955 / 1372 vessels |
| ctrv_damped | err_5min_m | 96 (81–114) | 31 | 212 | 146955 / 1372 vessels |
| ctrv_damped | err_10min_m | 280 (238–333) | 85 | 706 | 146955 / 1372 vessels |
| ctrv_damped | err_20min_m | 844 (726–997) | 264 | 2360 | 146955 / 1372 vessels |
| ctrv_damped | err_30min_m | 1607 (1391–1885) | 532 | 4564 | 146955 / 1372 vessels |
| ctrv_damped | err_45min_m | 3028 (2661–3493) | 1103 | 8479 | 146955 / 1372 vessels |
| ctrv_damped | err_60min_m | 4709 (4196–5338) | 1918 | 12751 | 146955 / 1372 vessels |
| kalman_cv | ade_m | 1888 (1658–2179) | 717 | 5195 | 146955 / 1372 vessels |
| kalman_cv | fde_m | 4719 (4205–5347) | 1912 | 12804 | 146955 / 1372 vessels |
| kalman_cv | err_5min_m | 94 (80–111) | 30 | 206 | 146955 / 1372 vessels |
| kalman_cv | err_10min_m | 278 (237–330) | 83 | 702 | 146955 / 1372 vessels |
| kalman_cv | err_20min_m | 843 (725–997) | 258 | 2370 | 146955 / 1372 vessels |
| kalman_cv | err_30min_m | 1609 (1392–1887) | 525 | 4590 | 146955 / 1372 vessels |
| kalman_cv | err_45min_m | 3034 (2665–3497) | 1094 | 8508 | 146955 / 1372 vessels |
| kalman_cv | err_60min_m | 4719 (4205–5347) | 1912 | 12804 | 146955 / 1372 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +4824 (+4411 to +5288) | +8019 (+7101 to +9009) |
| ctrv | +520 (+439 to +591) | +1185 (+905 to +1429) |
| ctrv_damped | -3 (-5 to -1) | -10 (-13 to -8) |
| kalman_cv | -0 (-1 to -0) | -1 (-1 to -0) |
