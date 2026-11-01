# Residual GBM context ablation (transfer_test, skagen; 316,680 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 1889 (1659–2179) | 4719 (4206–5349) | 94 | 278 | 843 | 1609 | 3034 |
| A_motion | 1842 (1717–1989) | 4526 (4304–4789) | 88 | 270 | 833 | 1593 | 2966 |
| B_vessel | 1838 (1720–1971) | 4541 (4315–4785) | 87 | 265 | 825 | 1575 | 2966 |
| C_location | 2611 (2461–2777) | 6342 (6048–6624) | 128 | 451 | 1341 | 2255 | 4152 |
| D_all | 2440 (2313–2570) | 6187 (5922–6442) | 117 | 330 | 1067 | 2278 | 3789 |
| E_fairway | 1570 (1435–1732) | 3842 (3605–4109) | 84 | 249 | 736 | 1370 | 2519 |
| F_all_fairway | 1539 (1430–1673) | 3764 (3576–3978) | 83 | 247 | 730 | 1355 | 2456 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -46 (-203 to +68) | -193 (-637 to +133) |
| B_vessel - cv | -51 (-231 to +82) | -178 (-650 to +196) |
| C_location - cv | +722 (+576 to +861) | +1623 (+1189 to +2025) |
| D_all - cv | +551 (+379 to +708) | +1468 (+987 to +1915) |
| E_fairway - cv | -318 (-450 to -214) | -877 (-1265 to -574) |
| F_all_fairway - cv | -349 (-507 to -218) | -955 (-1395 to -588) |
| B_vessel - A_motion | -5 (-37 to +25) | +15 (-75 to +100) |
| C_location - A_motion | +769 (+701 to +845) | +1816 (+1643 to +2002) |
| D_all - A_motion | +598 (+543 to +666) | +1661 (+1482 to +1860) |
| E_fairway - A_motion | -272 (-317 to -229) | -684 (-799 to -580) |
| F_all_fairway - A_motion | -303 (-350 to -263) | -762 (-893 to -661) |

Paired error differences at earlier horizons (m, 95% CI, vessel bootstrap):

| comparison | Δerr@5 | Δerr@10 | Δerr@20 | Δerr@30 | Δerr@45 |
|---|---|---|---|---|---|
| A_motion - cv | -6 (-7 to -5) | -8 (-12 to -5) | -11 (-49 to +17) | -16 (-130 to +66) | -68 (-338 to +133) |
| B_vessel - cv | -7 (-8 to -5) | -13 (-20 to -7) | -19 (-72 to +20) | -35 (-172 to +69) | -68 (-377 to +161) |
| C_location - cv | +34 (+31 to +37) | +173 (+157 to +191) | +498 (+444 to +553) | +646 (+550 to +740) | +1117 (+875 to +1343) |
| D_all - cv | +23 (+20 to +25) | +52 (+44 to +59) | +224 (+169 to +271) | +669 (+525 to +802) | +755 (+454 to +1007) |
| E_fairway - cv | -10 (-12 to -8) | -29 (-39 to -22) | -107 (-143 to -78) | -239 (-324 to -169) | -516 (-736 to -346) |
| F_all_fairway - cv | -11 (-13 to -8) | -31 (-42 to -22) | -114 (-161 to -74) | -254 (-370 to -158) | -579 (-853 to -356) |
| B_vessel - A_motion | -1 (-1 to -0) | -5 (-8 to -2) | -8 (-24 to +5) | -18 (-49 to +8) | +0 (-54 to +51) |
| C_location - A_motion | +39 (+36 to +42) | +182 (+166 to +198) | +508 (+469 to +554) | +663 (+600 to +732) | +1186 (+1082 to +1303) |
| D_all - A_motion | +28 (+26 to +30) | +60 (+54 to +67) | +235 (+209 to +266) | +685 (+624 to +759) | +823 (+744 to +913) |
| E_fairway - A_motion | -4 (-6 to -3) | -21 (-28 to -16) | -97 (-118 to -79) | -223 (-265 to -180) | -448 (-530 to -366) |
| F_all_fairway - A_motion | -5 (-7 to -3) | -23 (-31 to -16) | -103 (-126 to -84) | -238 (-279 to -205) | -511 (-589 to -449) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 91800 | 3601 | 3846 | 4028 | 6234 | 6133 | 3182 | 3142 |
| 0.5–1 | 17583 | 4930 | 4918 | 4729 | 6088 | 5913 | 4123 | 3944 |
| 1–2 | 12686 | 6194 | 5777 | 5465 | 6750 | 6391 | 4850 | 4608 |
| 2–5 | 11510 | 7337 | 6317 | 6048 | 6859 | 6673 | 5604 | 5409 |
| 5–10 | 5813 | 8662 | 6464 | 6160 | 7116 | 6784 | 5918 | 5859 |
| 10–inf | 7563 | 8313 | 5554 | 5244 | 6177 | 5935 | 5241 | 5359 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 56546 | 3883 | 4217 | 4300 | 7229 | 7020 | 3277 | 3310 |
| other | 48553 | 3425 | 3768 | 3721 | 4223 | 4250 | 3460 | 3322 |
| tanker | 26135 | 4594 | 4756 | 4963 | 6987 | 6975 | 3895 | 4082 |
| service | 10376 | 12595 | 6807 | 5983 | 7888 | 6907 | 7277 | 6034 |
| passenger | 4871 | 11096 | 9560 | 10165 | 10337 | 9990 | 6585 | 6830 |
| unknown | 474 | 5990 | 4673 | 4743 | 7097 | 7018 | 4111 | 4406 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (938 vessels) | seen_vessels (434 vessels) |
|---|---|---|
| B_vessel - A_motion | -2 (-118 to +109) | +72 (+15 to +125) |
| C_location - A_motion | +1455 (+1306 to +1640) | +3021 (+2801 to +3249) |
| D_all - A_motion | +1337 (+1161 to +1554) | +2746 (+2566 to +2927) |
| E_fairway - A_motion | -613 (-770 to -485) | -920 (-998 to -852) |
| F_all_fairway - A_motion | -736 (-906 to -604) | -851 (-942 to -763) |
| A_motion - cv | -357 (-876 to +69) | +352 (+276 to +427) |
