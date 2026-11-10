# Residual GBM context ablation (transfer_val, skagen; 376,524 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 1802 (1562–2127) | 4482 (3947–5200) | 90 | 267 | 814 | 1545 | 2892 |
| A_motion | 1779 (1626–1987) | 4349 (4013–4732) | 84 | 266 | 823 | 1552 | 2852 |
| C_location | 4525 (4127–4986) | 9630 (8826–10521) | 151 | 581 | 2524 | 4321 | 7401 |
| E_fairway | 1472 (1342–1644) | 3635 (3371–3970) | 80 | 238 | 715 | 1283 | 2328 |
| G_wind | 1469 (1339–1642) | 3648 (3388–3984) | 80 | 237 | 715 | 1278 | 2314 |
| H_wind_current | 1469 (1339–1642) | 3647 (3384–3990) | 80 | 237 | 715 | 1278 | 2315 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -23 (-193 to +107) | -133 (-619 to +225) |
| C_location - cv | +2722 (+2312 to +3157) | +5148 (+4251 to +6061) |
| E_fairway - cv | -331 (-502 to -213) | -847 (-1308 to -518) |
| G_wind - cv | -334 (-505 to -215) | -834 (-1297 to -503) |
| H_wind_current - cv | -333 (-505 to -214) | -835 (-1291 to -507) |
| C_location - A_motion | +2745 (+2422 to +3135) | +5281 (+4667 to +6006) |
| E_fairway - A_motion | -308 (-359 to -260) | -714 (-830 to -605) |
| G_wind - A_motion | -310 (-362 to -263) | -701 (-818 to -595) |
| H_wind_current - A_motion | -310 (-362 to -262) | -702 (-822 to -592) |
| G_wind - E_fairway | -3 (-4 to -2) | +13 (+8 to +18) |
| H_wind_current - E_fairway | -2 (-4 to -0) | +12 (+4 to +21) |

Paired error differences at earlier horizons (m, 95% CI, vessel bootstrap):

| comparison | Δerr@5 | Δerr@10 | Δerr@20 | Δerr@30 | Δerr@45 |
|---|---|---|---|---|---|
| A_motion - cv | -5 (-6 to -4) | -1 (-6 to +4) | +9 (-33 to +46) | +7 (-114 to +105) | -40 (-337 to +187) |
| C_location - cv | +61 (+54 to +71) | +314 (+275 to +358) | +1711 (+1496 to +1958) | +2775 (+2375 to +3232) | +4509 (+3796 to +5250) |
| E_fairway - cv | -10 (-12 to -7) | -29 (-38 to -23) | -98 (-142 to -66) | -262 (-390 to -173) | -563 (-858 to -362) |
| G_wind - cv | -10 (-12 to -7) | -30 (-39 to -23) | -98 (-142 to -66) | -267 (-395 to -178) | -578 (-872 to -376) |
| H_wind_current - cv | -9 (-12 to -7) | -30 (-39 to -23) | -98 (-141 to -66) | -268 (-396 to -178) | -576 (-874 to -371) |
| C_location - A_motion | +67 (+59 to +76) | +315 (+279 to +356) | +1701 (+1503 to +1934) | +2768 (+2428 to +3161) | +4548 (+3998 to +5204) |
| E_fairway - A_motion | -4 (-7 to -3) | -29 (-38 to -22) | -107 (-132 to -86) | -269 (-318 to -225) | -524 (-613 to -443) |
| G_wind - A_motion | -4 (-7 to -3) | -29 (-39 to -22) | -107 (-133 to -86) | -274 (-325 to -231) | -538 (-628 to -456) |
| H_wind_current - A_motion | -4 (-6 to -3) | -29 (-38 to -22) | -107 (-132 to -86) | -274 (-324 to -231) | -537 (-627 to -454) |
| G_wind - E_fairway | +0 (-0 to +0) | -1 (-1 to -0) | -0 (-1 to +1) | -5 (-7 to -4) | -14 (-18 to -11) |
| H_wind_current - E_fairway | +0 (-0 to +1) | -0 (-1 to +0) | -0 (-1 to +1) | -5 (-8 to -3) | -13 (-18 to -8) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| 0–0.5 | 37597 | 3426 | 3672 | 10372 | 3107 | 3126 | 3124 |
| 0.5–1 | 7072 | 4516 | 4701 | 9143 | 3705 | 3717 | 3708 |
| 1–2 | 4936 | 5932 | 5890 | 9214 | 4607 | 4608 | 4624 |
| 2–5 | 4343 | 7023 | 6673 | 9520 | 5099 | 5101 | 5105 |
| 5–10 | 2399 | 8428 | 5849 | 6482 | 5486 | 5485 | 5483 |
| 10–inf | 3167 | 8207 | 4876 | 5089 | 4808 | 4797 | 4804 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | C_location | E_fairway | G_wind | H_wind_current |
|---|---|---|---|---|---|---|---|
| other | 25438 | 3115 | 2909 | 4427 | 2732 | 2740 | 2737 |
| cargo | 18578 | 3966 | 4957 | 14234 | 3674 | 3688 | 3682 |
| tanker | 9437 | 4371 | 5038 | 15246 | 4076 | 4101 | 4120 |
| service | 3907 | 12528 | 6496 | 6211 | 6399 | 6417 | 6434 |
| passenger | 1711 | 12513 | 10502 | 13022 | 7993 | 8003 | 7953 |
| unknown | 443 | 5023 | 4127 | 12692 | 3197 | 3191 | 3197 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (674 vessels) | seen_vessels (74 vessels) |
|---|---|---|
| C_location - A_motion | +5069 (+4413 to +5809) | +8232 (+6784 to +9823) |
| E_fairway - A_motion | -704 (-839 to -597) | -857 (-1098 to -663) |
| G_wind - A_motion | -691 (-827 to -582) | -844 (-1078 to -654) |
| H_wind_current - A_motion | -692 (-828 to -582) | -837 (-1073 to -644) |
| A_motion - cv | -166 (-635 to +219) | +324 (-30 to +690) |
