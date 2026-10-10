# Residual GBM context ablation (val, vessel-held-out; 109,866 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 640 (581–703) | 1574 (1431–1722) | 160 | 510 |
| A_motion | 595 (542–652) | 1452 (1324–1582) | 148 | 477 |
| B_vessel | 589 (536–645) | 1435 (1308–1564) | 147 | 474 |
| C_location | 505 (449–562) | 1171 (1039–1304) | 141 | 427 |
| D_all | 502 (446–560) | 1163 (1031–1297) | 141 | 425 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -45 (-54 to -36) | -122 (-152 to -95) |
| B_vessel - cv | -51 (-60 to -42) | -139 (-169 to -110) |
| C_location - cv | -136 (-149 to -122) | -403 (-444 to -361) |
| D_all - cv | -138 (-150 to -125) | -411 (-447 to -373) |
| B_vessel - A_motion | -6 (-11 to -2) | -17 (-35 to +1) |
| C_location - A_motion | -91 (-101 to -81) | -281 (-312 to -252) |
| D_all - A_motion | -93 (-104 to -83) | -288 (-321 to -258) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 30502 | 1145 | 1106 | 1091 | 788 | 785 |
| 0.5–1 | 6718 | 1610 | 1485 | 1433 | 1146 | 1131 |
| 1–2 | 6969 | 1772 | 1622 | 1552 | 1301 | 1270 |
| 2–5 | 9347 | 1785 | 1633 | 1574 | 1316 | 1288 |
| 5–10 | 3704 | 2362 | 2063 | 2049 | 1968 | 1944 |
| 10–inf | 5742 | 2720 | 2356 | 2500 | 2324 | 2378 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 23914 | 984 | 934 | 919 | 550 | 553 |
| passenger | 15356 | 2573 | 2390 | 2390 | 2154 | 2162 |
| tanker | 8515 | 1233 | 1135 | 1134 | 636 | 642 |
| service | 8302 | 2032 | 1807 | 1693 | 1797 | 1692 |
| other | 6543 | 1285 | 1137 | 1174 | 1065 | 1088 |
| unknown | 352 | 937 | 870 | 846 | 650 | 656 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (692 vessels) |
|---|---|
| B_vessel - A_motion | -17 (-35 to +1) |
| C_location - A_motion | -281 (-312 to -252) |
| D_all - A_motion | -288 (-321 to -258) |
| A_motion - cv | -122 (-152 to -95) |

FDE@20 min (m) across seeds [0, 1, 2]:

| model | mean | sd | min | max |
|---|---|---|---|---|
| A_motion | 1452 | 2.0 | 1450 | 1454 |
| B_vessel | 1429 | 4.7 | 1426 | 1435 |
| C_location | 1170 | 1.4 | 1168 | 1171 |
| D_all | 1160 | 2.6 | 1158 | 1163 |
