# Results by past-only manoeuvring regime (transfer_test_skagen)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261021T214105Z_gbm_transfer_test_skagen`, `20261021T215122Z_gbm_transfer_test_skagen_vesselheldout`, `20261021T205202Z_baselines_transfer_test_skagen`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 24,649 | 25.3% | 365 | n/a | 1677 | 599 | 776 | 606 | 598 | 670 | 644 | 674 | 652 | 678 | 635 |
| steady | 57,477 | 59.0% | 983 | 97% | 6365 | 616 | 796 | 618 | 615 | 637 | 637 | 1395 | 1208 | 552 | 565 |
| turning | 9,508 | 9.8% | 949 | 76% | 5766 | 1760 | 2818 | 1741 | 1760 | 1646 | 1546 | 1876 | 1722 | 1329 | 1293 |
| speed_changing | 1,477 | 1.5% | 370 | 81% | 4963 | 2095 | 2276 | 2095 | 2095 | 1910 | 1858 | 2106 | 1971 | 1655 | 1657 |
| combined | 4,285 | 4.4% | 423 | 83% | 4389 | 2887 | 3640 | 2895 | 2887 | 2483 | 2368 | 2530 | 2424 | 2213 | 2141 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | +71 (+45 to +102) | -25 (-50 to -5) | +4 (-23 to +25) | -17 (-41 to +3) | +9 (-15 to +32) | -34 (-61 to -13) |
| steady | +21 (+7 to +33) | +0 (-15 to +16) | +758 (+721 to +794) | +571 (+542 to +599) | -85 (-104 to -69) | -72 (-94 to -53) |
| turning | -114 (-233 to -29) | -100 (-177 to -47) | +230 (+192 to +275) | +76 (+9 to +128) | -317 (-370 to -275) | -353 (-418 to -291) |
| speed_changing | -185 (-291 to -85) | -52 (-129 to +38) | +196 (+89 to +349) | +61 (-28 to +154) | -255 (-370 to -148) | -253 (-369 to -146) |
| combined | -403 (-651 to -138) | -115 (-185 to -48) | +47 (-42 to +135) | -59 (-143 to +20) | -271 (-398 to -176) | -342 (-454 to -256) |

## Vessel-held-out training (all transfer_test_skagen vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | +77 (+51 to +110) | -15 (-49 to +16) | +47 (+12 to +73) | -45 (-68 to -27) | +16 (-11 to +42) | -40 (-68 to -17) |
| steady | +29 (+11 to +45) | -2 (-18 to +15) | +814 (+775 to +850) | +340 (+320 to +361) | -95 (-115 to -78) | -84 (-104 to -67) |
| turning | -82 (-234 to +23) | -131 (-187 to -86) | +208 (+172 to +253) | +19 (-29 to +62) | -359 (-418 to -308) | -375 (-424 to -327) |
| speed_changing | -188 (-310 to -72) | -64 (-147 to +38) | +250 (+108 to +434) | +60 (-2 to +127) | -255 (-362 to -159) | -238 (-351 to -134) |
| combined | -407 (-656 to -128) | -124 (-209 to -43) | +64 (-22 to +165) | -32 (-92 to +31) | -276 (-402 to -184) | -327 (-445 to -243) |

## Threshold sensitivity (`regime_sensitivity_transfer_test_skagen.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning), 50 regime×config cells. Cells where the 95% CI lies entirely below 0 (first model better) / entirely above 0 (first model worse):

| comparison | CI below 0 | CI above 0 |
|---|---|---|
| A_motion − cv | 29 | 18 |
| B_vessel − A_motion | 31 | 0 |
| C_location − A_motion | 0 | 31 |
| D_all − A_motion | 3 | 20 |
| E_fairway − A_motion | 40 | 1 |
| F_all_fairway − A_motion | 48 | 0 |

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=24,649, C−A +4, E−A +9 | n=57,477, C−A +758, E−A -85 | n=9,508, C−A +230, E−A -317 | n=1,477, C−A +196, E−A -255 | n=4,285, C−A +47, E−A -271 |
| turn_deg_min=0.5 | n=24,649, C−A +4, E−A +9 | n=50,385, C−A +798, E−A -69 | n=16,600, C−A +336, E−A -267 | n=977, C−A +211, E−A -232 | n=4,785, C−A +60, E−A -274 |
| turn_deg_min=2 | n=24,649, C−A +4, E−A +9 | n=62,075, C−A +728, E−A -101 | n=4,910, C−A +117, E−A -343 | n=2,183, C−A +189, E−A -296 | n=3,579, C−A +22, E−A -249 |
| speed_change_kn=1 | n=24,649, C−A +4, E−A +9 | n=55,619, C−A +776, E−A -78 | n=7,814, C−A +269, E−A -302 | n=3,335, C−A +207, E−A -285 | n=5,979, C−A +48, E−A -303 |
| speed_change_kn=3 | n=24,649, C−A +4, E−A +9 | n=58,119, C−A +752, E−A -87 | n=10,271, C−A +218, E−A -318 | n=835, C−A +207, E−A -288 | n=3,522, C−A +43, E−A -258 |
| low_speed_kn=3 | n=18,685, C−A +17, E−A +37 | n=60,404, C−A +724, E−A -81 | n=10,707, C−A +199, E−A -291 | n=1,733, C−A +153, E−A -240 | n=5,867, C−A -11, E−A -255 |
| low_speed_kn=7 | n=33,265, C−A +16, E−A -18 | n=51,917, C−A +828, E−A -92 | n=8,228, C−A +268, E−A -331 | n=1,145, C−A +245, E−A -279 | n=2,841, C−A +131, E−A -292 |
| lookback_min=5 | n=24,695, C−A +10, E−A +23 | n=57,450, C−A +744, E−A -91 | n=11,918, C−A +258, E−A -309 | n=700, C−A +146, E−A -402 | n=2,633, C−A +73, E−A -246 |
| lookback_min=15 | n=24,591, C−A +4, E−A -7 | n=56,733, C−A +769, E−A -86 | n=8,455, C−A +231, E−A -293 | n=2,202, C−A +203, E−A -269 | n=5,415, C−A +47, E−A -213 |
| sustained turning (>=70% same sign) | n=24,649, C−A +4, E−A +9 | n=61,953, C−A +720, E−A -102 | n=5,032, C−A +227, E−A -315 | n=3,912, C−A +114, E−A -254 | n=1,850, C−A +23, E−A -294 |
