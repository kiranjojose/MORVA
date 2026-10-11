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


def ctrv_damped(hist, n_future, step_s, tau_s, window_steps=5, max_rate_deg_s=3.0, min_sog_kn=1.0, substeps=6):
    """CTRV whose turn rate decays exponentially: w(t) = w0 * exp(-t / tau).

    Heading theta(t) = theta0 + w0 * tau * (1 - exp(-t / tau)), so the total extra course change is bounded by
    w0 * tau (a bend ends) instead of growing without limit. tau -> 0 recovers CV; tau -> inf recovers CTRV.
    Position is integrated numerically at step_s / substeps with midpoint headings.
    """
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    sog, cog = _speed_course(hist, step_s)
    v = (sog * KNOT_MS)[:, None]
    th0 = np.radians(cog)[:, None]
    w0 = np.radians(estimate_turn_rate(hist, step_s, window_steps, max_rate_deg_s, min_sog_kn))[:, None]
    dt = step_s / substeps
    t_mid = (np.arange(n_future * substeps) + 0.5)[None, :] * dt
    theta = th0 + w0 * tau_s * (1 - np.exp(-t_mid / tau_s))
    x = np.cumsum(v * np.sin(theta) * dt, axis=1)[:, substeps - 1 :: substeps]
    y = np.cumsum(v * np.cos(theta) * dt, axis=1)[:, substeps - 1 :: substeps]
    lat, lon = from_local_xy(x, y, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)


def kalman_cv(hist, n_future, step_s, q, r_pos_m=15.0, r_vel_ms=0.5):
    """Constant-velocity Kalman filter over the history, then straight-line extrapolation.

    State [x, y, vx, vy] in the local frame at the anchor (metres, m/s). Measurements are the resampled positions
    and the reported SOG/COG velocity (ignored where missing). Process noise is white acceleration with spectral
    density q (m^2/s^3), the single tuned parameter; r_pos_m / r_vel_ms are measurement standard deviations.
    """
    n, t_len = hist.shape[:2]
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    px, py = to_local_xy(hist[..., 0], hist[..., 1], lat0[:, None], lon0[:, None])
    vx, vy = velocity_from_sog_cog(hist[..., 2], hist[..., 3])
    dt = float(step_s)
    f = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
    qm = q * np.array([[dt**3 / 3, 0, dt**2 / 2, 0], [0, dt**3 / 3, 0, dt**2 / 2],
                       [dt**2 / 2, 0, dt, 0], [0, dt**2 / 2, 0, dt]])
    v0x = np.where(np.isnan(vx[:, 0]), (px[:, 1] - px[:, 0]) / dt, vx[:, 0])
    v0y = np.where(np.isnan(vy[:, 0]), (py[:, 1] - py[:, 0]) / dt, vy[:, 0])
    s = np.stack([px[:, 0], py[:, 0], v0x, v0y], axis=1)
    p = np.tile(np.diag([r_pos_m**2, r_pos_m**2, 4.0, 4.0]), (n, 1, 1))
    eye = np.eye(4)
    for t in range(1, t_len):
        s = s @ f.T
        p = f @ p @ f.T + qm
        vel_ok = ~(np.isnan(vx[:, t]) | np.isnan(vy[:, t]))
        z = np.stack([px[:, t], py[:, t], np.where(vel_ok, vx[:, t], s[:, 2]), np.where(vel_ok, vy[:, t], s[:, 3])], 1)
        r_vel = np.where(vel_ok, r_vel_ms**2, 1e8)
        r = np.zeros((n, 4, 4))
        r[:, 0, 0] = r[:, 1, 1] = r_pos_m**2
        r[:, 2, 2] = r[:, 3, 3] = r_vel
        k = p @ np.linalg.inv(p + r)
        s = s + np.einsum("nij,nj->ni", k, z - s)
        p = (eye - k) @ p
    tau = _future_times(n_future, step_s)[None, :]
    lat, lon = from_local_xy(s[:, 0:1] + s[:, 2:3] * tau, s[:, 1:2] + s[:, 3:4] * tau, lat0[:, None], lon0[:, None])
    return np.stack([lat, lon], axis=-1)
