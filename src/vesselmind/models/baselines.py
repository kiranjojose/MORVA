"""Transparent kinematic baselines. All take hist [n, T, 4] (lat, lon, sog, cog) at a fixed
step and return predicted positions [n, n_future, 2] (lat, lon).

- persistence: vessel stays at last position
- cv:   constant velocity from last reported SOG/COG (finite-difference fallback if missing)
- ctrv: constant turn rate and velocity; turn rate from recent COG change
"""

import numpy as np

from vesselmind.geo import KNOT_MS, from_local_xy, to_local_xy, velocity_from_sog_cog


def _future_times(n_future: int, step_s: float) -> np.ndarray:
    return np.arange(1, n_future + 1) * step_s


def persistence(hist, n_future, step_s):
    return np.repeat(hist[:, -1:, :2], n_future, axis=1)


def _speed_course(hist, step_s):
    """Last SOG (kn) and COG (deg), falling back to the last finite-difference displacement."""
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    x, y = to_local_xy(hist[:, -2, 0], hist[:, -2, 1], lat0, lon0)
    fd_speed = np.hypot(x, y) / step_s / KNOT_MS
    fd_course = np.degrees(np.arctan2(-x, -y)) % 360  # from previous point to current
    sog = np.where(np.isnan(hist[:, -1, 2]), fd_speed, hist[:, -1, 2])
    cog = np.where(np.isnan(hist[:, -1, 3]), fd_course, hist[:, -1, 3])
    return sog, cog


def cv(hist, n_future, step_s):
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    sog, cog = _speed_course(hist, step_s)
    vx, vy = velocity_from_sog_cog(sog, cog)
    tau = _future_times(n_future, step_s)
    lat, lon = from_local_xy(vx[:, None] * tau, vy[:, None] * tau, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)


def estimate_turn_rate(hist, step_s, window_steps, max_rate_deg_s, min_sog_kn):
    """Mean COG rate (deg/s) over the last `window_steps`, clipped; 0 when slow or unknown."""
    cog = hist[:, -(window_steps + 1):, 3]
    d = (np.diff(cog, axis=1) + 180) % 360 - 180
    rate = np.nanmean(d, axis=1) / step_s if d.shape[1] else np.zeros(len(hist))
    rate = np.nan_to_num(np.clip(rate, -max_rate_deg_s, max_rate_deg_s))
    return np.where(np.nan_to_num(hist[:, -1, 2]) < min_sog_kn, 0.0, rate)


def ctrv(hist, n_future, step_s, window_steps=5, max_rate_deg_s=3.0, min_sog_kn=1.0):
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    sog, cog = _speed_course(hist, step_s)
    v = (sog * KNOT_MS)[:, None]
    th0 = np.radians(cog)[:, None]
    w = np.radians(estimate_turn_rate(hist, step_s, window_steps, max_rate_deg_s, min_sog_kn))[:, None]
    tau = _future_times(n_future, step_s)[None, :]

    straight = np.abs(w) < 1e-6
    w_safe = np.where(straight, 1.0, w)
    # Bearing measured clockwise from north: dx/dt = v sin(th), dy/dt = v cos(th)
    x_turn = v / w_safe * (np.cos(th0) - np.cos(th0 + w_safe * tau))
    y_turn = v / w_safe * (np.sin(th0 + w_safe * tau) - np.sin(th0))
    x = np.where(straight, v * np.sin(th0) * tau, x_turn)
    y = np.where(straight, v * np.cos(th0) * tau, y_turn)
    lat, lon = from_local_xy(x, y, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)
