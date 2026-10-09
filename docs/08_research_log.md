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
