"""V4 deviation screening: conformal p-values, injected deviations and rule scores."""

import numpy as np

from morva.anomaly.deviation import (
    box_excess_scores,
    conformal_pvalues,
    detection_summary,
    inject,
    rule_scores,
)
from morva.geo import KNOT_MS, from_local_xy, haversine_m, to_local_xy

STEP = 60
KNOTS = [5, 10, 15, 20, 30, 45, 60]


def straight_tracks(n=3, sog_kn=10.0, cog_deg=45.0, obs=20, fut=60, lat0=60.3, lon0=5.0):
    """Constant-velocity tracks: hist [n, obs, 4] ending at (lat0, lon0) and fut [n, fut, 2]."""
    v = sog_kn * KNOT_MS
    vx, vy = v * np.sin(np.radians(cog_deg)), v * np.cos(np.radians(cog_deg))
    t_h = np.arange(-obs + 1, 1) * STEP
    t_f = np.arange(1, fut + 1) * STEP
    lat_h, lon_h = from_local_xy(vx * t_h, vy * t_h, lat0, lon0)
    lat_f, lon_f = from_local_xy(vx * t_f, vy * t_f, lat0, lon0)
    hist = np.stack([lat_h, lon_h, np.full(obs, sog_kn), np.full(obs, cog_deg)], axis=-1)
    return np.repeat(hist[None], n, axis=0), np.repeat(np.stack([lat_f, lon_f], axis=-1)[None], n, axis=0)


def test_conformal_pvalues_formula_and_false_alarm_control():
    cal = np.array([[1.0], [2.0], [3.0], [4.0]])
    p = conformal_pvalues(cal, np.array([[0.5], [2.0], [4.0], [9.0]]))
    assert np.allclose(p[:, 0], [5 / 5, 4 / 5, 2 / 5, 1 / 5])
    rng = np.random.default_rng(1)
    cal, new = rng.normal(size=(2000, 3)), rng.normal(size=(20000, 3))
    fa = (conformal_pvalues(cal, new) <= 0.05).mean(axis=0)
    assert np.all(fa < 0.06) and np.all(fa > 0.04)


def test_injection_leaves_steps_before_onset_and_zero_deviations_unchanged():
    hist, fut = straight_tracks()
    for kind, mag in (("turn", 0.0), ("speed", 1.0), ("jump", 0.0)):
        assert np.allclose(inject(hist, fut, STEP, kind, 10, mag), fut, atol=1e-9)
    for kind, mag in (("turn", 60.0), ("stop", 0.0), ("speed", 1.5), ("jump", 1000.0)):
        out = inject(hist, fut, STEP, kind, 10, mag)
        assert np.allclose(out[:, :9], fut[:, :9], atol=1e-9), kind
        assert not np.allclose(out[:, 9:], fut[:, 9:]), kind


def test_injected_deviations_have_the_requested_geometry():
    hist, fut = straight_tracks(n=1, sog_kn=12.0, cog_deg=0.0)
    lat0, lon0 = hist[0, -1, 0], hist[0, -1, 1]

    def step_vectors(f):
        x, y = to_local_xy(f[0, :, 0], f[0, :, 1], lat0, lon0)
        return np.diff(x), np.diff(y)

    dx, dy = step_vectors(inject(hist, fut, STEP, "turn", 10, 90.0, rate_deg_min=10.0))
    assert np.isclose(np.degrees(np.arctan2(dx[-1], dy[-1])), 90.0, atol=1e-6)  # north -> east: starboard
    dx, dy = step_vectors(inject(hist, fut, STEP, "speed", 10, 0.5))
    assert np.isclose(np.hypot(dx[-1], dy[-1]), 0.5 * 12 * KNOT_MS * STEP)
    stop = inject(hist, fut, STEP, "stop", 10, 0.0, decel_steps=5)
    assert np.allclose(stop[0, 14:], stop[0, 14], atol=1e-9)  # stationary once the speed reaches zero
    jump = inject(hist, fut, STEP, "jump", 10, 800.0)
    d = haversine_m(jump[0, 9:, 0], jump[0, 9:, 1], fut[0, 9:, 0], fut[0, 9:, 1])
    assert np.allclose(d, 800.0, rtol=5e-3)  # tangent-plane approximation over ~22 km at 60° N


def test_rule_scores_are_near_zero_on_straight_tracks_and_grow_with_a_turn():
    hist, fut = straight_tracks()
    base = rule_scores(hist, fut, STEP, KNOTS)
    assert all(s.shape == (3, len(KNOTS)) for s in base.values())
    assert base["cv_distance"].max() < 1.0 and base["turn"].max() < 1e-6 and base["speed"].max() < 1e-6
    turned = rule_scores(hist, inject(hist, fut, STEP, "turn", 10, 45.0), STEP, KNOTS)
    assert np.all(np.diff(turned["turn"], axis=1) >= 0)  # running maxima
    assert np.isclose(turned["turn"][0, -1], 45.0, atol=1e-6) and turned["cv_distance"][0, -1] > 1000


def test_box_excess_is_negative_inside_and_scaled_by_half_width():
    lo, hi = np.full((1, 2, 2), -100.0), np.full((1, 2, 2), 100.0)
    y = np.array([[[0.0, 0.0], [300.0, 0.0]]])
    s = box_excess_scores(lo, hi, y)
    assert np.isclose(s[0, 0], -1.0) and np.isclose(s[0, 1], 2.0)


def test_detection_summary_counts_flags_from_the_onset():
    p_normal = np.array([[0.5, 0.5], [0.01, 0.5]])
    p_dev = np.array([[0.5, 0.01], [0.5, 0.5]])
    out = detection_summary(p_normal, p_dev, 0.05, [5, 10], onset_step=5, step_s=STEP)
    assert out["first_flag_false_alarm_rate"] == 0.5 and out["first_flag_detection_rate"] == 0.5
    assert out["median_delay_min"] == 5.0 and out["per_horizon"][10]["detection_rate"] == 0.5
