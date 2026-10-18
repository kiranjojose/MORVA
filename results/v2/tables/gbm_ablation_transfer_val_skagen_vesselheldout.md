# Residual GBM context ablation (transfer_val, skagen, vessel-held-out; 201,404 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 361 (304–441) | 877 (740–1070) | 98 | 290 |
| A_motion | 351 (304–417) | 860 (754–1006) | 92 | 278 |
| B_vessel | 343 (298–405) | 837 (736–967) | 91 | 275 |
| C_location | 517 (466–582) | 1292 (1172–1447) | 109 | 402 |
| D_all | 479 (433–539) | 1184 (1082–1316) | 112 | 394 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -10 (-25 to +1) | -17 (-68 to +20) |
| B_vessel - cv | -17 (-37 to -3) | -40 (-105 to +7) |
| C_location - cv | +156 (+136 to +178) | +416 (+360 to +472) |
| D_all - cv | +119 (+95 to +140) | +307 (+233 to +369) |
| B_vessel - A_motion | -8 (-13 to -3) | -23 (-40 to -5) |
| C_location - A_motion | +166 (+150 to +182) | +433 (+392 to +475) |
| D_all - A_motion | +128 (+115 to +143) | +324 (+288 to +363) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 44069 | 530 | 545 | 558 | 1133 | 1019 |
| 0.5–1 | 7616 | 985 | 977 | 938 | 1270 | 1167 |
| 1–2 | 5269 | 1338 | 1272 | 1192 | 1482 | 1354 |
| 2–5 | 4768 | 1858 | 1710 | 1601 | 1821 | 1696 |
| 5–10 | 2717 | 2138 | 1939 | 1797 | 1926 | 1838 |
| 10–inf | 3370 | 2041 | 1990 | 1837 | 1877 | 1868 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 27758 | 606 | 636 | 621 | 1260 | 1147 |
| other | 19110 | 680 | 707 | 686 | 845 | 777 |
| tanker | 11861 | 779 | 776 | 781 | 1356 | 1285 |
| service | 5510 | 2757 | 2285 | 2088 | 2513 | 2228 |
| passenger | 2910 | 1616 | 1671 | 1760 | 1988 | 1830 |
| unknown | 660 | 739 | 752 | 732 | 1203 | 1135 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (797 vessels) |
|---|---|
| B_vessel - A_motion | -23 (-40 to -5) |
| C_location - A_motion | +433 (+392 to +475) |
| D_all - A_motion | +324 (+288 to +363) |
| A_motion - cv | -17 (-68 to +20) |
