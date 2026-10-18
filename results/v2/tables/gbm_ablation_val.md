# Residual GBM context ablation (val; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 633 (577–693) | 1563 (1424–1714) | 157 | 503 |
| A_motion | 528 (496–564) | 1271 (1200–1347) | 136 | 430 |
| B_vessel | 479 (452–509) | 1127 (1066–1192) | 130 | 397 |
| C_location | 390 (363–418) | 861 (804–920) | 122 | 343 |
| D_all | 379 (354–405) | 835 (783–889) | 119 | 335 |
| E_fairway | 344 (317–373) | 795 (734–859) | 103 | 289 |
| F_all_fairway | 333 (308–360) | 757 (703–813) | 102 | 282 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -106 (-139 to -75) | -292 (-389 to -205) |
| B_vessel - cv | -154 (-196 to -112) | -436 (-557 to -315) |
| C_location - cv | -243 (-285 to -201) | -702 (-817 to -589) |
| D_all - cv | -254 (-299 to -211) | -728 (-853 to -609) |
| E_fairway - cv | -289 (-331 to -248) | -768 (-879 to -658) |
| F_all_fairway - cv | -300 (-344 to -258) | -806 (-923 to -694) |
| B_vessel - A_motion | -48 (-61 to -36) | -144 (-179 to -108) |
| C_location - A_motion | -138 (-151 to -124) | -409 (-445 to -374) |
| D_all - A_motion | -149 (-164 to -134) | -436 (-477 to -396) |
| E_fairway - A_motion | -183 (-197 to -169) | -476 (-509 to -444) |
| F_all_fairway - A_motion | -195 (-210 to -180) | -514 (-551 to -478) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 58022 | 1138 | 1042 | 973 | 651 | 646 | 585 | 569 |
| 0.5–1 | 13155 | 1586 | 1336 | 1177 | 882 | 848 | 782 | 742 |
| 1–2 | 13434 | 1735 | 1414 | 1223 | 974 | 915 | 866 | 815 |
| 2–5 | 17939 | 1799 | 1423 | 1213 | 942 | 898 | 856 | 810 |
| 5–10 | 7047 | 2411 | 1646 | 1334 | 1253 | 1176 | 1209 | 1123 |
| 10–inf | 10815 | 2656 | 1741 | 1495 | 1435 | 1404 | 1476 | 1379 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 46684 | 982 | 949 | 923 | 586 | 584 | 499 | 491 |
| passenger | 28963 | 2606 | 1710 | 1292 | 1043 | 993 | 1016 | 950 |
| tanker | 16413 | 1215 | 1149 | 1128 | 689 | 683 | 589 | 576 |
| service | 15854 | 1951 | 1629 | 1427 | 1396 | 1276 | 1343 | 1233 |
| other | 11488 | 1309 | 1183 | 1140 | 1054 | 1076 | 1001 | 971 |
| unknown | 1010 | 952 | 919 | 922 | 597 | 682 | 506 | 532 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (436 vessels) | seen_vessels (612 vessels) |
|---|---|---|
| B_vessel - A_motion | -22 (-30 to -14) | -192 (-236 to -145) |
| C_location - A_motion | -388 (-413 to -361) | -418 (-469 to -371) |
| D_all - A_motion | -379 (-408 to -350) | -458 (-514 to -405) |
| E_fairway - A_motion | -466 (-496 to -435) | -480 (-529 to -435) |
| F_all_fairway - A_motion | -476 (-505 to -445) | -529 (-580 to -478) |
| A_motion - cv | -60 (-81 to -43) | -384 (-515 to -264) |
