"""Wind and surface-current context from MET Norway models (V4 feature sets G and H).

Sources, read over OPeNDAP from https://thredds.met.no (no extra dependencies; ASCII responses are parsed here):

- MEPS deterministic, 2.5 km (`meps25epsarchive/YYYY/MM/DD/meps_det_2_5km_YYYYMMDDTHHZ.nc`), 10 m `wind_speed`
  and `wind_direction` (direction the wind comes from, degrees). Runs start every 3 h. To use only forecasts that
  existed before the valid time, each hour is taken from a run started 3-5 h earlier (leads 3, 4 and 5 h).
- NorKyst v3, 800 m (`fou-hi/norkystv3_his_files/YYYY/MM/DD/norkyst800_his_zdepth_YYYYMMDDT00Z_m00_AN.nc`), surface
  (0 m) `u_eastward` and `v_northward`, hourly. These are analyses, so they use observations from the same day; an
  operational system would use the forecast instead. NorKyst covers Norway and Skagen but not most Danish waters.

Only the grid points around each region are downloaded, once per day, and cached as Parquet (`t`, `lat`, `lon`,
values). Windows are matched to the nearest hour and the nearest grid point; a window farther than `max_dist_m`
from any grid point with data gets NaN. Features describe the field at the forecast origin relative to the vessel's
course at the origin: total speed, the component along the course (positive = pushing the vessel ahead) and the
component across it (positive = towards starboard).
"""

import re
import time
import urllib.error
import urllib.request
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl
from scipy.spatial import cKDTree

from morva.features.motion import anchor_frame, to_body
from morva.geo import to_local_xy

THREDDS = "https://thredds.met.no/thredds/dodsC"
MEPS_LEADS_H = (3, 4, 5)
MEPS_SHAPE = (1069, 949)        # y, x (checked 4 Nov 2026)
NORKYST_SHAPE = (1148, 2747)
_HEADER = re.compile(r"^([\w.]+)((?:\[\d+\])+)$")


def dap_ascii(text: str) -> dict[str, np.ndarray]:
    """Parse a DAP2 ASCII response into arrays keyed by variable name (grid maps keyed by their own name)."""
    body = text.split("-" * 45, 1)[-1]
    out, name, shape, values = {}, None, None, []

    def flush():
        if name is not None:
            out[name] = np.asarray(values, dtype=float).reshape(shape)

    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        m = _HEADER.match(line)
        if m:
            flush()
            name = m.group(1).split(".")[-1]
            shape = [int(d) for d in re.findall(r"\[(\d+)\]", m.group(2))]
            values = []
            continue
        if line.startswith("["):
            line = line.split(",", 1)[1] if "," in line else ""
        values.extend(float(v) for v in line.split(",") if v.strip())
    flush()
    return out


def _get(url: str, constraint: str, timeout: int = 300, attempts: int = 4) -> dict[str, np.ndarray]:
    """Fetch and parse one OPeNDAP ASCII request. The server sometimes answers with a DAP `Error {` body (status
    200), a 5xx status or a timeout that succeed on retry; these are retried with growing pauses. A 404 (file not
    in the archive) is raised at once."""
    query = constraint.replace("[", "%5B").replace("]", "%5D")
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(f"{url}.ascii?{query}", timeout=timeout) as r:
                text = r.read().decode()
            if "-" * 45 not in text and text.lstrip().startswith("Error {"):
                raise RuntimeError(f"{url}: server error {text[:200]!r}")
            return dap_ascii(text)
        except urllib.error.HTTPError as err:
            if err.code < 500 or attempt == attempts - 1:
                raise
        except (RuntimeError, TimeoutError, urllib.error.URLError):
            if attempt == attempts - 1:
                raise
        time.sleep(10 * 2 ** attempt)
    raise AssertionError("unreachable")


def index_box(lat: np.ndarray, lon: np.ndarray, box: dict, pad_deg: float) -> tuple[slice, slice] | None:
    """Row and column slices of a 2-D lat/lon grid covering `box` plus a margin; None if no point is inside."""
    inside = ((lat >= box["lat_min"] - pad_deg) & (lat <= box["lat_max"] + pad_deg)
              & (lon >= box["lon_min"] - pad_deg) & (lon <= box["lon_max"] + pad_deg))
    if not inside.any():
        return None
    rows, cols = np.nonzero(inside)
    return slice(rows.min(), rows.max() + 1), slice(cols.min(), cols.max() + 1)


