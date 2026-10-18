# Residual GBM context ablation (transfer_val, skagen; 238,829 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 361 (304–441) | 877 (740–1070) | 98 | 290 |
| A_motion | 350 (302–417) | 856 (747–1004) | 92 | 278 |
| B_vessel | 342 (298–404) | 833 (735–963) | 91 | 274 |
| C_location | 506 (455–572) | 1335 (1212–1488) | 104 | 362 |
| D_all | 446 (399–509) | 1197 (1091–1332) | 113 | 312 |
| E_fairway | 318 (273–383) | 766 (658–919) | 87 | 258 |
| F_all_fairway | 316 (273–376) | 757 (662–894) | 87 | 257 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -11 (-25 to -0) | -21 (-69 to +13) |
| B_vessel - cv | -18 (-38 to -5) | -43 (-108 to +2) |
| C_location - cv | +146 (+126 to +166) | +459 (+397 to +522) |
| D_all - cv | +85 (+63 to +103) | +320 (+248 to +384) |
| E_fairway - cv | -43 (-58 to -30) | -111 (-153 to -77) |
| F_all_fairway - cv | -45 (-66 to -29) | -119 (-178 to -74) |
| B_vessel - A_motion | -8 (-13 to -4) | -22 (-42 to -8) |
| C_location - A_motion | +156 (+141 to +172) | +479 (+434 to +527) |
| D_all - A_motion | +95 (+85 to +107) | +341 (+303 to +383) |
| E_fairway - A_motion | -32 (-40 to -25) | -90 (-114 to -69) |
| F_all_fairway - A_motion | -35 (-45 to -26) | -99 (-124 to -77) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 44069 | 530 | 543 | 551 | 1196 | 1037 | 496 | 507 |
| 0.5–1 | 7616 | 985 | 974 | 942 | 1291 | 1164 | 830 | 819 |
| 1–2 | 5269 | 1338 | 1263 | 1199 | 1485 | 1359 | 1080 | 1043 |
| 2–5 | 4768 | 1858 | 1704 | 1597 | 1802 | 1699 | 1500 | 1452 |
| 5–10 | 2717 | 2138 | 1925 | 1802 | 1924 | 1845 | 1701 | 1650 |
| 10–inf | 3370 | 2041 | 1979 | 1846 | 1885 | 1879 | 1856 | 1735 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 27758 | 606 | 624 | 620 | 1335 | 1169 | 534 | 544 |
| other | 19110 | 680 | 702 | 693 | 832 | 774 | 664 | 649 |
| tanker | 11861 | 779 | 770 | 777 | 1454 | 1298 | 691 | 722 |
| service | 5510 | 2757 | 2318 | 2085 | 2494 | 2229 | 2259 | 2034 |
| passenger | 2910 | 1616 | 1681 | 1676 | 1976 | 1879 | 1148 | 1251 |
| unknown | 660 | 739 | 751 | 727 | 1298 | 1207 | 646 | 630 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (511 vessels) | seen_vessels (286 vessels) |
|---|---|---|
| B_vessel - A_motion | -31 (-56 to -12) | +0 (-6 to +7) |
| C_location - A_motion | +398 (+348 to +457) | +693 (+642 to +749) |
| D_all - A_motion | +273 (+229 to +321) | +520 (+482 to +559) |
| E_fairway - A_motion | -92 (-125 to -63) | -86 (-100 to -72) |
| F_all_fairway - A_motion | -110 (-145 to -79) | -70 (-86 to -54) |
| A_motion - cv | -32 (-97 to +14) | +10 (+0 to +19) |
