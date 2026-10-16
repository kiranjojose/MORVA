# When does context help vessel trajectory prediction? A controlled AIS study in Danish straits

**Kiran Jose Puthussery · Preliminary research summary · October 2026 · MORVA V1**

## Motivation and research question

Short-term vessel trajectory prediction is relevant to maritime traffic monitoring, situational awareness and, in the
longer term, decision-support systems. AIS provides frequent observations of position, speed and course, but these
measurements describe what a vessel is doing rather than why it is doing it. A vessel that has started turning may
continue the turn, settle on a new course, follow a bend in a fairway or approach a terminal. Its recent motion alone
does not resolve these alternatives.

My starting point was therefore not to develop another large prediction architecture. I wanted to establish how far
transparent kinematic models could go, and then isolate the value of additional information. The primary question was:

> Does vessel and geographic context improve 5-, 10- and 20-minute trajectory prediction beyond transparent
> kinematic and motion-only learned baselines, in which manoeuvring regimes, and does the improvement transfer to
> unseen vessels and unseen waters?

This question was motivated partly by my naval-architecture background. Vessel type and dimensions are physically
related to manoeuvrability, while waterway geometry constrains where a manoeuvre can lead. At the same time, these
variables can act as shortcuts: dimensions may identify a frequently observed vessel, and raw coordinates may encode a
memorised route. I therefore treated generalisation as part of the research question rather than as an afterthought.

AIS trajectory-prediction research now spans classical machine learning, recurrent networks, graph models and
transformers, but reviews continue to identify data quality, heterogeneous evaluation and incomplete contextual
information as important problems [1,2]. A comparative study across channel, archipelago and port settings also shows
that the relative suitability of prediction methods depends on the traffic environment [3]. MORVA complements
this literature with a controlled feature ablation, past-only manoeuvring regimes, and separate tests for familiar
waters, unseen vessels and unseen waters.

## Data and experimental protocol

I used 18 daily files of historical shore-based AIS data made available by the Danish Maritime Authority, covering
19 September to 6 October 2026. The study area is a fixed bounding box covering the Great Belt, Øresund and southern
Kattegat (54.8–56.2° N, 10.4–13.0° E). I retained Class A transmitters because they represent the larger commercial and
passenger vessels most relevant to this first study and generally report more frequently than Class B equipment.

The raw in-area data contained 63.3 million rows. After removing 53.4% exact duplicate rows, applying quality flags and
segmenting tracks, the pipeline produced 359,738 gap-safe prediction windows from 1,971 vessels. Each sample contains
20 minutes of history and 20 minutes of future movement on a one-minute grid. A sample is rejected if an original AIS
gap anywhere in the window exceeds 180 seconds. This prevents interpolation from disguising a substantial observation
outage.

I split the data by complete UTC days: 19–30 September for training, 1–3 October for validation and 4–6 October for
testing. A window is assigned to a split only when its complete history and future lie inside that block. I used the
validation period for model development and exploratory analysis, documented the resulting hypotheses, and froze them
on 11 October before the single test evaluation. The test set contains 57,068 windows from 622 vessels.

The main metrics are average displacement error (ADE) and final displacement error at 20 minutes (FDE@20), calculated
as geodesic distances in metres. Model differences are paired on identical samples. I estimate 95% confidence intervals
by resampling whole vessels rather than individual windows, because windows belonging to the same vessel are strongly
correlated.

## Models and contextual ablation

The transparent baselines are persistence, constant velocity (CV), constant turn rate and velocity (CTRV), a damped
CTRV model and a constant-velocity Kalman filter. Parameters for damped CTRV and the Kalman filter were selected using
training data only.

The learned model is deliberately compact: a histogram gradient-boosting regressor predicts corrections to the CV
forecast. Corrections are represented in the vessel's local body frame as along-track and cross-track residuals at 5,
10, 15 and 20 minutes. This formulation gives the model a strong physical starting point and asks it to learn only the
departure from constant motion.

I trained four feature sets on otherwise identical targets and samples:

- **A — motion:** recent speed, speed change, course change, course jitter and past along/cross-track positions;
- **B — vessel:** motion plus vessel group, length, beam and draught;
- **C — location:** motion plus latitude, longitude and course orientation;
- **D — all:** motion, vessel and location variables.

For interpretation, each sample is assigned to one of five manoeuvring regimes using only the final 10 minutes of its
observed history: low-speed, steady transit, turning, speed-changing or combined turning and speed-changing. I repeated
the analysis across alternative turn, speed, low-speed and lookback thresholds so that the conclusion would not depend
on one arbitrary definition.

## Test results

