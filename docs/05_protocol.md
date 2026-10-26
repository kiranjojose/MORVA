# 05 — Protocol and hypothesis provenance

## Primary question
Does vessel and geographic context improve 5-, 10- and 20-minute vessel trajectory prediction over transparent
kinematic and motion-only learned baselines, and does the improvement vary by manoeuvring regime?

**First-paper scope:** past-only manoeuvring-regime evaluation of vessel and geographic context for 5–20 minute AIS
trajectory prediction in constrained Danish waters.

## Supporting questions
| RQ | Question | Status |
|---|---|---|
| RQ1 | How sensitive are the number and composition of usable windows to segmentation, gap and filter choices? | done (E0) |
| RQ2 | How accurate are persistence, CV, CTRV, damped CTRV and a Kalman filter at 5/10/20 min? | complete |
| RQ3 | How does error change across low-speed, steady, turning, speed-changing and combined regimes? | complete |
| RQ4 | Does a motion-only learned model improve over CV, and in which regimes and horizons? | complete |
| RQ5 | Do vessel type and size improve prediction beyond motion, particularly when turning or changing speed? | complete for V1 |
| RQ6 | Does geographic context improve prediction beyond motion, particularly near bends, ports, junctions? | raw-coordinate study complete; transferable features are V2 |
| RQ7 | Do improvements survive later time periods, unseen vessels and spatially held-out areas? | complete for V1 |

Secondary (later paper): can context-conditioned prediction residuals detect unusual behaviour better than fixed
speed, course and route-deviation thresholds?

## Split
Whole-day time blocks: train 19–30 Sep, val 1–3 Oct, **test 4–6 Oct**. A window belongs to a block only if its
full span lies inside it. Scalers, thresholds and tuning use train only (damped-CTRV τ tuned on train). Robustness:
vessel-held-out training with a same-size random-subset control and spatially held-out evaluation. The test split was
used once after the hypothesis freeze and is now closed to further model development.

## Hypotheses (FROZEN 2026-10-11)
> **Transparency note:** these hypotheses were drafted on 11 Oct 2026 **after** the validation analysis
> (`docs/06_results.md`) and frozen before the single test-set run. Numerical thresholds were not selected from test
> results.

- **H1 (learned motion):** a motion-only learned model reduces mean FDE@20 min relative to CV, with the largest
  improvement in non-steady regimes.
- **H2 (vessel context):** adding vessel type and dimensions improves prediction relative to motion-only, with a larger
  effect during turning and speed-changing than during steady transit.
- **H3 (geographic context):** adding geographic context produces a larger improvement than vessel-only context during
  turning and combined manoeuvres.
- **H4 (generalisation):** improvements from geographic context decrease under spatially held-out evaluation but remain
  positive if the features capture transferable fairway geometry rather than memorised coordinates.
- **H4b (raw-coordinate transfer), added after the spatial validation result:** geographic context represented by raw
  coordinates (latitude, longitude, course) does **not** transfer to unseen areas. Under spatially held-out evaluation
  it does not improve, and may worsen, FDE@20 min relative to the motion-only model, while the motion-only model
  still improves on CV.

> **Provenance of H4 / H4b.** H4 was drafted on 11 Oct 2026, before the spatially held-out run. On validation, that
> run contradicted H4 with raw coordinates (C − A = +1,122 m FDE@20; `results/tables/gbm_ablation_val_spatialheldout.md`,
> commit `8e851c0`). H4 is kept unchanged and will be reported as tested. H4b was added afterwards (see the
> research log) and is **validation-informed**, so the test set was its first independent check.

**FROZEN on 2026-10-11 20:24 UTC. Hypothesis text as of commit `9d4d83c`.** No changes to H1–H4b were made after this
point. The test split was accessed after the freeze, once per experiment, with `--confirm-test`.

## Test-set status
`baselines --split test --confirm-test` and the corresponding GBM evaluations were run once after freezing. The test
split is spent. Any further development uses validation or new data; any unavoidable rerun must be reported with its
reason in the research log.

## V2 split (set 2026-10-18)
Set before any V2 feature work and before the new days were ingested. Defined in `configs/experiment.yaml` and
`configs/data.yaml`.

**Time blocks** (whole UTC days, a window must lie entirely inside one block):

| Block | Days | Role |
|---|---|---|
| train | 19–30 Sep (12) | Model fitting. Unchanged from V1 so V1 and V2 models are directly comparable |
| val | 1–6 Oct (6) | Development and model selection. Merges the V1 validation days with the spent V1 test days |
| test | 7–15 Oct (9) | **Locked.** Downloaded and ingested only after this split was set |

