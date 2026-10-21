# Residual GBM context ablation (val, vessel-held-out; 89,705 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 633 (577–693) | 1563 (1424–1714) | 157 | 503 |
| A_motion | 593 (541–650) | 1451 (1329–1577) | 147 | 474 |
| B_vessel | 585 (533–639) | 1427 (1308–1552) | 146 | 470 |
| C_location | 509 (457–563) | 1189 (1066–1317) | 141 | 427 |
| D_all | 506 (453–562) | 1179 (1048–1312) | 141 | 427 |
| E_fairway | 424 (378–471) | 1023 (911–1143) | 116 | 342 |
| F_all_fairway | 420 (375–467) | 1003 (895–1120) | 115 | 341 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -40 (-48 to -32) | -112 (-139 to -87) |
| B_vessel - cv | -49 (-58 to -40) | -135 (-169 to -107) |
| C_location - cv | -124 (-137 to -112) | -374 (-413 to -334) |
| D_all - cv | -127 (-139 to -115) | -384 (-421 to -347) |
| E_fairway - cv | -210 (-226 to -193) | -540 (-577 to -501) |
| F_all_fairway - cv | -214 (-230 to -197) | -560 (-599 to -520) |
| B_vessel - A_motion | -9 (-13 to -4) | -23 (-40 to -6) |
| C_location - A_motion | -84 (-93 to -76) | -262 (-290 to -234) |
| D_all - A_motion | -87 (-96 to -77) | -272 (-301 to -241) |
| E_fairway - A_motion | -170 (-182 to -157) | -428 (-454 to -401) |
| F_all_fairway - A_motion | -174 (-187 to -161) | -448 (-479 to -418) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 58022 | 1138 | 1109 | 1091 | 809 | 799 | 689 | 676 |
| 0.5–1 | 13155 | 1586 | 1476 | 1416 | 1165 | 1140 | 1000 | 953 |
| 1–2 | 13434 | 1735 | 1593 | 1514 | 1300 | 1271 | 1099 | 1044 |
| 2–5 | 17939 | 1799 | 1651 | 1572 | 1348 | 1323 | 1111 | 1072 |
| 5–10 | 7047 | 2411 | 2115 | 2069 | 2017 | 1992 | 1737 | 1709 |
| 10–inf | 10815 | 2656 | 2313 | 2479 | 2316 | 2378 | 2134 | 2191 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 46684 | 982 | 933 | 921 | 569 | 565 | 489 | 487 |
| passenger | 28963 | 2606 | 2433 | 2414 | 2242 | 2262 | 1890 | 1847 |
| tanker | 16413 | 1215 | 1132 | 1129 | 642 | 640 | 566 | 566 |
| service | 15854 | 1951 | 1743 | 1622 | 1748 | 1635 | 1517 | 1439 |
| other | 11488 | 1309 | 1178 | 1203 | 1117 | 1134 | 1023 | 1041 |
| unknown | 1010 | 952 | 895 | 900 | 579 | 599 | 496 | 509 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (1048 vessels) |
|---|---|
| B_vessel - A_motion | -23 (-40 to -6) |
| C_location - A_motion | -262 (-290 to -234) |
| D_all - A_motion | -272 (-301 to -241) |
| E_fairway - A_motion | -428 (-454 to -401) |
| F_all_fairway - A_motion | -448 (-479 to -418) |
| A_motion - cv | -112 (-139 to -87) |
