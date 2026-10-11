"""Past-only manoeuvring regimes (definition: Kiran, 2026-10-11; see docs/04_methods.md).

Computed from the last `lookback_min` minutes of the observation history only. No future
position, future error or prediction is used, so regimes can never leak the answer.

Continuous variables are always kept alongside the label, so results never depend only on
the thresholds.
"""

from dataclasses import asdict, dataclass

import numpy as np

from vesselmind.geo import to_local_xy

REGIMES = ["low_speed", "steady", "turning", "speed_changing", "combined"]


@dataclass(frozen=True)
class RegimeParams:
    lookback_min: int = 10
    low_speed_kn: float = 5.0
    turn_deg_min: float = 1.0
    speed_change_kn: float = 2.0
    sustained_frac: float = 0.7  # sensitivity only: 'sustained turning'

    def label(self) -> str:
        return ", ".join(f"{k}={v:g}" for k, v in asdict(self).items())


def regime_variables(hist: np.ndarray, step_s: int, lookback_min: int) -> dict[str, np.ndarray]:
    k = int(lookback_min * 60 / step_s)
    sog, cog = hist[:, -(k + 1):, 2], hist[:, -(k + 1):, 3]
    d = (np.diff(cog, axis=1) + 180) % 360 - 180
    net = np.nansum(d, axis=1)
    minutes = k * step_s / 60
    same_sign = np.sign(d) == np.sign(net)[:, None]
    nonzero = (np.abs(d) > 1e-9) & ~np.isnan(d)

    # Course change from positions only: bearing of first half-leg vs second half-leg of the lookback
    lat0, lon0 = hist[:, -1, 0], hist[:, -1, 1]
    i0, im, i1 = -(k + 1), -(k // 2 + 1), -1

    def bearing(a, b):
        xa, ya = to_local_xy(hist[:, a, 0], hist[:, a, 1], lat0, lon0)
        xb, yb = to_local_xy(hist[:, b, 0], hist[:, b, 1], lat0, lon0)
        return np.degrees(np.arctan2(xb - xa, yb - ya))

    pos_change = (bearing(im, i1) - bearing(i0, im) + 180) % 360 - 180
    return {
        "mean_speed_kn": np.nanmean(sog, axis=1),
        "speed_change_kn": sog[:, -1] - sog[:, 0],
        "turn_signed_deg_min": net / minutes,
        "turn_abs_deg_min": np.abs(net) / minutes,
        "turn_consistency": np.where(nonzero.sum(1) > 0, (same_sign & nonzero).sum(1) / np.maximum(nonzero.sum(1), 1),
                                     np.nan),
        "turn_pos_abs_deg_min": np.abs(pos_change) / (minutes / 2),
        "cog_valid_frac": np.mean(~np.isnan(cog), axis=1),
    }


def assign_regimes(v: dict[str, np.ndarray], p: RegimeParams, sustained: bool = False) -> np.ndarray:
    turning = v["turn_abs_deg_min"] >= p.turn_deg_min
    if sustained:
        turning &= v["turn_consistency"] >= p.sustained_frac
    speed_changing = np.abs(v["speed_change_kn"]) >= p.speed_change_kn
    low = v["mean_speed_kn"] < p.low_speed_kn
    return np.select(
        [low, turning & speed_changing, turning, speed_changing],
        ["low_speed", "combined", "turning", "speed_changing"],
        default="steady",
    )


def turn_label_reliable(v: dict[str, np.ndarray], p: RegimeParams) -> np.ndarray:
    """Quality safeguard: enough COG, fast enough for COG to mean something, and the COG-based and
    position-based turn agree on which side of the threshold the window falls."""
    agree = (v["turn_abs_deg_min"] >= p.turn_deg_min) == (v["turn_pos_abs_deg_min"] >= p.turn_deg_min)
    return (v["cog_valid_frac"] >= 0.8) & (v["mean_speed_kn"] >= p.low_speed_kn) & agree


SENSITIVITY = (
    [("turn_deg_min", x) for x in (0.5, 2.0)]
    + [("speed_change_kn", x) for x in (1.0, 3.0)]
    + [("low_speed_kn", x) for x in (3.0, 7.0)]
    + [("lookback_min", x) for x in (5, 15)]
)