Windows ending after 16 Oct 00:00 UTC are excluded, so files downloaded later cannot enter the test block unnoticed.

**Regions.** The home area (Great Belt / Øresund / southern Kattegat) is the only area used for training. Two
independent waterways are ingested with the same pipeline but never contribute to model fitting:

| Region | Box | Why |
|---|---|---|
| Bornholm | 54.7–55.6° N, 14.0–15.6° E | Bornholmsgat traffic separation scheme. A constrained waterway with a home-like cargo, tanker and passenger mix; about 65 km east of the home area |
| Skagen | 57.2–58.0° N, 9.6–11.2° E | Skagen corner and Skagerrak entrance. A different waterway type (open-sea bend, more fishing); about 110 km north |

Windows in these regions are labelled `transfer_context` (training days), `transfer_val` (validation days) or
`transfer_test` (test days). `transfer_context` may support context built from historical traffic, such as V2
traffic-flow maps, because such history would exist for any real waterway. It is never used to fit model weights.
`transfer_test` is locked in the same way as `test`.

**Evaluation settings for V2:** home val/test (in-area), home val/test with vessel hold-out (unseen vessels), the V1
longitude-band hold-out (unseen bands), and transfer val/test (unseen waterways). About half of the vessels in
Bornholm also appear in the home area. Unseen-waterway results should therefore also be reported with the
`--holdout-eval-vessels` option, so that neither the waterway nor the vessels have been seen.

## V2 hypotheses (FROZEN 2026-10-21)

> **Transparency note:** these hypotheses were drafted after inspecting V2 validation results for the home area,
> unseen longitude bands, Bornholm and Skagen (research log, 18 Oct 2026). They are therefore
> **validation-informed**, not fully prospective. Neither V2 `test` nor `transfer_test` model outcomes were inspected
> before this freeze; those splits provide the first independent evaluation of these claims.

- **V2-H1 (transferable fairway context):** relative to the motion-only model A, adding historical-traffic fairway
  context (model E) reduces mean FDE@20 min in the home area and in each independent transfer waterway, Bornholm and
  Skagen, evaluated separately.
- **V2-H2 (raw coordinates do not transfer):** relative to model A, adding raw geographic coordinates (model C) does
  not reduce mean FDE@20 min in either independent transfer waterway, Bornholm or Skagen, evaluated separately.

The primary contrasts are `E_fairway - A_motion` for V2-H1 and `C_location - A_motion` for V2-H2. A reduction means
a negative paired mean FDE@20 difference. Each setting is reported separately with a paired 95% bootstrap confidence
interval; results are not pooled across waterways. Home and transfer evaluations that remove every evaluated vessel
from training, and results by manoeuvring regime and horizon, are prespecified robustness analyses rather than
additional headline hypotheses. Model F is exploratory: V2 does not make a confirmatory claim that vessel attributes
improve on E.

**FROZEN on 2026-10-21 06:15 UTC, before any V2 `test` or `transfer_test` model evaluation.** After this point the
hypothesis wording, primary contrasts and evaluation settings must not change in response to test outcomes. Any test
access or unavoidable rerun must be recorded in `docs/08_research_log.md`.

## V2 pre-test amendment (2026-10-21)

> Added after the freeze above and **before any V2 `test` or `transfer_test` model evaluation**. It does not change
> the wording of V2-H1, the primary contrasts or the evaluation settings. It makes the decision rules, the test-run
> configuration and the robustness analyses explicit, and states V2-H2 in a falsifiable form. The frozen text above
> is kept unchanged so the original freeze remains visible.

**Decision rules.** All intervals are paired, vessel-grouped bootstrap 95% CIs of the mean FDE@20 min difference on
identical windows, reported separately for each setting.

- **V2-H1** is supported only if the upper CI bound of `E_fairway − A_motion` is below 0 in all three settings:
  home, Bornholm and Skagen. Because every setting must succeed, no multiple-comparison correction is applied. If
  only some settings succeed, V2-H1 is reported as not supported, with the per-setting results.
- **V2-H2** is tested in the stronger form that raw coordinates make prediction worse in an independent waterway:
  it is supported only if the lower CI bound of `C_location − A_motion` is above 0 in both Bornholm and Skagen. A
  result whose CI includes 0 does not support V2-H2. This replaces the weaker reading of "does not reduce", which an
  inconclusive result would satisfy.

