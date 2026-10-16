# 06 — Results

The first sections report validation results from 1–3 October 2026. The final section reports the single test run on
4–6 October, performed after the hypothesis freeze. The test split is now closed to further model development.
Sources are the versioned tables under `results/tables/`.

## E2: Kinematic baselines (62,982 windows, 692 vessels)
| Model | ADE (m) | FDE@20 min (m) |
|---|---|---|
| Persistence | 2,899 | 5,413 |
| Constant velocity (CV) | **640** | **1,574** |
| CTRV | 837 | 2,042 |
| Damped CTRV (τ tuned on train) | 643 | 1,578 |

Extrapolating the current turn rate makes predictions worse (+468 m FDE vs CV). Turns in this area rarely persist
over 20 minutes.

## E3/E4: Learned residual model and context ablation
| Model | Features | FDE@20 min (m) | vs CV |
|---|---|---|---|
| A | motion | 1,273 | −19% |
| B | + vessel (type group, length, beam, draught) | 1,131 | −28% |
| C | + location (position, course) | 864 | −45% |
| D | all | **827** | **−47%** |

Stable across seeds 0–2 (sd ≤ 5.3 m).

## Generalisation: vessel-held-out evaluation
Training without any validation vessel (109,866 train windows), compared with a random training subset of the same size:

| FDE@20 min (m) | Full training | Same-size random subset | **Vessel-held-out** |
|---|---|---|---|
| CV | 1,574 | 1,574 | 1,574 |
| A motion | 1,272 | 1,295 | 1,452 |
| B + vessel | 1,130 | 1,157 | 1,435 |
| C + location | 865 | 904 | 1,171 |
| D all | 823 | 861 | **1,163 (−26% vs CV)** |

- **Location context generalises to vessels never seen in training** (−281 m vs motion-only, 95% CI −312 to −252).
- **Vessel attributes do not measurably help new vessels** (−17 m, CI −35 to +1). Their gain in the standard setup comes
  from recognising known vessels.
- Cargo and tanker gains are unchanged under held-out (D: 553 / 642 m); passenger-vessel gains mostly disappear (944 →
  2,162 m). Ferry prediction relies on having seen the same route operator.

## E2–E4 by past-only manoeuvring regime (`results/tables/regimes_val.md`)
Regime shares (val): steady 52%, turning 23%, low-speed 16%, combined 7%, speed-changing 2%.

| FDE@20 min (m) | Low-speed | Steady | Turning | Speed-changing | Combined |
|---|---|---|---|---|---|
| CV | 1,587 | 1,190 | 1,836 | 2,734 | 3,104 |
| CTRV | 1,788 | 1,301 | **3,257** | 2,971 | 3,800 |
| A motion | 1,072 | 1,105 | 1,501 | 2,028 | 1,959 |
| D all | 871 | 656 | 927 | 1,449 | 1,448 |

- **H1-direction:** motion-only learning helps most outside steady transit (A − CV: steady −85 m; combined −1,145 m).
- **Location (C − A)** improves every regime (−170 to −511 m), largest when turning. Holds in **50/50** regime ×
  threshold-sensitivity cells (95% CI excluding zero).
- **Vessel-held-out:** location still helps strongly for steady (−358 m) and turning (−362 m), less for combined
  (−135 m), and **not at low speed** (+24 m, CI 0 to +48). Harbour and low-speed behaviour seems to be vessel- or
  route-specific. Vessel attributes help little for unseen vessels and **hurt at low speed** (+66 m).

## RQ7/H4: Spatially held-out evaluation (`results/tables/gbm_ablation_val_spatialheldout.md`)
Each validation window is predicted by a model trained without its longitude band (4 bands, 3 km buffer).

| FDE@20 min (m) | In-area (standard) | Vessel-held-out | **Spatially held-out** |
|---|---|---|---|
| CV | 1,574 | 1,574 | 1,574 |
| A motion | 1,272 | 1,452 | 1,477 |
| B + vessel | 1,130 | 1,435 | 1,452 |
| C + location (raw lat/lon) | 865 | 1,171 | **2,599** |
| D all | 823 | 1,163 | 1,922 |

- **Raw coordinates do not transfer to unseen waters. They harm** (C − A = +1,122 m), because route corrections learned
  elsewhere are applied in the wrong place. The harm is largest in steady transit and at the edge bands.
- **Motion-only learning transfers** (−97 m vs CV); vessel attributes help when turning (−109 m) but not overall.
- So the strong in-area location gain is memorised geography, not transferable knowledge. Transferable geographic
  representations (fairway geometry, coast, bathymetry) are the next research step (V2).

---

# TEST RESULTS: single run after hypothesis freeze (4–6 Oct 2026; 57,068 windows)
Run 11 Oct 2026, 20:24–20:46 UTC, after the freeze commit `f8ded2d`. Every model trained on the train split only, exactly
as for validation. Sources: `results/tables/*_test*.md`, `results/tables/regimes_test.md`.

| FDE@20 min (m) | In-area | Unseen vessels | Unseen waters |
|---|---|---|---|
| CV | 1,554 | 1,554 | 1,554 |
| A motion | 1,267 | 1,429 | 1,465 |
| B + vessel | 1,128 | 1,367 | 1,442 |
| C + location | 863 | 1,165 | **2,592** |
| D all | **831 (−47%)** | 1,140 (−27%) | 1,918 (+23%) |

Kinematic baselines vs CV (ΔFDE): CTRV +467 m, damped CTRV +2 m, Kalman +0 m. Seeds 0–2: sd ≤ 3.6 m.
Validation and test agree to within ~25 m on every headline number.

## Hypothesis outcomes (test)
| | Frozen hypothesis | Evidence (ΔFDE@20, 95% CI, vessel bootstrap) | Outcome |
|---|---|---|---|
| H1 | Motion-only learning beats CV; largest gain in non-steady regimes | A − CV −287 (−380 to −195); steady −88 vs turning −316, low-speed −485, speed-changing −756, combined −1,078 | **Supported** |
| H2 | Vessel context helps beyond motion; more when turning or changing speed than in steady transit | B − A −138 (−176 to −103); turning −216 (−275 to −157) vs steady −75 (−107 to −48); speed-changing −119 (−191 to −45), CI overlaps steady | **Supported in-area** (turning clearly; speed-changing directionally). Shrinks for unseen vessels (−62, −84 to −41) and vanishes in unseen waters (−23, −51 to +9) |
| H3 | Geographic > vessel context in turning and combined | C − B turning −295 (−327 to −263); combined −132 (−188 to −75) | **Supported** (in-area) |
| H4 | Geographic gain decreases in unseen areas but stays positive | spatial C − A **+1,127** (+1,031 to +1,229) | **Rejected**: the gain reverses |
| H4b | Raw-coordinate context does not transfer; motion-only still beats CV (validation-informed) | spatial C − A +1,127; A − CV −89 (−137 to −39) | **Supported** |

Location context improves FDE in all 50 regime × threshold-sensitivity cells in-area (test), as on validation.
