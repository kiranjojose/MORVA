# 03 — Data card

| Field | Value |
|---|---|
| Provider | Danish Maritime Authority, historical AIS |
| Files | see `data/manifests/*.json` (checksums, sizes, dates) |
| Licence / terms | TODO: record exact terms and the date checked |
| Area of interest | TODO: freeze after inspection (provisional: `configs/data.yaml`) |
| Period | 2026-09-19 00:00 – 2026-10-06 23:59 UTC (18 daily files) |
| Transmitters kept | Class A only (V1) |
| Rows / vessels / segments | see funnel below |
| Known issues | sentinels (SOG 102.3, COG 360, heading 511), duplicates, position spikes, gaps, stale static data |
| Identity handling | MMSI pseudonymised in public figures |

## Data funnel (18 days, AOI, Class A)

| Stage | Rows | Note |
|---|---|---|
| In AOI, Class A | 63,336,434 | sum over the ingest log |
| After exact-duplicate removal | 29,498,080 | 53.4% of rows were identical copies |
| Passing hard quality flags | 29,146,229 | invalid MMSI 222.5k, partial duplicates 128.7k, speed spikes 1,085 |
| In segments (gap 20 min, ≥20 pts, ≥30 min) | 29,082,119 | 5,933 segments, 2,071 vessels |
| Prediction windows (moving, gap-safe) | 359,738 | 1,971 vessels |

## Threshold sensitivity (E0, `results/tables/sensitivity_gaps.csv`)
The segmentation gap (10/20/30 min) changes the number of segments (7,448 / 5,933 / 5,607) but the retained points and
windows by less than 0.1%. The window gap limit (120/180/300 s) changes the window count by −1.9% / 0 / +2.2%.
In this period and area, the usable dataset is therefore robust to these thresholds.
