# 03 — Data card

## Dataset identity

| Field | Value |
|---|---|
| Provider | Danish Maritime Authority (DMA), historical shore-based AIS |
| Source page | <https://www.dma.dk/safety-at-sea/navigational-information/ais-data> |
| Files | 18 daily ZIP files; checksums and provenance in `data/manifests/*.json` |
| Period | 19 September 2026 00:00:00 to 6 October 2026 23:59:58 UTC |
| Frozen area of interest | Great Belt, Øresund and southern Kattegat bounding box: 54.8–56.2° N, 10.4–13.0° E |
| AIS population retained | Class A mobile transmitters only |
| Public redistribution | Raw AIS files are not committed or redistributed by this repository |
| Identity handling | MMSI is required internally for grouping and evaluation; public aggregate tables and figures do not expose individual MMSIs |
| Terms checked | 16 October 2026 |

## Access and terms

The DMA states that continuously updated historical AIS CSV files are available for free download. Its AIS data
management policy states that access is provided under the Danish public-sector-information framework (Act no. 596 of
24 June 2005 on further use of public-sector information). The policy also states that the DMA does not guarantee the
correctness or continuity of the data and is not liable for damage arising from its use. Recipients are responsible for
lawful handling and must not combine the data with other sources to make people identifiable without the required
permission.

This repository publishes manifests, checksums, aggregate statistics and derived model results, but not the original
DMA files or vessel-level exports. This data card records the conditions visible on the DMA pages on the date above; it
is not a substitute for legal advice, and the terms should be rechecked before redistribution or commercial use.

## Why Class A only?

Class A includes the larger commercial, passenger and fishing vessels subject to carriage requirements and generally
reports more frequently than Class B. This choice creates a more consistent first study of commercial traffic but
excludes much recreational and small-craft activity. The results therefore do not describe all traffic present in the
study area.

## Processing and data funnel

| Stage | Rows / units | Decision |
|---|---:|---|
| In frozen AOI, Class A | 63,336,434 rows | Geographic and transmitter-class filter |
| After exact-row de-duplication | 29,498,080 rows | 53.4% were identical duplicate records |
| Passing hard quality flags | 29,146,229 rows | Invalid MMSI, conflicting duplicates and speed spikes excluded |
| In retained segments | 29,082,119 rows | 5,933 segments, 2,071 vessels |
| Prediction windows | 359,738 windows | 1,971 vessels; moving and gap-safe windows |

The pipeline converts the provider's sentinel values to missing values before modelling. Observed examples include SOG
102.3 knots and heading 511°. It also flags invalid positions, invalid MMSIs, duplicate timestamp records, high reported
SOG and implausible speed implied by consecutive positions.

Tracks are split when the reporting gap exceeds 20 minutes. Retained segments require at least 20 observations and 30
minutes of duration. Each segment is resampled to a one-minute grid, but a prediction window is rejected if any
original observation gap inside its 20-minute history plus 20-minute future exceeds 180 seconds. Windows with mean
history SOG below 1 knot are excluded from the prediction task.

## V2 extension (2026-10-18)

V2 adds nine later days and two independent waterways. The V1 funnel above describes the V1 study only.

| Field | Value |
|---|---|
| Files | 27 daily ZIP files, 19 September to 15 October 2026; the 9 new files were size-checked against the DMA listing, zip-tested and checksummed in `data/manifests/` |
| Home area | Unchanged V1 box. The only area used for model fitting |
| Transfer waterways | Bornholm 54.7–55.6° N, 14.0–15.6° E; Skagen 57.2–58.0° N, 9.6–11.2° E |

| Region | Rows after de-duplication | Passing hard flags | Segments | Vessels |
|---|---:|---:|---:|---:|
| Home | 43,812,556 | 43,289,862 | 8,492 | 2,516 |
| Bornholm | 11,157,079 | 11,095,262 | 4,125 | 1,879 |
| Skagen | 36,835,264 | 36,664,715 | 4,853 | 2,130 |

Prediction windows by split (`results/v2/tables/split_summary.json`):

