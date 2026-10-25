# 08 — Research log

Dated entries. Keep failed attempts.

## 2026-10-09 (Fri)
- Repo scaffolded: pipeline ingest → clean → segment → windows → time-block split → baselines (persistence/CV/CTRV) → vessel-bootstrap evaluation.
- 11 unit tests pass; end-to-end smoke test on SYNTHETIC data works.
- Synthetic observation (not a finding): CTRV beats CV at 5 min but is worse at 20 min when turns are short-lived. Check on real data whether to damp the turn rate over time.
- Next: download the first DMA day, write the manifest, inspect the header and reporting intervals, and pick the AOI.

## 2026-10-09 (Fri), first real data
- File: `aisdk-2026-10-05.zip` (Mon 5 Oct 2026, DMA, 621 MB zipped / 3.16 GB CSV). Manifest with SHA-256 in `data/manifests/`.
- Header matches the expected DMA schema (26 columns). Timestamps run 00:00:00–23:59:58, consistent with one UTC day.
- AOI (provisional box): 2.97 M rows, 481 MMSIs, Class A only.
- **~47% of rows are exact full-row duplicates** (1.41 M). Another 4,159 (MMSI, t) groups have conflicting positions; the first row is kept under the V1 rule. A provenance-based conflict rule remains future data-quality work.
- Invalid MMSIs excluded: one transmitter with MMSI < 1e6 (44k rows) and two 111xxxxxx SAR aircraft (16k rows).
- SOG sentinel 102.3: 13.7k rows. Median report interval 10 s, p99 180 s.
- **Bug fixed:** DMA writes ship type "Undefined" on rows without a merged static message, which could win the per-vessel mode. It is now treated as missing. Metadata coverage on windows ≈ 97% (type and length).
- 542 segments / 441 vessels → 18.5k windows. The split is within one day (auto fractions, PROVISIONAL), so vessels overlap between splits. Not usable for claims.
- Early VALIDATION-ONLY observation (one day, provisional): CV beats CTRV at every horizon (ADE 564 m vs 763 m; FDE@20 min 1418 m vs 1904 m). The turn-rate estimate from COG is probably too noisy, or turns don't persist. Idea for later: damp the turn rate over the horizon.
- Decision: download 14 consecutive days (22 Sep – 5 Oct 2026) and use whole-day time blocks.

## 2026-10-09 (Fri), full study period ingested
- 18 DMA daily files, 2026-09-19 to 2026-10-06, with manifests (SHA-256) for all of them. Pipeline run time 8 min, peak memory 6.5 GB.
- Ingest now removes exact full-row duplicates per file and logs them (`results/tables/ingest_log.json`): 63.3 M rows in AOI → 33.8 M exact duplicates removed (53%) → 29.5 M rows, 2,185 MMSIs.
- Quality stage: 128.7k partial duplicates (same MMSI+t, different values), 222.5k rows with invalid MMSI, 1,085 speed spikes, 13.2k SOG > 40 kn.
- Segmentation (gap 20 min): 5,933 segments from 2,071 vessels.
- Split FROZEN (explicit whole days): train 19–30 Sep, val 1–3 Oct, test 4–6 Oct (locked). Windows: train 238,830 / val 62,982 / test 57,068; excluded 858 (straddling midnight boundaries).
- Vessel overlap: 448 vessels in both train and val, 381 in both train and test. This is expected for regular traffic (ferries, liners) under a time split. A vessel-held-out robustness slice is planned.
- Validation baselines (692 vessels): ADE persistence 2,899 m, **CV 640 m (95% CI 581–703)**, CTRV 837 m (769–905). FDE@20 min: CV 1,574 m, CTRV 2,042 m. CV beats CTRV at every horizon; this held from 1 to 18 days. Next: paired difference CI, then breakdown by regime and ship type.
- The one-day pipeline-check runs in `results/runs/20261009T1246*` and `T1256*` are superseded (provisional intra-day split) and kept for the record only.

## 2026-10-09 (Fri, evening), regime exploration (train+val only)
- First turn measure (mean |dCOG| per min) mostly measured COG jitter: median 5.1°/min at 1–5 kn. Replaced it with the NET course change over 10 min (signed sum), and cross-checked against course from positions only: 31.3% vs 34.5% of 10–15 kn windows above 1°/min, correlation 0.58. So the turning is real, not a COG artefact.
- Share of windows by net past turn rate: >1°/min 42%, >2°/min 31%, >5°/min 16%. The AOI is manoeuvring-heavy (strait bends, ferry terminals, port approaches; see `regime_turn_hotspots.png`).
- **CTRV vs CV by past turn rate (val FDE@20 min):** nearly equal when straight (<0.5°/min: 1,226 vs 1,145 m); CTRV worst in moderate turns (2–5°/min: 3,380 vs 1,785 m, +1.6 km). Interpretation to test: turns in this area are short (bends), so extrapolating a turn for 20 min overshoots. Whether a turn *continues* depends on where the ship is, which motivates spatial/vessel context.
- Speed distributions differ clearly by ship type (tankers narrow at 10–12 kn; passenger and pilot vessels wide; fishing slow), which supports ship type as a context feature.
- Next decision at this stage: freeze a past-only manoeuvring-regime definition.

