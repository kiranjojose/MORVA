"""Deviation screening from calibrated forecasts (V4).

A detector is a score per window and horizon prefix: `scores[i, k]` summarises how unusual window i's observed
future is up to knot k, so it can be computed as soon as that much of the future has been observed. Every detector,
model-based or rule-based, is turned into a conformal p-value against calibration windows of normal traffic:

    p = (1 + #{calibration scores >= score}) / (n + 1)

For a new window exchangeable with the calibration windows, P(p <= alpha) <= alpha at each horizon, so flagging at
p <= alpha gives a false-alarm rate of at most alpha there, whatever the score. Detectors are then compared by how many
deviating windows they flag at the same false-alarm rate. Windows of one vessel are correlated, so the guarantee is
approximate and false-alarm rates are always measured on held-out normal windows. Flagging at the first horizon with
p <= alpha tests several horizons, so its overall false-alarm rate is reported separately; dividing alpha by the
number of horizons bounds it.

Real deviation labels do not exist, so deviations are injected into the observed futures of real windows: a turn, a
stop, a speed change or a position jump (a data fault), starting at a chosen step after the forecast origin. The
history is never changed, so the forecast and its box are those the model would have issued.
"""

import numpy as np

from morva.features.motion import anchor_frame, from_body
from morva.geo import KNOT_MS, from_local_xy, to_local_xy

KINDS = ("turn", "stop", "speed", "jump")


def conformal_pvalues(cal_scores: np.ndarray, scores: np.ndarray) -> np.ndarray:
    """P-values [n, K] for scores [n, K] against calibration scores [n_cal, K]; larger scores are more unusual."""
    n = cal_scores.shape[0]
    if n == 0:
        raise ValueError("no calibration windows")
    srt = np.sort(cal_scores, axis=0)
    greater_eq = np.stack([n - np.searchsorted(srt[:, k], scores[:, k], side="left")
                           for k in range(scores.shape[1])], axis=1)
    return (1 + greater_eq) / (n + 1)


def prefix_max(per_knot: np.ndarray) -> np.ndarray:
    """Running maximum over knots, so the score at knot k uses everything observed up to k."""
    return np.maximum.accumulate(per_knot, axis=1)


