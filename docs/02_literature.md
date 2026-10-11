# 02 — Literature

Matrix: [`references/literature_matrix.csv`](../references/literature_matrix.csv) (34 columns) · BibTeX:
[`references/references.bib`](../references/references.bib)

> Don't fill the matrix from abstracts alone. For important papers (especially R4, R5, R6), read the methods, dataset,
> evaluation, tables and limitations.

## Questions to answer for every paper (1–2 sentences each)

**Framing.** (1) What exact problem does it solve? (2) Trajectory, destination or route prediction, anomaly detection,
collision risk or traffic flow? (3) Claimed operational use case? (4) Claimed novelty?

**Data.** (5) Where was the AIS collected? (6) Dates and duration? (7) Vessels, messages, trajectories, samples?
(8) Class A, Class B, which vessel types? (9) Public dataset? (10) Reproducible from the paper?

**Preprocessing.** (11) Duplicates, invalid positions, gaps, missing fields, outliers? (12) Track segmentation?
(13) Resampling interval? (14) How much interpolation? (15) Stationary or low-speed vessels removed? (16) Could
preprocessing remove the difficult cases and flatter performance?

**Task.** (17) History length? (18) Horizons? (19) Predicting coordinates, displacement, course/speed, route class or
a distribution? (20) Autoregressive or direct? (21) One future or several?

**Features.** (22) Motion variables? (23) Vessel type, length, draught, nav status? (24) Geographic, route, fairway,
weather, current, bathymetry? (25) Neighbouring vessels or encounters? (26) Is every input available at prediction time?

**Models and baselines.** (27) Proposed model? (28) Transparent baselines? (29) **Constant velocity?** (30) CTRV or
Kalman? (31) Identical samples and splits for all models? (32) Is the gain from the architecture, extra context, or both?

**Evaluation validity.** (33) How are train/val/test split? (34) Can the same vessel appear in every split?
(35) Can overlapping windows cross splits? (36) Temporal or spatial leakage? (37) Unseen vessels, future periods or new
regions tested? (38) Hyperparameters chosen on test data?

**Metrics and evidence.** (39) Metrics? (40) Reported per horizon? (41) Median, tail errors or CIs? (42) Several seeds?
(43) Ablations? (44) Results by vessel type, region or manoeuvring regime? (45) Uncertainty calibrated or only
visualised?

**Limitations and relevance.** (46) Failure modes reported? (47) A limitation the authors don't discuss? (48) What can
VesselMind reproduce? (49) What should VesselMind do differently? (50) Does the paper strengthen, weaken or change our
research gap?

## Scope notes on R1–R7 (verify while reading)

| Paper | Use it for | Don't use it for / read critically |
|---|---|---|
| R1 Yang et al. 2024, AIS+ML review | Broad motivation; taxonomy of AIS applications; data quality, benchmark and multi-source challenges | Evaluation design; "best model" claims |
| R2 Ribeiro et al. 2023, anomaly review | Message vs trajectory anomalies; supervised/unsupervised; the ground-truth problem; future anomaly taxonomy | Does the field evaluate real operational anomalies or mostly statistical outliers and simulations? |
| R3 Li, Jiao & Yang 2023, systematic review | Trajectory-prediction taxonomy (Kalman, SVR, GP, RF, RNN/LSTM/GRU, seq2seq, graph, transformer); related work | Is there a consistent evaluation standard? |
| R4 Li, Jiao & Yang 2023, benchmark | 12 methods across a normal channel, archipelago and port; ranking depends on environment | Splits, horizons, **CV included?**, equal inputs, manoeuvres analysed separately, uncertainty, code/data public |
| R5 Zhang et al. 2023, clustering + anomaly | Route-dependent normality; prediction residuals as anomaly signals (Yantai Port) | Anomaly ground truth, threshold tuning, generalisation beyond the port, baselines |
| R6 Wolsing et al. 2022, AIS-track anomaly review | Anomaly taxonomy; route deviation dominates; regional dependence; private data; scarce ground truth; simulated anomalies | (Most useful review for the limitations section) |
| R7 Transp. Res. Procedia 2023 overview | Short orientation; terminology; finding references | Research gap or state-of-the-art claims |

## Additional papers the review still needs (find and verify)
- A reproducible CV/CTRV or Kalman-baseline study
- An uncertainty-aware vessel-prediction paper using Danish AIS (candidates: TrAISformer, GeoTrackNet)
- A feature-ablation study
- A navigation / fairway-context paper
- A multi-vessel interaction paper
- A probabilistic or multimodal prediction paper
- A cross-region generalisation paper
- A recent (2025–2026) trajectory-prediction review

---

## Working draft of the literature review

