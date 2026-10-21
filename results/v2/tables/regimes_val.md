# Results by past-only manoeuvring regime (val)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261018T205501Z_gbm_val`, `20261021T141849Z_gbm_val_vesselheldout`, `20261018T212948Z_gbm_val_spatialheldout`, `20261018T201719Z_baselines_val`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 18,472 | 15.3% | 371 | n/a | 2095 | 1625 | 1854 | 1646 | 1625 | 1120 | 964 | 956 | 925 | 953 | 898 |
| steady | 63,108 | 52.4% | 1008 | 95% | 6285 | 1172 | 1287 | 1171 | 1172 | 1087 | 1005 | 659 | 653 | 583 | 566 |
| turning | 27,283 | 22.7% | 917 | 81% | 6014 | 1808 | 3202 | 1805 | 1809 | 1487 | 1273 | 969 | 920 | 863 | 807 |
| speed_changing | 2,693 | 2.2% | 483 | 79% | 6140 | 2662 | 2923 | 2667 | 2664 | 1937 | 1769 | 1466 | 1387 | 1390 | 1324 |
| combined | 8,856 | 7.4% | 541 | 83% | 4247 | 3128 | 3818 | 3143 | 3129 | 2028 | 1689 | 1590 | 1508 | 1583 | 1495 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -505 (-745 to -287) | -156 (-187 to -120) | -164 (-209 to -117) | -194 (-237 to -149) | -166 (-207 to -126) | -222 (-268 to -181) |
| steady | -85 (-114 to -61) | -82 (-114 to -52) | -428 (-473 to -389) | -434 (-480 to -393) | -504 (-548 to -466) | -521 (-569 to -478) |
| turning | -321 (-431 to -228) | -214 (-271 to -158) | -518 (-570 to -471) | -566 (-631 to -509) | -623 (-678 to -576) | -680 (-739 to -628) |
| speed_changing | -726 (-981 to -448) | -167 (-218 to -111) | -470 (-589 to -351) | -550 (-665 to -436) | -546 (-656 to -437) | -612 (-725 to -502) |
| combined | -1100 (-1351 to -818) | -339 (-400 to -269) | -437 (-513 to -364) | -519 (-607 to -431) | -445 (-518 to -370) | -532 (-597 to -474) |

## Vessel-held-out training (all val vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -118 (-185 to -54) | +95 (+36 to +164) | +40 (+19 to +63) | +61 (+22 to +102) | -70 (-107 to -35) | -38 (-87 to +7) |
| steady | -35 (-45 to -26) | -24 (-37 to -14) | -334 (-368 to -305) | -347 (-380 to -317) | -466 (-496 to -438) | -482 (-516 to -450) |
| turning | -171 (-211 to -140) | -67 (-93 to -46) | -340 (-372 to -304) | -365 (-400 to -330) | -578 (-618 to -540) | -614 (-659 to -570) |
| speed_changing | -243 (-318 to -161) | -149 (-190 to -106) | -274 (-314 to -225) | -282 (-334 to -227) | -435 (-495 to -369) | -578 (-681 to -473) |
| combined | -427 (-551 to -288) | -88 (-156 to -29) | -135 (-253 to -17) | -141 (-206 to -84) | -440 (-517 to -354) | -504 (-587 to -416) |

## Spatially held-out (longitude band unseen in training, 0.05° buffer): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -196 (-320 to -89) | +16 (-42 to +97) | +211 (+142 to +295) | +146 (+69 to +237) | -84 (-135 to -26) | -88 (-174 to +26) |
| steady | -19 (-34 to -6) | -13 (-32 to +9) | +1377 (+1303 to +1459) | +620 (+576 to +665) | -430 (-466 to -398) | -431 (-468 to -396) |
| turning | -97 (-174 to -33) | -98 (-144 to -56) | +1239 (+1116 to +1366) | +382 (+312 to +448) | -623 (-682 to -570) | -650 (-707 to -598) |
| speed_changing | -220 (-393 to -57) | -35 (-126 to +60) | +773 (+614 to +934) | +402 (+250 to +546) | -658 (-930 to -395) | -614 (-834 to -392) |
| combined | -402 (-605 to -175) | +11 (-119 to +131) | +450 (+313 to +588) | +243 (+108 to +378) | -603 (-735 to -463) | -565 (-734 to -391) |

## Threshold sensitivity (`regime_sensitivity_val.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning), 50 regime×config cells. Cells where the 95% CI lies entirely below 0 (first model better) / entirely above 0 (first model worse):

| comparison | CI below 0 | CI above 0 |
|---|---|---|
| A_motion − cv | 50 | 0 |
| B_vessel − A_motion | 50 | 0 |
| C_location − A_motion | 50 | 0 |
| D_all − A_motion | 50 | 0 |
| E_fairway − A_motion | 50 | 0 |
| F_all_fairway − A_motion | 50 | 0 |

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=18,472, C−A -164, E−A -166 | n=63,108, C−A -428, E−A -504 | n=27,283, C−A -518, E−A -623 | n=2,693, C−A -470, E−A -546 | n=8,856, C−A -437, E−A -445 |
| turn_deg_min=0.5 | n=18,472, C−A -164, E−A -166 | n=52,220, C−A -412, E−A -481 | n=38,171, C−A -514, E−A -621 | n=1,768, C−A -500, E−A -566 | n=9,781, C−A -435, E−A -451 |
| turn_deg_min=2 | n=18,472, C−A -164, E−A -166 | n=73,577, C−A -437, E−A -521 | n=16,814, C−A -533, E−A -626 | n=4,086, C−A -435, E−A -514 | n=7,463, C−A -451, E−A -444 |
| speed_change_kn=1 | n=18,472, C−A -164, E−A -166 | n=59,861, C−A -417, E−A -492 | n=23,825, C−A -509, E−A -617 | n=5,940, C−A -554, E−A -643 | n=12,314, C−A -477, E−A -507 |
| speed_change_kn=3 | n=18,472, C−A -164, E−A -166 | n=64,204, C−A -429, E−A -506 | n=28,731, C−A -518, E−A -621 | n=1,597, C−A -450, E−A -512 | n=7,408, C−A -423, E−A -420 |
| low_speed_kn=3 | n=11,644, C−A -142, E−A -129 | n=65,036, C−A -416, E−A -492 | n=28,485, C−A -499, E−A -605 | n=2,978, C−A -441, E−A -510 | n=12,269, C−A -414, E−A -414 |
| low_speed_kn=7 | n=29,758, C−A -183, E−A -215 | n=57,616, C−A -459, E−A -536 | n=24,699, C−A -544, E−A -646 | n=2,271, C−A -519, E−A -592 | n=6,068, C−A -453, E−A -448 |
| lookback_min=5 | n=18,240, C−A -114, E−A -114 | n=68,072, C−A -422, E−A -498 | n=27,209, C−A -570, E−A -678 | n=1,280, C−A -575, E−A -657 | n=5,611, C−A -392, E−A -370 |
| lookback_min=15 | n=18,556, C−A -210, E−A -222 | n=59,489, C−A -421, E−A -497 | n=27,093, C−A -509, E−A -615 | n=3,943, C−A -463, E−A -531 | n=11,331, C−A -419, E−A -431 |
| sustained turning (>=70% same sign) | n=18,472, C−A -164, E−A -166 | n=75,148, C−A -440, E−A -522 | n=15,243, C−A -528, E−A -631 | n=7,398, C−A -459, E−A -487 | n=4,151, C−A -421, E−A -435 |
