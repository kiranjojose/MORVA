# Residual GBM context ablation (val; 376,524 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 5339 (4787–5905) | 11674 (10417–12913) | 328 | 986 | 2819 | 5026 | 8482 |
| A_motion | 2706 (2497–2906) | 5494 (5061–5946) | 240 | 647 | 1600 | 2649 | 4147 |
| C_location | 1988 (1829–2153) | 3935 (3599–4295) | 212 | 537 | 1240 | 1950 | 2980 |
| E_fairway | 2112 (1919–2312) | 4375 (3953–4792) | 190 | 492 | 1224 | 2040 | 3230 |
| G_wind | 2118 (1924–2317) | 4393 (3967–4815) | 189 | 494 | 1229 | 2042 | 3243 |
| H_wind_current | 2118 (1924–2321) | 4379 (3957–4801) | 190 | 495 | 1236 | 2045 | 3244 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -2634 (-3173 to -2088) | -6180 (-7397 to -4922) |
| C_location - cv | -3352 (-3913 to -2789) | -7738 (-9076 to -6419) |
| E_fairway - cv | -3227 (-3766 to -2688) | -7298 (-8574 to -6012) |
| G_wind - cv | -3221 (-3760 to -2683) | -7280 (-8555 to -5999) |
| H_wind_current - cv | -3221 (-3760 to -2686) | -7295 (-8571 to -6018) |
| C_location - A_motion | -718 (-804 to -630) | -1559 (-1765 to -1359) |
| E_fairway - A_motion | -593 (-682 to -521) | -1119 (-1315 to -959) |
| G_wind - A_motion | -587 (-677 to -515) | -1101 (-1308 to -935) |
| H_wind_current - A_motion | -587 (-680 to -515) | -1115 (-1323 to -952) |

Paired error differences at earlier horizons (m, 95% CI, vessel bootstrap):

| comparison | Δerr@5 | Δerr@10 | Δerr@20 | Δerr@30 | Δerr@45 |
|---|---|---|---|---|---|
| A_motion - cv | -88 (-104 to -71) | -339 (-404 to -273) | -1218 (-1466 to -969) | -2378 (-2867 to -1864) | -4335 (-5210 to -3447) |
| C_location - cv | -116 (-137 to -96) | -449 (-522 to -372) | -1578 (-1846 to -1308) | -3076 (-3618 to -2546) | -5502 (-6435 to -4561) |
| E_fairway - cv | -138 (-159 to -118) | -494 (-566 to -419) | -1594 (-1846 to -1326) | -2986 (-3501 to -2456) | -5252 (-6166 to -4344) |
| G_wind - cv | -139 (-161 to -119) | -492 (-564 to -418) | -1590 (-1844 to -1318) | -2984 (-3499 to -2454) | -5239 (-6148 to -4336) |
| H_wind_current - cv | -138 (-159 to -117) | -491 (-563 to -417) | -1582 (-1835 to -1311) | -2981 (-3496 to -2456) | -5238 (-6147 to -4336) |
| C_location - A_motion | -28 (-33 to -22) | -110 (-128 to -90) | -360 (-406 to -311) | -699 (-785 to -605) | -1167 (-1317 to -1016) |
| E_fairway - A_motion | -50 (-61 to -42) | -155 (-182 to -135) | -376 (-424 to -336) | -608 (-709 to -531) | -917 (-1041 to -805) |
| G_wind - A_motion | -51 (-63 to -42) | -153 (-179 to -133) | -371 (-420 to -332) | -607 (-705 to -531) | -904 (-1031 to -794) |
| H_wind_current - A_motion | -50 (-61 to -41) | -152 (-179 to -131) | -364 (-414 to -324) | -604 (-704 to -527) | -903 (-1036 to -792) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| 0–0.5 | 30614 | 7784 | 5519 | 3662 | 3816 | 3823 | 3799 |
| 0.5–1 | 10484 | 10860 | 6038 | 4118 | 4595 | 4621 | 4585 |
| 1–2 | 12331 | 12752 | 6409 | 4444 | 5072 | 5084 | 5069 |
| 2–5 | 18036 | 14649 | 6338 | 4506 | 5204 | 5227 | 5235 |
| 5–10 | 11293 | 13437 | 5577 | 4308 | 4985 | 5024 | 5005 |
| 10–inf | 18801 | 13840 | 3689 | 3174 | 3545 | 3563 | 3558 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| unknown | 101559 | 11674 | 5494 | 3935 | 4375 | 4393 | 4379 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (75 vessels) | seen_vessels (580 vessels) |
|---|---|---|
| C_location - A_motion | -1516 (-1999 to -1001) | -1562 (-1775 to -1359) |
| E_fairway - A_motion | -1939 (-3441 to -835) | -1062 (-1198 to -929) |
| G_wind - A_motion | -1985 (-3619 to -804) | -1040 (-1174 to -908) |
| H_wind_current - A_motion | -2034 (-3684 to -831) | -1052 (-1185 to -919) |
| A_motion - cv | -879 (-1809 to -102) | -6545 (-7938 to -5163) |