## 2026-10-09 (Fri, night), baseline diagnosis + E0 sensitivity
- **Damped CTRV** (turn rate decays as exp(−t/τ)), with τ tuned on 60k TRAIN windows over {30…600 s}: train ADE increases monotonically with τ, so the best τ is 30 s, i.e. essentially CV. Validation, paired vs CV: ΔADE +3 m (+1 to +5), ΔFDE +4 m (+1 to +7). Plain CTRV: ΔADE +197 m (+180 to +214), ΔFDE +468 m (+420 to +513).
- **Is the turn estimate lagging?** Diagnostic on train (40k windows): estimating the turn rate from the last 1, 2 or 5 min, with τ 60 or 300 s. Best case is −15 m vs CV, only in the 1–2°/min bin; everything else is worse. A fresher estimate does not rescue turn extrapolation.
- **Preliminary conclusion (validation):** in this manoeuvring-heavy area, turns rarely persist long enough for kinematic extrapolation to help. Past motion alone cannot tell whether a turn will continue, which motivates spatial context (where the bend ends) and vessel context. This becomes the motivation paragraph for the learned and context models.
- **E0 sensitivity:** see `docs/03_data_card.md`. The retained data is robust to the gap thresholds (<0.1% change for the segmentation gap, ±2% for the window gap). Keeping 20 min / 180 s.
- `clean` now also saves `points_clean.parquet` (pre-segmentation) for threshold experiments.

## 2026-10-10 (Sat), E3/E4: residual GBM context ablation (VALIDATION, preliminary)
- Model: CV forecast + HistGradientBoosting correction in the body frame (along/cross-track) at 5/10/15/20 min, linear interpolation in between, absolute-error loss, seed 0. Trained on all 238,830 train windows; about 50 s per feature set.
- FDE@20 min on val (62,982 windows, 692 vessels): CV 1,574 → A motion 1,273 → B +vessel 1,131 → C +location 864 → D all 827 m (−47% vs CV).
- Paired vs A_motion (vessel bootstrap): B −142 m (−175 to −106), C −409 (−446 to −370), D −446 (−486 to −402).
- **Location helps even when the past turn rate is near zero** (0–0.5°/min: 1,051 → 660 m). It anticipates bends and stops that past motion cannot show, which is consistent with the turn-persistence diagnosis.
- Largest absolute gains for passenger vessels (CV 2,573 → 944 m; ferries stopping and turning at terminals) and cargo/tanker on location (984 → 583, 1,233 → 690).
- **Vessel novelty check (important caveat):** for the 244 val vessels NOT seen in training, location still helps (−391 m, CI −428 to −352), almost as much as for seen vessels (−417). So it is spatial knowledge, not identity. Vessel attributes help unseen vessels only a little (−25 m vs −189 for seen ones): length/beam/draught likely act partly as a vessel fingerprint. Motion-only gains are also much smaller for unseen vessels (−66 vs −396). Seen and unseen vessels are different populations (regular traffic vs occasional visitors), so this mixes novelty with traffic type.
- Next checks identified at this stage: vessel-held-out evaluation, three seeds and the final regime breakdown. These
  were completed in the subsequent runs below.

## 2026-10-10 (Sat, evening), seeds, vessel-held-out and size control (VALIDATION)
- **Seeds 0–2:** FDE@20 sd ≤ 5.3 m for every feature set (A 1,272 / B 1,130 / C 865 / D 823 m). The ablation ranking is not a seed artefact.
- **Vessel-held-out** (all 692 val vessels removed from training; train windows 238,830 → 109,866): FDE@20 CV 1,574 → A 1,452 → B 1,435 → C 1,171 → D 1,163 m (D −411 m vs CV, −26%). Location vs motion −281 m (−312 to −252). **Vessel attributes vs motion −17 m (−35 to +1): no evidence they generalise to new vessels.**
- **Size control** (random 109,866 train windows, seen vessels kept): D 861 m. So training size accounts for ~40 m (823 → 861); vessel/route familiarity accounts for ~300 m (861 → 1,163).
- By ship group, D_all FDE (full / size-control / held-out): cargo 573 / 590 / 553, tanker 680 / 700 / 642, **passenger 944 / 1,015 / 2,162**, service 1,346 / 1,399 / 1,692. Fairway knowledge generalises completely for transiting cargo and tankers. Ferry gains depend on having seen the same ferries (each route is served by few vessels, so holding them out removes the route).
- **Headline (preliminary):** spatial context generalises to unseen vessels (−26% FDE vs CV); vessel attributes add little beyond motion for new vessels; large ferry gains are route familiarity. This is a defensible, nuanced answer to RQ4.

