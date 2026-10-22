# Residual GBM context ablation (transfer_test, bornholm, vessel-held-out; 197,673 train windows)

| model | ADE m (95% CI) | FDE@20 m (95% CI) | err@5 | err@10 |
|---|---|---|---|---|
| cv | 233 (203–271) | 569 (498–661) | 63 | 186 |
| A_motion | 233 (206–266) | 589 (527–668) | 59 | 179 |
| B_vessel | 236 (209–269) | 595 (535–672) | 59 | 182 |
| C_location | 817 (770–873) | 1845 (1745–1962) | 190 | 745 |
| D_all | 793 (755–838) | 1764 (1690–1857) | 239 | 702 |
| E_fairway | 196 (173–222) | 463 (412–523) | 56 | 162 |
| F_all_fairway | 201 (178–228) | 477 (426–538) | 56 | 164 |

Paired differences on identical windows (m, negative = first model better), vessel bootstrap:

| comparison | ΔADE | ΔFDE |
|---|---|---|
| A_motion - cv | +0 (-7 to +5) | +20 (+0 to +36) |
| B_vessel - cv | +4 (-5 to +11) | +26 (+4 to +46) |
| C_location - cv | +584 (+544 to +624) | +1276 (+1188 to +1362) |
| D_all - cv | +561 (+527 to +594) | +1195 (+1126 to +1259) |
| E_fairway - cv | -37 (-50 to -27) | -106 (-141 to -81) |
| F_all_fairway - cv | -32 (-45 to -22) | -92 (-130 to -65) |
| B_vessel - A_motion | +3 (-1 to +8) | +7 (-6 to +20) |
| C_location - A_motion | +584 (+546 to +621) | +1256 (+1177 to +1334) |
| D_all - A_motion | +561 (+531 to +593) | +1175 (+1116 to +1233) |
| E_fairway - A_motion | -37 (-46 to -30) | -126 (-152 to -106) |
| F_all_fairway - A_motion | -32 (-43 to -24) | -112 (-141 to -90) |

Mean FDE@20 min (m) by past turn rate (°/min):

| turn_bin | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | 44511 | 434 | 464 | 481 | 1824 | 1738 | 363 | 379 |
| 0.5–1 | 3682 | 876 | 900 | 895 | 1910 | 1799 | 674 | 687 |
| 1–2 | 2801 | 935 | 991 | 947 | 1964 | 1912 | 728 | 736 |
| 2–5 | 2726 | 847 | 912 | 856 | 1819 | 1843 | 690 | 688 |
| 5–10 | 656 | 2021 | 1831 | 1740 | 2150 | 2003 | 1612 | 1575 |
| 10–inf | 1185 | 2382 | 1907 | 1911 | 2036 | 1957 | 1767 | 1784 |

Mean FDE@20 min (m) by ship group:

| ship_group | n | cv | A_motion | B_vessel | C_location | D_all | E_fairway | F_all_fairway |
|---|---|---|---|---|---|---|---|---|
| cargo | 35398 | 404 | 431 | 436 | 1687 | 1654 | 325 | 337 |
| tanker | 10066 | 483 | 513 | 522 | 2006 | 1976 | 404 | 425 |
| passenger | 4764 | 1538 | 1547 | 1594 | 3169 | 2544 | 1183 | 1225 |
| other | 2694 | 1018 | 1068 | 1047 | 1659 | 1579 | 997 | 990 |
| service | 2516 | 929 | 792 | 776 | 1147 | 1209 | 707 | 691 |
| unknown | 123 | 309 | 327 | 329 | 1199 | 1246 | 327 | 332 |

ΔFDE@20 min (m) for vessels NOT seen in training vs vessels seen in training:

| comparison | unseen_vessels (904 vessels) |
|---|---|
| B_vessel - A_motion | +7 (-6 to +20) |
| C_location - A_motion | +1256 (+1177 to +1334) |
| D_all - A_motion | +1175 (+1116 to +1233) |
| E_fairway - A_motion | -126 (-152 to -106) |
| F_all_fairway - A_motion | -112 (-141 to -90) |
| A_motion - cv | +20 (+0 to +36) |
