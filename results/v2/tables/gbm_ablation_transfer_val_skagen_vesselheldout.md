# Residual GBM context ablation (transfer_val, skagen, vessel-held-out; 201,404 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 361 (304–441) | 877 (740–1070) | 98 | 290 |
| A_motion | 351 (304–417) | 860 (754–1006) | 92 | 278 |
| B_vessel | 343 (298–405) | 837 (736–967) | 91 | 275 |
| C_location | 517 (466–582) | 1292 (1172–1447) | 109 | 402 |
| D_all | 479 (433–539) | 1184 (1082–1316) | 112 | 394 |
| E_fairway | 318 (273–382) | 765 (659–916) | 87 | 258 |
| F_all_fairway | 317 (274–378) | 759 (663–897) | 87 | 256 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -10 (-25 to +1) | -17 (-68 to +20) |
| B_vessel - cv | -17 (-37 to -3) | -40 (-105 to +7) |
| C_location - cv | +156 (+136 to +178) | +416 (+360 to +472) |
| D_all - cv | +119 (+95 to +140) | +307 (+233 to +369) |
| E_fairway - cv | -43 (-59 to -30) | -112 (-156 to -76) |
| F_all_fairway - cv | -44 (-64 to -29) | -117 (-175 to -72) |
| B_vessel - A_motion | -8 (-13 to -3) | -23 (-40 to -5) |
| C_location - A_motion | +166 (+150 to +182) | +433 (+392 to +475) |
| D_all - A_motion | +128 (+115 to +143) | +324 (+288 to +363) |
| E_fairway - A_motion | -33 (-42 to -27) | -95 (-118 to -74) |
| F_all_fairway - A_motion | -34 (-44 to -27) | -100 (-125 to -80) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 44069 | 530 | 545 | 558 | 1133 | 1019 | 496 | 507 |
| 0.5–1 | 7616 | 985 | 977 | 938 | 1270 | 1167 | 829 | 821 |
| 1–2 | 5269 | 1338 | 1272 | 1192 | 1482 | 1354 | 1072 | 1051 |
| 2–5 | 4768 | 1858 | 1710 | 1601 | 1821 | 1696 | 1492 | 1458 |
| 5–10 | 2717 | 2138 | 1939 | 1797 | 1926 | 1838 | 1710 | 1654 |
| 10–inf | 3370 | 2041 | 1990 | 1837 | 1877 | 1868 | 1860 | 1758 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 27758 | 606 | 636 | 621 | 1260 | 1147 | 535 | 549 |
| other | 19110 | 680 | 707 | 686 | 845 | 777 | 663 | 649 |
| tanker | 11861 | 779 | 776 | 781 | 1356 | 1285 | 692 | 725 |
| service | 5510 | 2757 | 2285 | 2088 | 2513 | 2228 | 2242 | 2041 |
| passenger | 2910 | 1616 | 1671 | 1760 | 1988 | 1830 | 1146 | 1237 |
| unknown | 660 | 739 | 752 | 732 | 1203 | 1135 | 645 | 626 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (797 vessels) |
|---|---|
| B_vessel - A_motion | -23 (-40 to -5) |
| C_location - A_motion | +433 (+392 to +475) |
| D_all - A_motion | +324 (+288 to +363) |
| E_fairway - A_motion | -95 (-118 to -74) |
| F_all_fairway - A_motion | -100 (-125 to -80) |
| A_motion - cv | -17 (-68 to +20) |
