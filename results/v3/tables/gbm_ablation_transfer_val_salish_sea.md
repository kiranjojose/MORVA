# Residual GBM context ablation (transfer_val, salish_sea; 316,680 train windows)

| model | ADE m (95% CI) | FDE@60 m (95% CI) | err@5 | err@10 | err@20 | err@30 | err@45 |
|---|---|---|---|---|---|---|---|
| cv | 5130 (4401–5869) | 11347 (9838–12901) | 308 | 951 | 2716 | 4783 | 8131 |
| A_motion | 3677 (3223–4162) | 7547 (6664–8466) | 274 | 835 | 2200 | 3640 | 5706 |
| B_vessel | 4004 (3532–4508) | 8363 (7424–9324) | 280 | 850 | 2292 | 3787 | 6418 |
| C_location | 5933 (5580–6334) | 13537 (12741–14512) | 387 | 1206 | 3329 | 5370 | 9167 |
| D_all | 4826 (4435–5255) | 10153 (9440–10915) | 342 | 1142 | 2730 | 4655 | 7645 |
| E_fairway | 3061 (2671–3475) | 6368 (5608–7172) | 229 | 671 | 1798 | 2982 | 4795 |
| F_all_fairway | 3222 (2818–3645) | 6911 (6126–7760) | 229 | 673 | 1819 | 3089 | 5051 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | -1453 (-1810 to -1081) | -3800 (-4691 to -2854) |
| B_vessel - cv | -1126 (-1437 to -801) | -2983 (-3826 to -2155) |
| C_location - cv | +804 (+223 to +1508) | +2191 (+644 to +3916) |
| D_all - cv | -304 (-684 to +111) | -1194 (-2184 to -186) |
| E_fairway - cv | -2068 (-2459 to -1669) | -4979 (-5983 to -3986) |
| F_all_fairway - cv | -1907 (-2293 to -1536) | -4436 (-5404 to -3526) |
| B_vessel - A_motion | +327 (+201 to +448) | +816 (+462 to +1173) |
| C_location - A_motion | +2256 (+1909 to +2642) | +5990 (+5006 to +7028) |
| D_all - A_motion | +1149 (+954 to +1332) | +2606 (+2062 to +3094) |
| E_fairway - A_motion | -616 (-691 to -546) | -1179 (-1357 to -1014) |
| F_all_fairway - A_motion | -455 (-587 to -341) | -636 (-1048 to -248) |

Mean FDE@60 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 11009 | 7340 | 6614 | 7093 | 17025 | 10118 | 5273 | 5537 |
| 0.5–1 | 3698 | 10063 | 7666 | 8413 | 14122 | 10114 | 6547 | 7037 |
| 1–2 | 3996 | 11451 | 8441 | 9003 | 13713 | 10384 | 6964 | 7360 |
| 2–5 | 5844 | 13537 | 8905 | 9586 | 12568 | 10534 | 7456 | 7810 |
| 5–10 | 4054 | 14946 | 8538 | 9793 | 10138 | 10263 | 7575 | 8332 |
| 10–inf | 5646 | 15075 | 6539 | 8063 | 9674 | 9610 | 5972 | 7238 |

Mean FDE@60 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| passenger | 14235 | 17664 | 9781 | 11208 | 11268 | 12097 | 8438 | 9455 |
| service | 10478 | 5999 | 4874 | 5389 | 10943 | 7533 | 4086 | 4544 |
| cargo | 5372 | 8726 | 8545 | 8488 | 21963 | 11104 | 6787 | 6259 |
| other | 2263 | 7321 | 5354 | 6291 | 16271 | 8771 | 4723 | 5656 |
| tanker | 1337 | 6067 | 6142 | 6225 | 20845 | 9958 | 4771 | 4589 |
| unknown | 562 | 4877 | 3430 | 4022 | 10468 | 6663 | 2896 | 3399 |

ΔFDE@60 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (373 vessels) | seen_vessels (2 vessels) |
|---|---|---|
| B_vessel - A_motion | +816 (+496 to +1163) | +866 (-173 to +931) |
| C_location - A_motion | +5989 (+4935 to +6962) | +8476 (+347 to +8984) |
| D_all - A_motion | +2607 (+2123 to +3073) | -150 (-5045 to +156) |
| E_fairway - A_motion | -1178 (-1370 to -1017) | -2917 (-3140 to +648) |
| F_all_fairway - A_motion | -635 (-1041 to -233) | -3472 (-3610 to -1265) |
| A_motion - cv | -3801 (-4752 to -2829) | -1317 (-1353 to -737) |