## 2026-10-11 (Sun), regimes and research framing
- Adopted the past-only regime definition (low-speed / steady / turning / speed-changing / combined; last 10 min; net turn ≥ 1°/min; |ΔSOG| ≥ 2 kn; mean SOG < 5 kn), with continuous variables, a reliability safeguard (COG vs position-based turn agreement) and one-at-a-time sensitivity.
- Turn-label reliability: steady 95%, turning 81%, speed-changing 79%, combined 83%.
- Location context improves FDE in every regime and in all 50 regime × sensitivity cells (CI excluding 0). Under vessel-held-out training it does NOT help at low speed (+24 m), and vessel attributes hurt there (+66 m).
- RQ1–RQ7 and draft H1–H4 recorded in `05_protocol.md`, explicitly as drafted after validation and to be frozen before test. Literature reading questions and a working review draft (marked UNVERIFIED) are in `02_literature.md`; literature matrix expanded to 34 columns; R6 authors corrected to Wolsing, Roepert, Bauer & Wehrle (2022).
- New scope from the framing: Kalman-filter baseline (RQ2) and spatially held-out evaluation (RQ7/H4) before 16 Oct; engineered geographic features → V2.

## 2026-10-11 (Sun), Kalman baseline (RQ2)
- CV Kalman filter (state x, y, vx, vy; measurements: 1-min positions plus reported SOG/COG velocity; white-acceleration process noise q tuned on 60k TRAIN windows). Train ADE decreases monotonically with q: 1e-4 → 784 m, 1e-2 → 654 m, 1.0 → 643 m. The best q (largest in the grid) makes the filter follow the latest measurement, so it converges to CV: val paired ΔADE/ΔFDE vs CV = +0 m.
- Interpretation: smoothing over the 20-min history adds lag and does not improve on the latest reported SOG/COG. Together with CTRV and damped CTRV, every kinematic refinement tested collapses to, or loses against, CV. The most recent state is the best kinematic predictor in this area.
- Refactored `gbm` so feature sets can be fitted per spatial fold. Regression check on the synthetic workspace reproduces the earlier numbers exactly (A 1,013 / B 1,007 / C 1,086 / D 1,088 m).

## 2026-10-11 (Sun, night), spatially held-out evaluation (H4, VALIDATION)
- Design: 4 longitude bands (10.4 / 11.05 / 11.7 / 12.35 / 13.0 °E). For each band, train on train-split windows whose whole history+future stays more than 0.05° (~3 km) outside the band; evaluate val windows anchored in the band. Every val window is predicted by a model that never saw its band. Mean train size per fold 164k (size alone explains ~40 m, per the 10 Oct control).
- FDE@20 (all val): CV 1,574; A motion 1,477 (−97 vs CV); B +vessel 1,452; **C +location 2,599 (+1,122 vs A; +1,025 vs CV)**; D all 1,922 (+445 vs A).
- **Raw coordinates do not transfer; they actively harm in unseen areas.** The model applies route corrections learned elsewhere (bends, stops) at the wrong places. The harm is worst in steady transit (+1,414 m) and at the edge bands (fold 0 Great Belt west: C FDE 3,357 vs A 1,481; fold 3 Øresund: 2,250 vs 1,269), and smaller in interior bands (fold 1: 2,029 vs 1,910; fold 2: 1,607 vs 1,502), consistent with trees extrapolating at the edge of the coordinate range.
- Motion-only learning DOES transfer spatially (−97 m vs CV; combined −390, low-speed −206). Vessel attributes: ~0 overall, but −109 m (−159 to −58) when turning.
- **H4 as drafted ("decrease but remain positive") is contradicted on validation with raw lat/lon.** The location gain is memorised geography. This sharpens the research direction: geographic context needs transferable representations (distance/bearing to fairway centreline, coast, bathymetry, bend geometry) rather than coordinates. That is RQ6's "meaningful geographic features" → V2 and the central next research question.
- Note for honesty: H4 was drafted earlier today, BEFORE this run.

## 2026-10-11 (Sun, night), H4b added (option b)
- Decision: keep H4 unchanged and report it as tested; add H4b ("raw-coordinate context does not transfer to unseen areas"), explicitly marked as drafted AFTER the spatial validation result (commit `8e851c0`). Rewriting H4 was rejected because it would hide that the original prediction was wrong.
- The hypotheses are not frozen yet. The freeze (with commit hash) happens before the single test run.

## 2026-10-11 (Sun, 20:24 UTC), HYPOTHESES FROZEN
- H1–H4b frozen as of commit `9d4d83c`. Next: single test-set run of every experiment (baselines, GBM ablation, vessel-held-out, spatially held-out, regime report), each once, with `--confirm-test`.

## 2026-10-11 (Sun, 20:24–20:25 UTC), test run started
- First attempt (20:24:36) failed in argument parsing: the shell loop passed each command as one word (zsh does not word-split variables). The CLI exited before loading any data, so the test split was not accessed. Retried at 20:24:55 with explicit commands.
- Test baselines completed (`results/tables/baselines_test.md`). GBM test runs were started and completed in the
  following logged step.

