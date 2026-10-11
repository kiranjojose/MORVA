from datetime import UTC, datetime, timedelta

import numpy as np
import polars as pl
import pytest

from vesselmind.evaluation.metrics import grouped_bootstrap, per_sample_metrics, step_errors_m
from vesselmind.evaluation.splits import assign_split
from vesselmind.features.windows import build_windows
from vesselmind.geo import KNOT_MS, from_local_xy, haversine_m, to_local_xy
from vesselmind.models.baselines import ctrv, cv, persistence
from vesselmind.quality.checks import add_flags, normalize_sentinels
from vesselmind.trajectories.segment import segment_tracks

STEP = 60


def test_haversine_one_degree_latitude():
    assert haversine_m(55.0, 12.0, 56.0, 12.0) == pytest.approx(111_195, rel=1e-3)


def test_local_xy_roundtrip():
    lat, lon = from_local_xy(*to_local_xy(55.7, 12.3, 55.5, 12.0), 55.5, 12.0)
    assert lat == pytest.approx(55.7) and lon == pytest.approx(12.3)


def _hist_from_xy(x, y, sog, cog, lat0=55.5, lon0=12.0):
    lat, lon = from_local_xy(np.asarray(x), np.asarray(y), lat0, lon0)
    return np.stack([lat, lon, np.full(len(x), sog), np.asarray(cog, float)], axis=-1)[None]


def test_cv_exact_on_straight_line():
    v = 10 * KNOT_MS
    t = np.arange(-19, 1) * STEP
    hist = _hist_from_xy(v * t * np.sin(np.radians(45)), v * t * np.cos(np.radians(45)), 10, np.full(20, 45))
    tf = np.arange(1, 21) * STEP
    true = np.stack(from_local_xy(v * tf * np.sin(np.radians(45)), v * tf * np.cos(np.radians(45)),
                                  hist[0, -1, 0], hist[0, -1, 1]), axis=-1)[None]
    assert step_errors_m(cv(hist, 20, STEP), true).max() < 1.0


def test_ctrv_beats_cv_on_constant_turn():
    v, w = 12 * KNOT_MS, np.radians(0.3)  # 0.3 deg/s starboard turn
    t = np.arange(-19, 21) * STEP
    th = w * t
    x, y = v / w * (1 - np.cos(th)), v / w * np.sin(th)
    cog = np.degrees(th) % 360
    hist = _hist_from_xy(x[:20], y[:20], 12, cog[:20])
    true = np.stack(from_local_xy(x[20:], y[20:], 55.5, 12.0), axis=-1)[None]
    e_ctrv = step_errors_m(ctrv(hist, 20, STEP), true).max()
    e_cv = step_errors_m(cv(hist, 20, STEP), true).max()
    assert e_ctrv < 5.0 and e_cv > 100 * e_ctrv


def test_persistence_shape():
    hist = np.zeros((3, 20, 4))
    assert persistence(hist, 20, STEP).shape == (3, 20, 2)


def _points(mmsi, start, n, dt_s, lat0=55.5, lon0=12.0, sog=10.0):
    v = sog * KNOT_MS
    t = [start + timedelta(seconds=i * dt_s) for i in range(n)]
    lat, lon = from_local_xy(np.zeros(n), np.arange(n) * dt_s * v, lat0, lon0)
    return pl.DataFrame({"t": t, "mmsi": [mmsi] * n, "lat": lat, "lon": lon,
                         "sog": [sog] * n, "cog": [0.0] * n, "heading": [0.0] * n})


T0 = datetime(2025, 1, 1, tzinfo=UTC)


def test_sentinels_become_null():
    df = _points(219000001, T0, 3, 10).with_columns(sog=pl.Series([102.3, 5.0, 5.0]),
                                                    heading=pl.Series([511.0, 1.0, 2.0]))
    out = normalize_sentinels(df)
    assert out["sog"].null_count() == 1 and out["heading"].null_count() == 1


