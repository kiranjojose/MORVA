# Residual GBM context ablation (test; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 634 (576–691) | 1566 (1425–1706) | 158 | 502 |
| A_motion | 535 (498–570) | 1292 (1214–1371) | 138 | 434 |
| B_vessel | 487 (458–517) | 1152 (1090–1215) | 132 | 402 |
| C_location | 394 (365–421) | 872 (811–931) | 123 | 345 |
| D_all | 385 (359–410) | 851 (798–904) | 121 | 338 |
| E_fairway | 346 (317–374) | 802 (739–865) | 103 | 288 |
| F_all_fairway | 336 (309–362) | 768 (712–823) | 102 | 282 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -99 (-134 to -68) | -274 (-375 to -188) |
| B_vessel - cv | -146 (-192 to -105) | -414 (-545 to -299) |
| C_location - cv | -240 (-284 to -199) | -694 (-814 to -581) |
| D_all - cv | -249 (-295 to -207) | -715 (-842 to -599) |
| E_fairway - cv | -288 (-330 to -249) | -763 (-880 to -658) |
| F_all_fairway - cv | -298 (-341 to -257) | -798 (-919 to -686) |
| B_vessel - A_motion | -48 (-61 to -35) | -140 (-176 to -103) |
| C_location - A_motion | -141 (-156 to -128) | -420 (-459 to -385) |
| D_all - A_motion | -150 (-166 to -135) | -441 (-481 to -403) |
| E_fairway - A_motion | -189 (-203 to -176) | -490 (-523 to -457) |
| F_all_fairway - A_motion | -199 (-215 to -185) | -524 (-562 to -488) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 80479 | 1166 | 1076 | 1006 | 667 | 670 | 598 | 584 |
| 0.5–1 | 18387 | 1563 | 1339 | 1192 | 890 | 864 | 801 | 763 |
| 1–2 | 18793 | 1736 | 1414 | 1234 | 968 | 918 | 871 | 820 |
| 2–5 | 25608 | 1775 | 1418 | 1221 | 939 | 895 | 853 | 809 |
| 5–10 | 10000 | 2402 | 1675 | 1381 | 1291 | 1223 | 1226 | 1156 |
| 10–inf | 14266 | 2643 | 1796 | 1533 | 1468 | 1431 | 1479 | 1398 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 68935 | 994 | 961 | 935 | 602 | 599 | 515 | 506 |
| passenger | 40449 | 2603 | 1736 | 1312 | 1044 | 1003 | 1023 | 955 |
| tanker | 22913 | 1160 | 1103 | 1083 | 636 | 631 | 545 | 532 |
| service | 22116 | 1981 | 1688 | 1535 | 1458 | 1378 | 1379 | 1283 |
| other | 11929 | 1374 | 1332 | 1277 | 1193 | 1206 | 1112 | 1108 |
| unknown | 1191 | 1457 | 1259 | 1268 | 1141 | 1156 | 1108 | 1122 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (589 vessels) | seen_vessels (620 vessels) |
|---|---|---|
| B_vessel - A_motion | -15 (-23 to -6) | -200 (-247 to -151) |
| C_location - A_motion | -369 (-394 to -347) | -444 (-497 to -395) |
| D_all - A_motion | -361 (-389 to -335) | -479 (-536 to -426) |
| E_fairway - A_motion | -454 (-481 to -427) | -507 (-557 to -462) |
| F_all_fairway - A_motion | -460 (-489 to -432) | -555 (-609 to -507) |
| A_motion - cv | -41 (-55 to -29) | -385 (-527 to -264) |

FDE@20 min (m) across seeds [0, 1, 2]:

| model | mean | sd | min | max |
|---|---|---|---|---|
| A_motion | 1292 | 0.8 | 1291 | 1292 |
| B_vessel | 1151 | 1.1 | 1150 | 1152 |
| C_location | 869 | 4.5 | 864 | 872 |
| D_all | 847 | 3.7 | 844 | 851 |
| E_fairway | 801 | 1.4 | 800 | 802 |
| F_all_fairway | 771 | 2.3 | 768 | 772 |
