# Results by past-only manoeuvring regime (test)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261021T210814Z_gbm_test`, `20261021T214353Z_gbm_test_vesselheldout`, `20261021T220501Z_gbm_test_spatialheldout`, `20261021T205144Z_baselines_test`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 23,538 | 14.0% | 399 | n/a | 2191 | 1706 | 2011 | 1729 | 1706 | 1202 | 1038 | 1017 | 990 | 1015 | 960 |
| steady | 89,261 | 53.3% | 1175 | 95% | 6287 | 1187 | 1308 | 1185 | 1186 | 1108 | 1028 | 674 | 674 | 596 | 581 |
| turning | 38,174 | 22.8% | 1082 | 80% | 6039 | 1769 | 3210 | 1769 | 1769 | 1469 | 1273 | 954 | 908 | 847 | 799 |
| speed_changing | 3,751 | 2.2% | 617 | 79% | 6257 | 2571 | 2813 | 2573 | 2572 | 1904 | 1728 | 1398 | 1344 | 1348 | 1277 |
| combined | 12,809 | 7.6% | 665 | 84% | 4402 | 3052 | 3844 | 3062 | 3053 | 2037 | 1701 | 1588 | 1517 | 1554 | 1477 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -503 (-749 to -272) | -164 (-197 to -125) | -186 (-227 to -138) | -212 (-256 to -162) | -187 (-222 to -146) | -242 (-281 to -196) |
| steady | -79 (-108 to -55) | -80 (-119 to -47) | -433 (-478 to -388) | -434 (-478 to -387) | -511 (-553 to -469) | -527 (-571 to -481) |
| turning | -300 (-402 to -206) | -196 (-258 to -135) | -515 (-563 to -463) | -561 (-622 to -494) | -621 (-675 to -566) | -669 (-727 to -608) |
| speed_changing | -667 (-917 to -402) | -176 (-239 to -116) | -506 (-625 to -395) | -560 (-661 to -458) | -556 (-661 to -453) | -626 (-737 to -524) |
| combined | -1015 (-1291 to -759) | -335 (-392 to -275) | -448 (-509 to -388) | -520 (-582 to -455) | -483 (-542 to -412) | -559 (-612 to -506) |

## Vessel-held-out training (all test vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -93 (-166 to -10) | -39 (-66 to -10) | -10 (-34 to +15) | -38 (-62 to -15) | -124 (-154 to -94) | -154 (-194 to -115) |
| steady | -30 (-39 to -21) | -20 (-29 to -13) | -316 (-344 to -290) | -320 (-346 to -296) | -469 (-496 to -442) | -464 (-495 to -431) |
| turning | -157 (-191 to -126) | -69 (-92 to -46) | -329 (-359 to -300) | -355 (-383 to -329) | -588 (-637 to -537) | -601 (-651 to -549) |
| speed_changing | -244 (-345 to -158) | -90 (-123 to -52) | -193 (-252 to -137) | -288 (-326 to -247) | -529 (-660 to -401) | -528 (-626 to -435) |
| combined | -433 (-615 to -256) | -116 (-175 to -62) | -112 (-242 to -4) | -179 (-225 to -134) | -518 (-589 to -429) | -544 (-618 to -462) |

## Spatially held-out (longitude band unseen in training, 0.05° buffer): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -192 (-337 to -72) | +13 (-52 to +108) | +209 (+133 to +304) | +144 (+53 to +249) | -100 (-149 to -42) | -109 (-185 to -1) |
| steady | -17 (-34 to -1) | -7 (-28 to +13) | +1369 (+1286 to +1455) | +628 (+575 to +678) | -436 (-466 to -405) | -429 (-464 to -392) |
| turning | -78 (-141 to -17) | -91 (-135 to -49) | +1237 (+1118 to +1357) | +396 (+330 to +459) | -617 (-671 to -559) | -638 (-690 to -581) |
| speed_changing | -153 (-324 to -10) | -49 (-128 to +38) | +762 (+605 to +913) | +423 (+275 to +557) | -685 (-947 to -418) | -642 (-854 to -423) |
| combined | -339 (-572 to -102) | -6 (-126 to +109) | +416 (+291 to +550) | +226 (+101 to +365) | -653 (-798 to -506) | -632 (-823 to -463) |

## Threshold sensitivity (`regime_sensitivity_test.csv`)

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
| primary | n=23,538, C−A -186, E−A -187 | n=89,261, C−A -433, E−A -511 | n=38,174, C−A -515, E−A -621 | n=3,751, C−A -506, E−A -556 | n=12,809, C−A -448, E−A -483 |
| turn_deg_min=0.5 | n=23,538, C−A -186, E−A -187 | n=73,760, C−A -422, E−A -496 | n=53,675, C−A -506, E−A -611 | n=2,468, C−A -539, E−A -581 | n=14,092, C−A -448, E−A -485 |
| turn_deg_min=2 | n=23,538, C−A -186, E−A -187 | n=103,967, C−A -442, E−A -525 | n=23,468, C−A -527, E−A -629 | n=5,779, C−A -464, E−A -512 | n=10,781, C−A -460, E−A -492 |
| speed_change_kn=1 | n=23,538, C−A -186, E−A -187 | n=84,648, C−A -424, E−A -502 | n=33,144, C−A -505, E−A -609 | n=8,364, C−A -564, E−A -627 | n=17,839, C−A -485, E−A -545 |
| speed_change_kn=3 | n=23,538, C−A -186, E−A -187 | n=90,826, C−A -435, E−A -513 | n=40,365, C−A -516, E−A -623 | n=2,186, C−A -499, E−A -527 | n=10,618, C−A -428, E−A -447 |
| low_speed_kn=3 | n=15,130, C−A -152, E−A -134 | n=91,182, C−A -425, E−A -502 | n=39,765, C−A -497, E−A -604 | n=4,110, C−A -486, E−A -527 | n=17,346, C−A -433, E−A -461 |
| low_speed_kn=7 | n=40,394, C−A -197, E−A -227 | n=80,776, C−A -469, E−A -548 | n=34,344, C−A -544, E−A -651 | n=3,210, C−A -546, E−A -589 | n=8,809, C−A -456, E−A -496 |
| lookback_min=5 | n=23,275, C−A -126, E−A -122 | n=95,811, C−A -426, E−A -503 | n=38,771, C−A -567, E−A -677 | n=1,770, C−A -566, E−A -639 | n=7,906, C−A -452, E−A -455 |
| lookback_min=15 | n=23,571, C−A -243, E−A -251 | n=84,368, C−A -429, E−A -508 | n=37,732, C−A -504, E−A -608 | n=5,637, C−A -471, E−A -522 | n=16,225, C−A -412, E−A -451 |
| sustained turning (>=70% same sign) | n=23,538, C−A -186, E−A -187 | n=106,522, C−A -443, E−A -527 | n=20,913, C−A -533, E−A -632 | n=10,614, C−A -468, E−A -502 | n=5,946, C−A -449, E−A -494 |
