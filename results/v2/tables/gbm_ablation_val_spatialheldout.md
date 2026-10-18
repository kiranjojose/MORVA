# Residual GBM context ablation (val, spatially held-out (longitude bands); 163,998 train windows (mean per fold))

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 633 (577–693) | 1563 (1424–1714) | 157 | 503 |
| A_motion | 603 (554–655) | 1466 (1360–1586) | 147 | 484 |
| B_vessel | 597 (547–651) | 1440 (1328–1558) | 148 | 487 |
| C_location | 1031 (983–1083) | 2552 (2432–2671) | 186 | 800 |
| D_all | 828 (781–882) | 1927 (1820–2039) | 187 | 689 |
| E_fairway | 424 (386–465) | 1028 (939–1126) | 115 | 339 |
| F_all_fairway | 422 (382–466) | 1024 (926–1138) | 115 | 337 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -31 (-46 to -16) | -97 (-148 to -49) |
| B_vessel - cv | -36 (-51 to -21) | -123 (-168 to -78) |
| C_location - cv | +398 (+356 to +437) | +989 (+873 to +1103) |
| D_all - cv | +195 (+167 to +226) | +364 (+292 to +440) |
| E_fairway - cv | -210 (-231 to -188) | -535 (-588 to -482) |
| F_all_fairway - cv | -212 (-231 to -192) | -539 (-586 to -489) |
| B_vessel - A_motion | -5 (-14 to +4) | -27 (-54 to +5) |
| C_location - A_motion | +428 (+394 to +462) | +1085 (+998 to +1173) |
| D_all - A_motion | +226 (+206 to +247) | +461 (+415 to +510) |
| E_fairway - A_motion | -179 (-195 to -163) | -438 (-477 to -401) |
| F_all_fairway - A_motion | -181 (-197 to -165) | -442 (-486 to -396) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 58022 | 1138 | 1123 | 1119 | 2401 | 1722 | 737 | 738 |
| 0.5–1 | 13155 | 1586 | 1490 | 1428 | 2727 | 1961 | 996 | 985 |
| 1–2 | 13434 | 1735 | 1629 | 1553 | 2755 | 2045 | 1128 | 1098 |
| 2–5 | 17939 | 1799 | 1727 | 1680 | 2846 | 2089 | 1133 | 1128 |
| 5–10 | 7047 | 2411 | 2135 | 2076 | 2522 | 2249 | 1608 | 1618 |
| 10–inf | 10815 | 2656 | 2208 | 2222 | 2424 | 2363 | 1951 | 1959 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 46684 | 982 | 993 | 961 | 2426 | 1552 | 595 | 571 |
| passenger | 28963 | 2606 | 2350 | 2372 | 3166 | 2829 | 1683 | 1753 |
| tanker | 16413 | 1215 | 1200 | 1180 | 2749 | 1757 | 705 | 683 |
| service | 15854 | 1951 | 1721 | 1607 | 2156 | 1913 | 1447 | 1387 |
| other | 11488 | 1309 | 1236 | 1216 | 1789 | 1480 | 1053 | 1051 |
| unknown | 1010 | 952 | 947 | 970 | 2408 | 1452 | 572 | 617 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (436 vessels) | seen_vessels (612 vessels) |
|---|---|---|
| B_vessel - A_motion | -27 (-36 to -20) | -26 (-70 to +20) |
| C_location - A_motion | +1417 (+1346 to +1486) | +954 (+844 to +1068) |
| D_all - A_motion | +571 (+541 to +600) | +417 (+353 to +487) |
| E_fairway - A_motion | -417 (-442 to -392) | -447 (-502 to -397) |
| F_all_fairway - A_motion | -434 (-460 to -407) | -445 (-512 to -386) |
| A_motion - cv | -12 (-33 to +5) | -130 (-200 to -67) |
