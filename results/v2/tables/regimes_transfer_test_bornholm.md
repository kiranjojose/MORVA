# Results by past-only manoeuvring regime (transfer_test_bornholm)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261021T212556Z_gbm_transfer_test_bornholm`, `20261021T214735Z_gbm_transfer_test_bornholm_vesselheldout`, `20261021T205154Z_baselines_transfer_test_bornholm`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 3,365 | 6.1% | 57 | n/a | 1435 | 944 | 1007 | 957 | 943 | 932 | 1009 | 954 | 990 | 863 | 870 |
| steady | 46,232 | 83.2% | 891 | 99% | 6905 | 442 | 576 | 443 | 441 | 473 | 484 | 1814 | 2048 | 365 | 378 |
| turning | 4,797 | 8.6% | 789 | 76% | 7151 | 850 | 2653 | 844 | 850 | 881 | 809 | 2044 | 2273 | 659 | 658 |
| speed_changing | 377 | 0.7% | 79 | 89% | 8938 | 3550 | 3929 | 3525 | 3550 | 2969 | 2996 | 3597 | 3420 | 1974 | 2071 |
| combined | 790 | 1.4% | 75 | 82% | 5405 | 3293 | 3929 | 3317 | 3294 | 2740 | 2615 | 3379 | 3002 | 2256 | 2214 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -13 (-94 to +67) | +78 (-40 to +211) | +22 (-18 to +57) | +58 (-18 to +152) | -68 (-107 to -43) | -61 (-122 to -25) |
| steady | +31 (+27 to +36) | +11 (+4 to +21) | +1341 (+1262 to +1428) | +1575 (+1502 to +1653) | -108 (-122 to -95) | -95 (-108 to -81) |
| turning | +32 (-23 to +88) | -72 (-118 to -43) | +1163 (+1057 to +1283) | +1392 (+1284 to +1502) | -223 (-276 to -184) | -223 (-278 to -185) |
| speed_changing | -581 (-828 to -27) | +27 (-98 to +87) | +628 (+334 to +936) | +451 (+219 to +982) | -995 (-1436 to -73) | -898 (-1313 to -59) |
| combined | -553 (-973 to -148) | -124 (-370 to +205) | +640 (-83 to +1400) | +262 (-140 to +610) | -484 (-669 to -283) | -526 (-843 to -166) |

## Vessel-held-out training (all transfer_test_bornholm vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -10 (-95 to +75) | +61 (-49 to +178) | +10 (-30 to +42) | +21 (-42 to +95) | -69 (-109 to -43) | -67 (-132 to -27) |
| steady | +35 (+29 to +42) | +13 (+4 to +22) | +1381 (+1314 to +1452) | +1293 (+1255 to +1336) | -107 (-121 to -95) | -91 (-105 to -78) |
| turning | +54 (-6 to +119) | -80 (-131 to -42) | +1058 (+971 to +1152) | +1044 (+965 to +1118) | -240 (-302 to -191) | -236 (-303 to -187) |
| speed_changing | -681 (-967 to -23) | -58 (-179 to +10) | +880 (+461 to +1157) | +421 (+64 to +829) | -893 (-1260 to -49) | -870 (-1250 to -39) |
| combined | -645 (-1044 to -230) | -15 (-238 to +264) | +654 (-0 to +1327) | +338 (-65 to +705) | -414 (-581 to -215) | -401 (-665 to -55) |

## Threshold sensitivity (`regime_sensitivity_transfer_test_bornholm.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning), 50 regime×config cells. Cells where the 95% CI lies entirely below 0 (first model better) / entirely above 0 (first model worse):

| comparison | CI below 0 | CI above 0 |
|---|---|---|
| A_motion − cv | 15 | 12 |
| B_vessel − A_motion | 12 | 8 |
| C_location − A_motion | 0 | 32 |
| D_all − A_motion | 0 | 30 |
| E_fairway − A_motion | 50 | 0 |
| F_all_fairway − A_motion | 50 | 0 |

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=3,365, C−A +22, E−A -68 | n=46,232, C−A +1341, E−A -108 | n=4,797, C−A +1163, E−A -223 | n=377, C−A +628, E−A -995 | n=790, C−A +640, E−A -484 |
| turn_deg_min=0.5 | n=3,365, C−A +22, E−A -68 | n=43,080, C−A +1356, E−A -100 | n=7,949, C−A +1154, E−A -220 | n=283, C−A +569, E−A -927 | n=884, C−A +658, E−A -560 |
| turn_deg_min=2 | n=3,365, C−A +22, E−A -68 | n=48,572, C−A +1335, E−A -114 | n=2,457, C−A +1110, E−A -213 | n=489, C−A +792, E−A -1019 | n=678, C−A +524, E−A -382 |
| speed_change_kn=1 | n=3,365, C−A +22, E−A -68 | n=45,816, C−A +1346, E−A -104 | n=4,537, C−A +1200, E−A -209 | n=793, C−A +687, E−A -719 | n=1,050, C−A +607, E−A -479 |
| speed_change_kn=3 | n=3,365, C−A +22, E−A -68 | n=46,346, C−A +1340, E−A -108 | n=4,891, C−A +1155, E−A -233 | n=263, C−A +404, E−A -1312 | n=696, C−A +625, E−A -444 |
| low_speed_kn=3 | n=2,330, C−A +12, E−A -55 | n=46,760, C−A +1327, E−A -107 | n=4,985, C−A +1118, E−A -216 | n=399, C−A +585, E−A -959 | n=1,087, C−A +464, E−A -421 |
| low_speed_kn=7 | n=5,917, C−A +86, E−A -64 | n=44,127, C−A +1396, E−A -112 | n=4,590, C−A +1211, E−A -224 | n=357, C−A +656, E−A -1058 | n=570, C−A +826, E−A -566 |
| lookback_min=5 | n=3,380, C−A +18, E−A -50 | n=46,443, C−A +1353, E−A -109 | n=4,903, C−A +1061, E−A -250 | n=222, C−A +366, E−A -1083 | n=613, C−A +324, E−A -574 |
| lookback_min=15 | n=3,336, C−A +48, E−A -76 | n=45,639, C−A +1333, E−A -107 | n=5,091, C−A +1236, E−A -187 | n=539, C−A +906, E−A -1151 | n=956, C−A +651, E−A -335 |
| sustained turning (>=70% same sign) | n=3,365, C−A +22, E−A -68 | n=48,494, C−A +1329, E−A -113 | n=2,535, C−A +1230, E−A -222 | n=876, C−A +726, E−A -698 | n=291, C−A +366, E−A -502 |
