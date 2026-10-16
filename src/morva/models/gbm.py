"""Gradient-boosted residual predictor: CV forecast + learned correction in the body frame.

Targets are the (along, cross) offsets of the true future position from the CV forecast at knot
horizons (default 5/10/15/20 min). One HistGradientBoostingRegressor per (knot, axis). The full
1-min trajectory is recovered by linear interpolation of the residual between knots (residual 0 at t=0).
"""

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

from morva.features.motion import anchor_frame, from_body, to_body
from morva.geo import from_local_xy, to_local_xy


def residual_targets(hist, fut, step_s, knots_steps):
    lat0, lon0, v, th = anchor_frame(hist, step_s)
    idx = np.asarray(knots_steps) - 1
    x, y = to_local_xy(fut[:, idx, 0], fut[:, idx, 1], lat0[:, None], lon0[:, None])
    along, cross = to_body(x, y, th[:, None])
    t = np.asarray(knots_steps)[None, :] * step_s
    return along - v[:, None] * t, cross  # [n, K] each


def residuals_to_positions(hist, r_along, r_cross, step_s, n_future, knots_steps):
    lat0, lon0, v, th = anchor_frame(hist, step_s)
    steps = np.arange(1, n_future + 1)
    kn = np.concatenate([[0], knots_steps])
    ra = np.stack([np.interp(steps, kn, np.concatenate([[0], r])) for r in r_along])
    rc = np.stack([np.interp(steps, kn, np.concatenate([[0], r])) for r in r_cross])
    along = v[:, None] * steps[None, :] * step_s + ra
    x, y = from_body(along, rc, th[:, None])
    lat, lon = from_local_xy(x, y, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)


class ResidualGBM:
    def __init__(self, knots_steps=(5, 10, 15, 20), categorical=None, seed=0, **hgb_params):
        self.knots = list(knots_steps)
        self.categorical = categorical
        self.seed = seed
        self.params = {"max_iter": 400, "learning_rate": 0.08, "max_leaf_nodes": 63, "min_samples_leaf": 50,
                       "l2_regularization": 1.0, "early_stopping": True, "validation_fraction": 0.1,
                       "n_iter_no_change": 20, **hgb_params}
        self.models = {}

    def fit(self, X, hist, fut, step_s):
        ta, tc = residual_targets(hist, fut, step_s, self.knots)
        for k in range(len(self.knots)):
            for axis, y in (("along", ta[:, k]), ("cross", tc[:, k])):
                m = HistGradientBoostingRegressor(categorical_features=self.categorical, random_state=self.seed,
                                                  loss="absolute_error", **self.params)
                self.models[(k, axis)] = m.fit(X, y)
        return self

    def predict(self, X, hist, step_s, n_future):
        ra = np.column_stack([self.models[(k, "along")].predict(X) for k in range(len(self.knots))])
        rc = np.column_stack([self.models[(k, "cross")].predict(X) for k in range(len(self.knots))])
        return residuals_to_positions(hist, ra, rc, step_s, n_future, self.knots)

    def n_iter(self):
        return {f"{k}_{a}": int(m.n_iter_) for (k, a), m in self.models.items()}
