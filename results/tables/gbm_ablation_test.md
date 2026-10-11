# Residual GBM context ablation (test; 238,830 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 627 (565–684) | 1554 (1400–1694) | 155 | 496 |
| A_motion | 526 (486–565) | 1267 (1180–1355) | 135 | 427 |
| B_vessel | 478 (446–513) | 1128 (1059–1202) | 129 | 396 |
| C_location | 387 (356–420) | 863 (796–933) | 121 | 342 |
| D_all | 377 (347–407) | 831 (770–895) | 118 | 335 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -102 (-134 to -70) | -287 (-380 to -195) |
| B_vessel - cv | -150 (-193 to -107) | -426 (-547 to -303) |
| C_location - cv | -240 (-285 to -195) | -691 (-810 to -571) |
| D_all - cv | -251 (-297 to -204) | -723 (-846 to -593) |
| B_vessel - A_motion | -48 (-61 to -35) | -138 (-176 to -103) |
| C_location - A_motion | -138 (-153 to -123) | -404 (-441 to -366) |
| D_all - A_motion | -149 (-166 to -132) | -435 (-479 to -393) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 27301 | 1134 | 1034 | 968 | 646 | 635 |
| 0.5–1 | 6387 | 1563 | 1314 | 1172 | 890 | 849 |
| 1–2 | 6423 | 1694 | 1378 | 1195 | 947 | 895 |
| 2–5 | 8553 | 1816 | 1436 | 1223 | 962 | 909 |
| 5–10 | 3333 | 2470 | 1696 | 1383 | 1298 | 1218 |
| 10–inf | 5071 | 2584 | 1751 | 1521 | 1435 | 1401 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 22586 | 981 | 946 | 920 | 590 | 584 |
| passenger | 13539 | 2648 | 1743 | 1328 | 1099 | 1024 |
| tanker | 7859 | 1196 | 1138 | 1117 | 676 | 666 |
| service | 7500 | 1869 | 1564 | 1367 | 1328 | 1220 |
| other | 4926 | 1344 | 1225 | 1208 | 1095 | 1133 |
| unknown | 658 | 960 | 935 | 974 | 569 | 644 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (241 vessels) | seen_vessels (381 vessels) |
|---|---|---|
| B_vessel - A_motion | -18 (-28 to -3) | -185 (-233 to -141) |
| C_location - A_motion | -382 (-411 to -352) | -412 (-461 to -365) |
| D_all - A_motion | -383 (-416 to -350) | -455 (-512 to -404) |
| A_motion - cv | -55 (-78 to -37) | -378 (-511 to -265) |

FDE@20 min (m) across seeds [0, 1, 2]:

| model | mean | sd | min | max |
|---|---|---|---|---|
| A_motion | 1267 | 1.4 | 1265 | 1268 |
| B_vessel | 1126 | 2.4 | 1124 | 1128 |
| C_location | 864 | 1.9 | 862 | 866 |
| D_all | 828 | 3.6 | 824 | 831 |