**Table 1. Mean FDE@20 (m) on the test period.** “Unseen vessels” removes every test vessel from training. “Unseen
waters” predicts each longitude band using a model trained outside that band with a buffer.

| Model | In-area | Unseen vessels | Unseen waters |
|---|---:|---:|---:|
| Constant velocity | 1,554 | 1,554 | 1,554 |
| A: motion only | 1,267 | 1,429 | 1,465 |
| B: + vessel attributes | 1,128 | 1,367 | 1,442 |
| C: + raw location | 863 | 1,165 | 2,592 |
| D: all features | **831** | **1,140** | 1,918 |

The first finding is that a simple CV forecast is a demanding baseline. Ordinary CTRV is 467 m worse than CV at 20
minutes. Damping the turn and filtering the state both converge to approximately the CV result. The recent turn rate
does not reliably indicate how long the turn will continue; extrapolating it over the full horizon frequently
overshoots bends and course alterations.

The motion-only learned model improves FDE@20 by 287 m over CV in-area. The gain is small during steady transit
(88 m) and much larger during turning (316 m), speed-changing (756 m) and combined manoeuvres (1,078 m). This supports
the hypothesis that learned corrections are most useful where constant-motion assumptions break down.

Within the same waters, contextual features produce a much larger gain. The full model reduces FDE@20 from 1,554 to
831 m, a 47% improvement over CV. Raw location is more informative than vessel attributes during turning and combined
manoeuvres. The in-area location gain occurs in every regime and persists across all 50 combinations of regime and
threshold sensitivity tested.

The generalisation experiments change the interpretation. When all test vessels are excluded from training, the full
model still improves on CV by 27%, and raw location improves by 264 m over motion alone. The model can therefore apply
local route regularities to vessels it has not previously observed. Vessel features contribute much less under this
condition, suggesting that part of their in-area value comes from recurring vessel or service patterns rather than
from transferable manoeuvring physics.

The spatial hold-out produces the most important negative result. When the longitude band being predicted is absent
from training, raw location makes FDE@20 **1,127 m worse** than motion alone. The location model has learned useful
local corrections, but those corrections are attached to absolute coordinates and are applied incorrectly in unseen
waters. My original H4 predicted that the geographic benefit would decrease but remain positive; the test evidence
rejects it. A validation-informed H4b—that raw-coordinate context would not transfer—was supported on the test period
and is reported separately for transparency.

![Test FDE at 20 minutes in the three generalisation settings](../results/figures/generalisation_test.png)

## Interpretation, limitations and next direction

The study suggests that the difficult part of short-horizon vessel prediction is not simply detecting a manoeuvre. It
is identifying how that manoeuvre relates to the waterway and when it will end. Absolute coordinates provide this
information within a familiar region, but they are not a transferable representation of navigational context.

These findings are limited to 18 days, one Danish study area and Class A AIS. The spatial folds are longitude bands,
not independent waterways, and the learned comparison uses one gradient-boosting model family. AIS does not expose
rudder commands, propulsion state, pilot instructions, route plans or all environmental and traffic influences. This
work therefore evaluates statistical trajectory forecasting, not navigational intent or a safety-certified function.

The next research step is to replace raw coordinates with representations that have the same physical meaning across
locations: distance and bearing to a fairway centreline, local fairway curvature, proximity to ports and anchorages,
bathymetry, coastline constraints and historical traffic-flow fields. These representations should then be evaluated
on genuinely different waterways, with calibrated predictive uncertainty. If prediction residuals are later used for
anomaly screening, that will require a separate evaluation because an unusual trajectory is not automatically unsafe,
illegal or erroneous.

## References

1. Y. Yang, Y. Liu, G. Li, Z. Zhang and Y. Liu, “Harnessing the power of machine learning for AIS data-driven
   maritime research: A comprehensive review,” *Transportation Research Part E*, 183, 103426, 2024.
2. H. Li, H. Jiao and Z. Yang, “Ship trajectory prediction based on machine learning and deep learning: A systematic
   review and methods analysis,” *Engineering Applications of Artificial Intelligence*, 126, 107062, 2023.
3. H. Li, H. Jiao and Z. Yang, “AIS data-driven ship trajectory prediction modelling and analysis based on machine
   learning and deep learning methods,” *Transportation Research Part E*, 175, 103152, 2023.

**Reproducibility and provenance.** Code and documentation: <https://github.com/kiranjojose/MORVA>. The repository records the data manifests and checksums, experiment configuration,
quality reports, run summaries and the failed pre-access test command. Raw DMA files are not redistributed. The test
set is now spent; any subsequent model development is treated as post-hoc and returns to validation or new data.
