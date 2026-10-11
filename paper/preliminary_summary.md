# When does context help vessel trajectory prediction? A controlled AIS study in Danish straits

**Kiran (kiranjojose) · Preliminary research summary · October 2026 · VesselMind V1**

> **OUTLINE, written by Claude as scaffolding.** Kiran rewrites every section in Kiran's own words. Facts come from
> `docs/06_results.md` and `results/tables/`. Test numbers are filled in after the single post-freeze run.
> Target length: 2 pages.

## 1. Question (≈80 words)
- Short-horizon (5–20 min) vessel position prediction underpins situational awareness and autonomy.
- Learned models often add context and a new architecture at the same time, so the cause of the gain is unclear.
- Question: does vessel and geographic context improve prediction beyond transparent kinematic and motion-only learned
  baselines, in which manoeuvring regimes, and does the gain transfer to unseen vessels and unseen waters?

## 2. Data and protocol (≈150 words)
- Danish Maritime Authority historical AIS, 19 Sep – 6 Oct 2026 (18 days), Great Belt / Øresund / southern Kattegat,
  Class A. 63.3 M rows → 29.5 M after exact-duplicate removal (53%) → 359,738 prediction windows, 1,971 vessels.
- 20-min history → 20-min forecast at 1-min steps; windows never bridge AIS gaps over 180 s.
- Whole-day time split: train 19–30 Sep, validation 1–3 Oct, test 4–6 Oct (locked; one run after hypothesis freeze
  on 11 Oct, commit `f1b61da`).
- Metrics: ADE and FDE@20 min (geodesic), paired comparisons on identical windows, 95% CIs from vessel-grouped bootstrap.
- Past-only manoeuvring regimes: low-speed, steady, turning, speed-changing, combined (with threshold sensitivity).

## 3. Methods (≈100 words)
- Kinematic: persistence, constant velocity (CV), CTRV, damped CTRV, CV Kalman filter (tuning on train only).
- Learned: gradient-boosted correction to CV in the vessel's body frame (along- and cross-track), 4 feature sets:
  A motion · B + vessel (type group, length, beam, draught) · C + location (lat, lon, course) · D all.
- Generalisation: vessel-held-out training (with a same-size random-subset control) and spatial hold-out
  (4 longitude bands, 3 km buffer).

## 4. Results (≈350 words + 1 table + 1 figure)
**Table 1.** FDE@20 min (m), **test split** (single run after hypothesis freeze; 57,068 windows)

| Model | In-area | Unseen vessels | Unseen waters |
|---|---|---|---|
| CV | 1,554 | 1,554 | 1,554 |
| A motion | 1,267 | 1,429 | 1,465 |
| B + vessel | 1,128 | 1,367 | 1,442 |
| C + location | 863 | 1,165 | 2,592 |
| D all | **831 (−47%)** | 1,140 (−27%) | 1,918 (+23%) |

Key findings (test):
1. **Kinematic refinements do not beat CV.** CTRV +467 m; damped CTRV and Kalman converge to CV. Turns in these
   waters are short, and the latest reported state beats history-based extrapolation.
2. **Motion-only learning helps most where kinematics fail:** combined manoeuvres −1,078 m vs CV, steady transit −88 m.
3. **Location context gives the largest in-area gain** (D −47% vs CV), in every regime and in all 50 regime ×
   threshold cells.
4. **Generalisation splits the story:** location gains survive on unseen vessels (−264 m vs motion-only) but **reverse
   in unseen waters (+1,127 m)**. Raw coordinates are memorised geography.

**Figure 1.** `results/figures/regime_fde_*.png` (error by regime), or a 3-panel in-area / unseen vessel / unseen area.

## 5. Hypotheses (≈100 words)
| | Hypothesis (frozen 11 Oct) | Test result |
|---|---|---|
| H1 | Motion-only learning beats CV; largest gain in non-steady regimes | Supported |
| H2 | Vessel context helps beyond motion; more when turning or changing speed | Supported in-area; weak for unseen vessels; absent in unseen waters |
| H3 | Geographic > vessel context in turning and combined manoeuvres | Supported |
| H4 | Geographic gain decreases in unseen areas but stays positive | **Rejected** (gain reverses) |
| H4b | Raw-coordinate context does not transfer to unseen areas (validation-informed) | Supported |

## 6. Limitations (≈80 words)
18 days, one region, Class A only; raw-coordinate location; seen and unseen vessels are different populations;
single GBM family; no uncertainty output yet; no interaction or weather features; synthetic anomaly work not started.

## 7. What this motivates (≈100 words): the PhD direction
- Learn **transferable** representations of navigational context (fairway geometry, traffic-flow fields from historical
  AIS, bathymetry) that work in waters without training labels.
- Physics-aware constraints from ship manoeuvring (naval-architecture background).
- Calibrated uncertainty and context-conditioned residuals for anomaly screening.

**Code and data provenance:** github.com/kiranjojose/vesselmind (public from 15 Oct) · `make pipeline` reproduces all
results from the documented DMA files.