## 2026-10-11 (Sun, 20:46 UTC), TEST RUN COMPLETE
- All five steps ran once (baselines, GBM 3 seeds, vessel-held-out, spatially held-out, regime report). Validation and test agree within ~25 m on every headline number.
- H1 supported; H2 supported in-area (turning clearly), weaker for unseen vessels (test −62 m, significant here unlike validation −17 m n.s.) and absent in unseen waters; H3 supported (C − B turning −295, combined −132); **H4 rejected** (spatial C − A +1,127 m); H4b supported.
- The test split is now spent. Any further model development uses validation only and is reported as post-hoc.

## 2026-10-18 (Sun), V2 split and independent waterways
- New DMA days 7–15 Oct 2026 were published (DMA posts each file about three days later). They were downloaded only after the V2 split below had been written into the config, so no V2 decision was made with them in view.
- V2 time split: train 19–30 Sep (unchanged), val 1–6 Oct (V1 val + spent V1 test), test 7–15 Oct (locked); `test_end` = 16 Oct 00:00 UTC excludes later windows.
- One-day traffic check on 24 Sep (Class A, already-seen training data) for candidate waterways outside the home box. Moving vessels (SOG > 5 kn) / moving rows: Skagen 262 / 350k, Bornholm 201 / 308k, northern Kattegat 174 / 202k, Little Belt 50 / 67k, Horns Rev 38 / 64k. Vessels also seen in the home area that day: Bornholm 104, northern Kattegat 104, Skagen 60, Little Belt 14, Horns Rev 0.
- Chose **Bornholm** (constrained TSS, home-like traffic mix) as the main unseen waterway and **Skagen** (open-sea bend, more fishing) as a different-type stress test. Rejected Little Belt and Horns Rev (too little traffic), and northern Kattegat (continues the home routes and their through-traffic).
- Pipeline changes: ingest tags `region`; segments never cross regions; transfer windows are labelled `transfer_context/val/test` so every existing `split == "train"` selection stays home-only; `transfer_test` is locked like `test`.
- `clean` and `windows` now process one region at a time (tracks in `data/processed/tracks/<region>.parquet`; vessel attributes keyed by MMSI and region), so peak memory stays near the V1 level and the home area is cleaned exactly as in V1, without points from other areas.
- Regression check: after re-ingesting the 18 V1 days with region tags, home-area rows match the V1 ingest log exactly on every day (0 mismatches).
- Downloaded the 9 new files (several network stalls; resumed downloads checked by size against the DMA listing and by `unzip -t`), checksummed and ingested them. No test-period content was looked at beyond row and window counts.
- **Determinism fix:** `add_flags` used an unstable sort, so the record kept from a conflicting duplicate (same MMSI and timestamp, different values) could change between runs. Found because home train had 238,829 windows against V1's 238,830. The missing window (vessel 219007393, 25 Sep 04:47) depends on a duplicate pair with SOG 1.3 vs 0.2 kn, and the 0.2 kn record puts it below the 1-knot threshold. The sort is now stable, so the first record in file order is always kept (as the docstring said), with a regression test. Two full reruns give identical windows. V1 val counts are identical (62,982). V1 train differs by this one window. V1 test windows rise from 57,068 to 57,079, because segments that used to end at the end of the data now continue into 7 Oct. V1 results are not re-run.
- V2 split counts (windows): home train 238,829 / val 120,412 / test 167,533; Bornholm context 80,760 / val 41,675 / test 55,561; Skagen context 156,175 / val 67,809 / test 97,396. Peak memory for `clean` is 10.1 GB.

## 2026-10-18 (Sun, evening), V1 models on the new validation data (reference for V2)
- Outputs now go to `results/v2/` (`results_dir` in `configs/experiment.yaml`), so V2 runs never overwrite V1 tables. The three V1 tables changed by the split commit were restored from `1c9bcfc`. `baselines` and `gbm` take `--region`, so each waterway is evaluated on its own.
- All runs are validation only (home val 1–6 Oct; transfer_val 1–6 Oct). FDE@20 (m):

| Model | In-area | In-area, unseen vessels | Bornholm | Bornholm, unseen vessels | Skagen | Skagen, unseen vessels |
|---|---:|---:|---:|---:|---:|---:|
| CV | 1,563 | 1,563 | 583 | 583 | 877 | 877 |
| A motion | 1,271 | 1,451 | 584 | 589 | 856 | 860 |
| B + vessel | 1,127 | 1,427 | 595 | 604 | 833 | 837 |
| C + raw location | 861 | 1,189 | 1,778 | 1,945 | 1,335 | 1,292 |
| D all | 835 | 1,179 | 1,983 | 1,631 | 1,197 | 1,184 |

- **Raw coordinates fail on truly independent waterways**, more severely than in the V1 longitude-band test: C − A = +1,194 m (CI +1,089 to +1,297) in Bornholm and +479 m (+434 to +527) in Skagen. Removing the evaluated vessels from training changes little, so this is geography, not vessel familiarity.
- **New finding: motion-only learning gives no gain over CV in the transfer waterways** (A − CV: Bornholm +1 m, −21 to +19; Skagen −21 m, −69 to +13), against −292 m in-area. CV error there is already low (583 m Bornholm, 877 m Skagen) because most traffic is straight transit through a traffic separation scheme or open water. V2 therefore has little room to improve on CV in these waters overall. The realistic test for fairway features is (a) no harm relative to A, and (b) gains in turning and bend regimes. This should shape the V2 hypotheses.
- The in-area vessel-held-out training set falls to 89,705 windows (val now covers 6 days and 1,048 vessels). Part of the in-area unseen-vessel gap is therefore a training-size effect; a same-size random control is needed before interpreting it.