**Test-run configuration.**

- Code and configuration are those of commit `02a2c6c` (unchanged at the freeze commit `da2ed78`): split, fairway
  map settings, feature sets and GBM settings.
- All models are trained once on the train block (19–30 Sep) only. Fairway maps use the training period of each
  region only. Nothing is retrained or re-tuned on validation data.
- The headline results use seed 0 (the configuration seed). Seeds 1 and 2 are run for the primary settings and
  reported as a stability check only; they do not decide the hypotheses.
- Each command below is run once with `--confirm-test`, and each run is recorded in `docs/08_research_log.md`.

| Purpose | Command |
|---|---|
| Baselines, home | `morva baselines --split test --confirm-test` |
| Baselines, each waterway | `morva baselines --split transfer_test --region {bornholm,skagen} --confirm-test` |
| V2-H1 / V2-H2, home | `morva gbm --split test --seeds 0 1 2 --confirm-test` |
| V2-H1 / V2-H2, each waterway | `morva gbm --split transfer_test --region {bornholm,skagen} --seeds 0 1 2 --confirm-test` |
| Robustness: unseen vessels, home | `morva gbm --split test --holdout-eval-vessels --confirm-test` |
| Robustness: unseen vessels, each waterway | `morva gbm --split transfer_test --region {bornholm,skagen} --holdout-eval-vessels --confirm-test` |
| Robustness: unseen longitude bands | `morva gbm --split test --spatial-holdout --confirm-test` |

**Robustness analyses (prespecified, not headline hypotheses).**

- Removing every evaluated vessel from training, in the home area and in each waterway.
- Unseen longitude bands within the home area, the V2 counterpart of V1-H4. The band's historical traffic remains in
  its fairway map by design; only the model weights have not seen the band.
- Breakdowns by past turn rate (the turn-rate bins written by every `gbm` run) and by horizon (errors at 5, 10 and
  20 min). The five-regime report from V1 is not extended for V2.

**Exploratory, not confirmatory.**

- `F_all_fairway − E_fairway` (vessel attributes beyond fairway context), as already stated above.
- `E_fairway − C_location` in the home area. On validation, E was better than raw coordinates even in-area
  (795 vs 861 m); this comparison is reported descriptively and makes no claim.

## V2 pre-test amendment 2 (2026-10-21)

> Added after amendment 1 and **before any V2 `test` or `transfer_test` model evaluation**. The frozen hypothesis
> text and amendment 1 above are kept unchanged. This amendment changes the reporting implementation and pins a new
> commit; it does not change model fitting, prediction generation, regime assignment, metrics or the decision rules
> in amendment 1.

**Regime-reporting coverage.** The regime-reporting implementation (`morva regime-report`) originally supported
models A–D in the home area only. Before test-set evaluation it was extended so that the prespecified
manoeuvring-regime analysis covers every evaluated model (A–F) in every setting: the home area, Bornholm and Skagen.
The model list is read from the configuration; the vessel-held-out and longitude-band sections are included when
those runs exist (longitude bands apply to the home area only); `--region` and the transfer splits are supported;
and test splits require `--confirm-test`. The five past-only regimes, their thresholds and the threshold-sensitivity
configurations are unchanged. The past-turn-rate bins written by every `gbm` run remain a supplementary breakdown;
the five-regime report is the primary regime analysis.

Before this amendment the change was checked on validation data and synthetic data only: the window-weighted regime
means reproduce each run's overall FDE@20 exactly (for example, E in Bornholm: 474 m in both), all tests pass, and
the synthetic end-to-end run includes the report for the home area and a transfer waterway.

- Affected files: `src/morva/cli.py` (regime reporting only), `tests/test_core.py`, `Makefile` (smoke steps).
- Old pinned commit: `02a2c6c`. New pinned commit: `9491f7d`, which replaces `02a2c6c` in the test-run
  configuration of amendment 1. Code and configuration must not change again before the test run.

**Additional test-run commands**, each run once after the `gbm` and `baselines` runs listed in amendment 1:

| Purpose | Command |
|---|---|
| Regimes, home | `morva regime-report --split test --confirm-test` |
| Regimes, each waterway | `morva regime-report --split transfer_test --region {bornholm,skagen} --confirm-test` |

