# Residual GBM context ablation (transfer_val, bornholm; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 243 (199–297) | 583 (491–695) | 69 | 197 |
| A_motion | 236 (198–283) | 584 (505–681) | 64 | 184 |
| B_vessel | 240 (202–289) | 595 (515–695) | 64 | 187 |
| C_location | 859 (799–925) | 1778 (1653–1910) | 239 | 789 |
| D_all | 808 (755–861) | 1983 (1856–2106) | 211 | 654 |
| E_fairway | 204 (169–251) | 474 (403–567) | 62 | 171 |
| F_all_fairway | 208 (173–256) | 485 (414–579) | 62 | 174 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -7 (-15 to -0) | +1 (-21 to +19) |
| B_vessel - cv | -3 (-11 to +4) | +12 (-12 to +33) |
| C_location - cv | +616 (+560 to +668) | +1195 (+1080 to +1306) |
| D_all - cv | +566 (+516 to +610) | +1401 (+1276 to +1518) |
| E_fairway - cv | -38 (-50 to -29) | -109 (-140 to -84) |
| F_all_fairway - cv | -35 (-46 to -25) | -98 (-128 to -71) |
| B_vessel - A_motion | +4 (-1 to +9) | +11 (-6 to +27) |
| C_location - A_motion | +623 (+570 to +673) | +1194 (+1089 to +1297) |
| D_all - A_motion | +573 (+527 to +615) | +1400 (+1284 to +1506) |
| E_fairway - A_motion | -31 (-40 to -24) | -110 (-138 to -89) |
| F_all_fairway - A_motion | -27 (-37 to -20) | -99 (-127 to -77) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 33364 | 427 | 449 | 465 | 1738 | 1969 | 356 | 369 |
| 0.5–1 | 2421 | 948 | 943 | 969 | 1966 | 2055 | 762 | 786 |
| 1–2 | 2186 | 972 | 950 | 937 | 1932 | 2047 | 767 | 766 |
| 2–5 | 2038 | 1013 | 1013 | 962 | 1953 | 2215 | 824 | 815 |
| 5–10 | 579 | 1966 | 1776 | 1697 | 2022 | 1904 | 1615 | 1564 |
| 10–inf | 1087 | 2226 | 1745 | 1781 | 1819 | 1760 | 1611 | 1627 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 26759 | 394 | 409 | 417 | 1628 | 1881 | 311 | 318 |
| tanker | 6865 | 449 | 472 | 488 | 1804 | 2311 | 369 | 392 |
| passenger | 3445 | 1595 | 1566 | 1578 | 3189 | 2517 | 1233 | 1278 |
| other | 2867 | 781 | 782 | 826 | 1209 | 1305 | 774 | 781 |
| service | 1487 | 1865 | 1570 | 1543 | 2184 | 2356 | 1550 | 1503 |
| unknown | 252 | 670 | 677 | 660 | 1752 | 2158 | 578 | 585 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (418 vessels) | seen_vessels (334 vessels) |
|---|---|---|
| B_vessel - A_motion | +9 (-22 to +33) | +14 (+2 to +30) |
| C_location - A_motion | +1267 (+1115 to +1424) | +1101 (+971 to +1221) |
| D_all - A_motion | +1452 (+1278 to +1622) | +1333 (+1181 to +1477) |
| E_fairway - A_motion | -130 (-177 to -100) | -83 (-104 to -61) |
| F_all_fairway - A_motion | -117 (-167 to -85) | -75 (-97 to -52) |
| A_motion - cv | -3 (-33 to +24) | +5 (-23 to +22) |
