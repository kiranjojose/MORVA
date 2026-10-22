# Residual GBM context ablation (test, vessel-held-out; 86,113 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 634 (576–691) | 1566 (1425–1706) | 158 | 502 |
| A_motion | 597 (544–647) | 1462 (1340–1585) | 149 | 476 |
| B_vessel | 585 (536–634) | 1419 (1305–1533) | 148 | 473 |
| C_location | 515 (461–566) | 1205 (1077–1328) | 143 | 431 |
| D_all | 509 (456–560) | 1186 (1061–1306) | 142 | 429 |
| E_fairway | 421 (375–462) | 1010 (898–1111) | 117 | 340 |
| F_all_fairway | 417 (371–458) | 1003 (893–1106) | 116 | 336 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -37 (-49 to -25) | -103 (-139 to -68) |
| B_vessel - cv | -48 (-62 to -34) | -146 (-189 to -105) |
| C_location - cv | -119 (-136 to -103) | -361 (-414 to -314) |
| D_all - cv | -124 (-138 to -111) | -380 (-419 to -342) |
| E_fairway - cv | -213 (-233 to -195) | -556 (-606 to -513) |
| F_all_fairway - cv | -217 (-235 to -199) | -563 (-609 to -519) |
| B_vessel - A_motion | -11 (-15 to -8) | -43 (-55 to -31) |
| C_location - A_motion | -82 (-90 to -74) | -258 (-284 to -234) |
| D_all - A_motion | -87 (-94 to -80) | -277 (-298 to -257) |
| E_fairway - A_motion | -176 (-188 to -165) | -453 (-476 to -427) |
| F_all_fairway - A_motion | -180 (-194 to -168) | -459 (-488 to -431) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 80479 | 1166 | 1142 | 1126 | 848 | 844 | 703 | 712 |
| 0.5–1 | 18387 | 1563 | 1462 | 1416 | 1178 | 1150 | 983 | 967 |
| 1–2 | 18793 | 1736 | 1591 | 1534 | 1320 | 1279 | 1085 | 1064 |
| 2–5 | 25608 | 1775 | 1629 | 1561 | 1332 | 1308 | 1072 | 1059 |
| 5–10 | 10000 | 2402 | 2137 | 2024 | 2033 | 1980 | 1691 | 1660 |
| 10–inf | 14266 | 2643 | 2327 | 2253 | 2288 | 2257 | 2086 | 2052 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 68935 | 994 | 947 | 935 | 596 | 591 | 508 | 504 |
| passenger | 40449 | 2603 | 2444 | 2340 | 2280 | 2249 | 1834 | 1833 |
| tanker | 22913 | 1160 | 1089 | 1080 | 606 | 608 | 527 | 526 |
| service | 22116 | 1981 | 1763 | 1669 | 1748 | 1661 | 1500 | 1461 |
| other | 11929 | 1374 | 1292 | 1296 | 1219 | 1238 | 1124 | 1132 |
| unknown | 1191 | 1457 | 1307 | 1298 | 1214 | 1195 | 1113 | 1113 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (1209 vessels) |
|---|---|
| B_vessel - A_motion | -43 (-55 to -31) |
| C_location - A_motion | -258 (-284 to -234) |
| D_all - A_motion | -277 (-298 to -257) |
| E_fairway - A_motion | -453 (-476 to -427) |
| F_all_fairway - A_motion | -459 (-488 to -431) |
| A_motion - cv | -103 (-139 to -68) |
