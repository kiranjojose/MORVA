# 06 — Results

This file has two parts. **V1** (below) reports validation results from 1–3 October 2026 and the single V1 test run on
4–6 October; sources are under `results/tables/`. **V2** (at the end) reports the fairway-context study with two
independent waterways, validated on 1–6 October and tested once on 7–15 October; sources are under
`results/v2/tables/`. Both test periods are closed to further model development.

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

- **V1-H1 direction:** motion-only learning helps most outside steady transit (A − CV: steady −85 m; combined −1,145 m).
- **Location (C − A)** improves every regime (−170 to −511 m), largest when turning. Holds in **50/50** regime ×
  threshold-sensitivity cells (95% CI excluding zero).
- **Vessel-held-out:** location still helps strongly for steady (−358 m) and turning (−362 m), less for combined
  (−135 m), and **not at low speed** (+24 m, CI 0 to +48). Harbour and low-speed behaviour seems to be vessel- or
  route-specific. Vessel attributes help little for unseen vessels and **hurt at low speed** (+66 m).

## RQ7/V1-H4: Spatially held-out evaluation (`results/tables/gbm_ablation_val_spatialheldout.md`)
Each validation window is predicted by a model trained without its longitude band (4 bands, 3 km buffer).

| FDE@20 min (m) | In-area (standard) | Vessel-held-out | **Spatially held-out** |
|---|---|---|---|
| CV | 1,574 | 1,574 | 1,574 |
| A motion | 1,272 | 1,452 | 1,477 |
| B + vessel | 1,130 | 1,435 | 1,452 |
| C + location (raw lat/lon) | 865 | 1,171 | **2,599** |
| D all | 823 | 1,163 | 1,922 |

- **Raw coordinates do not transfer to held-out longitude bands. They harm** (C − A = +1,122 m), because route corrections learned
  elsewhere are applied in the wrong place. The harm is largest in steady transit and at the edge bands.
- **Motion-only learning transfers** (−97 m vs CV); vessel attributes help when turning (−109 m) but not overall.
- So the strong in-area location gain is memorised geography, not transferable knowledge. This result motivated V2's
  evaluation of fairway-relative context.

---

# TEST RESULTS: single run after hypothesis freeze (4–6 Oct 2026; 57,068 windows)
Run 11 Oct 2026, 20:24–20:46 UTC, after the freeze commit `f8ded2d`. Every model trained on the train split only, exactly
as for validation. Sources: `results/tables/*_test*.md`, `results/tables/regimes_test.md`.

| FDE@20 min (m) | Home | Home: unseen vessels | Home: held-out longitude bands |
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
| V1-H1 | Motion-only learning beats CV; largest gain in non-steady regimes | A − CV −287 (−380 to −195); steady −88 vs turning −316, low-speed −485, speed-changing −756, combined −1,078 | **Supported** |
| V1-H2 | Vessel context helps beyond motion; more when turning or changing speed than in steady transit | B − A −138 (−176 to −103); turning −216 (−275 to −157) vs steady −75 (−107 to −48); speed-changing −119 (−191 to −45), CI overlaps steady | **Supported in-area** (turning clearly; speed-changing directionally). Shrinks for unseen vessels (−62, −84 to −41) and vanishes in held-out longitude bands (−23, −51 to +9) |
| V1-H3 | Geographic > vessel context in turning and combined | C − B turning −295 (−327 to −263); combined −132 (−188 to −75) | **Supported** (in-area) |
| V1-H4 | Geographic gain decreases in unseen areas but stays positive | spatial C − A **+1,127** (+1,031 to +1,229) | **Rejected**: the gain reverses |
| V1-H4b | Raw-coordinate context does not transfer; motion-only still beats CV (validation-informed) | spatial C − A +1,127; A − CV −89 (−137 to −39) | **Supported** |

Location context improves FDE in all 50 regime × threshold-sensitivity cells in-area (test), as on validation.

---

# V2: FAIRWAY CONTEXT AND INDEPENDENT WATERWAYS

Models are trained on the home area (19–30 Sep) only, with the same hyperparameters as V1. Bornholm and Skagen are
never used for training; their fairway maps come from their own AIS in the same training period. Feature sets:
E = motion + fairway (35 features), F = motion + vessel + fairway (39 features); see `docs/04_methods.md`, "V2".
Confidence intervals are paired, vessel-grouped bootstrap 95% intervals, as in V1.

