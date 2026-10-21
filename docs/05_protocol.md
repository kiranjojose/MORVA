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

