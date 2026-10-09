| model | metric | mean (95% CI, vessel bootstrap) | median | p90 | n |
|---|---|---|---|---|---|
| persistence | ade_m | 2899 (2763–3046) | 3007 | 4539 | 62982 / 692 vessels |
| persistence | fde_m | 5413 (5159–5694) | 5664 | 8570 | 62982 / 692 vessels |
| persistence | err_5min_m | 1419 (1353–1490) | 1471 | 2216 | 62982 / 692 vessels |
| persistence | err_10min_m | 2792 (2661–2933) | 2900 | 4377 | 62982 / 692 vessels |
| persistence | err_20min_m | 5413 (5159–5694) | 5664 | 8570 | 62982 / 692 vessels |
| cv | ade_m | 640 (581–703) | 270 | 1728 | 62982 / 692 vessels |
| cv | fde_m | 1574 (1431–1722) | 744 | 4154 | 62982 / 692 vessels |
| cv | err_5min_m | 160 (144–176) | 41 | 465 | 62982 / 692 vessels |
| cv | err_10min_m | 510 (462–559) | 159 | 1479 | 62982 / 692 vessels |
| cv | err_20min_m | 1574 (1431–1722) | 744 | 4154 | 62982 / 692 vessels |
| ctrv | ade_m | 837 (769–905) | 422 | 2210 | 62982 / 692 vessels |
| ctrv | fde_m | 2042 (1893–2185) | 1134 | 5151 | 62982 / 692 vessels |
| ctrv | err_5min_m | 213 (190–236) | 63 | 575 | 62982 / 692 vessels |
| ctrv | err_10min_m | 672 (611–733) | 264 | 1861 | 62982 / 692 vessels |
| ctrv | err_20min_m | 2042 (1893–2185) | 1134 | 5151 | 62982 / 692 vessels |
| ctrv_damped | ade_m | 643 (583–707) | 275 | 1729 | 62982 / 692 vessels |
| ctrv_damped | fde_m | 1578 (1435–1727) | 753 | 4156 | 62982 / 692 vessels |
| ctrv_damped | err_5min_m | 163 (147–180) | 44 | 466 | 62982 / 692 vessels |
| ctrv_damped | err_10min_m | 514 (464–565) | 167 | 1480 | 62982 / 692 vessels |
| ctrv_damped | err_20min_m | 1578 (1435–1727) | 753 | 4156 | 62982 / 692 vessels |

Paired difference vs CV on identical windows (model − CV, m; negative = better). Damped-CTRV tau = 30 s, tuned on train.

| model | ΔADE (95% CI) | ΔFDE (95% CI) |
|---|---|---|
| persistence | +2259 (+2099 to +2427) | +3839 (+3511 to +4182) |
| ctrv | +197 (+180 to +214) | +468 (+420 to +513) |
| ctrv_damped | +3 (+1 to +5) | +4 (+1 to +7) |