Settings are labelled by the kind of evidence they provide:

- **Home: chronological test**: later days, same waters;
- **Home: unseen vessels**: every evaluated vessel removed from training;
- **Home: held-out longitude bands**: local spatial extrapolation within the home area (as in V1);
- **Independent waterway: Bornholm / Skagen**: transfer to separate geographic regions.

## Validation (1–6 Oct; seed 0)

| FDE@20 min (m) | Home | Home: held-out longitude bands | Independent waterway: Bornholm | Independent waterway: Skagen |
|---|---:|---:|---:|---:|
| CV | 1,563 | 1,563 | 583 | 877 |
| A motion | 1,271 | 1,466 | 584 | 856 |
| C + raw location | 861 | 2,552 | 1,778 | 1,335 |
| E + fairway | 795 | 1,028 | 474 | 766 |

These results informed the V2 hypotheses.

## Freeze, amendments and test access

| Step | Date (UTC) | Commit | Content |
|---|---|---|---|
| V2 hypotheses frozen | 21 Oct 06:15 | `da2ed78` | V2-H1 and V2-H2, validation-informed |
| Pre-test amendment 1 | 21 Oct | `3575154` | Explicit decision rules; V2-H2 rule strengthened; test configuration and commands pinned |
| Reporting code extended | 21 Oct | `9491f7d` | Regime report covers models A–F and the waterways; pinned code for the test run |
| Pre-test amendment 2 | 21 Oct | `e0437e9` | Regime-reporting change recorded; reason for the V2-H2 change; original rule kept as sensitivity analysis |
| Single test run | 21 Oct 20:51–22:05 | `e0437e9` | 13 prespecified commands, each run once, no reruns |

No V2 `test` or `transfer_test` model results were inspected before the test run.

**V2-H2 amendment.** Before test evaluation, the V2-H2 rule was strengthened from the original directional reading
("C does not reduce mean FDE@20", which an inconclusive result would satisfy) to requiring the lower bound of the
paired 95% CI for C − A to exceed zero in both waterways. The reason was that the original rule could be met without
evidence. The conclusion is unchanged under the original rule.

**Seed.** The hypotheses were decided on seed 0, the configuration seed fixed before the test run. Seeds 1 and 2 are
a sensitivity analysis only.

## TEST RESULTS: single run after the V2 freeze (7–15 Oct 2026)

Windows (vessels): home 167,533 (1,209); Bornholm 55,561 (904); Skagen 97,396 (1,011).

**Mean FDE@20 (m), seed 0**

| Model | Home: chronological test | Home: unseen vessels | Home: held-out longitude bands | Independent waterway: Bornholm | Independent waterway: Skagen |
|---|---:|---:|---:|---:|---:|
| CV | 1,566 | 1,566 | 1,566 | 569 | 846 |
| A motion | 1,292 | 1,462 | 1,483 | 585 | 844 |
| B + vessel | 1,152 | 1,419 | 1,458 | 592 | 822 |
| C + raw location | 872 | 1,205 | 2,572 | 1,816 | 1,320 |
| D all (raw location) | 851 | 1,186 | 1,954 | 2,026 | 1,183 |
| E + fairway | 802 | 1,010 | 1,031 | **459** | 749 |
| F all (fairway) | **768** | **1,003** | **1,030** | 470 | **740** |

**Median / 90th percentile FDE@20 (m), seed 0**

| Model | Home: chronological test | Home: unseen vessels | Home: held-out longitude bands | Independent waterway: Bornholm | Independent waterway: Skagen |
|---|---:|---:|---:|---:|---:|
| CV | 754 / 4,105 | 754 / 4,105 | 754 / 4,105 | 170 / 1,552 | 257 / 2,380 |
| A motion | 694 / 3,193 | 772 / 3,742 | 834 / 3,647 | 213 / 1,543 | 314 / 2,258 |
| C + raw location | 416 / 2,104 | 511 / 3,250 | 2,206 / 4,841 | 1,285 / 3,935 | 848 / 2,659 |
| E + fairway | 336 / 1,961 | 377 / 2,815 | 455 / 2,648 | 190 / 1,028 | 316 / 1,811 |
| F all (fairway) | 330 / 1,859 | 392 / 2,732 | 463 / 2,649 | 197 / 1,058 | 316 / 1,776 |

