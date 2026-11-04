"""V4 environmental context: OPeNDAP ASCII parsing, grid lookup and course-relative wind and current."""

from datetime import UTC, datetime

import numpy as np
import polars as pl

from morva.context.environment import FieldSampler, current_features, dap_ascii, index_box, wind_features
from morva.geo import KNOT_MS, from_local_xy

ASCII = """Dataset {
    Grid {
     ARRAY:
        Float32 wind_speed[time = 2][height7 = 1][y = 2][x = 3];
    } wind_speed;
} meps.nc;
---------------------------------------------
wind_speed.wind_speed[2][1][2][3]
[0][0][0], 1.0, 2.0, 3.0
[0][0][1], 4.0, 5.0, 6.0
[1][0][0], 7.0, 8.0, 9.0
[1][0][1], 10.0, 11.0, 12.0

wind_speed.time[2]
1790208000, 1790211600

lat.lat[2][2]
[0], 60.0, 60.1
[1], 60.2, 60.3
"""


def test_dap_ascii_parses_grids_maps_and_arrays():
    g = dap_ascii(ASCII)
    assert g["wind_speed"].shape == (2, 1, 2, 3) and g["wind_speed"][1, 0, 1, 2] == 12.0
    assert g["time"].tolist() == [1790208000, 1790211600]
    assert g["lat"].shape == (2, 2) and g["lat"][1, 0] == 60.2


def test_index_box_returns_covering_slices():
    lat, lon = np.meshgrid(np.arange(58.0, 62.0, 0.5), np.arange(3.0, 8.0, 0.5), indexing="ij")
    ys, xs = index_box(lat, lon, {"lat_min": 59.0, "lat_max": 60.0, "lon_min": 4.0, "lon_max": 5.0}, 0.0)
    assert (lat[ys, xs].min(), lat[ys, xs].max(), lon[ys, xs].min(), lon[ys, xs].max()) == (59.0, 60.0, 4.0, 5.0)
    assert index_box(lat, lon, {"lat_min": 70.0, "lat_max": 71.0, "lon_min": 4.0, "lon_max": 5.0}, 0.0) is None


def _field(values, cols):
    t = [datetime(2026, 9, 24, h, tzinfo=UTC) for h in (0, 1)]
    return pl.DataFrame({"t": [t[0], t[0], t[1], t[1]], "lat": [60.0, 60.1] * 2, "lon": [5.0, 5.0] * 2,
                         **{c: [v[i] for v in values] for i, c in enumerate(cols)}})


def test_sampler_uses_nearest_point_and_hour_and_rejects_far_points():
    df = _field([(1.0,), (2.0,), (3.0,), (4.0,)], ["a"])
    s = FieldSampler(df, ["a"], max_dist_m=3000)
    t = np.array(["2026-09-24T00:20", "2026-09-24T00:40", "2026-09-24T00:40", "2026-09-24T03:00"],
                 dtype="datetime64[us]")
    out = s.sample(np.array([60.001, 60.099, 61.0, 60.0]), np.array([5.0, 5.0, 5.0, 5.0]), t)[:, 0]
    assert out[0] == 1.0 and out[1] == 4.0  # nearest point, nearest hour
    assert np.isnan(out[2]) and np.isnan(out[3])  # 100 km away; 2 h from the last field time


def _northbound(n=1, lat0=60.05, lon0=5.0):
    t = np.arange(-19, 1) * 60.0
    lat, lon = from_local_xy(np.zeros_like(t), 10 * KNOT_MS * t, lat0, lon0)
    return np.repeat(np.stack([lat, lon, np.full(20, 10.0), np.zeros(20)], axis=-1)[None], n, axis=0)


def test_wind_from_the_north_is_a_headwind_and_current_to_the_east_is_a_starboard_set():
    t0 = np.array(["2026-09-24T00:00"], dtype="datetime64[us]")
    wind = FieldSampler(_field([(8.0, 0.0), (8.0, 0.0), (8.0, 0.0), (8.0, 0.0)], ["speed", "from"]),
                        ["speed", "from"], 10_000)
    w = wind_features(wind, _northbound(), t0, 60)
    assert np.isclose(w["wind_speed"][0], 8.0) and np.isclose(w["wind_along"][0], -8.0)
    assert np.isclose(w["wind_cross"][0], 0.0, atol=1e-9)
    cur = FieldSampler(_field([(0.5, 0.0)] * 4, ["u", "v"]), ["u", "v"], 10_000)
    c = current_features(cur, _northbound(), t0, 60)
    assert np.isclose(c["current_cross"][0], 0.5) and np.isclose(c["current_along"][0], 0.0, atol=1e-9)
