# Residual GBM context ablation (transfer_val, oslofjord; 376,524 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 4350 (3523–5200) | 9486 (7636–11399) | 271 | 804 | 2298 | 4099 | 6905 |
| A_motion | 2642 (2249–3033) | 5149 (4331–5985) | 240 | 687 | 1705 | 2664 | 4065 |
| C_location | 3520 (3027–4050) | 6364 (5378–7578) | 290 | 868 | 2351 | 3690 | 5502 |
| E_fairway | 2117 (1849–2403) | 4159 (3538–4763) | 206 | 552 | 1389 | 2225 | 3192 |
| G_wind | 2115 (1848–2398) | 4114 (3510–4711) | 205 | 559 | 1389 | 2225 | 3200 |
| H_wind_current | 2128 (1859–2417) | 4158 (3547–4759) | 204 | 558 | 1391 | 2233 | 3227 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -1707 (-2313 to -1079) | -4337 (-5923 to -2695) |
| C_location - cv | -829 (-1591 to +12) | -3122 (-4994 to -1173) |
| E_fairway - cv | -2232 (-2870 to -1600) | -5327 (-6921 to -3730) |
| G_wind - cv | -2235 (-2875 to -1603) | -5372 (-6995 to -3749) |
| H_wind_current - cv | -2222 (-2857 to -1596) | -5328 (-6937 to -3722) |
| C_location - A_motion | +878 (+662 to +1177) | +1215 (+828 to +1718) |
| E_fairway - A_motion | -525 (-662 to -398) | -990 (-1285 to -746) |
| G_wind - A_motion | -528 (-664 to -400) | -1035 (-1342 to -770) |
| H_wind_current - A_motion | -515 (-651 to -389) | -991 (-1289 to -737) |

Paired error differences at earlier horizons (m, 95% CI, vessel bootstrap):

| comparison | Δerr@5 | Δerr@10 | Δerr@20 | Δerr@30 | Δerr@45 |
|---|---|---|---|---|---|
| A_motion - cv | -31 (-41 to -20) | -117 (-158 to -78) | -594 (-763 to -414) | -1436 (-1936 to -921) | -2840 (-3911 to -1759) |
| C_location - cv | +18 (+3 to +35) | +64 (-6 to +140) | +53 (-198 to +374) | -410 (-1054 to +312) | -1403 (-2791 to +38) |
| E_fairway - cv | -66 (-76 to -55) | -252 (-293 to -210) | -909 (-1112 to -711) | -1874 (-2385 to -1373) | -3713 (-4874 to -2598) |
| G_wind - cv | -67 (-77 to -55) | -245 (-284 to -204) | -909 (-1115 to -710) | -1874 (-2376 to -1378) | -3705 (-4870 to -2596) |
| H_wind_current - cv | -67 (-77 to -56) | -246 (-287 to -203) | -907 (-1107 to -709) | -1867 (-2372 to -1374) | -3678 (-4818 to -2572) |
| C_location - A_motion | +49 (+41 to +60) | +182 (+146 to +223) | +646 (+511 to +828) | +1026 (+787 to +1353) | +1437 (+1036 to +1972) |
| E_fairway - A_motion | -35 (-44 to -24) | -135 (-175 to -92) | -315 (-400 to -226) | -438 (-579 to -316) | -873 (-1115 to -645) |
| G_wind - A_motion | -36 (-44 to -25) | -127 (-166 to -86) | -316 (-402 to -227) | -438 (-580 to -322) | -864 (-1107 to -640) |
| H_wind_current - A_motion | -36 (-45 to -26) | -129 (-170 to -85) | -313 (-397 to -229) | -431 (-571 to -310) | -837 (-1074 to -613) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| 0–0.5 | 5435 | 7211 | 6321 | 9541 | 4762 | 4728 | 4762 |
| 0.5–1 | 1698 | 10003 | 7159 | 8294 | 5344 | 5314 | 5340 |
| 1–2 | 2224 | 11457 | 7024 | 7723 | 5403 | 5381 | 5351 |
| 2–5 | 3652 | 10525 | 6385 | 6893 | 5086 | 5095 | 5077 |
| 5–10 | 2877 | 10977 | 4281 | 4666 | 3817 | 3678 | 3856 |
| 10–inf | 5443 | 9306 | 2216 | 2577 | 2237 | 2183 | 2240 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| unknown | 21329 | 9486 | 5149 | 6364 | 4159 | 4114 | 4158 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (119 vessels) | seen_vessels (21 vessels) |
|---|---|---|
| C_location - A_motion | +984 (+622 to +1483) | +3976 (+3381 to +4467) |
| E_fairway - A_motion | -968 (-1284 to -693) | -1262 (-1476 to -1032) |
| G_wind - A_motion | -1014 (-1347 to -719) | -1287 (-1522 to -1049) |
| H_wind_current - A_motion | -965 (-1289 to -684) | -1312 (-1548 to -1071) |
| A_motion - cv | -4692 (-6282 to -2761) | -90 (-303 to +179) |
