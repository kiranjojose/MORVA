# Results by past-only manoeuvring regime (transfer_val_bornholm)

Regime parameters: lookback_min=10, low_speed_kn=5, turn_deg_min=1, speed_change_kn=2, sustained_frac=0.7. Runs: `20261018T205927Z_gbm_transfer_val_bornholm`, `20261018T210810Z_gbm_transfer_val_bornholm_vesselheldout`, `20261018T201728Z_baselines_transfer_val_bornholm`.

## Mean FDE@20 min (m)

| regime | windows | share | vessels | turn label reliable | persistence | cv | ctrv | ctrv_damped | kalman_cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low_speed | 3,609 | 8.7% | 57 | n/a | 1394 | 859 | 921 | 864 | 859 | 827 | 954 | 883 | 946 | 777 | 816 |
| steady | 33,758 | 81.0% | 745 | 99% | 6884 | 415 | 526 | 415 | 415 | 442 | 449 | 1779 | 2009 | 343 | 354 |
| turning | 3,403 | 8.2% | 651 | 77% | 7073 | 893 | 2667 | 881 | 892 | 890 | 821 | 2046 | 2293 | 702 | 698 |
| speed_changing | 296 | 0.7% | 72 | 87% | 8128 | 5789 | 6065 | 5779 | 5720 | 5004 | 5172 | 5835 | 5614 | 4343 | 4403 |
| combined | 609 | 1.5% | 69 | 79% | 4509 | 4000 | 4155 | 4035 | 3990 | 3141 | 3079 | 3543 | 3218 | 2793 | 2682 |

## Paired ΔFDE@20 min by regime (m, 95% CI, vessel bootstrap; negative = first model better)

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -32 (-93 to +25) | +127 (+42 to +226) | +56 (+20 to +88) | +119 (+49 to +204) | -50 (-85 to -18) | -11 (-59 to +34) |
| steady | +27 (+22 to +33) | +7 (+0 to +12) | +1337 (+1249 to +1431) | +1567 (+1475 to +1659) | -99 (-116 to -84) | -87 (-102 to -73) |
| turning | -2 (-66 to +57) | -69 (-115 to -34) | +1156 (+1053 to +1265) | +1403 (+1289 to +1518) | -188 (-245 to -133) | -192 (-246 to -144) |
| speed_changing | -785 (-1713 to -75) | +167 (-130 to +707) | +830 (+28 to +1329) | +609 (+353 to +1029) | -661 (-1267 to +300) | -601 (-1175 to +314) |
| combined | -859 (-1270 to -469) | -62 (-397 to +281) | +402 (-161 to +1166) | +77 (-413 to +505) | -348 (-526 to -140) | -459 (-710 to -166) |

## Vessel-held-out training (all transfer_val_bornholm vessels unseen): paired ΔFDE@20 min by regime

| regime | A_motion − cv | B_vessel − A_motion | C_location − A_motion | D_all − A_motion | E_fairway − A_motion | F_all_fairway − A_motion |
|---|---|---|---|---|---|---|
| low_speed | -25 (-82 to +29) | +80 (+18 to +159) | +37 (+10 to +73) | +73 (+19 to +147) | -51 (-89 to -20) | -9 (-52 to +32) |
| steady | +33 (+27 to +39) | +16 (+6 to +26) | +1523 (+1422 to +1629) | +1172 (+1102 to +1238) | -103 (-118 to -89) | -90 (-107 to -74) |
| turning | +4 (-56 to +59) | -64 (-97 to -34) | +1246 (+1137 to +1369) | +975 (+896 to +1055) | -189 (-235 to -141) | -196 (-244 to -149) |
| speed_changing | -774 (-1765 to -76) | +136 (-102 to +534) | +1264 (+401 to +1811) | +599 (+377 to +878) | -648 (-1298 to +398) | -676 (-1360 to +402) |
| combined | -868 (-1309 to -458) | -58 (-315 to +208) | +547 (-142 to +1468) | +185 (-340 to +730) | -368 (-571 to -144) | -391 (-633 to -104) |

## Threshold sensitivity (`regime_sensitivity_transfer_val_bornholm.csv`)

10 configurations (primary, one-at-a-time changes, sustained turning), 50 regime×config cells. Cells where the 95% CI lies entirely below 0 (first model better) / entirely above 0 (first model worse):

| comparison | CI below 0 | CI above 0 |
|---|---|---|
| A_motion − cv | 17 | 11 |
| B_vessel − A_motion | 10 | 16 |
| C_location − A_motion | 0 | 37 |
| D_all − A_motion | 0 | 39 |
| E_fairway − A_motion | 40 | 0 |
| F_all_fairway − A_motion | 30 | 0 |

| config | low_speed | steady | turning | speed_changing | combined |
|---|---|---|---|---|---|
| primary | n=3,609, C−A +56, E−A -50 | n=33,758, C−A +1337, E−A -99 | n=3,403, C−A +1156, E−A -188 | n=296, C−A +830, E−A -661 | n=609, C−A +402, E−A -348 |
| turn_deg_min=0.5 | n=3,609, C−A +56, E−A -50 | n=31,915, C−A +1339, E−A -92 | n=5,246, C−A +1205, E−A -200 | n=220, C−A +862, E−A -773 | n=685, C−A +439, E−A -347 |
| turn_deg_min=2 | n=3,609, C−A +56, E−A -50 | n=35,410, C−A +1333, E−A -104 | n=1,751, C−A +1071, E−A -166 | n=389, C−A +794, E−A -598 | n=516, C−A +352, E−A -340 |
| speed_change_kn=1 | n=3,609, C−A +56, E−A -50 | n=33,513, C−A +1338, E−A -97 | n=3,271, C−A +1179, E−A -190 | n=541, C−A +983, E−A -541 | n=741, C−A +436, E−A -313 |
| speed_change_kn=3 | n=3,609, C−A +56, E−A -50 | n=33,834, C−A +1337, E−A -99 | n=3,475, C−A +1142, E−A -190 | n=220, C−A +647, E−A -788 | n=537, C−A +395, E−A -360 |
| low_speed_kn=3 | n=2,464, C−A +62, E−A -49 | n=34,340, C−A +1315, E−A -97 | n=3,660, C−A +1076, E−A -174 | n=325, C−A +754, E−A -613 | n=886, C−A +309, E−A -307 |
| low_speed_kn=7 | n=5,482, C−A +90, E−A -40 | n=32,263, C−A +1391, E−A -104 | n=3,224, C−A +1215, E−A -196 | n=267, C−A +937, E−A -687 | n=439, C−A +507, E−A -418 |
| lookback_min=5 | n=3,605, C−A +43, E−A -40 | n=34,252, C−A +1342, E−A -99 | n=3,162, C−A +1087, E−A -247 | n=159, C−A +517, E−A -583 | n=497, C−A +243, E−A -286 |
| lookback_min=15 | n=3,607, C−A +66, E−A -56 | n=33,254, C−A +1328, E−A -97 | n=3,672, C−A +1244, E−A -180 | n=399, C−A +1087, E−A -720 | n=743, C−A +476, E−A -251 |
| sustained turning (>=70% same sign) | n=3,609, C−A +56, E−A -50 | n=35,413, C−A +1324, E−A -102 | n=1,748, C−A +1257, E−A -204 | n=660, C−A +667, E−A -455 | n=245, C−A +205, E−A -439 |