def test_flags_duplicate_spike_and_bad_mmsi():
    df = _points(219000001, T0, 30, 10)
    df = df.with_columns(lat=pl.when(pl.int_range(pl.len()) == 15).then(pl.col("lat") + 0.5)
                         .otherwise(pl.col("lat")))
    df = pl.concat([df, df[3:4], _points(12345, T0, 2, 10)])
    out = add_flags(df, max_implied_speed_kn=50, max_plausible_sog_kn=40)
    assert out["flag_duplicate"].sum() == 1
    assert out["flag_bad_mmsi"].sum() == 2
    spikes = out.filter(pl.col("flag_speed_spike"))
    assert len(spikes) == 1 and spikes["t"][0] == T0 + timedelta(seconds=150)


def test_segmentation_splits_on_gap():
    a = _points(219000001, T0, 200, 10)
    b = _points(219000001, T0 + timedelta(hours=2), 200, 10)
    flagged = add_flags(pl.concat([a, b]), 50, 40)
    seg = segment_tracks(flagged, gap_s=1200, min_points=20, min_duration_s=600)
    assert seg["segment_id"].n_unique() == 2


def test_windows_never_bridge_long_gaps():
    a = _points(219000001, T0, 360, 10)                               # 1 h
    b = _points(219000001, T0 + timedelta(minutes=65), 360, 10)       # 5-min gap, same segment
    flagged = add_flags(pl.concat([a, b]), 50, 40)
    tracks = segment_tracks(flagged, gap_s=1200, min_points=20, min_duration_s=600)
    cfg = dict(step_s=60, obs_steps=20, future_steps=20, stride_steps=1, max_gap_s=180, min_mean_sog_kn=1.0)
    _, _, meta = build_windows(tracks, cfg)
    gap_start, gap_end = T0 + timedelta(seconds=3590), T0 + timedelta(minutes=65)
    w_start = meta["t0"] - timedelta(minutes=19)
    w_end = meta["t0"] + timedelta(minutes=20)
    overlaps = ((w_start < gap_end) & (w_end > gap_start)).sum()
    assert len(meta) > 0 and overlaps == 0


def test_split_blocks_do_not_overlap_in_time():
    t0 = [T0 + timedelta(minutes=m) for m in range(0, 600, 5)]
    meta = pl.DataFrame({"t0": t0, "mmsi": [1] * len(t0)})
    out = assign_split(meta, T0 + timedelta(hours=6), T0 + timedelta(hours=8), 60, 20, 20)
    train_end = out.filter(pl.col("split") == "train")["t0"].max() + timedelta(minutes=20)
    val_start = out.filter(pl.col("split") == "val")["t0"].min() - timedelta(minutes=19)
    assert train_end <= T0 + timedelta(hours=6) <= val_start
    assert (out["split"] == "excluded").sum() > 0


def test_metrics_and_grouped_bootstrap():
    err = np.tile(np.arange(1, 21, dtype=float), (4, 1))
    m = per_sample_metrics(err, 60, [5, 10, 20])
    assert m["fde_m"][0] == 20 and m["err_5min_m"][0] == 5 and m["ade_m"][0] == pytest.approx(10.5)
    mean, lo, hi = grouped_bootstrap([1, 1, 3, 3], ["a", "a", "b", "b"], n_boot=500)
    assert mean == 2 and lo >= 1 and hi <= 3


def test_ctrv_damped_limits():
    from vesselmind.models.baselines import ctrv_damped

    v, w = 12 * KNOT_MS, np.radians(0.3)
    t = np.arange(-19, 1) * STEP
    th = w * t
    hist = _hist_from_xy(v / w * (1 - np.cos(th)), v / w * np.sin(th), 12, np.degrees(th) % 360)
    near_cv = step_errors_m(ctrv_damped(hist, 20, STEP, tau_s=1e-3), cv(hist, 20, STEP)).max()
    near_ctrv = step_errors_m(ctrv_damped(hist, 20, STEP, tau_s=1e7), ctrv(hist, 20, STEP)).max()
    assert near_cv < 2.0 and near_ctrv < 5.0