def _grid_subset(url: str, box: dict, pad_deg: float, coarse: int,
                 shape: tuple[int, int], names: tuple[str, str]) -> tuple[slice, slice] | None:
    """Locate the region on a coarse view of the grid, then widen by one coarse step on each side."""
    yx = f"[0:{coarse}:{shape[0] - 1}][0:{coarse}:{shape[1] - 1}]"
    ll = _get(url, f"{names[0]}{yx},{names[1]}{yx}")
    sub = index_box(ll[names[0]], ll[names[1]], box, pad_deg)
    if sub is None:
        return None
    ys, xs = sub
    return (slice(max(ys.start - 1, 0) * coarse, ys.stop * coarse),
            slice(max(xs.start - 1, 0) * coarse, xs.stop * coarse))


def _rng(s: slice, stride: int, n: int) -> str:
    return f"[{s.start}:{stride}:{min(s.stop, n) - 1}]"


def _long_frame(times: np.ndarray, lat: np.ndarray, lon: np.ndarray, fields: dict[str, np.ndarray]) -> pl.DataFrame:
    nt, npts = len(times), lat.size
    df = pl.DataFrame({
        "t": np.repeat(times, npts),
        "lat": np.tile(lat.ravel(), nt), "lon": np.tile(lon.ravel(), nt),
        **{k: v.reshape(nt, npts).ravel() for k, v in fields.items()},
    })
    return df.drop_nans(subset=list(fields)).with_columns(pl.col("t").dt.replace_time_zone("UTC"))


def _epoch(seconds: np.ndarray) -> np.ndarray:
    return (np.asarray(seconds) * 1e6).astype("int64").astype("datetime64[us]")


def fetch_meps_day(day: date, box: dict, stride: int = 1, pad_deg: float = 0.2, max_fallback: int = 2
                   ) -> pl.DataFrame:
    """Hourly 10 m wind for one UTC day around `box`, each hour from the run started 3-5 h earlier.

    A few runs are missing from the archive (e.g. 22 Sep 2026 09Z, 30 Sep 2026 21Z). For their hours the previous
    run is used instead, up to `max_fallback` runs back (leads 6-8 h, then 9-11 h), which was still issued before
    the valid time. Column `lead_h` records the lead time used."""
    parts = []
    for run_h in range(-6, 24, 3):  # the run started at run_h covers the hours run_h + 3 ... run_h + 5
        for back in range(max_fallback + 1):
            init = datetime(day.year, day.month, day.day, tzinfo=UTC) + timedelta(hours=run_h - 3 * back)
            leads = [h + 3 * back for h in MEPS_LEADS_H]
            url = f"{THREDDS}/meps25epsarchive/{init:%Y/%m/%d}/meps_det_2_5km_{init:%Y%m%dT%H}Z.nc"
            try:
                sub = _grid_subset(url, box, pad_deg, coarse=20, shape=MEPS_SHAPE, names=("latitude", "longitude"))
                break
            except urllib.error.HTTPError as err:
                if err.code != 404 or back == max_fallback:
                    raise
        if sub is None:
            raise ValueError(f"box {box['name']} is outside the MEPS grid")
        ys, xs = sub
        yx = f"{_rng(ys, stride, MEPS_SHAPE[0])}{_rng(xs, stride, MEPS_SHAPE[1])}"
        r = f"[{leads[0]}:1:{leads[-1]}][0]{yx}"
        g = _get(url, f"wind_speed{r},wind_direction{r},latitude{yx},longitude{yx},time[{leads[0]}:1:{leads[-1]}]")
        expected = np.array([(init + timedelta(hours=h)).timestamp() for h in leads])
        if not np.allclose(g["time"], expected):
            raise ValueError(f"{url}: lead times {g['time']} differ from the expected {expected}")
        times = init.replace(tzinfo=None) + np.array([timedelta(hours=h) for h in leads])
        fields = {k: np.where(np.abs(g[k]) > 1e30, np.nan, g[k])[:, 0] for k in ("wind_speed", "wind_direction")}
        df = _long_frame(times.astype("datetime64[us]"), g["latitude"], g["longitude"], fields)
        parts.append(df.with_columns(lead_h=pl.col("t").dt.hour().sub(init.hour).mod(24).cast(pl.Int8)))
    start = datetime(day.year, day.month, day.day, tzinfo=UTC)
    return pl.concat(parts).filter((pl.col("t") >= start) & (pl.col("t") < start + timedelta(days=1)))


