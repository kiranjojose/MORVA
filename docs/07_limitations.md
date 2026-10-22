# 07 — Limitations

## Geographic and temporal scope

V1 used 18 days of traffic in one Danish area. V2 extends this to 27 days and adds two independent waterways, Bornholm
and Skagen, but the evidence still covers only three Danish geographic settings over the same autumn weeks. All three
share one national AIS receiver network and navigational-data environment, and part of their traffic: in the V2
validation period, vessels also seen in home training account for 44% of Bornholm and 28% of Skagen windows (results
with those vessels removed from training are reported separately). Seasonal conditions, severe weather, other
countries' traffic cultures and other waterway types (rivers, archipelagos, open ocean, busy port basins) remain
untested. The V2 test period is one to two weeks after training; agreement between validation and test supports
short-term repeatability, not long-term robustness.

The longitude-band hold-out uses four bands with a buffer inside the home area. It tests local spatial extrapolation,
which is not the same as transfer to an independent region; V2 therefore reports it separately from the two
independent waterways. The folds also differ in traffic mix
and sit at different positions within the coordinate range. Tree models can extrapolate particularly poorly at the
outer bands, so the experiment measures both geographic novelty and feature-range extrapolation.

## AIS observation limits

The source is shore-based AIS and V1 retains Class A transmitters only. Small craft and vessels without functioning AIS
are not represented, and receiver coverage, reporting frequency and duplicates vary. Dynamic fields originate from
onboard instruments; static and voyage-related fields can be missing, stale or entered incorrectly. AIS does not
provide rudder angle, engine command, pilot instruction, route plan or a complete account of wind, current, depth and
traffic interactions. The model predicts from an incomplete observation of the navigational situation.

More than half of the in-area raw rows were exact duplicates. Conflicting records with the same MMSI and timestamp are
currently handled through quality flags and the existing de-duplication rule; a stronger provenance-based resolution
strategy would be preferable. Interpolation regularises irregular reports, but it also smooths real motion. The
180-second gap rule limits rather than removes this risk.

## Dependence between samples

Prediction windows overlap and recurring vessels contribute many samples. Vessel-grouped bootstrap confidence
intervals address within-vessel dependence more honestly than resampling windows, but they do not fully represent
dependence by day, route, operator or weather condition. The mean error can still be dominated by high-frequency
services. Future studies should report route- and day-block uncertainty in addition to vessel-grouped intervals.

The vessel-held-out experiment changes the training population as well as vessel familiarity. A same-size random
subset controls for training quantity, but unseen vessels are not exchangeable with familiar vessels: they may belong
to different services, ship types or routes. The result should therefore be interpreted as performance on this unseen
vessel population, not as a causal estimate of vessel identity alone.

## Model and feature scope

The learned comparison uses one residual histogram-gradient-boosting family. Three random seeds show that its ranking
is stable, but this does not establish superiority over well-tuned sequence, graph or probabilistic models. The Kalman
baseline is a constant-velocity formulation; alternative dynamic or route-conditioned filters could behave
differently.

The location feature set contains raw latitude, longitude and course orientation. Its strong in-area result reflects
useful local regularities, but V1 and V2 show that this representation does not transfer. It should not be described
as learning fairway geometry or navigational understanding. Only one learned model family (residual gradient boosting
with one hyperparameter configuration) was evaluated, and the hypotheses were decided on one prespecified seed.

## Fairway context (V2)

The V2 fairway features are derived from historical AIS of the same waterway. They cannot be computed for waters
without AIS history, and their quality depends on traffic volume and receiver coverage: flow features were missing for
3.5–6.6% of test windows, and sparse areas give noisier maps. The map describes where vessels have sailed, not where
they may sail: it contains no chart, depth, coastline or regulatory information, and recent changes to routes are not
represented until they appear in the traffic history.

The method pools all same-direction traffic in a 1.5 km block and does not choose between branches. Near junctions and
route splits the flow direction is a mixture, and only a lower coherence value signals the ambiguity. Route choice at
junctions is therefore not modelled.

Fairway alignment says little about low-speed behaviour such as berthing, anchoring and manoeuvring in port. In the
V2 test, fairway context gave no detectable improvement for low-speed windows in Skagen, and one threshold
configuration favoured the motion-only model there.

Vessel type, length, beam and draught are coarse proxies for manoeuvring capability. Important variables such as
loading condition, trim, propulsion arrangement and control input are unavailable or unreliable. Vessel attributes
can also act as identity or service fingerprints, as indicated by their reduced benefit under held-out evaluation.

## Regime definitions

The five manoeuvring regimes are analytical categories derived from the final 10 minutes of history. Their thresholds
are interpretable but are not universal ship-handling laws. Course over ground is unstable at low speed, and a net
course change can hide oscillating motion. Position-derived turn agreement, reliability flags and threshold
sensitivity reduce this concern; they do not create operationally validated regime labels. Expert review and tests in
other waterways remain necessary.

## Statistical and operational meaning

ADE and FDE measure positional accuracy, not collision risk, route validity or decision usefulness. A statistically
significant improvement of several hundred metres may be useful for regional traffic forecasting and insufficient for
close-quarters navigation. The project has not yet established an operational accuracy requirement with VTS operators,
navigators or ports.

The current model is deterministic and does not provide calibrated uncertainty or multiple plausible futures. Near a
junction or terminal, several trajectories may be reasonable. A single mean trajectory can be misleading even when
its aggregate displacement error is competitive.

The V1 hypotheses were developed after validation analysis and frozen before the single V1 test run. V1-H1–V1-H4 are
therefore validation-informed rather than a preregistration made before any results were seen. V1-H4b was explicitly
added after the spatial validation result and received its first independent check on the V1 test split. V2-H1 and
V2-H2 were likewise informed by V2 validation results and frozen before the V2 test run. Two pre-test amendments made
the decision rules and reporting coverage explicit; the stronger V2-H2 rule and the original rule produce the same
conclusion. This provenance is recorded because presenting either stage as fully prospective would overstate the
strength of confirmation.

## Safety, anomaly and deployment limits

MORVA is an offline research prototype. It has not been tested for real-time latency, missing live feeds, cyber
security, operator workload, alert fatigue or failure recovery. It is not a replacement for radar, bridge judgement,
VTS procedures or certified navigation equipment.

No real anomaly-detection claim is made. Statistical deviation, an AIS gap or large prediction residual may be caused
by legitimate manoeuvring, weather, traffic avoidance, receiver loss or data error. Synthetic anomaly injections can
test sensitivity to constructed patterns, but cannot demonstrate detection of real incidents, unsafe behaviour or
illegal activity. Any anomaly extension needs a separate taxonomy, credible labels, human review and evaluation of
false alarms.