## 2026-10-18 (Sun, night), feature set E: fairway context from historical traffic (VALIDATION)
- `morva fairway` builds a flow map per region from moving track points (≥ 3 kn, one point per vessel-minute) in the region's training period: a 300 m grid × 12 course bins storing counts, course sums and position moments. A query pools a 1.5 km block and ±1 course bin, so only same-direction traffic counts. Features (no absolute coordinates): same-direction density, flow coherence, heading offset from the flow, lateral offset from the flow centroid and lane width at the anchor; flow heading change, lateral offset and density at the constant-velocity positions 5, 10 and 20 min ahead (13 features). Config `fairway:` in `configs/experiment.yaml`.
- Leakage guard: a training window gets a map without the day(s) its own future covers (leave-day-out). Val and transfer windows use the full training-period map. Check: train and val feature distributions match (median |offset| 104 vs 104 m; median |heading| 3.3° vs 3.1°), and the flow bend 20 min ahead correlates equally with the actual turn on train and val (0.23 vs 0.25). When the map shows a bend > 20°, vessels turn the same way 81% (train), 82% (val), 85% (Bornholm), 70% (Skagen) of the time.
- New feature sets: E_fairway = motion + fairway (counterpart of C), F_all_fairway = motion + vessel + fairway (counterpart of D). One seed.
- FDE@20 (m), validation:

| Model | In-area | Unseen longitude bands | Bornholm | Bornholm, unseen vessels | Skagen | Skagen, unseen vessels |
|---|---:|---:|---:|---:|---:|---:|
| CV | 1,563 | 1,563 | 583 | 583 | 877 | 877 |
| A motion | 1,271 | 1,466 | 584 | 589 | 856 | 860 |
| C + raw location | 861 | 2,552 | 1,778 | 1,945 | 1,335 | 1,292 |
| D all (raw location) | 835 | 1,927 | 1,983 | 1,631 | 1,197 | 1,184 |
| **E + fairway** | **795** | **1,028** | **474** | **476** | 766 | 765 |
| F all (fairway) | 757 | 1,024 | 485 | 489 | **757** | **759** |

- E − A (paired, 95% CI): in-area −476 (−509 to −444); unseen bands −438 (−477 to −401); Bornholm −110 (−138 to −89); Skagen −90 (−114 to −69). Unchanged with vessel hold-out (−113, −95). Compare C − A: −409 in-area but +1,085 / +1,194 / +479 in unseen settings.
- **Fairway features keep and exceed the in-area gain of raw coordinates and transfer to unseen waters.** E is better than C even in-area (795 vs 861 m), so the flow map seems to be a better representation of route geometry, not only a more transferable one. In Bornholm, where motion-only learning could not beat CV, E improves on CV by 109 m (19%).
- By past turn rate, E improves on A in every bin and every setting. Steady transit gains too (Bornholm 449 → 356 m), probably from the lateral offset to the lane centre. In unseen bands, C is worst in steady transit (2,401 m) while E is best there (737 m).
- Vessel attributes add little once fairway context is present (F − E: −38 in-area, +11 Bornholm, −9 Skagen).
- Caveats: validation only and one seed; the result informs the V2 hypotheses, which must be frozen before any test run. The unseen-band maps include historical traffic of the held-out band, by design: the model's weights have not seen the band, but its traffic history is treated as available context, as for the transfer waterways.

## 2026-10-21 (Wed), V2 hypothesis freeze
- Reviewed the V2 protocol, data-card extension and all 18 Oct research-log entries before any V2 `test` or `transfer_test` model evaluation.
- Froze two validation-informed headline hypotheses: **V2-H1**, E (motion + fairway) improves on motion-only A in-area and separately in both independent waterways; **V2-H2**, raw-location C does not improve on A in either independent waterway. The exact wording and primary contrasts are in `docs/05_protocol.md`.
- The hypotheses are explicitly **validation-informed** by the 18 Oct `val` and `transfer_val` results, following the provenance treatment used for H4b. Locked-split row/window counts are bookkeeping only and were not used to formulate the claims.
- Prespecified robustness reporting: repeat transfer comparisons after removing evaluated vessels from home training; report manoeuvring-regime and horizon breakdowns. These are not additional headline hypotheses. Model F remains exploratory because validation showed little consistent gain from vessel attributes beyond E.
- **Freeze time: 2026-10-21 06:15 UTC.** No V2 `test` or `transfer_test` model outcomes had been inspected. The next permitted test access is the single recorded confirmatory run.
- **Pre-test amendment (21 Oct, before any test access):** added explicit decision rules (V2-H1 needs the CI upper bound below 0 in home, Bornholm and Skagen; V2-H2 is tested in the stronger form "C − A has a CI lower bound above 0 in both waterways"), pinned the test configuration (commit `02a2c6c`, train-only fitting, seed 0 headline with seeds 1–2 for stability, exact commands), added unseen longitude bands as a prespecified robustness analysis, disclosed the input-only fairway coverage summaries for the locked splits, and listed E − C in-area as exploratory. See `docs/05_protocol.md`, "V2 pre-test amendment". The frozen hypothesis text is unchanged.
- **Pre-test amendment 2 (21 Oct, before any test access):** extended `regime-report` from models A–D in the home area to all six models in the home area, Bornholm and Skagen (reporting only; regimes, thresholds, metrics and decision rules unchanged). Checked on validation: regime means reproduce each run's overall FDE exactly; reports written for `val`, `transfer_val` Bornholm and Skagen. The in-area vessel-held-out validation run was re-run with E and F because the report refused the older A–D run. Pinned commit moves from `02a2c6c` to `9491f7d`. Recorded the reason for the stronger V2-H2 rule (the original rule could be met by an inconclusive result) and added the original rule as a secondary sensitivity analysis. See `docs/05_protocol.md`, "V2 pre-test amendment 2".