def test_body_frame_roundtrip_and_axes():
    from vesselmind.features.motion import from_body, to_body

    th = np.radians(90.0)  # heading east: east is 'along', south is starboard 'cross'
    a, c = to_body(np.array([100.0, 0.0]), np.array([0.0, -50.0]), th)
    assert a[0] == pytest.approx(100) and c[1] == pytest.approx(50)
    x, y = from_body(*to_body(np.array([3.0]), np.array([-7.0]), 1.234), 1.234)
    assert x[0] == pytest.approx(3) and y[0] == pytest.approx(-7)


def test_residual_targets_zero_on_cv_path_and_invertible():
    from vesselmind.models.gbm import residual_targets, residuals_to_positions

    v = 10 * KNOT_MS
    t = np.arange(-19, 1) * STEP
    s, c = np.sin(np.radians(30)), np.cos(np.radians(30))
    hist = _hist_from_xy(v * t * s, v * t * c, 10, np.full(20, 30.0))
    tf = np.arange(1, 21) * STEP
    fut = np.stack(from_local_xy(v * tf * s, v * tf * c, hist[0, -1, 0], hist[0, -1, 1]), axis=-1)[None]
    ra, rc = residual_targets(hist, fut, STEP, [5, 10, 15, 20])
    assert np.abs(ra).max() < 1.0 and np.abs(rc).max() < 1.0
    # A known residual must be reproduced at the knots
    pred = residuals_to_positions(hist, np.array([[10, 20, 30, 40.0]]), np.array([[-5, -10, -15, -20.0]]),
                                  STEP, 20, [5, 10, 15, 20])
    ra2, rc2 = residual_targets(hist, pred, STEP, [5, 10, 15, 20])
    assert np.allclose(ra2, [[10, 20, 30, 40]], atol=0.5) and np.allclose(rc2, [[-5, -10, -15, -20]], atol=0.5)


def test_regimes_label_straight_turn_and_slow():
    from vesselmind.features.regimes import RegimeParams, assign_regimes, regime_variables, turn_label_reliable

    v_ms, w = 12 * KNOT_MS, np.radians(2.0 / 60)  # 2 deg/min starboard turn
    t = np.arange(-19, 1) * STEP
    straight = _hist_from_xy(np.zeros(20), v_ms * t, 12, np.zeros(20))
    th = w * t
    turning = _hist_from_xy(v_ms / w * (1 - np.cos(th)), v_ms / w * np.sin(th), 12, np.degrees(th) % 360)
    slow = _hist_from_xy(np.zeros(20), 1 * KNOT_MS * t, 2, np.zeros(20))
    hist = np.concatenate([straight, turning, slow])
    p = RegimeParams()
    v = regime_variables(hist, STEP, p.lookback_min)
    assert list(assign_regimes(v, p)) == ["steady", "turning", "low_speed"]
    assert v["turn_signed_deg_min"][1] == pytest.approx(2.0, abs=0.05)
    assert v["turn_pos_abs_deg_min"][1] == pytest.approx(2.0, abs=0.2)  # positions agree with COG
    assert v["turn_consistency"][1] == pytest.approx(1.0)
    assert list(turn_label_reliable(v, p)) == [True, True, False]


def test_kalman_cv_matches_cv_on_noise_free_straight_line():
    from vesselmind.models.baselines import kalman_cv

    v = 10 * KNOT_MS
    t = np.arange(-19, 1) * STEP
    hist = _hist_from_xy(v * t * np.sin(np.radians(70)), v * t * np.cos(np.radians(70)), 10, np.full(20, 70.0))
    assert step_errors_m(kalman_cv(hist, 20, STEP, q=1e-4), cv(hist, 20, STEP)).max() < 5.0
