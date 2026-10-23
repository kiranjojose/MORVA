"""Split-conformal calibration of 2-D prediction boxes (conformalized quantile regression).

For each knot, the predicted interval is a box in the vessel's body frame: [lo, hi] along-track times [lo, hi]
cross-track. The conformity score of a calibration window is how far its true residual lies outside the box on the
worse of the two axes, max over axes of max(lo - y, y - hi). Widening every box by the finite-sample quantile of
these scores gives joint coverage of at least the target level for new windows exchangeable with the calibration
windows (Romano, Patterson and Candès, 2019). Windows of one vessel are correlated, so the guarantee is approximate;
coverage is therefore always measured on held-out windows.
"""

import numpy as np


def box_scores(lo: np.ndarray, hi: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Scores [n, knots] for boxes lo/hi and truths y of shape [n, knots, 2]; <= 0 means inside the box."""
    return np.max(np.maximum(lo - y, y - hi), axis=-1)


def conformal_offset(scores: np.ndarray, level: float) -> np.ndarray:
    """Per-knot widening [knots]: the k-th smallest calibration score, k = ceil((n + 1) * level). With too few
    calibration windows for the level (k > n) no finite widening is valid, so the offset is infinite."""
    n = scores.shape[0]
    if n == 0:
        raise ValueError("no calibration windows")
    k = int(np.ceil((n + 1) * level))
    if k > n:
        return np.full(scores.shape[1], np.inf)
    return np.sort(scores, axis=0)[k - 1]


def coverage(lo: np.ndarray, hi: np.ndarray, y: np.ndarray, offset: np.ndarray) -> np.ndarray:
    """Share of windows whose truth lies inside the widened box, per knot [knots]."""
    return (box_scores(lo, hi, y) <= offset[None, :]).mean(axis=0)


def half_widths(lo: np.ndarray, hi: np.ndarray, offset: np.ndarray) -> np.ndarray:
    """Mean half-width of the widened box per knot and axis [knots, 2], in metres."""
    return np.maximum((hi - lo) / 2 + offset[None, :, None], 0).mean(axis=0)
