# Residual GBM context ablation (val, random train subsample 109,866; 109,866 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 640 (581–703) | 1574 (1431–1722) | 160 | 510 |
| A_motion | 539 (501–580) | 1295 (1209–1384) | 139 | 440 |
| B_vessel | 491 (459–526) | 1157 (1089–1226) | 134 | 410 |
| C_location | 411 (378–447) | 904 (835–976) | 127 | 366 |
| D_all | 396 (366–429) | 861 (801–925) | 125 | 356 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -101 (-136 to -70) | -279 (-382 to -187) |
| B_vessel - cv | -149 (-191 to -108) | -417 (-540 to -300) |
| C_location - cv | -229 (-270 to -190) | -670 (-786 to -558) |
| D_all - cv | -244 (-287 to -203) | -713 (-833 to -598) |
| B_vessel - A_motion | -48 (-60 to -36) | -138 (-172 to -103) |
| C_location - A_motion | -128 (-141 to -115) | -391 (-428 to -352) |
| D_all - A_motion | -143 (-159 to -128) | -434 (-476 to -391) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 30502 | 1145 | 1060 | 990 | 689 | 668 |
| 0.5–1 | 6718 | 1610 | 1368 | 1200 | 918 | 866 |
| 1–2 | 6969 | 1772 | 1460 | 1266 | 1029 | 955 |
| 2–5 | 9347 | 1785 | 1437 | 1237 | 975 | 913 |
| 5–10 | 3704 | 2362 | 1646 | 1362 | 1283 | 1203 |
| 10–inf | 5742 | 2720 | 1801 | 1596 | 1517 | 1462 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 23914 | 984 | 957 | 930 | 607 | 590 |
| passenger | 15356 | 2573 | 1727 | 1342 | 1070 | 1015 |
| tanker | 8515 | 1233 | 1165 | 1138 | 719 | 700 |
| service | 8302 | 2032 | 1724 | 1530 | 1544 | 1399 |
| other | 6543 | 1285 | 1162 | 1117 | 1039 | 1028 |
| unknown | 352 | 937 | 912 | 883 | 672 | 664 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (246 vessels) | seen_vessels (446 vessels) |
|---|---|---|
| B_vessel - A_motion | -22 (-31 to -12) | -185 (-228 to -138) |
| C_location - A_motion | -377 (-413 to -340) | -397 (-449 to -345) |
| D_all - A_motion | -389 (-428 to -348) | -452 (-507 to -397) |
| A_motion - cv | -60 (-103 to -34) | -367 (-510 to -250) |