| Split | Home | Bornholm | Skagen |
|---|---:|---:|---:|
| train / transfer_context (19–30 Sep) | 238,829 | 80,760 | 156,175 |
| val / transfer_val (1–6 Oct) | 120,412 | 41,675 | 67,809 |
| test / transfer_test (7–15 Oct, locked) | 167,533 | 55,561 | 97,396 |

The locked-split counts above are dataset bookkeeping, not model evaluation. Before the V2 hypothesis freeze on
21 October 2026, no model metrics or outcome comparisons were inspected for `test` or `transfer_test`. V2 hypotheses
were informed only by `val` and `transfer_val`; the locked splits are their first independent evaluation.

One input-only summary was also computed for every split, including the locked ones: `morva fairway` records, per
split, how many windows have flow features and the median absolute flow offset and heading difference
(`results/v2/tables/fairway_summary.json`). These describe model inputs only; no prediction errors or other outcomes
were computed for the locked splits.

Many transfer-waterway vessels also appear in home training. In `transfer_val`, they account for 44% of Bornholm
windows (334 of 752 vessels) and 28% of Skagen windows (286 of 797 vessels). Unseen-waterway results should
therefore be reported both for all vessels and with every evaluated vessel removed from training.

Skagen has many more raw rows than Bornholm but relatively fewer windows, because much of its traffic is slow
fishing activity below the 1-knot window threshold.

## Data completeness and observed quality

After sentinel conversion, the missing fractions are approximately:

| Variable | Missing fraction |
|---|---:|
| SOG | 0.38% |
| COG | 5.43% |
| Heading | 15.07% |
| Length | 3.05% |
| Width | 3.08% |
| Draught | 13.60% |

Ship type is propagated to the vessel-level metadata used by the window table, but AIS static and voyage-related
information may still be stale, manually entered or incorrectly configured. “Undefined” ship type values are treated
as missing when vessel metadata are constructed.

## Split and unit of analysis

The unit of modelling is a 40-minute window: 20 minutes of history followed by a 20-minute future, sampled at
one-minute intervals. Consecutive anchors are five minutes apart, so windows overlap and must not be treated as
independent observations.

| Split | Dates (UTC) | Windows | Vessels |
|---|---|---:|---:|
| Train | 19–30 September | 238,830 | 1,535 |
| Validation | 1–3 October | 62,982 | 692 |
| Test | 4–6 October | 57,068 | 622 |
| Excluded at boundaries | — | 858 | 119 |

A window is assigned to a split only when its full history and future are contained inside that time block. There are
448 vessels shared between train and validation and 381 shared between train and test, reflecting recurring traffic.
Separate vessel-held-out experiments remove this overlap during training.

## Threshold sensitivity

Changing the segmentation gap among 10, 20 and 30 minutes changes the number of segments substantially but changes
retained points and prediction windows by less than 0.1%. Changing the permitted within-window source gap among 120,
180 and 300 seconds changes the number of windows by approximately −1.9%, 0% and +2.2%, respectively. The usable sample
count is therefore stable under these alternatives, although sample-count stability does not by itself establish that
model errors are unaffected.

## Known biases and appropriate use

- Shore-based receiver coverage and message duplication are not uniform.
- Class A selection favours larger commercial and passenger vessels.
- The 18-day period cannot represent seasonal, weather or long-term traffic variation.
- Repeated services, especially ferries, are over-represented through overlapping windows.
- AIS reports motion and self-entered metadata, not helm orders, propulsion commands or navigational intent.
- An AIS outage or abnormal-looking trajectory is not evidence of unsafe or illegal behaviour.

The dataset is appropriate for this bounded historical prediction study. It is not sufficient by itself for a claim of
global generalisation, real-time operational reliability or safety certification.

## V3 extension (2026-10-23 onwards)

V3 extends the forecast horizon and adds a second AIS source. The counts in this section describe the validation build
through 15 October; they are intentionally labelled provisional until the post-freeze test-data build is complete.
The V1 and V2 counts above remain the records for those stages.

