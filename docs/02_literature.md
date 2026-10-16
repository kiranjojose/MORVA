# 02 — Literature position for the preliminary summary

This is a deliberately bounded review. I verified the three papers cited in `paper/preliminary_summary.md`; the wider
reading programme remains in `references/literature_matrix.csv` and should be completed before a journal submission.

## Verified sources used in the summary

### Yang et al. (2024): AIS and machine learning across maritime applications

Yang et al. review the use of machine learning with AIS across trajectory-level and higher-level maritime research,
including trajectory prediction, collision avoidance, anomaly detection and energy efficiency. The paper is useful
here as a broad account of the field rather than as evidence for a particular prediction model. It identifies AIS data
quality, the need for benchmark datasets and the integration of AIS with additional information sources as continuing
research needs. These points support MORVA's emphasis on provenance, controlled comparisons and contextual
information.

**Verified from:** full text and publication record. DOI: `10.1016/j.tre.2024.103426`.

### Li, Jiao and Yang (2023a): systematic review and methods analysis

This systematic review covers ship-trajectory-prediction literature from 2000 to June 2023. From 1,356 initial records,
the authors retain 84 papers for systematic analysis and compare thirteen method families: Kalman filter, support
vector regression, Gaussian process regression, back-propagation neural network, random forest, RNN, LSTM, Bi-LSTM,
GRU, Bi-GRU, sequence-to-sequence, spatio-temporal graph convolutional network and transformer. The review stresses
that prediction suitability depends on the application and that future work must address navigation intention,
vessel interaction, interpretability, reliability and multi-source information. This supports treating architecture as
only one part of the problem and motivates explicit context and generalisation analysis.

**Verified from:** open-access full text, Sections 2–6. DOI: `10.1016/j.engappai.2023.107062`.

### Li, Jiao and Yang (2023b): comparative prediction benchmark

The companion experimental study implements five classical machine-learning and seven deep-learning approaches and
compares them on six evaluation measures. Its three AIS datasets represent a normal channel at Chengshan Jiao, complex
traffic in the Zhoushan Archipelago and a port setting at Caofeidian. The study is relevant because it evaluates model
fitness across different maritime environments rather than assuming one universally best method. MORVA takes a
different but complementary approach: it holds the learned architecture fixed while ablating motion, vessel and
location information and then evaluates transfer to unseen vessels and spatial bands.

**Verified from:** open-access publication record and article abstract/method description. DOI:
`10.1016/j.tre.2023.103152`.

## Short state-of-the-art position

AIS trajectory prediction has progressed from motion extrapolation and state estimation to classical machine learning,
recurrent sequence models, graph-based interaction models and transformers. The literature shows two broad trends.
First, increasingly expressive models are used to capture nonlinear movement, longer temporal dependencies and
interactions. Second, researchers are adding contextual information such as vessel characteristics, geographic
structure, weather and surrounding traffic.

The main unresolved issue for this study is not whether a complex model can fit a familiar AIS dataset. It is whether
the reported improvement is attributable to the model, to extra information, or to shortcuts created by repeated
vessels and familiar geography. Differences in regions, preprocessing, prediction horizons, data splits and metrics
make comparisons across papers difficult. A model evaluated on random or overlapping samples may answer a different
question from a model evaluated on later days, unseen vessels or unseen waters.

MORVA therefore occupies a narrower position than a general state-of-the-art architecture paper. It uses strong
kinematic baselines and a fixed residual learner to ask when motion, vessel and raw geographic context help. Its
spatial result also exposes a distinction that aggregate in-area accuracy can hide: location can be highly predictive
without being transferable.

## Gap addressed by the first study

The first study addresses four connected gaps:

1. **Attribution:** context feature groups are changed while the learned model and evaluation samples remain fixed.
2. **Interpretability:** performance is reported by past-only manoeuvring regime rather than only as one aggregate.
3. **Generalisation:** chronological, vessel-held-out and spatially held-out settings are reported separately.
4. **Negative evidence:** the failure of raw coordinates outside their training waters is retained as a result rather
   than hidden by the strong in-area score.

This does not establish that MORVA is the state of the art in absolute predictive accuracy. The present claim is
methodological and empirical: context gains must be decomposed and tested under the form of novelty relevant to the
intended application.

## References

- Yang, Y., Liu, Y., Li, G., Zhang, Z. and Liu, Y. (2024). *Harnessing the power of machine learning for AIS
  data-driven maritime research: A comprehensive review.* Transportation Research Part E, 183, 103426.
  <https://doi.org/10.1016/j.tre.2024.103426>
- Li, H., Jiao, H. and Yang, Z. (2023a). *Ship trajectory prediction based on machine learning and deep learning: A
  systematic review and methods analysis.* Engineering Applications of Artificial Intelligence, 126, 107062.
  <https://doi.org/10.1016/j.engappai.2023.107062>
- Li, H., Jiao, H. and Yang, Z. (2023b). *AIS data-driven ship trajectory prediction modelling and analysis based on
  machine learning and deep learning methods.* Transportation Research Part E, 175, 103152.
  <https://doi.org/10.1016/j.tre.2023.103152>

## Reading still required before journal submission

The paper-level review is not complete. The next literature pass should add primary studies on: strong CV/CTRV and
Kalman baselines; Danish AIS prediction; fairway and chart context; calibrated and multimodal uncertainty;
interaction-aware prediction; cross-region transfer; and anomaly evaluation with credible ground truth. Each paper
should be entered in the literature matrix from its methods, data, evaluation tables and limitations—not from its
abstract alone.
