# Residual GBM context ablation (transfer_test, skagen; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 348 (297–417) | 846 (720–1009) | 96 | 280 |
| A_motion | 344 (299–402) | 844 (741–978) | 90 | 271 |
| B_vessel | 336 (295–391) | 822 (731–939) | 89 | 268 |
| C_location | 500 (452–562) | 1320 (1205–1465) | 102 | 358 |
| D_all | 439 (395–495) | 1183 (1081–1307) | 112 | 308 |
| E_fairway | 311 (270–368) | 749 (653–883) | 85 | 252 |
| F_all_fairway | 308 (270–359) | 740 (654–856) | 85 | 250 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -5 (-16 to +3) | -1 (-41 to +28) |
| B_vessel - cv | -12 (-28 to -0) | -23 (-79 to +18) |
| C_location - cv | +152 (+134 to +171) | +475 (+419 to +531) |
| D_all - cv | +90 (+73 to +106) | +337 (+271 to +393) |
| E_fairway - cv | -37 (-52 to -26) | -96 (-137 to -65) |
| F_all_fairway - cv | -41 (-61 to -26) | -106 (-164 to -64) |
| B_vessel - A_motion | -7 (-13 to -3) | -22 (-40 to -7) |
| C_location - A_motion | +157 (+141 to +174) | +476 (+429 to +528) |
| D_all - A_motion | +95 (+84 to +107) | +339 (+298 to +381) |
| E_fairway - A_motion | -33 (-43 to -25) | -95 (-123 to -74) |
| F_all_fairway - A_motion | -36 (-48 to -27) | -105 (-135 to -82) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 62747 | 526 | 550 | 558 | 1205 | 1046 | 498 | 507 |
| 0.5–1 | 11065 | 910 | 925 | 903 | 1251 | 1125 | 788 | 776 |
| 1–2 | 7994 | 1281 | 1235 | 1167 | 1450 | 1321 | 1036 | 997 |
| 2–5 | 7179 | 1685 | 1580 | 1482 | 1651 | 1557 | 1375 | 1323 |
| 5–10 | 3641 | 2150 | 1949 | 1833 | 1949 | 1874 | 1731 | 1675 |
| 10–inf | 4770 | 1917 | 1919 | 1774 | 1808 | 1798 | 1796 | 1689 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 38017 | 603 | 634 | 627 | 1393 | 1211 | 532 | 543 |
| other | 30810 | 601 | 640 | 629 | 743 | 693 | 613 | 596 |
| tanker | 15938 | 771 | 770 | 778 | 1517 | 1345 | 690 | 717 |
| service | 7519 | 2615 | 2269 | 2047 | 2425 | 2179 | 2186 | 1963 |
| passenger | 4734 | 1781 | 1821 | 1830 | 2063 | 1998 | 1264 | 1352 |
| unknown | 378 | 1378 | 1204 | 1073 | 1533 | 1453 | 1194 | 1088 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (690 vessels) | seen_vessels (321 vessels) |
|---|---|---|
| B_vessel - A_motion | -26 (-47 to -7) | -8 (-16 to -2) |
| C_location - A_motion | +407 (+353 to +465) | +707 (+654 to +758) |
| D_all - A_motion | +282 (+239 to +331) | +529 (+491 to +565) |
| E_fairway - A_motion | -96 (-131 to -69) | -91 (-105 to -76) |
| F_all_fairway - A_motion | -113 (-148 to -82) | -77 (-92 to -61) |
| A_motion - cv | -9 (-53 to +28) | +24 (+12 to +36) |

FDE@20 min (m) across seeds [0, 1, 2]:

| model | mean | sd | min | max |
|---|---|---|---|---|
| A_motion | 844 | 0.9 | 843 | 844 |
| B_vessel | 824 | 1.0 | 822 | 824 |
| C_location | 1276 | 45.9 | 1229 | 1320 |
| D_all | 1075 | 93.7 | 1012 | 1183 |
| E_fairway | 750 | 0.8 | 749 | 751 |
| F_all_fairway | 739 | 2.1 | 737 | 741 |
