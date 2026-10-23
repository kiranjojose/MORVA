"""Quantile residual model: prediction intervals around the constant-velocity forecast (V3).

Same targets as `ResidualGBM`: the along-track and cross-track offsets of the true future position from the CV
forecast, in the vessel's body frame, at knot horizons. One HistGradientBoostingRegressor with quantile loss per
(knot, axis, quantile). Intervals are made valid by conformal calibration (`morva.evaluation.conformal`).
"""

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

from morva.models.gbm import residual_targets

AXES = ("along", "cross")


class QuantileResidualGBM:
    def __init__(self, knots_steps, quantiles, categorical=None, seed=0, **hgb_params):
        self.knots = list(knots_steps)
        self.quantiles = sorted(quantiles)
        self.categorical = categorical
        self.seed = seed
        self.params = {"max_iter": 300, "learning_rate": 0.08, "max_leaf_nodes": 63, "min_samples_leaf": 50,
                       "l2_regularization": 1.0, "early_stopping": True, "validation_fraction": 0.1,
                       "n_iter_no_change": 20, **hgb_params}
        self.models = {}

    def fit(self, X, hist, fut, step_s):
        ta, tc = residual_targets(hist, fut, step_s, self.knots)
        for k in range(len(self.knots)):
            for axis, y in zip(AXES, (ta[:, k], tc[:, k]), strict=True):
                for q in self.quantiles:
                    m = HistGradientBoostingRegressor(loss="quantile", quantile=q,
                                                      categorical_features=self.categorical,
                                                      random_state=self.seed, **self.params)
                    self.models[(k, axis, q)] = m.fit(X, y)
        return self

    def predict(self, X) -> np.ndarray:
        """Residual quantiles, shape [n, knots, 2 (along, cross), quantiles], sorted along the last axis so
        independently fitted quantiles never cross."""
        out = np.stack([np.stack([np.column_stack([self.models[(k, a, q)].predict(X) for q in self.quantiles])
                                  for a in AXES], axis=1) for k in range(len(self.knots))], axis=1)
        return np.sort(out, axis=-1)

    def interval(self, pred: np.ndarray, level: float) -> tuple[np.ndarray, np.ndarray]:
        """Lower and upper residual bounds [n, knots, 2] for a central interval of the given level."""
        lo_q, hi_q = round((1 - level) / 2, 6), round((1 + level) / 2, 6)
        qs = [round(q, 6) for q in self.quantiles]
        if lo_q not in qs or hi_q not in qs:
            raise ValueError(f"level {level} needs quantiles {lo_q} and {hi_q}; configured {self.quantiles}")
        return pred[..., qs.index(lo_q)], pred[..., qs.index(hi_q)]

    def n_iter(self):
        return {f"{k}_{a}_{q:g}": int(m.n_iter_) for (k, a, q), m in self.models.items()}


def residual_truth(hist, fut, step_s, knots_steps) -> np.ndarray:
    """True residuals [n, knots, 2] to compare with predicted intervals."""
    ta, tc = residual_targets(hist, fut, step_s, knots_steps)
    return np.stack([ta, tc], axis=-1)