def fetch_norkyst_day(day: date, box: dict, stride: int = 2, pad_deg: float = 0.1) -> pl.DataFrame | None:
    """Hourly surface current for one UTC day around `box`; None if the box is outside the NorKyst grid."""
    url = (f"{THREDDS}/fou-hi/norkystv3_his_files/{day:%Y/%m/%d}/"
           f"norkyst800_his_zdepth_{day:%Y%m%d}T00Z_m00_AN.nc")
    sub = _grid_subset(url, box, pad_deg, coarse=10, shape=NORKYST_SHAPE, names=("lat", "lon"))
    if sub is None:
        return None
    ys, xs = sub
    yx = f"{_rng(ys, stride, NORKYST_SHAPE[0])}{_rng(xs, stride, NORKYST_SHAPE[1])}"
    g = _get(url, f"u_eastward[0:1:23][0]{yx},v_northward[0:1:23][0]{yx},lat{yx},lon{yx},time")
    fields = {}
    for k in ("u_eastward", "v_northward"):  # packed Int16: scale 0.001, fill -32767 (checked 4 Nov 2026)
        v = g[k][:, 0]
        fields[k] = np.where(v == -32767, np.nan, v * 0.001)
    return _long_frame(_epoch(g["time"]), g["lat"], g["lon"], fields)


class FieldSampler:
    """Nearest-hour, nearest-point lookup in a cached field (long format with `t`, `lat`, `lon`)."""

    def __init__(self, df: pl.DataFrame, value_cols: list[str], max_dist_m: float):
        self.cols, self.max_dist = value_cols, max_dist_m
        pts = df.select("lat", "lon").unique().sort("lat", "lon")
        self.lat0, self.lon0 = float(pts["lat"].mean()), float(pts["lon"].mean())
        self.tree = cKDTree(np.column_stack(to_local_xy(pts["lat"].to_numpy(), pts["lon"].to_numpy(),
                                                        self.lat0, self.lon0)))
        self.points = pts.with_row_index("pt")
        df = df.join(self.points, on=["lat", "lon"])
        self.times = np.sort(df["t"].unique().to_numpy())
        grid = np.full((len(self.times), len(pts), len(value_cols)), np.nan)
        ti = np.searchsorted(self.times, df["t"].to_numpy())
        grid[ti, df["pt"].to_numpy()] = df.select(value_cols).to_numpy()
        self.grid = grid

    def sample(self, lat: np.ndarray, lon: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Values [n, len(value_cols)] at the nearest grid point and hour; NaN if too far in space or > 1 h away."""
        dist, pt = self.tree.query(np.column_stack(to_local_xy(lat, lon, self.lat0, self.lon0)))
        t = np.asarray(t, dtype="datetime64[us]")
        ti = np.clip(np.searchsorted(self.times, t), 1, len(self.times) - 1)
        ti = np.where(np.abs(self.times[ti - 1] - t) <= np.abs(self.times[ti] - t), ti - 1, ti)
        out = self.grid[ti, pt].copy()
        far = (dist > self.max_dist) | (np.abs(self.times[ti] - t) > np.timedelta64(1, "h"))
        out[far] = np.nan
        return out


def relative_components(east: np.ndarray, north: np.ndarray, course_rad: np.ndarray) -> tuple:
    """Speed and the along-course / starboard components of a vector given in east/north components."""
    along, cross = to_body(east, north, course_rad)
    return np.hypot(east, north), along, cross


def wind_features(sampler: FieldSampler, hist: np.ndarray, t0: np.ndarray, step_s: int) -> dict[str, np.ndarray]:
    lat0, lon0, _, th = anchor_frame(hist, step_s)
    speed, from_deg = sampler.sample(lat0, lon0, t0).T
    to = np.radians(from_deg + 180.0)  # the wind blows towards from + 180 deg
    _, along, cross = relative_components(speed * np.sin(to), speed * np.cos(to), th)
    return {"wind_speed": speed, "wind_along": along, "wind_cross": cross}


def current_features(sampler: FieldSampler, hist: np.ndarray, t0: np.ndarray, step_s: int) -> dict[str, np.ndarray]:
    lat0, lon0, _, th = anchor_frame(hist, step_s)
    u, v = sampler.sample(lat0, lon0, t0).T
    speed, along, cross = relative_components(u, v, th)
    return {"current_speed": speed, "current_along": along, "current_cross": cross}


def cached_days(cache_dir: Path, days: list[date], fetch, box: dict) -> pl.DataFrame | None:
    """Load cached days, fetching missing ones; None if the source does not cover the box."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for d in days:
        path = cache_dir / f"{d:%Y-%m-%d}.parquet"
        if not path.exists():
            df = fetch(d, box)
            if df is None:
                return None
            df.write_parquet(path)
        parts.append(pl.read_parquet(path))
    return pl.concat(parts) if parts else None
