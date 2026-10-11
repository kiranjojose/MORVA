# Residual GBM context ablation (test, spatially held-out (longitude bands); 163,999 train windows (mean per fold))

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 627 (565–684) | 1554 (1400–1694) | 155 | 496 |
| A_motion | 599 (544–652) | 1465 (1338–1590) | 145 | 478 |
| B_vessel | 595 (539–650) | 1442 (1313–1566) | 147 | 483 |
| C_location | 1039 (982–1097) | 2592 (2452–2730) | 192 | 815 |
| D_all | 813 (758–869) | 1918 (1792–2046) | 181 | 681 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -28 (-44 to -14) | -89 (-137 to -39) |
| B_vessel - cv | -32 (-47 to -17) | -112 (-158 to -66) |
| C_location - cv | +412 (+368 to +459) | +1039 (+917 to +1169) |
| D_all - cv | +186 (+157 to +216) | +364 (+291 to +448) |
| B_vessel - A_motion | -4 (-13 to +6) | -23 (-51 to +9) |
| C_location - A_motion | +440 (+401 to +480) | +1127 (+1031 to +1229) |
| D_all - A_motion | +214 (+194 to +235) | +453 (+403 to +505) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 27301 | 1134 | 1126 | 1124 | 2461 | 1709 |
| 0.5–1 | 6387 | 1563 | 1481 | 1415 | 2783 | 1929 |
| 1–2 | 6423 | 1694 | 1584 | 1522 | 2787 | 2001 |
| 2–5 | 8553 | 1816 | 1751 | 1689 | 2866 | 2093 |
| 5–10 | 3333 | 2470 | 2158 | 2125 | 2524 | 2288 |
| 10–inf | 5071 | 2584 | 2185 | 2218 | 2399 | 2386 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 22586 | 981 | 989 | 957 | 2498 | 1525 |
| passenger | 13539 | 2648 | 2412 | 2430 | 3162 | 2873 |
| tanker | 7859 | 1196 | 1183 | 1162 | 2778 | 1697 |
| service | 7500 | 1869 | 1645 | 1548 | 2112 | 1876 |
| other | 4926 | 1344 | 1292 | 1292 | 1897 | 1575 |
| unknown | 658 | 960 | 957 | 994 | 2586 | 1441 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (241 vessels) | seen_vessels (381 vessels) |
|---|---|---|
| B_vessel - A_motion | -23 (-32 to -12) | -23 (-65 to +22) |
| C_location - A_motion | +1489 (+1418 to +1557) | +987 (+870 to +1115) |
| D_all - A_motion | +544 (+507 to +580) | +417 (+348 to +487) |
| A_motion - cv | -13 (-36 to +4) | -118 (-194 to -53) |
