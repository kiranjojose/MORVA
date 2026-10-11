# Residual GBM context ablation (test, vessel-held-out; 116,213 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 627 (565–684) | 1554 (1400–1694) | 155 | 496 |
| A_motion | 583 (528–635) | 1429 (1299–1552) | 144 | 465 |
| B_vessel | 566 (514–614) | 1367 (1250–1478) | 143 | 461 |
| C_location | 498 (440–552) | 1165 (1027–1294) | 137 | 418 |
| D_all | 492 (435–545) | 1140 (1009–1261) | 137 | 419 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -44 (-54 to -34) | -124 (-154 to -92) |
| B_vessel - cv | -61 (-75 to -48) | -187 (-230 to -143) |
| C_location - cv | -130 (-145 to -115) | -389 (-432 to -344) |
| D_all - cv | -136 (-150 to -122) | -414 (-456 to -371) |
| B_vessel - A_motion | -17 (-24 to -11) | -62 (-84 to -41) |
| C_location - A_motion | -86 (-97 to -75) | -264 (-297 to -233) |
| D_all - A_motion | -91 (-102 to -82) | -289 (-320 to -259) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 27301 | 1134 | 1105 | 1076 | 795 | 789 |
| 0.5–1 | 6387 | 1563 | 1451 | 1369 | 1154 | 1107 |
| 1–2 | 6423 | 1694 | 1531 | 1431 | 1237 | 1200 |
| 2–5 | 8553 | 1816 | 1626 | 1533 | 1322 | 1287 |
| 5–10 | 3333 | 2470 | 2116 | 2007 | 2049 | 1985 |
| 10–inf | 5071 | 2584 | 2236 | 2151 | 2238 | 2193 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 22586 | 981 | 931 | 916 | 567 | 568 |
| passenger | 13539 | 2648 | 2410 | 2236 | 2229 | 2173 |
| tanker | 7859 | 1196 | 1124 | 1116 | 639 | 635 |
| service | 7500 | 1869 | 1655 | 1534 | 1662 | 1556 |
| other | 4926 | 1344 | 1234 | 1250 | 1150 | 1171 |
| unknown | 658 | 960 | 905 | 935 | 545 | 586 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (622 vessels) |
|---|---|
| B_vessel - A_motion | -62 (-84 to -41) |
| C_location - A_motion | -264 (-297 to -233) |
| D_all - A_motion | -289 (-320 to -259) |
| A_motion - cv | -124 (-154 to -92) |
