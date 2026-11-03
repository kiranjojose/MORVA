# 01 — Problem statement and motivation

## Study scope

**Title:** When does geographic context transfer? A controlled AIS study of vessel trajectory prediction in Danish and
US waters.

**Primary question (V1):** Does vessel and geographic context improve 5-, 10- and 20-minute vessel trajectory
prediction beyond transparent kinematic and motion-only learned baselines, in which manoeuvring regimes, and does the
improvement transfer to unseen vessels and unseen waters?

This file states the question as it was posed for V1. V2 added independent Danish waterways and a fairway-relative
representation of geography; V3 extended the horizon to 60 minutes, added two US waterways and asked whether
calibrated prediction boxes stay calibrated in new waters. Those extensions are set out in the
[roadmap](00_plan.md) and [protocol](05_protocol.md).

## Motivation

AIS gives a detailed record of where a vessel has been, its speed over ground and its recent course. It does not tell
you what the vessel intends to do. A turning vessel may be following a fairway bend, approaching a terminal, avoiding
traffic or about to settle on a new course, and the same turn rate can lead to quite different futures.

Coming from naval architecture, I expected two kinds of context to matter. Vessel type and principal dimensions relate
to inertia, service speed and manoeuvring capability: a loaded tanker, a ferry and a tug do not handle or operate in
the same way. And manoeuvres happen inside a geographic system, where fairways, traffic separation schemes,
coastlines, ports and recurring routes limit where a vessel can go. Recent motion describes the current state; vessel
and geographic context may say how that state will develop.

The same reasoning carries a risk. Vessel dimensions can act as a fingerprint for ships seen many times in the data,
and raw latitude and longitude let a model memorise local routes. A model can score well without learning anything
that carries over to new vessels or another waterway. So MORVA reports vessel-held-out and spatially held-out
performance next to in-area accuracy.

The project starts from baselines. At 5–20 minutes, constant velocity is physically interpretable, cheap and often
right during steady transit. A learned model earns its place only if it beats this baseline under a leakage-aware
evaluation, and if I can explain where the gain comes from and where it stops.

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

V1 is a controlled investigation of **when context helps**, not a new deep neural architecture. It contributes:

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
