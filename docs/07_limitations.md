# 07 — Limitations

## Geographic and temporal scope

The study uses 18 days of traffic in one Danish area. Although the area contains straits, ferry routes, port approaches
and several vessel classes, it does not represent seasonal conditions, severe weather, other traffic cultures or the
geometry of unrelated waterways. The chronological test period is only three days later than the training period.
Agreement between validation and test therefore supports short-term repeatability, not long-term robustness.

The spatial hold-out uses four longitude bands with a buffer. This is stricter than the in-area split but is not the
same as training in one waterway and testing in a genuinely independent region. The folds also differ in traffic mix
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
useful local regularities, but the spatial experiment demonstrates that this representation does not transfer. It
should not be described as learning fairway geometry or navigational understanding. Engineered features based on local
fairway bearing, curvature, coastline, bathymetry and traffic-flow structure are still required.

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

The hypotheses were developed after validation analysis and frozen before the single test run. H1–H4 are therefore
validation-informed rather than a preregistration made before any results were seen. H4b was explicitly added after
the spatial validation result and received its first independent check on the test split. This provenance is recorded
because presenting all hypotheses as fully prospective would overstate the strength of confirmation.

## Safety, anomaly and deployment limits

MORVA is an offline research prototype. It has not been tested for real-time latency, missing live feeds, cyber
security, operator workload, alert fatigue or failure recovery. It is not a replacement for radar, bridge judgement,
VTS procedures or certified navigation equipment.

No real anomaly-detection claim is made. Statistical deviation, an AIS gap or large prediction residual may be caused
by legitimate manoeuvring, weather, traffic avoidance, receiver loss or data error. Synthetic anomaly injections can
test sensitivity to constructed patterns, but cannot demonstrate detection of real incidents, unsafe behaviour or
illegal activity. Any anomaly extension needs a separate taxonomy, credible labels, human review and evaluation of
false alarms.
