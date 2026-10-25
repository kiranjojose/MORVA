# Residual GBM context ablation (transfer_val, skagen; 316,680 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 1982 (1696–2337) | 4940 (4283–5714) | 100 | 295 | 891 | 1694 | 3182 |
| A_motion | 1953 (1793–2140) | 4807 (4500–5158) | 94 | 287 | 883 | 1686 | 3143 |
| B_vessel | 1951 (1800–2118) | 4842 (4524–5210) | 94 | 282 | 866 | 1669 | 3144 |
| C_location | 2876 (2688–3081) | 6984 (6622–7368) | 139 | 497 | 1484 | 2469 | 4578 |
| D_all | 2578 (2409–2750) | 6106 (5773–6446) | 119 | 438 | 1160 | 2258 | 4286 |
| E_fairway | 1604 (1437–1798) | 3935 (3647–4261) | 89 | 261 | 762 | 1401 | 2555 |
| F_all_fairway | 1570 (1426–1735) | 3883 (3624–4156) | 88 | 259 | 753 | 1372 | 2478 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -29 (-214 to +119) | -133 (-644 to +284) |
| B_vessel - cv | -31 (-246 to +136) | -99 (-703 to +365) |
| C_location - cv | +894 (+703 to +1069) | +2044 (+1499 to +2538) |
| D_all - cv | +595 (+384 to +770) | +1165 (+618 to +1623) |
| E_fairway - cv | -379 (-544 to -243) | -1005 (-1467 to -616) |
| F_all_fairway - cv | -413 (-614 to -252) | -1058 (-1599 to -613) |
| B_vessel - A_motion | -2 (-41 to +33) | +35 (-82 to +139) |
| C_location - A_motion | +923 (+830 to +1023) | +2177 (+1963 to +2413) |
| D_all - A_motion | +625 (+554 to +699) | +1299 (+1135 to +1471) |
| E_fairway - A_motion | -350 (-427 to -284) | -872 (-1059 to -713) |
| F_all_fairway - A_motion | -384 (-463 to -328) | -924 (-1154 to -766) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 28472 | 3769 | 4106 | 4341 | 6901 | 5847 | 3270 | 3239 |
| 0.5–1 | 5171 | 5163 | 5287 | 5162 | 6918 | 6064 | 4240 | 4126 |
| 1–2 | 3696 | 6492 | 6315 | 5979 | 7569 | 6745 | 5020 | 4900 |
| 2–5 | 3394 | 7901 | 6856 | 6402 | 7531 | 7108 | 5774 | 5578 |
| 5–10 | 1771 | 9189 | 6759 | 6348 | 7473 | 7271 | 6298 | 6213 |
| 10–inf | 2367 | 8697 | 5434 | 5028 | 6072 | 5994 | 5165 | 5338 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 18081 | 4056 | 4570 | 4546 | 8032 | 6578 | 3356 | 3361 |
| other | 13662 | 3248 | 3745 | 3938 | 4479 | 4230 | 3391 | 3353 |
| tanker | 7103 | 4823 | 5224 | 5397 | 7942 | 6858 | 4132 | 4322 |
| service | 3882 | 11719 | 6262 | 5588 | 7479 | 7069 | 6675 | 5912 |
| passenger | 1979 | 11625 | 9790 | 10076 | 10159 | 9944 | 6743 | 6535 |
| unknown | 164 | 7345 | 6765 | 7816 | 8667 | 8558 | 5797 | 6491 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (392 vessels) | seen_vessels (267 vessels) |
|---|---|---|
| B_vessel - A_motion | +24 (-132 to +171) | +60 (-32 to +151) |
| C_location - A_motion | +1679 (+1460 to +1938) | +3314 (+3067 to +3568) |
| D_all - A_motion | +916 (+744 to +1097) | +2171 (+1961 to +2388) |
| E_fairway - A_motion | -780 (-1047 to -562) | -1081 (-1183 to -979) |
| F_all_fairway - A_motion | -886 (-1195 to -665) | -1012 (-1134 to -876) |
| A_motion - cv | -397 (-1245 to +188) | +467 (+371 to +554) |
