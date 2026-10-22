# Residual GBM context ablation (transfer_test, skagen, vessel-held-out; 198,364 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 348 (297–417) | 846 (720–1009) | 96 | 280 |
| A_motion | 346 (302–404) | 853 (754–983) | 90 | 272 |
| B_vessel | 338 (297–392) | 829 (739–943) | 90 | 270 |
| C_location | 536 (489–597) | 1372 (1264–1509) | 106 | 410 |
| D_all | 440 (397–494) | 1044 (946–1163) | 101 | 367 |
| E_fairway | 311 (271–367) | 750 (655–879) | 85 | 252 |
| F_all_fairway | 308 (269–360) | 739 (651–858) | 85 | 250 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -2 (-15 to +7) | +8 (-38 to +40) |
| B_vessel - cv | -10 (-26 to +2) | -16 (-74 to +26) |
| C_location - cv | +188 (+166 to +211) | +527 (+467 to +589) |
| D_all - cv | +91 (+73 to +107) | +198 (+140 to +245) |
| E_fairway - cv | -37 (-53 to -26) | -95 (-139 to -63) |
| F_all_fairway - cv | -41 (-60 to -26) | -106 (-162 to -66) |
| B_vessel - A_motion | -8 (-13 to -4) | -24 (-41 to -10) |
| C_location - A_motion | +190 (+172 to +211) | +519 (+474 to +570) |
| D_all - A_motion | +94 (+83 to +105) | +190 (+164 to +219) |
| E_fairway - A_motion | -35 (-45 to -28) | -103 (-132 to -81) |
| F_all_fairway - A_motion | -38 (-49 to -30) | -114 (-143 to -94) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 62747 | 526 | 556 | 568 | 1272 | 847 | 499 | 503 |
| 0.5–1 | 11065 | 910 | 938 | 909 | 1293 | 1045 | 788 | 773 |
| 1–2 | 7994 | 1281 | 1246 | 1168 | 1482 | 1294 | 1033 | 1004 |
| 2–5 | 7179 | 1685 | 1611 | 1481 | 1669 | 1552 | 1376 | 1331 |
| 5–10 | 3641 | 2150 | 1970 | 1826 | 1938 | 1887 | 1727 | 1685 |
| 10–inf | 4770 | 1917 | 1924 | 1768 | 1815 | 1798 | 1811 | 1709 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 38017 | 603 | 654 | 631 | 1456 | 986 | 533 | 543 |
| other | 30810 | 601 | 646 | 644 | 812 | 668 | 618 | 591 |
| tanker | 15938 | 771 | 776 | 785 | 1550 | 1133 | 691 | 714 |
| service | 7519 | 2615 | 2233 | 2043 | 2414 | 2167 | 2170 | 1987 |
| passenger | 4734 | 1781 | 1844 | 1818 | 2090 | 1842 | 1262 | 1352 |
| unknown | 378 | 1378 | 1216 | 1113 | 1542 | 1379 | 1164 | 1085 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (1011 vessels) |
|---|---|
| B_vessel - A_motion | -24 (-41 to -10) |
| C_location - A_motion | +519 (+474 to +570) |
| D_all - A_motion | +190 (+164 to +219) |
| E_fairway - A_motion | -103 (-132 to -81) |
| F_all_fairway - A_motion | -114 (-143 to -94) |
| A_motion - cv | +8 (-38 to +40) |