The waterways differ in intrinsic difficulty: CV error is much lower in Bornholm and Skagen, where most traffic is
straight transit. In relative terms E reduces mean FDE@20 against A by 38% at home, 22% in Bornholm and 11% in Skagen.
Error distributions are right-skewed (means well above medians). In the waterways, E mainly shortens the tail: the
Bornholm p90 falls from 1,543 m (A) to 1,028 m (E), while the median changes little. CV has the lowest Bornholm median
(170 m), so E's mean gain there comes from fewer large errors, not from typical windows.

## Hypothesis outcomes (test)

| | Frozen hypothesis and decision rule | Evidence (ΔFDE@20, 95% CI, vessel bootstrap) | Outcome |
|---|---|---|---|
| V2-H1 | E improves on A at home and in each waterway; CI upper bound < 0 in all three | home −490 (−523 to −457); Bornholm −127 (−157 to −106); Skagen −95 (−123 to −74) | **Supported** |
| V2-H2 | C is worse than A in both waterways (amended rule); CI lower bound > 0 in both | Bornholm +1,231 (+1,142 to +1,320); Skagen +476 (+429 to +528) | **Supported**; also supported under the original rule |

Validation and test paired differences agreed within 17 m for the three V2-H1 comparisons and within 37 m for the two
V2-H2 comparisons (Bornholm C − A: +1,194 validation, +1,231 test), without changing any hypothesis outcome.

## Robustness (prespecified)

| E − A, ΔFDE@20 (m, 95% CI) | Value |
|---|---|
| Home: unseen vessels | −453 (−476 to −427) |
| Independent waterway: Bornholm, evaluated vessels removed from training | −126 (−152 to −106) |
| Independent waterway: Skagen, evaluated vessels removed from training | −103 (−132 to −81) |
| Home: held-out longitude bands | −452 (−494 to −416) |

C − A in held-out longitude bands is +1,090 m (+1,004 to +1,185), reproducing V1-H4b on new days.

- **Seeds 0–2 (sensitivity):** A and E vary by at most 2 m in every setting. C is unstable in the waterways
  (Bornholm 1,816 / 1,816 / 2,218 m; Skagen 1,320 / 1,279 / 1,229 m). This is consistent with tree extrapolation
  outside the training coordinate range, but the seed results alone do not establish that mechanism.
- **Regimes** (primary regime analysis, `results/v2/tables/regimes_*test*.md`): E − A has a CI below 0 in every regime
  of every setting except Skagen low-speed, which showed no detectable difference (+9 m, CI −15 to +32). The largest
  waterway gains are in turning (Bornholm −223, Skagen −317) and combined manoeuvres (−484, −271). C − A is negative in
  every home regime but positive in steady, turning and speed-changing in both waterways.
- **Threshold sensitivity:** each setting has 50 cells (10 regime-threshold configurations × 5 regimes), 150 in all.
  E − A has a CI below 0 in 140 of 150 cells (all 50 at home, all 50 in Bornholm, 40 in Skagen) and a lower point
  estimate in 142. In Skagen, all 10 cells without a CI below 0 are low-speed: 9 are inconclusive and one (low-speed
  threshold 3 kn) favours A (+37 m, CI +13 to +64). C − A has a CI above 0 in 32 Bornholm and 31 Skagen cells and below
  0 in none. The cells reuse the same windows and differ only in regime assignment, so they are correlated: the grid
  shows that the conclusion does not depend on one threshold configuration, and is a descriptive robustness check, not
  150 independent tests.

## Exploratory (no claim)

- Home E − C: −70 m (mean difference only; not a prespecified comparison).
- F − E: home −35, Bornholm +11, Skagen −10 m. F had no frozen comparison; vessel attributes add little once fairway
  context is present.
- Bornholm: motion-only learning does not improve on CV (A − CV +16 m), whereas E does (E − CV −110 m, −144 to −86).

The V2 test period is now spent. Further development uses validation data only and is reported as post hoc.
