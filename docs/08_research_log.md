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

