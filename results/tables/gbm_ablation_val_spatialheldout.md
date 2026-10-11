# Residual GBM context ablation (val, spatially held-out (longitude bands); 163,999 train windows (mean per fold))

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 640 (581–703) | 1574 (1431–1722) | 160 | 510 |
| A_motion | 607 (556–661) | 1477 (1359–1597) | 149 | 488 |
| B_vessel | 603 (550–656) | 1452 (1331–1570) | 151 | 492 |
| C_location | 1047 (992–1100) | 2599 (2464–2724) | 197 | 829 |
| D_all | 822 (770–873) | 1922 (1804–2037) | 187 | 692 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -33 (-51 to -18) | -97 (-154 to -46) |
| B_vessel - cv | -37 (-53 to -22) | -122 (-172 to -77) |
| C_location - cv | +407 (+362 to +452) | +1025 (+907 to +1155) |
| D_all - cv | +182 (+151 to +211) | +348 (+276 to +425) |
| B_vessel - A_motion | -4 (-15 to +8) | -25 (-59 to +15) |
| C_location - A_motion | +440 (+403 to +477) | +1122 (+1029 to +1215) |
| D_all - A_motion | +215 (+196 to +235) | +445 (+399 to +496) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 30502 | 1145 | 1130 | 1127 | 2440 | 1695 |
| 0.5–1 | 6718 | 1610 | 1515 | 1452 | 2762 | 1931 |
| 1–2 | 6969 | 1772 | 1679 | 1589 | 2867 | 2080 |
| 2–5 | 9347 | 1785 | 1733 | 1682 | 2939 | 2103 |
| 5–10 | 3704 | 2362 | 2123 | 2076 | 2513 | 2249 |
| 10–inf | 5742 | 2720 | 2202 | 2235 | 2427 | 2418 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 23914 | 984 | 1001 | 968 | 2507 | 1518 |
| passenger | 15356 | 2573 | 2337 | 2371 | 3194 | 2826 |
| tanker | 8515 | 1233 | 1215 | 1192 | 2716 | 1702 |
| service | 8302 | 2032 | 1776 | 1671 | 2293 | 2027 |
| other | 6543 | 1285 | 1192 | 1158 | 1793 | 1459 |
| unknown | 352 | 937 | 920 | 889 | 2220 | 1386 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (244 vessels) | seen_vessels (448 vessels) |
|---|---|---|
| B_vessel - A_motion | -30 (-41 to -20) | -23 (-70 to +35) |
| C_location - A_motion | +1477 (+1381 to +1571) | +979 (+867 to +1104) |
| D_all - A_motion | +532 (+495 to +569) | +409 (+346 to +472) |
| A_motion - cv | -11 (-45 to +14) | -131 (-209 to -63) |
