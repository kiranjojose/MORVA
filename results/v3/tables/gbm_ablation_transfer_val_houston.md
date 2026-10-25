# Residual GBM context ablation (transfer_val, houston; 316,680 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 2747 (2479–3054) | 6086 (5571–6709) | 188 | 552 | 1509 | 2574 | 4290 |
| A_motion | 2167 (2034–2321) | 4580 (4348–4844) | 170 | 492 | 1286 | 2111 | 3345 |
| B_vessel | 2436 (2291–2604) | 5406 (5149–5695) | 173 | 507 | 1367 | 2301 | 3815 |
| C_location | 3848 (3696–3997) | 9049 (8692–9408) | 231 | 710 | 2032 | 3288 | 6117 |
| D_all | 3192 (3063–3324) | 7200 (6976–7444) | 215 | 667 | 1693 | 2927 | 5092 |
| E_fairway | 2217 (2070–2407) | 4768 (4497–5098) | 160 | 426 | 1256 | 2108 | 3589 |
| F_all_fairway | 2269 (2107–2466) | 5044 (4762–5400) | 146 | 430 | 1231 | 2210 | 3597 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -580 (-757 to -418) | -1505 (-1942 to -1123) |
| B_vessel - cv | -310 (-483 to -161) | -679 (-1132 to -278) |
| C_location - cv | +1101 (+835 to +1346) | +2963 (+2274 to +3569) |
| D_all - cv | +445 (+228 to +629) | +1115 (+537 to +1587) |
| E_fairway - cv | -530 (-677 to -382) | -1318 (-1675 to -972) |
| F_all_fairway - cv | -477 (-613 to -347) | -1041 (-1409 to -715) |
| B_vessel - A_motion | +269 (+216 to +326) | +826 (+684 to +972) |
| C_location - A_motion | +1681 (+1557 to +1806) | +4469 (+4144 to +4785) |
| D_all - A_motion | +1025 (+953 to +1094) | +2620 (+2414 to +2814) |
| E_fairway - A_motion | +50 (+14 to +101) | +187 (+103 to +305) |
| F_all_fairway - A_motion | +102 (+45 to +171) | +464 (+321 to +622) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 17275 | 4364 | 4062 | 4995 | 10591 | 7832 | 4768 | 5019 |
| 0.5–1 | 4818 | 5297 | 4545 | 5361 | 9617 | 7526 | 4795 | 5078 |
| 1–2 | 5989 | 6459 | 5205 | 5853 | 9954 | 7575 | 5296 | 5456 |
| 2–5 | 11278 | 7187 | 5564 | 5947 | 8683 | 7013 | 5193 | 5266 |
| 5–10 | 7262 | 7403 | 5156 | 5925 | 7929 | 6888 | 4870 | 5034 |
| 10–inf | 7810 | 7278 | 3315 | 4738 | 6164 | 5878 | 3639 | 4454 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| service | 35695 | 5513 | 4016 | 4915 | 7491 | 6716 | 4302 | 4604 |
| unknown | 6812 | 6900 | 4567 | 5878 | 7963 | 6843 | 4683 | 5375 |
| tanker | 5035 | 7795 | 7835 | 7829 | 18165 | 9856 | 7875 | 7371 |
| passenger | 2658 | 8468 | 4536 | 5730 | 9988 | 8850 | 4142 | 5130 |
| other | 2570 | 4911 | 3878 | 4345 | 8599 | 5976 | 4121 | 4301 |
| cargo | 1662 | 7883 | 8048 | 7818 | 18542 | 10280 | 7716 | 7115 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (771 vessels) | seen_vessels (5 vessels) |
|---|---|---|
| B_vessel - A_motion | +828 (+694 to +990) | -36 (-1039 to +1302) |
| C_location - A_motion | +4450 (+4156 to +4757) | +12545 (+4895 to +14851) |
| D_all - A_motion | +2622 (+2416 to +2829) | +1950 (-3311 to +2675) |
| E_fairway - A_motion | +188 (+98 to +307) | -157 (-2516 to +327) |
| F_all_fairway - A_motion | +467 (+320 to +639) | -651 (-1020 to -131) |
| A_motion - cv | -1509 (-1955 to -1139) | -83 (-2485 to +827) |