## 2026-10-21 (Wed, 20:51–22:05 UTC), V2 TEST RUN COMPLETE
- Single confirmatory pass, exactly as listed in `docs/05_protocol.md` amendments 1 and 2, at commit `e0437e9` (code and configuration identical to pinned `9491f7d`). The four commits up to `e0437e9` were pushed before the run. Each command was run once, all exited 0; no reruns.

| Start (UTC) | End | Command |
|---|---|---|
| 20:51:36 | 20:51:47 | `baselines --split test` |
| 20:51:47 | 20:51:55 | `baselines --split transfer_test --region bornholm` |
| 20:51:55 | 20:52:04 | `baselines --split transfer_test --region skagen` |
| 20:52:04 | 21:08:15 | `gbm --split test --seeds 0 1 2` |
| 21:08:15 | 21:25:56 | `gbm --split transfer_test --region bornholm --seeds 0 1 2` |
| 21:25:56 | 21:41:06 | `gbm --split transfer_test --region skagen --seeds 0 1 2` |
| 21:41:06 | 21:43:53 | `gbm --split test --holdout-eval-vessels` |
| 21:43:53 | 21:47:35 | `gbm --split transfer_test --region bornholm --holdout-eval-vessels` |
| 21:47:35 | 21:51:22 | `gbm --split transfer_test --region skagen --holdout-eval-vessels` |
| 21:51:22 | 22:05:01 | `gbm --split test --spatial-holdout` |
| 22:05:01 | 22:05:04 | `regime-report --split test` |
| 22:05:04 | 22:05:06 | `regime-report --split transfer_test --region bornholm` |
| 22:05:06 | 22:05:09 | `regime-report --split transfer_test --region skagen` |

All with `--confirm-test`. Run folders `results/v2/runs/20261021T2*`; tables in `results/v2/tables/*test*`.

- **V2-H1 SUPPORTED.** `E_fairway − A_motion`, paired FDE@20 (m, 95% CI): home −490 (−523 to −457); Bornholm −127 (−157 to −106); Skagen −95 (−123 to −74). Upper bound below 0 in all three settings.
- **V2-H2 SUPPORTED** under the amended (primary) rule. `C_location − A_motion`: Bornholm +1,231 (+1,142 to +1,320); Skagen +476 (+429 to +528). Lower bound above 0 in both waterways. Sensitivity: also supported under the original rule.
- FDE@20 (m), seed 0:

| Model | Home | Bornholm | Skagen |
|---|---:|---:|---:|
| CV | 1,566 | 569 | 846 |
| A motion | 1,292 | 585 | 844 |
| B + vessel | 1,152 | 592 | 822 |
| C + raw location | 872 | 1,816 | 1,320 |
| D all (raw location) | 851 | 2,026 | 1,183 |
| E + fairway | 802 | 459 | 749 |
| F all (fairway) | 768 | 470 | 740 |

- Validation and test agree closely (E − A val/test: −476/−490, −110/−127, −90/−95; C − A in waterways: +1,194/+1,231, +479/+476).
- Seed stability (FDE@20, seeds 0/1/2): A and E vary by at most 2 m in every setting. C is unstable in the transfer waterways (Bornholm 1,816/1,816/2,218; Skagen 1,320/1,279/1,229), consistent with tree extrapolation outside the training coordinate range. The headline uses seed 0 as prespecified.
- Robustness (prespecified, not headline). E − A: home with unseen vessels −453 (−476 to −427); Bornholm with unseen vessels −126 (−152 to −106); Skagen with unseen vessels −103 (−132 to −81); home with unseen longitude bands −452 (−494 to −416). C − A in unseen longitude bands +1,090 (+1,004 to +1,185), reproducing the V1 H4b result on new data.
- Regimes (primary regime analysis, A–F). E − A has a CI below 0 in every regime and setting except Skagen low-speed (+9, −15 to +32). C − A is below 0 in every home regime, but above 0 in steady, turning and speed-changing in both waterways. Threshold sensitivity: E − A has a CI below 0 in 50/50 cells (home), 50/50 (Bornholm) and 40/41 (Skagen, one cell above 0); C − A is above 0 in 32 (Bornholm) and 31 (Skagen) cells and below 0 in none.
- Exploratory (descriptive, no claim): home E − C −70 m; F − E home −35, Bornholm +11, Skagen −10 m.
- The test and transfer_test splits are now spent. Any further development uses validation data only and is reported as post hoc.

