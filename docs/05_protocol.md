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
