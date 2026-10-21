# Results by past-only manoeuvring regime (transfer_val_skagen)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261018T210357Z_gbm_transfer_val_skagen`, `20261018T211241Z_gbm_transfer_val_skagen_vesselheldout`, `20261018T201735Z_baselines_transfer_val_skagen`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 15,895 | 23.4% | 313 | n/a | 1717 | 670 | 864 | 678 | 669 | 728 | 695 | 737 | 716 | 728 | 690 |
| steady | 41,103 | 60.6% | 770 | 97% | 6255 | 604 | 763 | 605 | 604 | 614 | 617 | 1355 | 1172 | 537 | 551 |
| turning | 6,649 | 9.8% | 747 | 79% | 5716 | 1835 | 2868 | 1816 | 1835 | 1694 | 1589 | 1918 | 1761 | 1388 | 1349 |
| speed_changing | 1,114 | 1.6% | 302 | 79% | 4836 | 2184 | 2336 | 2183 | 2184 | 1942 | 1852 | 2108 | 1965 | 1735 | 1717 |
| combined | 3,048 | 4.5% | 349 | 86% | 4455 | 3057 | 3862 | 3069 | 3057 | 2561 | 2455 | 2630 | 2535 | 2331 | 2249 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | +58 (+25 to +91) | -32 (-56 to -12) | +9 (-17 to +30) | -12 (-36 to +9) | -0 (-23 to +21) | -37 (-63 to -15) |
| steady | +9 (-7 to +22) | +3 (-12 to +16) | +741 (+701 to +778) | +558 (+528 to +588) | -77 (-95 to -60) | -63 (-85 to -45) |
| turning | -140 (-265 to -35) | -106 (-167 to -53) | +223 (+180 to +277) | +67 (-2 to +128) | -306 (-357 to -256) | -346 (-400 to -296) |
| speed_changing | -242 (-367 to -117) | -90 (-160 to -20) | +166 (+95 to +250) | +23 (-58 to +112) | -207 (-313 to -100) | -225 (-332 to -121) |
| combined | -496 (-782 to -169) | -106 (-167 to -21) | +69 (-32 to +169) | -26 (-95 to +55) | -230 (-359 to -105) | -313 (-413 to -221) |

## Vessel-held-out training (all transfer_val_skagen vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | +62 (+28 to +96) | -42 (-65 to -22) | +12 (-18 to +36) | -6 (-35 to +21) | -2 (-24 to +17) | -36 (-60 to -14) |
| steady | +12 (-6 to +26) | +9 (-10 to +37) | +664 (+628 to +699) | +532 (+502 to +563) | -80 (-99 to -64) | -66 (-88 to -48) |
| turning | -122 (-265 to +1) | -126 (-168 to -87) | +205 (+152 to +266) | +34 (-25 to +91) | -330 (-383 to -277) | -357 (-402 to -312) |
| speed_changing | -252 (-397 to -109) | -77 (-143 to -4) | +150 (+36 to +246) | +59 (-28 to +151) | -203 (-326 to -77) | -224 (-347 to -107) |
| combined | -501 (-785 to -164) | -111 (-158 to -49) | +107 (-26 to +224) | -27 (-108 to +49) | -235 (-369 to -117) | -299 (-397 to -211) |

## Threshold sensitivity (`regime_sensitivity_transfer_val_skagen.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning), 50 regime×config cells. Cells where the 95% CI lies entirely below 0 (first model better) / entirely above 0 (first model worse):

| comparison | CI below 0 | CI above 0 |
|---|---|---|
| A_motion − cv | 30 | 11 |
| B_vessel − A_motion | 34 | 0 |
| C_location − A_motion | 0 | 31 |
| D_all − A_motion | 1 | 19 |
| E_fairway − A_motion | 40 | 1 |
| F_all_fairway − A_motion | 49 | 0 |

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=15,895, C−A +9, E−A -0 | n=41,103, C−A +741, E−A -77 | n=6,649, C−A +223, E−A -306 | n=1,114, C−A +166, E−A -207 | n=3,048, C−A +69, E−A -230 |
| turn_deg_min=0.5 | n=15,895, C−A +9, E−A -0 | n=36,107, C−A +781, E−A -59 | n=11,645, C−A +324, E−A -262 | n=734, C−A +216, E−A -200 | n=3,428, C−A +69, E−A -229 |
| turn_deg_min=2 | n=15,895, C−A +9, E−A -0 | n=44,200, C−A +713, E−A -90 | n=3,552, C−A +122, E−A -346 | n=1,584, C−A +179, E−A -222 | n=2,578, C−A +43, E−A -226 |
| speed_change_kn=1 | n=15,895, C−A +9, E−A -0 | n=39,660, C−A +759, E−A -70 | n=5,427, C−A +255, E−A -296 | n=2,557, C−A +219, E−A -231 | n=4,270, C−A +73, E−A -265 |
| speed_change_kn=3 | n=15,895, C−A +9, E−A -0 | n=41,636, C−A +734, E−A -78 | n=7,220, C−A +211, E−A -303 | n=581, C−A +151, E−A -224 | n=2,477, C−A +71, E−A -223 |
| low_speed_kn=3 | n=10,453, C−A +11, E−A +25 | n=44,237, C−A +693, E−A -71 | n=7,707, C−A +193, E−A -271 | n=1,282, C−A +142, E−A -183 | n=4,130, C−A +17, E−A -221 |
| low_speed_kn=7 | n=22,750, C−A +31, E−A -26 | n=36,390, C−A +820, E−A -83 | n=5,702, C−A +261, E−A -316 | n=856, C−A +213, E−A -218 | n=2,111, C−A +139, E−A -238 |
| lookback_min=5 | n=15,966, C−A +14, E−A +14 | n=41,245, C−A +728, E−A -81 | n=8,198, C−A +244, E−A -309 | n=487, C−A +63, E−A -377 | n=1,913, C−A +128, E−A -161 |
| lookback_min=15 | n=15,864, C−A +7, E−A -14 | n=40,364, C−A +755, E−A -74 | n=6,068, C−A +228, E−A -281 | n=1,625, C−A +220, E−A -193 | n=3,888, C−A +48, E−A -224 |
| sustained turning (>=70% same sign) | n=15,895, C−A +9, E−A -0 | n=44,209, C−A +707, E−A -92 | n=3,543, C−A +204, E−A -316 | n=2,805, C−A +122, E−A -204 | n=1,357, C−A +39, E−A -265 |
