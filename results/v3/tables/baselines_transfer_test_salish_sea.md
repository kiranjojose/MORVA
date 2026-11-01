| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 6394 (5951–6820) | 6102 | 11621 | 110193 / 622 vessels |
| persistence | fde_m | 11146 (10243–12159) | 10719 | 21785 | 110193 / 622 vessels |
| persistence | err_5min_m | 1288 (1215–1362) | 1238 | 2424 | 110193 / 622 vessels |
| persistence | err_10min_m | 2486 (2341–2633) | 2384 | 4659 | 110193 / 622 vessels |
| persistence | err_20min_m | 4703 (4413–4992) | 4531 | 8634 | 110193 / 622 vessels |
| persistence | err_30min_m | 6662 (6220–7099) | 6366 | 12231 | 110193 / 622 vessels |
| persistence | err_45min_m | 9160 (8496–9799) | 8814 | 17163 | 110193 / 622 vessels |
| persistence | err_60min_m | 11146 (10243–12159) | 10719 | 21785 | 110193 / 622 vessels |
| cv | ade_m | 4951 (4292–5655) | 2949 | 11946 | 110193 / 622 vessels |
| cv | fde_m | 10991 (9590–12361) | 6749 | 26621 | 110193 / 622 vessels |
| cv | err_5min_m | 295 (249–346) | 73 | 881 | 110193 / 622 vessels |
| cv | err_10min_m | 914 (775–1063) | 300 | 2619 | 110193 / 622 vessels |
| cv | err_20min_m | 2619 (2250–3024) | 1300 | 6693 | 110193 / 622 vessels |
| cv | err_30min_m | 4611 (3970–5292) | 2691 | 11293 | 110193 / 622 vessels |
| cv | err_45min_m | 7840 (6794–8943) | 4698 | 18952 | 110193 / 622 vessels |
| cv | err_60min_m | 10991 (9590–12361) | 6749 | 26621 | 110193 / 622 vessels |
| ctrv | ade_m | 4722 (4233–5205) | 3254 | 10816 | 110193 / 622 vessels |
| ctrv | fde_m | 9522 (8679–10369) | 6562 | 22032 | 110193 / 622 vessels |
| ctrv | err_5min_m | 392 (327–460) | 101 | 1121 | 110193 / 622 vessels |
| ctrv | err_10min_m | 1139 (966–1321) | 413 | 3226 | 110193 / 622 vessels |
| ctrv | err_20min_m | 2911 (2530–3321) | 1610 | 7284 | 110193 / 622 vessels |
| ctrv | err_30min_m | 4699 (4145–5241) | 3014 | 11389 | 110193 / 622 vessels |
| ctrv | err_45min_m | 7243 (6513–7959) | 4907 | 16915 | 110193 / 622 vessels |
| ctrv | err_60min_m | 9522 (8679–10369) | 6562 | 22032 | 110193 / 622 vessels |
| ctrv_damped | ade_m | 4959 (4297–5668) | 2942 | 11984 | 110193 / 622 vessels |
| ctrv_damped | fde_m | 10986 (9586–12353) | 6741 | 26658 | 110193 / 622 vessels |
| ctrv_damped | err_5min_m | 301 (253–354) | 77 | 885 | 110193 / 622 vessels |
| ctrv_damped | err_10min_m | 924 (781–1077) | 303 | 2638 | 110193 / 622 vessels |
| ctrv_damped | err_20min_m | 2635 (2263–3044) | 1300 | 6737 | 110193 / 622 vessels |
| ctrv_damped | err_30min_m | 4627 (3981–5314) | 2680 | 11348 | 110193 / 622 vessels |
| ctrv_damped | err_45min_m | 7843 (6791–8955) | 4690 | 18996 | 110193 / 622 vessels |
| ctrv_damped | err_60min_m | 10986 (9586–12353) | 6741 | 26658 | 110193 / 622 vessels |
| kalman_cv | ade_m | 4950 (4291–5654) | 2948 | 11943 | 110193 / 622 vessels |
| kalman_cv | fde_m | 10989 (9589–12358) | 6747 | 26623 | 110193 / 622 vessels |
| kalman_cv | err_5min_m | 295 (249–346) | 73 | 882 | 110193 / 622 vessels |
| kalman_cv | err_10min_m | 914 (775–1063) | 299 | 2620 | 110193 / 622 vessels |
| kalman_cv | err_20min_m | 2619 (2250–3024) | 1300 | 6694 | 110193 / 622 vessels |
| kalman_cv | err_30min_m | 4610 (3969–5291) | 2690 | 11291 | 110193 / 622 vessels |
| kalman_cv | err_45min_m | 7839 (6793–8941) | 4698 | 18946 | 110193 / 622 vessels |
| kalman_cv | err_60min_m | 10989 (9589–12358) | 6747 | 26623 | 110193 / 622 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, Kalman q = 1 m²/s³, both tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +1443 (+704 to +2234) | +154 (-1591 to +1994) |
| ctrv | -229 (-548 to +69) | -1469 (-2417 to -557) |
| ctrv_damped | +8 (-1 to +17) | -5 (-17 to +6) |
| kalman_cv | -1 (-1 to -1) | -2 (-3 to -1) |
