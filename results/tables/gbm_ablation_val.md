# Residual GBM context ablation (val)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 640 (581–703) | 1574 (1431–1722) | 160 | 510 |
| A_motion | 530 (493–569) | 1273 (1190–1358) | 137 | 432 |
| B_vessel | 481 (449–514) | 1131 (1066–1200) | 131 | 399 |
| C_location | 391 (360–426) | 864 (797–934) | 123 | 347 |
| D_all | 378 (349–410) | 827 (767–887) | 120 | 338 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -110 (-147 to -78) | -301 (-407 to -207) |
| B_vessel - cv | -159 (-204 to -117) | -443 (-571 to -320) |
| C_location - cv | -249 (-292 to -208) | -711 (-830 to -597) |
| D_all - cv | -262 (-307 to -220) | -747 (-869 to -630) |
| B_vessel - A_motion | -49 (-61 to -37) | -142 (-175 to -106) |
| C_location - A_motion | -139 (-152 to -125) | -409 (-446 to -370) |
| D_all - A_motion | -153 (-168 to -137) | -446 (-486 to -402) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| 0–0.5 | 30502 | 1145 | 1051 | 981 | 660 | 648 |
| 0.5–1 | 6718 | 1610 | 1350 | 1184 | 882 | 837 |
| 1–2 | 6969 | 1772 | 1437 | 1244 | 991 | 919 |
| 2–5 | 9347 | 1785 | 1404 | 1209 | 932 | 872 |
| 5–10 | 3704 | 2362 | 1607 | 1303 | 1209 | 1134 |
| 10–inf | 5742 | 2720 | 1730 | 1491 | 1434 | 1385 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|
| cargo | 23914 | 984 | 953 | 927 | 583 | 573 |
| passenger | 15356 | 2573 | 1660 | 1271 | 999 | 944 |
| tanker | 8515 | 1233 | 1159 | 1135 | 690 | 680 |
| service | 8302 | 2032 | 1708 | 1499 | 1486 | 1346 |
| other | 6543 | 1285 | 1148 | 1092 | 1017 | 1022 |
| unknown | 352 | 937 | 897 | 843 | 641 | 635 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (244 vessels) | seen_vessels (448 vessels) |
|---|---|---|
| B_vessel - A_motion | -25 (-35 to -15) | -189 (-232 to -141) |
| C_location - A_motion | -391 (-428 to -352) | -417 (-463 to -364) |
| D_all - A_motion | -394 (-434 to -354) | -467 (-518 to -407) |
| A_motion - cv | -66 (-102 to -40) | -396 (-538 to -268) |
