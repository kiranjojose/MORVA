# 03 — Data card

| Field | Value |
|---|---|
| Provider | Danish Maritime Authority, historical AIS |
| Files | see `data/manifests/*.json` (checksums, sizes, dates) |
| Licence / terms | TODO: record exact terms and the date checked |
| Area of interest | TODO: freeze after inspection (provisional: `configs/data.yaml`) |
| Period | TODO |
| Transmitters kept | Class A only (V1) |
| Rows / vessels / segments | from `results/tables/quality_report.json` |
| Known issues | sentinels (SOG 102.3, COG 360, heading 511), duplicates, position spikes, gaps, stale static data |
| Identity handling | MMSI pseudonymised in public figures |
