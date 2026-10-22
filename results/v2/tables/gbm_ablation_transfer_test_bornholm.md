# Residual GBM context ablation (transfer_test, bornholm; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 233 (203–271) | 569 (498–661) | 63 | 186 |
| A_motion | 231 (204–266) | 585 (521–671) | 59 | 178 |
| B_vessel | 235 (208–268) | 592 (528–670) | 59 | 180 |
| C_location | 874 (823–930) | 1816 (1704–1938) | 239 | 803 |
| D_all | 820 (782–862) | 2026 (1931–2124) | 211 | 661 |
| E_fairway | 194 (171–221) | 459 (407–520) | 56 | 160 |
| F_all_fairway | 198 (175–225) | 470 (418–533) | 56 | 163 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -1 (-7 to +4) | +16 (-1 to +30) |
| B_vessel - cv | +2 (-5 to +9) | +23 (+3 to +41) |
| C_location - cv | +642 (+595 to +687) | +1247 (+1148 to +1343) |
| D_all - cv | +588 (+551 to +625) | +1457 (+1361 to +1557) |
| E_fairway - cv | -38 (-51 to -29) | -110 (-144 to -86) |
| F_all_fairway - cv | -35 (-47 to -25) | -99 (-132 to -74) |
| B_vessel - A_motion | +4 (-1 to +8) | +6 (-8 to +21) |
| C_location - A_motion | +643 (+599 to +686) | +1231 (+1142 to +1320) |
| D_all - A_motion | +589 (+555 to +624) | +1441 (+1352 to +1536) |
| E_fairway - A_motion | -37 (-48 to -30) | -127 (-157 to -106) |
| F_all_fairway - A_motion | -33 (-44 to -26) | -115 (-147 to -92) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 44511 | 434 | 462 | 477 | 1779 | 2011 | 359 | 372 |
| 0.5–1 | 3682 | 876 | 889 | 892 | 1892 | 2020 | 669 | 683 |
| 1–2 | 2801 | 935 | 971 | 925 | 2046 | 2157 | 730 | 731 |
| 2–5 | 2726 | 847 | 898 | 852 | 1903 | 2192 | 684 | 681 |
| 5–10 | 656 | 2021 | 1826 | 1722 | 2127 | 2000 | 1609 | 1566 |
| 10–inf | 1185 | 2382 | 1944 | 1931 | 2062 | 1946 | 1756 | 1761 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 35398 | 404 | 426 | 430 | 1642 | 1885 | 321 | 328 |
| tanker | 10066 | 483 | 507 | 517 | 1943 | 2502 | 397 | 417 |
| passenger | 4764 | 1538 | 1555 | 1629 | 3372 | 2706 | 1183 | 1227 |
| other | 2694 | 1018 | 1063 | 1036 | 1568 | 1766 | 992 | 994 |
| service | 2516 | 929 | 796 | 742 | 1110 | 1150 | 709 | 689 |
| unknown | 123 | 309 | 323 | 329 | 1071 | 1126 | 309 | 330 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (545 vessels) | seen_vessels (359 vessels) |
|---|---|---|
| B_vessel - A_motion | +10 (-13 to +33) | +0 (-5 to +6) |
| C_location - A_motion | +1313 (+1176 to +1450) | +1103 (+985 to +1227) |
| D_all - A_motion | +1526 (+1394 to +1658) | +1309 (+1180 to +1455) |
| E_fairway - A_motion | -134 (-180 to -100) | -115 (-134 to -99) |
| F_all_fairway - A_motion | -123 (-172 to -87) | -104 (-121 to -89) |
| A_motion - cv | +8 (-20 to +31) | +29 (+23 to +34) |

FDE@20 min (m) across seeds [0, 1, 2]:

| model | mean | sd | min | max |
|---|---|---|---|---|
| A_motion | 585 | 0.8 | 584 | 585 |
| B_vessel | 591 | 0.9 | 590 | 592 |
| C_location | 1950 | 232.2 | 1816 | 2218 |
| D_all | 1881 | 139.3 | 1749 | 2026 |
| E_fairway | 460 | 1.4 | 459 | 461 |
| F_all_fairway | 470 | 2.4 | 468 | 473 |
