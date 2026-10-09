# 01 — Problem statement

**Study title:** Context-Aware Vessel Behaviour Modelling from Historical AIS: Reproducible Baselines, Prediction and Anomaly Analysis.

**One-sentence objective:** Test whether knowing *what kind of ship* it is and *where* it sails improves short-term prediction of where it will be, and the detection of unusual behaviour, using real historical AIS from Danish waters.

**Headline question:** Does vessel context improve 5/10/20-minute trajectory prediction over kinematic baselines, and does that depend on manoeuvring regime (open-water transit vs. turning / port approach)?

## Research questions (V1)
| ID | Question | Experiment |
|---|---|---|
| RQ1 | Which preprocessing choices materially change usable trajectory quality? | E0 |
| RQ3 | How accurate are 5/10/20-min forecasts vs. constant velocity / CTRV? | E2, E3 |
| RQ4 | Do vessel attributes improve forecasts, and in which regime? | E4 |
| RQ5 | Can transparent behavioural deviations be detected on synthetic injections? | E5 |

## Non-objectives
No navigational-safety certification, no inference of intent, no real-time surveillance, no fuel claims from AIS alone.

> TODO (Kiran): rewrite the motivation paragraph in your own words. Why does vessel context matter, from a naval-architecture point of view?