**V2-H2: reason for the stronger rule, and the original rule as a sensitivity analysis.** The decision rule for
V2-H2 was strengthened in amendment 1; the claim itself, that raw coordinates (model C) do not transfer to an
independent waterway, is unchanged. The original wording, "does not reduce mean FDE@20", would be satisfied by an
underpowered or inconclusive result: a confidence interval that includes 0 would count as support. The amended rule
requires positive evidence of harm (the lower CI bound of `C_location − A_motion` above 0 in both waterways), so it
is harder, not easier, to support. The change was motivated by this weakness alone, without reference to any test
result.

The primary V2-H2 conclusion follows the amended rule. As a secondary sensitivity analysis, the report also states
the conclusion under the original rule (supported if the upper CI bound of `C_location − A_motion` is at or above 0
in both waterways, i.e. no detectable reduction), so readers can see whether the interpretation depends on the
amendment.

## Hypothesis naming in combined documents (added 2026-10-22, after both test runs)

The V1 hypotheses above are written H1–H4b and the V2 hypotheses V2-H1 and V2-H2. In documents covering both stages
(README, results, summary) the V1 hypotheses are referred to as V1-H1 to V1-H4b, so that, for example, V1-H2 (vessel
context) is never confused with V2-H2 (raw-coordinate negative transfer). The frozen text above is unchanged.

## V3 hypotheses (FROZEN 2026-10-26)

> **Status:** frozen before test access. Drafted on 25 Oct 2026 after the V3 validation runs (research log,
> 24/25 Oct), edited and frozen on 26 Oct, so these hypotheses are **validation-informed**, not preregistered before
> model development. No V3 test data had been downloaded or inspected at the freeze. The draft V3-H1 to V3-H3 in
> `docs/00_plan.md` are replaced as described under "Changes from the plan".

**Setting and models.** As fixed in `configs/v3/`: models trained on the home area, 19 Sep–6 Oct 2026; flow maps
from each region's own training block; the locked test period is 16–29 Oct (2026 for Danish regions, 2025 for US
regions). E = motion + fairway, A = motion only, C = motion + raw location. Hypotheses are decided on seed 0. All
confidence intervals are paired and vessel-grouped (1,000 bootstrap resamples), as in V2.

**Primary hypotheses**

- **V3-H1 (cross-country transfer):** in the Salish Sea, E improves on A at 20 and 60 minutes.
  *Decision rule:* the upper bound of the 95% CI of the paired difference E − A is below 0 at both horizons.
  *Validation:* −402 m at 20 min (−458 to −356); −1,179 m at 60 min (−1,357 to −1,014).
- **V3-H2 (raw coordinates across countries):** in the Salish Sea, C is worse than A at 20 and 60 minutes.
  *Decision rule:* the lower bound of the 95% CI of C − A is above 0 at both horizons.
  *Validation:* +1,128 m at 20 min (+965 to +1,325) and +5,990 m at 60 min (+5,006 to +7,028).
- **V3-H3 (local calibration):** conformal boxes from model E, calibrated on the evaluated region's own calibration
  days (12–15 Oct), have **marginal empirical coverage** within 3 percentage points of nominal for 80% and 90% boxes
  at 20 and 60 minutes in each of Bornholm, Skagen and the Salish Sea.
  *Decision rule:* all 12 point estimates (3 regions × 2 levels × 2 horizons) lie within ±3 points of nominal.
  Coverage means aggregate (marginal) coverage over all windows of a region, not coverage within ship types, regimes
  or locations.
  *Validation:* 78.2–81.2% for 80% boxes and 88.9–91.2% for 90% boxes.
- **V3-H4 (home calibration at home):** home-calibrated E boxes have coverage within 3 percentage points of nominal
  for 80% and 90% boxes at 20 and 60 minutes in the home area. This is marginal empirical coverage, not a claim of
  conditional or operational calibration.
  *Decision rule:* all 4 point estimates within ±3 points. *Validation:* 79.5, 79.1, 89.7 and 89.4%.

**Prespecified descriptive analyses (no confirmatory claim)**

- Home-calibrated coverage in each independent waterway, to show how much calibration shifts between waters
  (validation: from 38% to 86% for 80% boxes).
- Houston: E vs A overall, merchant-only (cargo and tanker) and by ship group. Validation showed a small benefit at
  20 min (−30 m, −55 to −3) that reversed at 60 min (+187 m, +103 to +305).
