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
- **~47% of rows are exact full-row duplicates** (1.41 M). Another 4,159 (MMSI, t) groups have conflicting positions; the first row is kept for now. TODO: decide on a rule for the conflicts.
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
- Waiting on: Kiran's regime definition.

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
- TODO: vessel-held-out evaluation (exclude val vessels from training) to separate these effects; 3 seeds; regime breakdown with Kiran's definition.

## 2026-10-10 (Sat, evening), seeds, vessel-held-out and size control (VALIDATION)
- **Seeds 0–2:** FDE@20 sd ≤ 5.3 m for every feature set (A 1,272 / B 1,130 / C 865 / D 823 m). The ablation ranking is not a seed artefact.
- **Vessel-held-out** (all 692 val vessels removed from training; train windows 238,830 → 109,866): FDE@20 CV 1,574 → A 1,452 → B 1,435 → C 1,171 → D 1,163 m (D −411 m vs CV, −26%). Location vs motion −281 m (−312 to −252). **Vessel attributes vs motion −17 m (−35 to +1): no evidence they generalise to new vessels.**
- **Size control** (random 109,866 train windows, seen vessels kept): D 861 m. So training size accounts for ~40 m (823 → 861); vessel/route familiarity accounts for ~300 m (861 → 1,163).
- By ship group, D_all FDE (full / size-control / held-out): cargo 573 / 590 / 553, tanker 680 / 700 / 642, **passenger 944 / 1,015 / 2,162**, service 1,346 / 1,399 / 1,692. Fairway knowledge generalises completely for transiting cargo and tankers. Ferry gains depend on having seen the same ferries (each route is served by few vessels, so holding them out removes the route).
- **Headline (preliminary):** spatial context generalises to unseen vessels (−26% FDE vs CV); vessel attributes add little beyond motion for new vessels; large ferry gains are route familiarity. This is a defensible, nuanced answer to RQ4.