## 2026-10-22 (Thu), V1–V2 write-up and corrections
- Drafted the V1→V2 updates to the README, `06_results.md`, `04_methods.md` (new V2 section), `07_limitations.md`, `00_plan.md` and the preliminary summary, after an external review of the drafts. Setting labels now separate "held-out longitude bands" (local spatial extrapolation) from "independent waterway" (Bornholm, Skagen); V1 hypotheses are referred to as V1-H1 to V1-H4b in combined documents.
- **Correction (feature count):** the fairway group has 14 features (5 at the anchor plus 3 at each of the 5, 10 and 20-min points), not 13 as written in the 18 Oct entry above and in the message of commit `02a2c6c`. E has 35 features and F has 39; the stored run summaries list them.
- **Correction (sensitivity denominator):** in the 21 Oct test entry, "40/41 (Skagen, one cell above 0)" is wrong. Each setting has 50 regime × threshold cells (150 in all). In Skagen, E − A has a CI below 0 in 40 of 50 cells, a lower point estimate in 42, and a CI above 0 in one (low-speed threshold 3 kn: +37 m, +13 to +64); all 10 cells without a CI below 0 are low-speed. Overall: CI below 0 in 140 of 150 cells. The cells share windows and are a descriptive robustness check, not independent tests.
- **Correction (validation–test agreement):** validation and test paired differences agree within 17 m for the V2-H1 comparisons but within 37 m for V2-H2 (Bornholm C − A +1,194 validation, +1,231 test). No hypothesis outcome changes.
- **Post-test code (reporting only):** added `summary-figure --v2` (`src/morva/cli.py`, `src/morva/viz/plots.py`) to draw `results/v2/figures/transfer_test.png` from the stored test summaries. It reads saved results only; no model was fitted or evaluated, and no test outcome was recomputed.
- Removed the tool acknowledgement section from the README.

## 2026-10-23 (Fri), V3 data feasibility and split
- Planned V3 (`docs/00_plan.md`): calibrated intervals, 60-minute horizons, transfer to the USA, map-history needs; interactions moved to V4, behaviour deviation to V5; Finland deferred (no historical archive).
- US data: NOAA/BOEM Marine Cadastre 2025 daily files. Downloaded the map-period and validation days only (19 Sep–15 Oct 2025, 27 files, 6.3 GB, `data/raw/us` via the raw store); every file matches the server's byte size and passes `zstd -t`. No test-period file (16–29 Oct 2025) was downloaded. Provenance manifests for the US files follow when the US adapter exists.
- One-day traffic count on 24 Sep 2025 (a map-period day; Class A; moving vessel-minutes) set the US boxes before any model was run: Salish Sea primary, Houston optional and reported overall and merchant-only. A Puget Sound-only box was rejected (133 moving vessels, 17 merchant).
- **V3 split and regions set before any V3 validation analysis**, in new files `configs/v3/data.yaml` and `configs/v3/experiment.yaml` (V2 configs unchanged): train 19 Sep–6 Oct, model selection 7–11 Oct, interval calibration 12–15 Oct, test 16–29 Oct (locked), in 2026 for Danish regions and 2025 for US regions; 20-minute history and 60-minute future. Fixed: sources, regions, calendars, windows and split. Provisional until the V3 freeze: fairway, GBM and uncertainty settings. `tests/test_v3_config.py` guards the fixed parts.
- **V3 infrastructure (no validation analysis run):**
  - Multi-source ingestion: `sources.py` reads V1/V2 single-source and V3 multi-source configs; new Marine Cadastre 2025 adapter (`ingestion/marinecadastre.py`, `.csv.zst` via `zstandard`) maps fields, numeric ship-type codes and navigational status onto the DMA canonical schema and keeps Class A only. On the real 24 Sep 2025 file it reproduces the box traffic count exactly (Salish Sea 256 moving vessels / 50,958 vessel-minutes; Houston 488 / 74,220) with a schema identical to the DMA interim files.
  - Per-region calendars with a calibration block (`resolve_calendars`, `assign_calendar_split`); flow maps use each region's own training block.
  - 60-minute windows and horizon labels taken from the configuration (tables show FDE@60 and errors at 5–45 min for V3, unchanged FDE@20 for V2).
  - Quantile residual model (`models/quantile.py`) and split-conformal 2-D boxes (`evaluation/conformal.py`), and a new `morva intervals` command with home or local (`--local-calibration`) calibration and vessel-grouped coverage intervals.
  - Tests (33 pass) cover the adapter, calendars, conformal boxes and the quantile model. A test caught a bug during development: the conformal offset used the empirical quantile at k/n with method "higher", which picks the next order statistic up and over-widens the boxes; it now takes the k-th smallest score, k = ceil((n + 1) × level), and is infinite when k > n.
  - `make smoke-v3` runs the full V3 chain on synthetic DMA and Marine Cadastre data. Synthetic coverage (56–68% for nominal 80%) reflects one synthetic day and tiny calibration sets, not the method.
  - V2 regression: rebuilding the real V2 windows and flow features with the new code reproduces the committed V2 split and fairway summaries byte for byte.
  - Provenance manifests written for the 27 US files. The map-history option (`map_history_days`, RQ4) is configured but not yet implemented.

