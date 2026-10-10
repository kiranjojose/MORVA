"""Past-only features for learned predictors, in the vessel's body frame at the anchor point.

Body frame: origin at the last observed position, 'along' axis = course over ground at the anchor,
'cross' axis = 90 deg to starboard. Expressing the past path and the future target in this frame
makes the problem heading-invariant, so the model learns manoeuvres rather than compass directions.
"""

import numpy as np
import polars as pl

from vesselmind.geo import KNOT_MS, to_local_xy
from vesselmind.models.baselines import _speed_course


def to_body(x, y, theta_rad):
    """ENU (x east, y north) -> (along, cross-to-starboard) for a course theta (clockwise from north)."""
    s, c = np.sin(theta_rad), np.cos(theta_rad)
    return x * s + y * c, x * c - y * s


def from_body(along, cross, theta_rad):
    s, c = np.sin(theta_rad), np.cos(theta_rad)
    return along * s + cross * c, along * c - cross * s


def anchor_frame(hist, step_s):
    """Anchor lat/lon, speed (m/s) and course (rad) used by both features and targets."""
    sog, cog = _speed_course(hist, step_s)
    return hist[:, -1, 0], hist[:, -1, 1], sog * KNOT_MS, np.radians(cog)


def _net_turn(cog, k, step_s):
    d = (np.diff(cog[:, -(k + 1):], axis=1) + 180) % 360 - 180
    return np.nansum(d, axis=1) / (k * step_s / 60)  # signed deg/min, + = starboard


MOTION_FEATURES = [
    "sog", "sog_mean", "sog_std", "dsog_2", "dsog_5", "dsog_10", "dsog_19",
    "turn_2", "turn_5", "turn_10", "turn_19", "cog_jitter",
    "fd_speed_ratio",
    "along_m2", "cross_m2", "along_m5", "cross_m5", "along_m10", "cross_m10", "along_m19", "cross_m19",
]
VESSEL_FEATURES = ["ship_group", "length", "width", "draught"]
LOCATION_FEATURES = ["lat", "lon", "sin_cog", "cos_cog"]

SHIP_GROUPS = {
    "Cargo": "cargo", "Tanker": "tanker", "Passenger": "passenger", "HSC": "passenger",
    "Tug": "service", "Pilot": "service", "SAR": "service", "Dredging": "service", "Towing": "service",
    "Towing long/wide": "service", "Port tender": "service", "Law enforcement": "service",
    "Anti-pollution": "service", "Diving": "service",
}
SHIP_GROUP_CODES = {g: i for i, g in enumerate(["cargo", "tanker", "passenger", "service", "other"])}


def motion_features(hist: np.ndarray, step_s: int) -> dict[str, np.ndarray]:
    lat0, lon0, v, th = anchor_frame(hist, step_s)
    sog, cog = hist[:, :, 2], hist[:, :, 3]
    f = {
        "sog": hist[:, -1, 2],
        "sog_mean": np.nanmean(sog, axis=1),
        "sog_std": np.nanstd(sog, axis=1),
    }
    for k in (2, 5, 10, 19):
        f[f"dsog_{k}"] = sog[:, -1] - sog[:, -1 - k]
        f[f"turn_{k}"] = _net_turn(cog, k, step_s)
    d = (np.diff(cog[:, -11:], axis=1) + 180) % 360 - 180
    f["cog_jitter"] = np.nanmean(np.abs(d), axis=1)
    x1, y1 = to_local_xy(hist[:, -2, 0], hist[:, -2, 1], lat0, lon0)
    f["fd_speed_ratio"] = np.hypot(x1, y1) / step_s / np.maximum(v, 0.1)
    for k in (2, 5, 10, 19):
        x, y = to_local_xy(hist[:, -1 - k, 0], hist[:, -1 - k, 1], lat0, lon0)
        f[f"along_m{k}"], f[f"cross_m{k}"] = to_body(x, y, th)
    return f


def build_features(hist: np.ndarray, meta: pl.DataFrame, step_s: int, sets: list[str]) -> tuple[np.ndarray, list[str]]:
    """sets: subset of {'motion', 'vessel', 'location'}. Returns X and column names (NaN = missing)."""
    cols: dict[str, np.ndarray] = {}
    if "motion" in sets:
        cols.update(motion_features(hist, step_s))
    if "vessel" in sets:
        groups = meta["ship_type"].replace_strict(SHIP_GROUPS, default="other", return_dtype=pl.String)
        codes = groups.replace_strict(SHIP_GROUP_CODES, return_dtype=pl.Float64)
        cols["ship_group"] = np.where(meta["ship_type"].is_null().to_numpy(), np.nan, codes.to_numpy())
        for c in ("length", "width", "draught"):
            cols[c] = meta[c].cast(pl.Float64).to_numpy()
    if "location" in sets:
        _, _, _, th = anchor_frame(hist, step_s)
        cols.update(lat=hist[:, -1, 0], lon=hist[:, -1, 1], sin_cog=np.sin(th), cos_cog=np.cos(th))
    names = list(cols)
    return np.column_stack([cols[n] for n in names]).astype(np.float64), names
