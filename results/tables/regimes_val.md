# Results by past-only manoeuvring regime (validation, preliminary)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261010T150815Z_gbm_val`, `20261010T151423Z_gbm_val_vesselheldout`, `20261009T144057Z_baselines_val`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 9,890 | 15.7% | 266 | n/a | 2108 | 1587 | 1788 | 1609 | 1072 | 923 | 903 | 871 |
| steady | 32,761 | 52.0% | 652 | 95% | 6280 | 1190 | 1301 | 1188 | 1105 | 1019 | 671 | 656 |
| turning | 14,293 | 22.7% | 603 | 81% | 6061 | 1836 | 3257 | 1836 | 1501 | 1298 | 989 | 927 |
| speed_changing | 1,414 | 2.2% | 295 | 79% | 5905 | 2734 | 2971 | 2737 | 2028 | 1844 | 1539 | 1449 |
| combined | 4,624 | 7.3% | 357 | 83% | 4190 | 3104 | 3800 | 3125 | 1959 | 1637 | 1547 | 1448 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion |
|---|---|---|---|---|
| low_speed | -515 (-759 to -282) | -149 (-188 to -108) | -170 (-220 to -117) | -201 (-254 to -148) |
| steady | -85 (-113 to -60) | -86 (-121 to -56) | -433 (-479 to -391) | -449 (-497 to -403) |
| turning | -335 (-440 to -233) | -203 (-261 to -145) | -511 (-562 to -464) | -573 (-634 to -512) |
| speed_changing | -706 (-935 to -472) | -183 (-242 to -122) | -488 (-645 to -336) | -579 (-727 to -432) |
| combined | -1145 (-1476 to -819) | -322 (-375 to -264) | -412 (-483 to -338) | -511 (-596 to -433) |

## Vessel-held-out training (all val vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion |
|---|---|---|---|---|
| low_speed | -108 (-170 to -44) | +66 (+6 to +125) | +24 (+0 to +48) | +41 (+7 to +74) |
| steady | -48 (-60 to -38) | -21 (-32 to -9) | -358 (-389 to -329) | -362 (-395 to -333) |
| turning | -182 (-220 to -146) | -53 (-76 to -32) | -362 (-395 to -327) | -387 (-420 to -351) |
| speed_changing | -274 (-372 to -155) | -98 (-165 to -31) | -291 (-344 to -237) | -319 (-392 to -249) |
| combined | -446 (-575 to -303) | -33 (-104 to +42) | -135 (-253 to -31) | -156 (-221 to -94) |

## Threshold sensitivity (`regime_sensitivity_val.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning). Location context (C − A) improves FDE with a 95% CI excluding zero in 50 of 50 regime×config cells.

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=9,890, C−A -170 | n=32,761, C−A -433 | n=14,293, C−A -511 | n=1,414, C−A -488 | n=4,624, C−A -412 |
| turn_deg_min=0.5 | n=9,890, C−A -170 | n=27,247, C−A -414 | n=19,807, C−A -516 | n=921, C−A -532 | n=5,117, C−A -412 |
| turn_deg_min=2 | n=9,890, C−A -170 | n=38,143, C−A -444 | n=8,911, C−A -514 | n=2,172, C−A -436 | n=3,866, C−A -427 |
| speed_change_kn=1 | n=9,890, C−A -170 | n=31,136, C−A -425 | n=12,489, C−A -508 | n=3,039, C−A -545 | n=6,428, C−A -446 |
| speed_change_kn=3 | n=9,890, C−A -170 | n=33,329, C−A -435 | n=15,050, C−A -509 | n=846, C−A -449 | n=3,867, C−A -400 |
| low_speed_kn=3 | n=6,132, C−A -151 | n=33,943, C−A -419 | n=14,941, C−A -493 | n=1,578, C−A -449 | n=6,388, C−A -402 |
| low_speed_kn=7 | n=15,844, C−A -183 | n=29,816, C−A -465 | n=12,970, C−A -540 | n=1,192, C−A -537 | n=3,160, C−A -432 |
| lookback_min=5 | n=9,773, C−A -118 | n=35,395, C−A -422 | n=14,187, C−A -571 | n=675, C−A -642 | n=2,952, C−A -384 |
| lookback_min=15 | n=9,933, C−A -209 | n=30,849, C−A -431 | n=14,302, C−A -498 | n=2,030, C−A -433 | n=5,868, C−A -410 |
| sustained turning (>=70% same sign) | n=9,890, C−A -170 | n=39,085, C−A -444 | n=7,969, C−A -521 | n=3,867, C−A -450 | n=2,171, C−A -395 |