| Field | Value |
|---|---|
| Danish source | Danish Maritime Authority daily ZIP files, 19 Sep–29 Oct 2026 |
| US source | NOAA/BOEM Marine Cadastre 2025 daily `.csv.zst` files, 19 Sep–29 Oct 2025 |
| Population | Class A mobile transmitters in every region |
| Test-data access | The V3 hypotheses and commands were frozen on 26 Oct 2026 before test-file access. All 14 US test files (16–29 Oct 2025) were downloaded and manifested later that day. Danish files for 16–23 Oct 2026 were downloaded and manifested after the freeze on 26 Oct; files for 24–29 Oct will be added only after DMA publishes them |
| US terms | The catalogue states that the data support coastal and ocean planning, are not for navigation and are provided as is. It lists no access constraint, but does not expressly address commercial reuse; NOAA should therefore be consulted before product use |

The five frozen geographic boxes are:

| Region | Source year | Bounding box | Role |
|---|---:|---|---|
| Home | 2026 | 54.8–56.2° N, 10.4–13.0° E | The only model-training area |
| Bornholm | 2026 | 54.7–55.6° N, 14.0–15.6° E | Danish transfer waterway |
| Skagen | 2026 | 57.2–58.0° N, 9.6–11.2° E | Danish transfer waterway |
| Salish Sea | 2025 | 47.0–48.8° N, 124.7–122.2° W | Primary cross-country transfer area |
| Houston | 2025 | 28.9–29.8° N, 95.3–94.3° W | Descriptive stress test |

The US boxes were fixed on 23 Oct 2026 using a traffic count from 24 Sep 2025, within the map-history period and before
any US model evaluation. An initial Puget Sound-only box (47.0–48.3° N, 123.2–122.2° W) was rejected because it
contained only 133 moving vessels, including 17 merchant vessels. The adopted Salish Sea box extends across the
Canada–United States boundary to retain traffic in the Strait of Juan de Fuca and Haro Strait; the Marine Cadastre
files contain observations in those Canadian waters.

| Region | Rows | Passing hard flags | Segments | Vessels | Median / 90th-percentile reporting interval |
|---|---:|---:|---:|---:|---|
| Home | 43,812,556 | 43,289,862 | 8,492 | 2,516 | 10 s / 12 s |
| Bornholm | 11,157,079 | 11,095,262 | 4,125 | 1,879 | 10 s / 12 s |
| Skagen | 36,835,264 | 36,664,715 | 4,853 | 2,130 | 10 s / 12 s |
| Salish Sea | 6,173,752 | 6,172,596 | 7,456 | 1,116 | 80 s / 183 s |
| Houston | 11,666,364 | 11,664,565 | 10,839 | 1,648 | 79 s / 181 s |

The Marine Cadastre archive is nominally sampled at one-minute resolution, but consecutive in-region observations in
this build are typically 79–80 seconds apart, compared with 10 seconds for DMA. Its 90th-percentile interval is
181–183 seconds, close to and slightly above MORVA's 180-second within-window limit. The gap filter therefore removes
sparser US stretches preferentially: the retained US windows represent the better-covered portion of the source data,
not the complete US traffic record. This selection should be considered when comparing US and Danish performance.

Prediction windows (vessels in brackets), V3 validation build. These counts must be replaced after the frozen
test-data preparation:

| Region | Training period (19 Sep–6 Oct) | Validation (7–11 Oct) | Calibration (12–15 Oct) |
|---|---:|---:|---:|
| Home | 316,680 (1,766), used for training | 80,145 (742) | 66,974 (659) |
| Bornholm | 100,896 (1,424), map only | 25,021 (558) | 20,330 (439) |
| Skagen | 196,210 (1,647), map only | 44,871 (659) | 39,675 (527) |
| Salish Sea | 140,940 (776), map only | 34,247 (375) | 36,761 (371) |
| Houston | 259,700 (1,308), map only | 54,432 (776) | 48,628 (711) |

Traffic mix differs strongly between regions. In Houston, 35,695 of 54,432 validation windows (66%) come from the
service group, principally tugs and towboats, whereas cargo and tanker vessels contribute 6,697. The Salish Sea also
contains substantial passenger and service traffic. All US results are consequently reported by ship group as well as
in aggregate. Flow features are available for 96–98% of validation windows in every region.