## 2026-10-24/25, V3 VALIDATION (model selection 7–11 Oct; calibration 12–15 Oct used only inside `intervals`)
- Built V3 data at `6e3e38c`: 27 DMA and 27 Marine Cadastre days; windows per region on its own calendar; no test windows exist (latest labelled window ends 15 Oct). Validation windows: home 80,145; Bornholm 25,021; Skagen 44,871; Salish Sea 34,247; Houston 54,432.
- Code added before the runs (uncommitted at run time): `intervals --sweep` (fit once, evaluate home and every waterway with home and local calibration); quantiles reduced to the 80%/90% bounds [0.05, 0.1, 0.9, 0.95] to halve fitting time.
- Runs: baselines (5), models A–F (5), interval sweeps for E and A. Paused once on 23 Oct at 09:46 UTC after the Bornholm model run to free the machine; resumed 24 Oct 23:47 UTC with the remaining commands only. No run was repeated.
- **Point forecasts, mean error at 20 / 60 min (m):**

| Setting | CV | A motion | C raw location | E fairway | E − A at 60 (95% CI) | C − A at 60 | E vs A, 20 / 60 min |
|---|---|---|---|---|---|---|---|
| Home | 1,589 / 7,983 | 1,285 / 5,817 | 835 / 2,956 | 783 / 3,420 | −2,397 (−2,643 to −2,172) | −2,861 | −39% / −41% |
| Bornholm | 531 / 3,283 | 552 / 3,696 | 2,118 / 9,553 | 410 / 2,416 | −1,280 (−1,422 to −1,154) | +5,857 | −26% / −35% |
| Skagen | 891 / 4,940 | 883 / 4,807 | 1,484 / 6,984 | 762 / 3,935 | −872 (−1,059 to −713) | +2,177 | −14% / −18% |
| Salish Sea | 2,716 / 11,347 | 2,200 / 7,547 | 3,329 / 13,537 | 1,798 / 6,368 | −1,179 (−1,357 to −1,014) | +5,990 | −18% / −16% |
| Houston | 1,509 / 6,086 | 1,286 / 4,580 | 2,032 / 9,049 | 1,256 / 4,768 | +187 (+103 to +305) | +4,469 | −2% / +4% |

- Fairway context transfers to the USA on validation: in the Salish Sea E improves on A by 18% at 20 min and 16% at 60 min. In Houston it does not help: E is slightly worse than A at 60 min. Houston merchant-only (cargo and tanker, 6,697 windows): FDE@60 CV 7,817, A 7,888, E 7,836; for service craft (tugs and towboats, 35,695 windows) E is worse than A (4,302 vs 4,016 m).
- Raw coordinates fail in every independent waterway, including both US areas (C − A +2,177 to +5,990 m at 60 min).
- New in-area observation: at 60 min raw location beats fairway context at home (2,956 vs 3,420 m), whereas at 20 min E is better (783 vs 835 m).
- E's relative gain over A grows with horizon in Bornholm (26 → 35%) and Skagen (14 → 18%) but not in the Salish Sea (18 → 16%), so draft V3-H3 is not supported on validation.
- **Intervals (conformal boxes; coverage on validation days):** home calibration gives nominal coverage at home (E: 80% boxes 79.5% at 20 min and 79.1% at 60; 90% boxes 89.7% and 89.4%). It does not transfer: Bornholm over-covers (E 86% / 83% for 80% boxes), Skagen under-covers at 60 min (69%), and the US areas under-cover badly (Salish Sea 61% / 58%; Houston 50% / 38%). Local calibration on the region's own four calibration days restores near-nominal coverage everywhere (E, 80% boxes at 20 / 60 min: Bornholm 80.0 / 81.2%, Skagen 79.3 / 79.7%, Salish Sea 78.2 / 78.8%, Houston 77.7 / 79.4%; 90% boxes 88.7–91.2%).
- Fairway context makes intervals much narrower than motion-only at the same coverage (home 80% boxes at 20 min: half-widths 876 / 796 m for E vs 1,400 / 1,599 m for A). With home calibration, E's narrower boxes under-cover more in the US than A's (Houston 80% at 60 min: E 38%, A 78%).
- Draft V3-H1 (home calibration within ±3 points at home, Bornholm and Skagen) is not supported on validation: it holds at home only. These results are validation-informed and will shape the V3 hypotheses before the freeze. Map-history (RQ4) and junction features (RQ5) are not yet run.

