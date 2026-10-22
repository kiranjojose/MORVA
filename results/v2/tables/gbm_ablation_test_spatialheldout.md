# Residual GBM context ablation (test, spatially held-out (longitude bands); 163,998 train windows (mean per fold))

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 634 (576–691) | 1566 (1425–1706) | 158 | 502 |
| A_motion | 609 (557–656) | 1483 (1367–1594) | 149 | 488 |
| B_vessel | 604 (550–655) | 1458 (1335–1579) | 150 | 490 |
| C_location | 1039 (993–1090) | 2572 (2459–2698) | 188 | 805 |
| D_all | 840 (786–892) | 1954 (1836–2073) | 189 | 697 |
| E_fairway | 424 (382–463) | 1031 (932–1123) | 115 | 338 |
| F_all_fairway | 423 (378–462) | 1030 (927–1126) | 115 | 336 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -25 (-41 to -10) | -83 (-140 to -35) |
| B_vessel - cv | -30 (-45 to -14) | -108 (-156 to -63) |
| C_location - cv | +406 (+363 to +450) | +1006 (+886 to +1131) |
| D_all - cv | +206 (+177 to +236) | +388 (+313 to +465) |
| E_fairway - cv | -210 (-231 to -189) | -535 (-591 to -482) |
| F_all_fairway - cv | -211 (-231 to -191) | -535 (-586 to -484) |
| B_vessel - A_motion | -5 (-14 to +6) | -25 (-53 to +13) |
| C_location - A_motion | +430 (+397 to +465) | +1090 (+1004 to +1185) |
| D_all - A_motion | +231 (+212 to +251) | +472 (+424 to +519) |
| E_fairway - A_motion | -185 (-202 to -170) | -452 (-494 to -416) |
| F_all_fairway - A_motion | -186 (-204 to -170) | -452 (-500 to -404) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 80479 | 1166 | 1153 | 1153 | 2438 | 1767 | 748 | 757 |
| 0.5–1 | 18387 | 1563 | 1483 | 1422 | 2732 | 1969 | 994 | 983 |
| 1–2 | 18793 | 1736 | 1637 | 1567 | 2776 | 2079 | 1126 | 1102 |
| 2–5 | 25608 | 1775 | 1717 | 1671 | 2802 | 2066 | 1123 | 1111 |
| 5–10 | 10000 | 2402 | 2173 | 2102 | 2544 | 2275 | 1629 | 1630 |
| 10–inf | 14266 | 2643 | 2232 | 2249 | 2460 | 2404 | 1961 | 1976 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 68935 | 994 | 1003 | 972 | 2417 | 1549 | 607 | 586 |
| passenger | 40449 | 2603 | 2368 | 2389 | 3148 | 2853 | 1680 | 1746 |
| tanker | 22913 | 1160 | 1152 | 1134 | 2700 | 1752 | 658 | 633 |
| service | 22116 | 1981 | 1761 | 1676 | 2260 | 1968 | 1471 | 1428 |
| other | 11929 | 1374 | 1385 | 1342 | 1904 | 1651 | 1163 | 1182 |
| unknown | 1191 | 1457 | 1299 | 1337 | 2056 | 1573 | 1150 | 1166 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (589 vessels) | seen_vessels (620 vessels) |
|---|---|---|
| B_vessel - A_motion | -21 (-28 to -13) | -26 (-69 to +25) |
| C_location - A_motion | +1366 (+1295 to +1443) | +957 (+849 to +1085) |
| D_all - A_motion | +572 (+545 to +603) | +424 (+359 to +492) |
| E_fairway - A_motion | -409 (-432 to -386) | -473 (-529 to -421) |
| F_all_fairway - A_motion | -423 (-448 to -398) | -466 (-532 to -400) |
| A_motion - cv | +3 (-11 to +15) | -125 (-201 to -57) |
