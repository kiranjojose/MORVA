# Results by past-only manoeuvring regime (validation, preliminary)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261011T203406Z_gbm_test`, `20261011T203621Z_gbm_test_vesselheldout`, `20261011T204639Z_gbm_test_spatialheldout`, `20261011T202500Z_baselines_test`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 8,559 | 15.0% | 237 | n/a | 2083 | 1671 | 1933 | 1692 | 1671 | 1186 | 1020 | 1001 | 974 |
| steady | 30,102 | 52.7% | 598 | 95% | 6290 | 1155 | 1274 | 1154 | 1155 | 1067 | 993 | 654 | 641 |
| turning | 12,909 | 22.6% | 553 | 81% | 5955 | 1779 | 3141 | 1773 | 1779 | 1462 | 1247 | 952 | 894 |
| speed_changing | 1,273 | 2.2% | 281 | 80% | 6403 | 2589 | 2877 | 2595 | 2590 | 1834 | 1714 | 1396 | 1324 |
| combined | 4,225 | 7.4% | 323 | 83% | 4307 | 3157 | 3839 | 3166 | 3158 | 2079 | 1773 | 1641 | 1560 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion |
|---|---|---|---|---|
| low_speed | -485 (-713 to -278) | -166 (-203 to -127) | -185 (-234 to -139) | -212 (-258 to -162) |
| steady | -88 (-123 to -60) | -75 (-107 to -48) | -413 (-456 to -369) | -427 (-471 to -380) |
| turning | -316 (-429 to -215) | -216 (-275 to -157) | -511 (-566 to -460) | -568 (-636 to -505) |
| speed_changing | -756 (-1044 to -440) | -119 (-191 to -45) | -438 (-537 to -332) | -510 (-591 to -414) |
| combined | -1078 (-1316 to -816) | -306 (-381 to -231) | -438 (-520 to -362) | -519 (-605 to -427) |

## Vessel-held-out training (all test vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion |
|---|---|---|---|---|
| low_speed | -149 (-210 to -85) | -71 (-111 to -32) | +16 (-8 to +42) | -20 (-48 to +13) |
| steady | -35 (-46 to -24) | -35 (-51 to -21) | -334 (-368 to -301) | -345 (-379 to -311) |
| turning | -190 (-234 to -144) | -101 (-140 to -63) | -327 (-367 to -289) | -372 (-414 to -335) |
| speed_changing | -234 (-332 to -140) | -122 (-186 to -60) | -278 (-341 to -203) | -317 (-382 to -252) |
| combined | -482 (-615 to -336) | -99 (-177 to -30) | -136 (-247 to -36) | -172 (-244 to -111) |

## Spatially held-out (longitude band unseen in training, 0.05° buffer): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion |
|---|---|---|---|---|
| low_speed | -178 (-299 to -73) | +20 (-48 to +111) | +192 (+128 to +271) | +148 (+70 to +243) |
| steady | -16 (-32 to -3) | -8 (-29 to +14) | +1435 (+1351 to +1514) | +601 (+553 to +650) |
| turning | -99 (-165 to -26) | -97 (-146 to -52) | +1284 (+1157 to +1410) | +383 (+310 to +446) |
| speed_changing | -117 (-300 to +69) | -72 (-184 to +48) | +839 (+652 to +1026) | +360 (+227 to +492) |
| combined | -386 (-618 to -133) | +22 (-94 to +128) | +440 (+318 to +570) | +259 (+138 to +391) |

## Threshold sensitivity (`regime_sensitivity_test.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning). Location context (C − A) improves FDE with a 95% CI excluding zero in 50 of 50 regime×config cells.

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=8,559, C−A -185 | n=30,102, C−A -413 | n=12,909, C−A -511 | n=1,273, C−A -438 | n=4,225, C−A -438 |
| turn_deg_min=0.5 | n=8,559, C−A -185 | n=24,770, C−A -402 | n=18,241, C−A -498 | n=844, C−A -480 | n=4,654, C−A -430 |
| turn_deg_min=2 | n=8,559, C−A -185 | n=35,147, C−A -422 | n=7,864, C−A -534 | n=1,906, C−A -417 | n=3,592, C−A -449 |
| speed_change_kn=1 | n=8,559, C−A -185 | n=28,492, C−A -402 | n=11,263, C−A -499 | n=2,883, C−A -534 | n=5,871, C−A -481 |
| speed_change_kn=3 | n=8,559, C−A -185 | n=30,627, C−A -414 | n=13,597, C−A -511 | n=748, C−A -451 | n=3,537, C−A -423 |
| low_speed_kn=3 | n=5,499, C−A -164 | n=30,840, C−A -405 | n=13,463, C−A -492 | n=1,393, C−A -421 | n=5,873, C−A -415 |
| low_speed_kn=7 | n=13,870, C−A -201 | n=27,568, C−A -444 | n=11,652, C−A -534 | n=1,074, C−A -474 | n=2,904, C−A -440 |
| lookback_min=5 | n=8,443, C−A -133 | n=32,421, C−A -413 | n=12,944, C−A -556 | n=606, C−A -531 | n=2,654, C−A -380 |
| lookback_min=15 | n=8,600, C−A -237 | n=28,392, C−A -407 | n=12,719, C−A -500 | n=1,906, C−A -476 | n=5,451, C−A -401 |
| sustained turning (>=70% same sign) | n=8,559, C−A -185 | n=35,791, C−A -427 | n=7,220, C−A -519 | n=3,520, C−A -445 | n=1,978, C−A -425 |
