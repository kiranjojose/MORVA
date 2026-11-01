| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 4273 (4119–4423) | 4341 | 8084 | 179930 / 1145 vessels |
| persistence | fde_m | 7742 (7414–8064) | 7830 | 15364 | 179930 / 1145 vessels |
| persistence | err_5min_m | 847 (819–875) | 857 | 1541 | 179930 / 1145 vessels |
| persistence | err_10min_m | 1631 (1579–1683) | 1662 | 2987 | 179930 / 1145 vessels |
| persistence | err_20min_m | 3068 (2968–3162) | 3140 | 5684 | 179930 / 1145 vessels |
| persistence | err_30min_m | 4371 (4221–4519) | 4442 | 8239 | 179930 / 1145 vessels |
| persistence | err_45min_m | 6135 (5903–6359) | 6250 | 11887 | 179930 / 1145 vessels |
| persistence | err_60min_m | 7742 (7414–8064) | 7830 | 15364 | 179930 / 1145 vessels |
| cv | ade_m | 2677 (2470–2912) | 1831 | 5855 | 179930 / 1145 vessels |
| cv | fde_m | 5934 (5519–6395) | 4089 | 12994 | 179930 / 1145 vessels |
| cv | err_5min_m | 181 (162–200) | 74 | 454 | 179930 / 1145 vessels |
| cv | err_10min_m | 533 (483–587) | 257 | 1338 | 179930 / 1145 vessels |
| cv | err_20min_m | 1462 (1332–1605) | 860 | 3455 | 179930 / 1145 vessels |
| cv | err_30min_m | 2510 (2299–2741) | 1609 | 5624 | 179930 / 1145 vessels |
| cv | err_45min_m | 4189 (3872–4544) | 2807 | 9256 | 179930 / 1145 vessels |
| cv | err_60min_m | 5934 (5519–6395) | 4089 | 12994 | 179930 / 1145 vessels |
| ctrv | ade_m | 2999 (2877–3140) | 2193 | 6546 | 179930 / 1145 vessels |
| ctrv | fde_m | 6286 (6066–6511) | 4718 | 13728 | 179930 / 1145 vessels |
| ctrv | err_5min_m | 219 (195–244) | 94 | 549 | 179930 / 1145 vessels |
| ctrv | err_10min_m | 645 (592–705) | 318 | 1676 | 179930 / 1145 vessels |
| ctrv | err_20min_m | 1755 (1648–1880) | 1065 | 4277 | 179930 / 1145 vessels |
| ctrv | err_30min_m | 2930 (2787–3093) | 1995 | 6853 | 179930 / 1145 vessels |
| ctrv | err_45min_m | 4650 (4468–4848) | 3348 | 10380 | 179930 / 1145 vessels |
| ctrv | err_60min_m | 6286 (6066–6511) | 4718 | 13728 | 179930 / 1145 vessels |
| ctrv_damped | ade_m | 2682 (2476–2916) | 1832 | 5877 | 179930 / 1145 vessels |
| ctrv_damped | fde_m | 5947 (5531–6407) | 4104 | 13035 | 179930 / 1145 vessels |
| ctrv_damped | err_5min_m | 180 (162–200) | 75 | 450 | 179930 / 1145 vessels |
| ctrv_damped | err_10min_m | 533 (481–587) | 256 | 1337 | 179930 / 1145 vessels |
| ctrv_damped | err_20min_m | 1464 (1334–1607) | 854 | 3479 | 179930 / 1145 vessels |
| ctrv_damped | err_30min_m | 2514 (2305–2746) | 1607 | 5650 | 179930 / 1145 vessels |
| ctrv_damped | err_45min_m | 4197 (3881–4552) | 2813 | 9290 | 179930 / 1145 vessels |
| ctrv_damped | err_60min_m | 5947 (5531–6407) | 4104 | 13035 | 179930 / 1145 vessels |
| kalman_cv | ade_m | 2677 (2470–2910) | 1831 | 5854 | 179930 / 1145 vessels |
| kalman_cv | fde_m | 5933 (5517–6393) | 4087 | 12993 | 179930 / 1145 vessels |
| kalman_cv | err_5min_m | 180 (162–200) | 74 | 454 | 179930 / 1145 vessels |
| kalman_cv | err_10min_m | 533 (482–587) | 257 | 1337 | 179930 / 1145 vessels |
| kalman_cv | err_20min_m | 1462 (1332–1605) | 859 | 3454 | 179930 / 1145 vessels |
| kalman_cv | err_30min_m | 2509 (2298–2741) | 1608 | 5624 | 179930 / 1145 vessels |
| kalman_cv | err_45min_m | 4187 (3871–4543) | 2806 | 9255 | 179930 / 1145 vessels |
| kalman_cv | err_60min_m | 5933 (5517–6393) | 4087 | 12993 | 179930 / 1145 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +1596 (+1312 to +1865) | +1808 (+1218 to +2395) |
| ctrv | +322 (+199 to +448) | +352 (+24 to +680) |
| ctrv_damped | +5 (+4 to +6) | +13 (+11 to +15) |
| kalman_cv | -1 (-1 to -1) | -2 (-2 to -1) |
