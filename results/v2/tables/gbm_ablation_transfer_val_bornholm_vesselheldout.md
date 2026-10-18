# Residual GBM context ablation (transfer_val, bornholm, vessel-held-out; 201,330 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 243 (199–297) | 583 (491–695) | 69 | 197 |
| A_motion | 238 (200–286) | 589 (511–687) | 64 | 186 |
| B_vessel | 243 (205–292) | 604 (525–698) | 65 | 190 |
| C_location | 782 (726–846) | 1945 (1809–2094) | 197 | 642 |
| D_all | 733 (684–787) | 1631 (1525–1746) | 194 | 542 |
| E_fairway | 205 (170–252) | 476 (405–571) | 62 | 172 |
| F_all_fairway | 210 (174–257) | 489 (418–582) | 63 | 174 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -5 (-13 to +2) | +7 (-16 to +26) |
| B_vessel - cv | +0 (-9 to +8) | +21 (-4 to +44) |
| C_location - cv | +539 (+487 to +588) | +1362 (+1230 to +1485) |
| D_all - cv | +491 (+448 to +531) | +1049 (+952 to +1138) |
| E_fairway - cv | -38 (-49 to -28) | -107 (-138 to -81) |
| F_all_fairway - cv | -33 (-45 to -23) | -94 (-127 to -66) |
| B_vessel - A_motion | +5 (+0 to +10) | +15 (+0 to +30) |
| C_location - A_motion | +544 (+495 to +590) | +1355 (+1232 to +1475) |
| D_all - A_motion | +495 (+456 to +533) | +1042 (+959 to +1123) |
| E_fairway - A_motion | -33 (-42 to -26) | -113 (-139 to -93) |
| F_all_fairway - A_motion | -28 (-38 to -21) | -100 (-129 to -77) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 33364 | 427 | 454 | 477 | 1922 | 1587 | 357 | 372 |
| 0.5–1 | 2421 | 948 | 959 | 969 | 2137 | 1825 | 766 | 785 |
| 1–2 | 2186 | 972 | 960 | 940 | 2033 | 1769 | 769 | 771 |
| 2–5 | 2038 | 1013 | 1011 | 952 | 1998 | 1810 | 829 | 824 |
| 5–10 | 579 | 1966 | 1788 | 1685 | 2122 | 1899 | 1620 | 1581 |
| 10–inf | 1087 | 2226 | 1747 | 1783 | 1824 | 1795 | 1620 | 1664 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 26759 | 394 | 416 | 426 | 1794 | 1474 | 312 | 322 |
| tanker | 6865 | 449 | 478 | 493 | 1942 | 1732 | 371 | 395 |
| passenger | 3445 | 1595 | 1558 | 1598 | 3480 | 2742 | 1246 | 1265 |
| other | 2867 | 781 | 796 | 846 | 1280 | 1226 | 770 | 800 |
| service | 1487 | 1865 | 1565 | 1542 | 2369 | 2189 | 1544 | 1513 |
| unknown | 252 | 670 | 690 | 669 | 2025 | 1714 | 597 | 602 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (752 vessels) |
|---|---|
| B_vessel - A_motion | +15 (+0 to +30) |
| C_location - A_motion | +1355 (+1232 to +1475) |
| D_all - A_motion | +1042 (+959 to +1123) |
| E_fairway - A_motion | -113 (-139 to -93) |
| F_all_fairway - A_motion | -100 (-129 to -77) |
| A_motion - cv | +7 (-16 to +26) |