- E vs A at 20 and 60 minutes in Bornholm and Skagen, with the relative gain at each horizon.
- Interval half-widths of E vs A at equal coverage (local calibration).
- Home area: C vs E at 20 and 60 minutes (validation: E better at 20, C better at 60).
- Absolute interval half-widths as well as coverage, because nominal coverage does not establish operational utility.
- In validation, the calibration days (12–15 Oct) follow the evaluated model-selection days (7–11 Oct). In the locked
  test evaluation (16–29 Oct), the calibration days precede the evaluated days, as they would in deployment.

**Changes from the plan (all made after validation, before any test access)**

- *Plan V3-H1* (home-calibrated coverage within ±3 points at home, Bornholm and Skagen) is split. Coverage at home
  becomes V3-H4. Coverage in new waters becomes V3-H3 with **local** calibration, because validation showed that home
  calibration does not transfer (Bornholm over-covers, Skagen under-covers at 60 min, the US areas under-cover
  strongly). Home-calibrated coverage in new waters is kept as a descriptive analysis.
- *Plan V3-H2* (E improves on A in the Salish Sea at 20 and 60 min) is kept as V3-H1.
- *Plan V3-H3* (E's relative gain is larger at 60 than at 20 minutes in the independent waterways) is dropped as a
  hypothesis: validation contradicted it in the Salish Sea (18% → 16%). It becomes descriptive.
- *New* V3-H2 extends the V2 raw-coordinate result to another country. At the freeze it was strengthened to require
  negative transfer at both 20 and 60 minutes after the 20-minute paired intervals were computed on validation, using
  the reporting-only per-horizon intervals added in `0eed614`.
- Map-history (RQ4) and junction features (RQ5) are dropped from V3. The map-history option is configured but not
  implemented, and no junction representation exists. Adding either after inspecting the main validation results
  would expand the study and delay the locked test. They remain future exploratory work and will not be run on the
  V3 validation or test splits as part of this protocol.

## V3 frozen implementation and test pass

**Completed prerequisite:** paired confidence intervals at every forecast horizon were added on 25 Oct in commit
`0eed614`. The pinned code for the test run is `ba7032c`, a later commit containing that reporting change.

**Pinned code and configuration:** commit `ba7032c`. This includes the per-horizon paired-difference reporting added
in `0eed614` and the V3 validation write-up. The only subsequent change before test access is this protocol freeze;
model code, feature definitions, configurations, regions, splits, hypotheses and decision rules must not change.

**Data preparation (run once, before the test pass).** Download DMA daily files 2026-10-16 to 2026-10-29 and Marine
Cadastre daily files 2025-10-16 to 2025-10-29; verify each against the provider's byte size and archive integrity;
record manifests (`morva manifest`, with `--source marinecadastre` for US files). Then run, with the V3
configurations: `ingest`, `clean`, `windows`, `fairway`. This rebuilds all splits from the same code and
configuration. Training windows, flow maps and model settings are unchanged; windows at the 15/16 Oct boundary may
change slightly because tracks no longer end at the data boundary. The train, validation and calibration window
counts are recorded before and after, and any difference is reported. Test-period data become available only after
DMA publishes 29 Oct (expected about 1 Nov 2026); the test pass runs once all 28 test files are present.

The following 12 commands form one test pass. They are run once, in this order, from the repository root. Every command
uses the frozen V3 data and experiment configurations. `--confirm-test` is required and each start/end time, exit
status and output run directory is recorded in `docs/08_research_log.md`.

```bash
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml baselines --split test --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml baselines --split transfer_test --region bornholm --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml baselines --split transfer_test --region skagen --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml baselines --split transfer_test --region salish_sea --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml baselines --split transfer_test --region houston --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml gbm --split test --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml gbm --split transfer_test --region bornholm --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml gbm --split transfer_test --region skagen --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml gbm --split transfer_test --region salish_sea --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml gbm --split transfer_test --region houston --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml intervals --split test --feature-set E_fairway --sweep --confirm-test
uv run morva --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml intervals --split test --feature-set A_motion --sweep --confirm-test
```

The `intervals --sweep` commands evaluate the home test split and every configured transfer region with both home and
local calibration; they therefore cover V3-H3, V3-H4 and the prespecified interval comparisons without separate
region commands. Seed 0 is the only confirmatory point-model seed. No test-time tuning, rerun after a successful
command, model selection or threshold adjustment is permitted. A failed command may be rerun only after its cause is
documented and only if no result from that command was produced or inspected.

**FROZEN on 2026-10-26 before downloading or inspecting any V3 test-period data.** The test and `transfer_test` splits
are now available only for the single pass above. All later analyses are post-freeze and must be labelled exploratory.

