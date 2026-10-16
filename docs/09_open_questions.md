# 09 — Open research questions

These questions define work that remains after V1. Completed decisions and hypothesis provenance are recorded in
`docs/04_methods.md`, `docs/05_protocol.md` and `docs/08_research_log.md`.

## Transferable geographic representation

1. Which fairway-relative features retain meaning across different waterways?
2. Should routes be represented as centrelines, navigable polygons, traffic-flow fields or a learned graph?
3. How should distance to an upcoming bend be defined when several route branches are plausible?
4. Can a model use chart-derived context without encoding region identity as a shortcut?
5. Does transfer improve when position is expressed in a local route frame instead of latitude and longitude?
6. Which independent regions provide a credible cross-waterway evaluation?

## Vessel context and manoeuvring physics

1. Why do type and dimensions help in-area but contribute less for held-out vessels and waters?
2. Do length-normalised turn and acceleration features transfer better than raw dimensions?
3. Can simple speed- and length-dependent turn constraints prevent physically implausible predictions?
4. How should ferries, high-speed craft, tugs and service vessels be represented when operating patterns dominate
   static dimensions?
5. Are draught values reliable enough to model loading condition, or should they be excluded without validation?

## Evaluation design

1. How should spatial folds be constructed to separate geographic novelty from tree extrapolation at feature-range
   boundaries?
2. Can route-held-out and independent-waterway tests complement the current longitude-band evaluation?
3. Should confidence intervals resample vessels, days, routes or a hierarchy of all three?
4. How much do overlapping windows alter effective sample size?
5. Which accuracy and calibration measures correspond to an actual maritime decision?
6. How stable are results across seasons, weather conditions and receiver coverage?

## Prediction formulation

1. Is residual correction to CV still the best target when route geometry is available?
2. Would a regime-aware mixture of experts improve transfer without fragmenting the data?
3. Should the model predict positions, velocity changes, route-relative coordinates or trajectory distributions?
4. Which probabilistic formulation gives calibrated and operationally understandable uncertainty?
5. How should several plausible route branches be scored without rewarding unrealistic candidate diversity?

## Data and context

1. How should conflicting records with the same MMSI and timestamp be resolved?
2. Which environmental sources—wind, current, wave and bathymetry—are available with adequate spatial and temporal
   alignment?
3. How should nearby vessels and COLREG encounter geometry be included without future leakage?
4. Can destination, ETA and navigation status be normalised reliably enough to represent intent?
5. What data-quality changes occur when Class B traffic or satellite AIS is introduced?

## Behaviour deviation

1. What constitutes an operationally meaningful anomaly rather than a statistical outlier?
2. Which deviation categories can be labelled with acceptable confidence?
3. Can calibrated prediction residuals outperform transparent route, speed and turn thresholds?
4. How should legitimate avoidance, pilotage, weather response and port manoeuvring be distinguished from concerning
   behaviour?
5. What false-alarm rate is acceptable for human review?