def box_excess_scores(lo: np.ndarray, hi: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Model score [n, K]: how far the true residual y lies outside the predicted box, in units of the box's
    half-width on the worse axis, as a running maximum over knots. Inputs [n, K, 2] as in `conformal.box_scores`."""
    half = np.maximum((hi - lo) / 2, 1.0)
    return prefix_max(np.max(np.maximum(lo - y, y - hi) / half, axis=-1))


def _future_xy(hist, fut, step_s):
    """Future positions in metres from the forecast origin, prepended with the origin itself: [n, T + 1] each."""
    lat0, lon0, v, th = anchor_frame(hist, step_s)
    x, y = to_local_xy(fut[..., 0], fut[..., 1], lat0[:, None], lon0[:, None])
    zero = np.zeros((len(fut), 1))
    return np.hstack([zero, x]), np.hstack([zero, y]), lat0, lon0, v, th


def rule_scores(hist: np.ndarray, fut: np.ndarray, step_s: int, knots_steps, min_speed_kn: float = 1.0) -> dict:
    """Model-free comparison scores [n, K], each a running maximum up to the knot:

    - `cv_distance`: distance (m) of the observed position from the constant-velocity forecast;
    - `turn`: largest course change (deg) of a one-step displacement from the course at the origin, ignoring steps
      slower than `min_speed_kn`;
    - `speed`: largest change (kn) of one-step speed from the speed at the origin.
    """
    x, y, _, _, v, th = _future_xy(hist, fut, step_s)
    steps = np.arange(x.shape[1])
    cv_x, cv_y = from_body(v[:, None] * steps * step_s, np.zeros_like(x), th[:, None])
    dist = np.hypot(x - cv_x, y - cv_y)[:, 1:]
    dx, dy = np.diff(x, axis=1), np.diff(y, axis=1)
    speed_kn = np.hypot(dx, dy) / step_s / KNOT_MS
    course = np.arctan2(dx, dy)
    turn = np.abs(np.degrees((course - th[:, None] + np.pi) % (2 * np.pi) - np.pi))
    turn = np.where(speed_kn >= min_speed_kn, turn, 0.0)
    dspeed = np.abs(speed_kn - v[:, None] / KNOT_MS)
    idx = np.asarray(knots_steps) - 1
    return {name: np.maximum.accumulate(s, axis=1)[:, idx]
            for name, s in (("cv_distance", dist), ("turn", turn), ("speed", dspeed))}


def inject(hist: np.ndarray, fut: np.ndarray, step_s: int, kind: str, onset_step: int, magnitude: float,
           rate_deg_min: float = 10.0, decel_steps: int = 5, rng: np.random.Generator | None = None) -> np.ndarray:
    """Return a copy of `fut` [n, T, 2] with a deviation from step `onset_step` (1-based; earlier steps unchanged).

    - `turn`: later one-step displacements turn by `magnitude` degrees in total at `rate_deg_min` (positive =
      starboard);
    - `stop`: speed falls linearly to zero over `decel_steps`, then the vessel stays put; `magnitude` is ignored;
    - `speed`: later one-step displacements are scaled by `magnitude` (e.g. 0.5 or 1.5);
    - `jump`: positions from the onset are shifted by `magnitude` metres in a random direction (a data fault).
    """
    if kind not in KINDS:
        raise ValueError(f"unknown deviation {kind!r}; expected one of {KINDS}")
    if not 1 <= onset_step <= fut.shape[1]:
        raise ValueError(f"onset_step must be in 1..{fut.shape[1]}")
    x, y, lat0, lon0, _, _ = _future_xy(hist, fut, step_s)
    dx, dy = np.diff(x, axis=1), np.diff(y, axis=1)
    after = np.arange(1, fut.shape[1] + 1) >= onset_step  # displacement j ends at step j + 1 (1-based)
    if kind == "turn":
        minutes = (np.arange(1, fut.shape[1] + 1) - onset_step + 1) * step_s / 60
        angle = np.radians(np.sign(magnitude) * np.minimum(abs(magnitude), rate_deg_min * minutes))
        angle = np.where(after, angle, 0.0)[None, :]
        s, c = np.sin(angle), np.cos(angle)
        dx, dy = dx * c + dy * s, -dx * s + dy * c  # clockwise rotation in the east/north plane
    elif kind in ("stop", "speed"):
        if kind == "stop":
            k = np.arange(1, fut.shape[1] + 1) - onset_step + 1
            factor = np.where(after, np.clip(1 - k / decel_steps, 0.0, 1.0), 1.0)
        else:
            factor = np.where(after, magnitude, 1.0)
        dx, dy = dx * factor[None, :], dy * factor[None, :]
    nx, ny = np.cumsum(dx, axis=1), np.cumsum(dy, axis=1)
    if kind == "jump":
        rng = rng or np.random.default_rng(0)
        bearing = rng.uniform(0, 2 * np.pi, size=(len(fut), 1))
        nx = nx + np.where(after, magnitude * np.sin(bearing), 0.0)
        ny = ny + np.where(after, magnitude * np.cos(bearing), 0.0)
    lat, lon = from_local_xy(nx, ny, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)


def detection_summary(p_normal: np.ndarray, p_deviating: np.ndarray, alpha: float, knots_steps,
                      onset_step: int, step_s: int) -> dict:
    """False-alarm and detection rates at significance `alpha`.

    Per horizon: share of normal windows flagged (false alarms) and of deviating windows flagged (detections).
    First-flag: a window is flagged at the first knot with p <= alpha; reported are the overall false-alarm rate,
    the detection rate, and the median delay (minutes) from the deviation onset to the flagging knot, counting only
    knots at or after the onset.
    """
    knots = np.asarray(knots_steps)
    usable = knots >= onset_step
    flag_n, flag_d = p_normal <= alpha, p_deviating[:, usable] <= alpha
    first = np.argmax(flag_d, axis=1)
    detected = flag_d.any(axis=1)
    delay_min = (knots[usable][first[detected]] - onset_step) * step_s / 60
    return {
        "alpha": alpha,
        "per_horizon": {int(k): {"false_alarm_rate": float(flag_n[:, i].mean()),
                                 "detection_rate": float((p_deviating[:, i] <= alpha).mean())}
                        for i, k in enumerate(knots)},
        "first_flag_false_alarm_rate": float(flag_n.any(axis=1).mean()),
        "first_flag_detection_rate": float(detected.mean()),
        "median_delay_min": float(np.median(delay_min)) if detected.any() else None,
        "n_normal": int(len(p_normal)),
        "n_deviating": int(len(p_deviating)),
    }


def residual_box_inputs(model, X: np.ndarray, hist: np.ndarray, fut: np.ndarray, step_s: int, level: float):
    """Predicted box bounds and true residuals [n, K, 2] for a fitted `QuantileResidualGBM`."""
    from morva.models.quantile import residual_truth

    lo, hi = model.interval(model.predict(X), level)
    return lo, hi, residual_truth(hist, fut, step_s, model.knots)

