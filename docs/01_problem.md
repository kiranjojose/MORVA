# 01 — Problem statement and motivation

## Study scope

**Title:** Context-aware vessel behaviour modelling from historical AIS: reproducible baselines, prediction and
generalisation analysis.

**Primary question:** Does vessel and geographic context improve 5-, 10- and 20-minute vessel trajectory prediction
beyond transparent kinematic and motion-only learned baselines, in which manoeuvring regimes, and does the improvement
transfer to unseen vessels and unseen waters?

## Motivation

AIS provides a detailed record of where a vessel has been, its speed over ground and its recent course. These
observations are valuable, but they do not directly reveal navigational intent. A vessel that is turning may be
following a fairway bend, approaching a terminal, avoiding traffic or preparing to settle on a new course. The same
observed turn rate can therefore lead to different future trajectories.

From a naval-architecture perspective, I expected two forms of context to matter. First, vessel type and principal
dimensions are related to inertia, service speed and manoeuvring capability. A large loaded tanker, a ferry and a tug
do not respond or operate in the same way. Second, manoeuvres occur inside a geographic system: fairways, traffic
separation schemes, coastlines, ports and recurring routes constrain where the vessel can go. Recent motion describes
the current state, while vessel and geographic context may help explain how that state is likely to evolve.

This reasoning also creates a methodological risk. Vessel dimensions can act as a fingerprint for ships repeatedly
seen in the data, and raw latitude and longitude can let a model memorise local routes. A model can therefore achieve
high accuracy without learning a representation that transfers to a new vessel population or a different waterway.
For this reason, VesselMind studies not only in-area accuracy but also vessel-held-out and spatially held-out
performance.

The project is deliberately baseline-led. At a 5–20-minute horizon, constant velocity is physically interpretable,
computationally cheap and often appropriate during steady transit. A learned model is useful only if it improves on
this baseline under a leakage-aware evaluation and if the source and limits of the improvement can be explained.

## Research questions

| ID | Research question |
|---|---|
| RQ1 | How sensitive is the usable dataset to segmentation, reporting-gap and motion-filter choices? |
| RQ2 | How accurately do persistence, constant velocity, CTRV, damped CTRV and a CV Kalman filter predict positions at 5, 10 and 20 minutes? |
| RQ3 | How does prediction error change across low-speed, steady, turning, speed-changing and combined manoeuvring regimes defined only from past observations? |
| RQ4 | Does a motion-only learned correction improve on constant velocity, and in which regimes? |
| RQ5 | Do vessel type and dimensions add information beyond motion history? |
| RQ6 | Does geographic context add information beyond motion history, and is raw position a transferable representation of that context? |
| RQ7 | Do improvements survive a later time period, unseen vessels and spatially held-out waters? |

## Intended contribution

The first study is a controlled investigation of **when context helps**, rather than a proposal for a new deep neural
architecture. It contributes:

- a reproducible AIS quality and trajectory-window pipeline;
- transparent kinematic baselines evaluated on the same samples as the learned models;
- a motion/vessel/location feature ablation;
- past-only manoeuvring regimes with threshold sensitivity;
- chronological, vessel-held-out and spatially held-out evaluation; and
- explicit reporting of a rejected hypothesis and negative transfer from raw coordinates.

## Non-objectives

V1 is not a navigational-safety system, collision-avoidance system or real-time surveillance product. It does not claim
to infer vessel intent, certify unusual behaviour, estimate fuel use from AIS alone or detect real incidents. Anomaly
screening is a later research question and requires its own labels, evaluation and operational definition.
