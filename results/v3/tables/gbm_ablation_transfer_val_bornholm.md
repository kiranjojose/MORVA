# Residual GBM context ablation (transfer_val, bornholm; 316,680 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 1261 (1138–1430) | 3283 (2950–3752) | 60 | 175 | 531 | 1034 | 2031 |
| A_motion | 1410 (1320–1521) | 3696 (3473–3961) | 56 | 171 | 552 | 1142 | 2297 |
| B_vessel | 1429 (1343–1522) | 3736 (3538–3946) | 57 | 171 | 561 | 1154 | 2342 |
| C_location | 4015 (3773–4256) | 9553 (9025–10077) | 146 | 734 | 2118 | 3665 | 6148 |
| D_all | 4050 (3801–4292) | 9482 (8940–10011) | 151 | 701 | 2225 | 3469 | 6522 |
| E_fairway | 918 (851–991) | 2416 (2249–2601) | 53 | 148 | 410 | 754 | 1443 |
| F_all_fairway | 929 (862–1005) | 2438 (2277–2614) | 53 | 150 | 419 | 764 | 1468 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | +149 (+49 to +222) | +413 (+87 to +627) |
| B_vessel - cv | +168 (+60 to +246) | +453 (+112 to +686) |
| C_location - cv | +2754 (+2496 to +2992) | +6270 (+5690 to +6818) |
| D_all - cv | +2790 (+2522 to +3038) | +6200 (+5583 to +6779) |
| E_fairway - cv | -343 (-461 to -259) | -867 (-1202 to -641) |
| F_all_fairway - cv | -331 (-457 to -246) | -845 (-1204 to -599) |
| B_vessel - A_motion | +19 (-26 to +63) | +40 (-83 to +158) |
| C_location - A_motion | +2605 (+2379 to +2822) | +5857 (+5386 to +6336) |
| D_all - A_motion | +2641 (+2406 to +2873) | +5786 (+5269 to +6293) |
| E_fairway - A_motion | -492 (-550 to -443) | -1280 (-1422 to -1154) |
| F_all_fairway - A_motion | -481 (-539 to -426) | -1258 (-1409 to -1120) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 19979 | 2927 | 3491 | 3635 | 9613 | 9579 | 2237 | 2301 |
| 0.5–1 | 1706 | 4386 | 4705 | 4400 | 9855 | 9596 | 3043 | 2985 |
| 1–2 | 1358 | 4488 | 4809 | 4450 | 10166 | 10071 | 3121 | 3028 |
| 2–5 | 1255 | 3656 | 3917 | 3491 | 10086 | 10037 | 2626 | 2511 |
| 5–10 | 257 | 7337 | 6225 | 4875 | 6926 | 5816 | 5038 | 4326 |
| 10–inf | 466 | 7750 | 3559 | 3553 | 4095 | 3728 | 3703 | 3347 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 16360 | 2523 | 3175 | 3274 | 9222 | 9394 | 1953 | 1996 |
| tanker | 4544 | 3111 | 3792 | 4061 | 11005 | 11453 | 2526 | 2595 |
| passenger | 1932 | 8493 | 7498 | 6489 | 12190 | 9516 | 5074 | 4722 |
| service | 1123 | 4442 | 2937 | 3019 | 5723 | 5046 | 2417 | 2404 |
| other | 1007 | 5227 | 5359 | 5351 | 7732 | 7058 | 4393 | 4602 |
| unknown | 55 | 1320 | 2403 | 2456 | 6724 | 6642 | 1486 | 1739 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (304 vessels) | seen_vessels (254 vessels) |
|---|---|---|
| B_vessel - A_motion | +12 (-164 to +202) | +76 (-72 to +201) |
| C_location - A_motion | +6412 (+5728 to +7082) | +5136 (+4475 to +5788) |
| D_all - A_motion | +6259 (+5529 to +6973) | +5174 (+4425 to +5920) |
| E_fairway - A_motion | -1343 (-1520 to -1183) | -1199 (-1421 to -1029) |
| F_all_fairway - A_motion | -1335 (-1538 to -1145) | -1158 (-1381 to -978) |
| A_motion - cv | +198 (-330 to +590) | +693 (+607 to +797) |