> **Status: UNVERIFIED DRAFT (11 Oct 2026).** Every statement about a paper must be checked against the paper itself,
> with page or table references, before it appears in any submitted document. Rewrite it in your own words. Written
> without reference to VesselMind's results.

### AIS-based maritime behaviour modelling
AIS provides large-scale observations of vessel position, course, speed, identity and selected static or
voyage-related attributes. These records support research in trajectory reconstruction, traffic-pattern extraction,
trajectory prediction, collision-risk assessment, anomaly detection and emissions analysis. Reviews describe a shift
from descriptive AIS analytics towards machine-learning systems for situational awareness and autonomous navigation.
The value of AIS comes with substantial data-quality challenges: irregular reporting, duplicates, missing or stale
static fields, inconsistent identifiers, positional errors and incomplete receiver coverage. Yang et al. [R1] identify
the lack of common benchmark datasets and the limited integration of AIS with other sources as continuing barriers to
reliable comparison and deployment. *(verify)*

### Ship trajectory prediction
Methods can be grouped into kinematic models (constant velocity, constant turn rate), classical data-driven methods
(Kalman filters, support-vector methods, Gaussian processes, tree ensembles) and deep learning (RNNs, encoder-decoders,
graph models, transformers, probabilistic generative models). Li, Jiao and Yang's systematic review [R3] traces this
development and compares input requirements, computational characteristics, strengths and limitations. Suitability
depends on horizon, traffic environment, data availability and application, so architecture alone is not a sufficient
basis for judging prediction quality. *(verify)* Their experimental benchmark [R4] compares 12 methods across a normal
channel, a complex archipelago and a port area, and shows that performance varies with the maritime environment
*(verify)*. Broader problems remain: private datasets, differing preprocessing, inconsistent horizons and metrics, and
comparisons that do not always include strong transparent kinematic baselines.

### Context-aware prediction
Past position, speed and course show recent motion but not necessarily future intent. A vessel starting a course
alteration may keep turning, settle on a new course, enter a port approach, follow a fairway bend or react to traffic.
Vessel particulars, route geometry, environment and interactions may carry information that motion history does not.
Context is often introduced together with a new architecture, which makes it hard to tell whether the gain comes from
the information or the model. Raw coordinates may let a model memorise regional routes rather than learn transferable
behaviour. Controlled feature ablations, and evaluation on unseen vessels, later periods and held-out areas, are
therefore needed.

### Manoeuvring regimes
Prediction difficulty is not uniform. Straight, steady transit suits simple extrapolation; course alterations, speed
changes and low-speed manoeuvring violate constant-motion assumptions. A complex model can look beneficial mainly
because of a dataset's regime mix. Benchmarks compare geographic scenarios, but fewer studies isolate performance by
regimes defined strictly from information available before prediction *(verify against R3/R4)*. Regime-conditioned
evaluation shows whether a model helps generally or only in specific behaviours, and links statistical performance to
interpretable ship-handling conditions.

### Uncertainty and generalisation
Future trajectories can be multimodal near junctions, ports and encounters; a single prediction may average between
valid routes. Uncertainty outputs are only useful if calibrated. High accuracy in a familiar region does not establish
generalisation: repeated vessels, overlapping windows, random splits and memorised geography can all inflate results.
Credible evaluation needs chronological separation, protection against windows crossing split boundaries, and
vessel- and spatially held-out analysis.

### AIS anomaly detection
Reviews distinguish route deviations, unexpected activity, close approaches, unusual port calls or zone entries,
identity and reporting anomalies, and speed or course behaviours, addressed with clustering, density estimation,
reconstruction or prediction errors, and rule-based constraints. Wolsing et al. [R6] review 44 studies: route
deviation dominates, many models are region-specific, datasets are often private, and reliable labelled ground truth is
scarce, so simulated anomalies are common. These measure sensitivity to the injected pattern, not detection of real
incidents. *(verify)* Ribeiro et al. [R2] similarly emphasise limited labels and heterogeneous definitions of
abnormality. A statistical outlier is not automatically unsafe or illegal; slowing may be abnormal in a lane but
expected near a berth. Zhang et al. [R5] combine compressed trajectories, DTW similarity, density-based clustering and
transformer prediction near Yantai Port, which illustrates learned route normality but raises questions of regional
dependence and ground truth. *(verify)*

### Identified research gap
Inconsistent preprocessing and evaluation; strong kinematic baselines not always emphasised; performance rarely
explained by interpretable manoeuvring regimes; context and architecture changed at the same time; repeated vessels and
familiar geography inflating generalisation; uncertainty not calibrated; anomaly studies lacking common data and real
ground truth. The proposed direction is not another architecture but a controlled study of **when context helps**:
identical samples, transparent and learned baselines, motion/vessel/geographic ablation, past-only regimes, and
temporal, vessel and spatial generalisation tests.
