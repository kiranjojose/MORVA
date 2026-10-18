"""Fairway context from historical traffic (V2 feature group "fairway").

A flow map summarises where, and in which direction, moving vessels sailed during the training period of a
region. It is a grid of `cell_m` cells by `n_dir_bins` course bins; each (cell, bin) stores the count of
vessel-minutes, the sum of sin/cos course, and first and second moments of position inside the cell.

A query at a position and course pools a block of (2r + 1)^2 cells and the course bins within ±`dir_radius_bins`
of the query course, so only same-direction traffic contributes (the opposite lane of a TSS is ignored). From the
pooled moments it returns:

    logdens  log(1 + vessel-minutes per map day) of same-direction traffic
    coher    mean resultant length of the pooled courses (1 = one clear direction)
    hdg      flow course minus query course, degrees in [-180, 180), + = flow turns to starboard
    offset   query position relative to the flow centroid, metres along the flow's starboard axis
    width    lateral standard deviation of the pooled traffic, metres

Features describe the vessel's relation to the local flow, never its absolute position, so their meaning is the
same in any waterway. They are evaluated at the anchor and at the constant-velocity positions `ahead_min` ahead.

Leakage guard: the map is built from the region's training period only. A window whose future falls inside the
map period (a training window) is given a map without the day(s) its future covers, so it can never see its own
future path. Validation, test and transfer windows use the full map.
"""

from datetime import date, timedelta

import numpy as np
import polars as pl

from morva.features.motion import anchor_frame
from morva.geo import to_local_xy

# Per (cell, bin) statistics, all relative to the cell centre
STATS = ("n", "cos", "sin", "dx", "dy", "dxx", "dyy", "dxy")


def fairway_feature_names(ahead_min) -> list[str]:
    names = ["flow_logdens_0", "flow_coher_0", "flow_hdg_0", "flow_offset_0", "flow_width_0"]
    for k in ahead_min:
        names += [f"flow_logdens_{k}", f"flow_hdg_{k}", f"flow_offset_{k}"]
    return names


class FlowMaps:
    """Total flow statistics for one region plus per-day statistics for leave-day-out maps."""

    def __init__(self, box: dict, cfg: dict):
        self.cfg = cfg
        self.cell = float(cfg["cell_m"])
        self.nb = int(cfg["n_dir_bins"])
        self.lat0 = (box["lat_min"] + box["lat_max"]) / 2
        self.lon0 = (box["lon_min"] + box["lon_max"]) / 2
        x0, y0 = to_local_xy(box["lat_min"], box["lon_min"], self.lat0, self.lon0)
        x1, y1 = to_local_xy(box["lat_max"], box["lon_max"], self.lat0, self.lon0)
        self.xmin, self.ymin = float(x0), float(y0)
        self.nx = int(np.ceil((x1 - x0) / self.cell))
        self.ny = int(np.ceil((y1 - y0) / self.cell))
        self.total = np.zeros((len(STATS), self.nx, self.ny, self.nb), np.float32)
        self.by_day: dict[date, np.ndarray] = {}

    def xy(self, lat, lon):
        return to_local_xy(lat, lon, self.lat0, self.lon0)

    def _grid(self, x, y, course_rad) -> np.ndarray:
        ix = np.floor((x - self.xmin) / self.cell).astype(np.int64)
        iy = np.floor((y - self.ymin) / self.cell).astype(np.int64)
        ok = (ix >= 0) & (ix < self.nx) & (iy >= 0) & (iy < self.ny)
        ix, iy, x, y, course_rad = ix[ok], iy[ok], x[ok], y[ok], course_rad[ok]
        ib = np.round(course_rad / (2 * np.pi / self.nb)).astype(np.int64) % self.nb
        dx = x - (self.xmin + (ix + 0.5) * self.cell)
        dy = y - (self.ymin + (iy + 0.5) * self.cell)
        flat = (ix * self.ny + iy) * self.nb + ib
        size = self.nx * self.ny * self.nb
        weights = (None, np.cos(course_rad), np.sin(course_rad), dx, dy, dx * dx, dy * dy, dx * dy)
        g = np.stack([np.bincount(flat, weights=w, minlength=size) for w in weights])
        return g.reshape(len(STATS), self.nx, self.ny, self.nb).astype(np.float32)

    @classmethod
    def build(cls, points: pl.DataFrame, box: dict, cfg: dict) -> "FlowMaps":
        """points: track points (t, mmsi, lat, lon, sog, cog) from the map period only."""
        maps = cls(box, cfg)
        pts = (
            points.filter((pl.col("sog") >= cfg["min_sog_kn"]) & pl.col("cog").is_not_null())
            .with_columns(_slot=pl.col("t").dt.truncate(f"{int(cfg['sample_s'])}s"))
            .unique(["mmsi", "_slot"], keep="first", maintain_order=True)  # one point per vessel per slot
            .with_columns(_day=pl.col("t").dt.date())
        )
        for (day,), g in pts.group_by("_day", maintain_order=True):
            x, y = maps.xy(g["lat"].to_numpy(), g["lon"].to_numpy())
            maps.by_day[day] = maps._grid(x, y, np.radians(g["cog"].to_numpy()))
            maps.total += maps.by_day[day]
        maps.n_points = len(pts)
        return maps

    def without(self, days: tuple) -> tuple[np.ndarray, int]:
        """Map statistics with the given days removed, and the number of days remaining."""
        g = self.total.copy()
        for d in days:
            g -= self.by_day[d]
        return g, len(self.by_day) - len(days)

    def query(self, grid: np.ndarray, n_days: int, x, y, course_rad) -> dict[str, np.ndarray]:
        """Pooled same-direction flow at query points (x, y in region metres, course in rad)."""
        r, h = int(self.cfg["block_radius_cells"]), int(self.cfg["dir_radius_bins"])
        n_q = len(x)
        acc = {k: np.zeros(n_q) for k in ("n", "c", "s", "sx", "sy", "sxx", "syy", "sxy")}
        ix0 = np.floor((x - self.xmin) / self.cell).astype(np.int64)
        iy0 = np.floor((y - self.ymin) / self.cell).astype(np.int64)
        ib0 = np.round(course_rad / (2 * np.pi / self.nb)).astype(np.int64) % self.nb
        valid_q = np.isfinite(x) & np.isfinite(y) & np.isfinite(course_rad)
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                ix, iy = ix0 + di, iy0 + dj
                ok = valid_q & (ix >= 0) & (ix < self.nx) & (iy >= 0) & (iy < self.ny)
                if not ok.any():
                    continue
                ixo, iyo = ix[ok], iy[ok]
                relx = self.xmin + (ixo + 0.5) * self.cell - x[ok]
                rely = self.ymin + (iyo + 0.5) * self.cell - y[ok]
                for db in range(-h, h + 1):
                    n, c, s, dx, dy, dxx, dyy, dxy = grid[:, ixo, iyo, (ib0[ok] + db) % self.nb].astype(np.float64)
                    acc["n"][ok] += n
                    acc["c"][ok] += c
                    acc["s"][ok] += s
                    acc["sx"][ok] += n * relx + dx
                    acc["sy"][ok] += n * rely + dy
                    acc["sxx"][ok] += n * relx * relx + 2 * relx * dx + dxx
                    acc["syy"][ok] += n * rely * rely + 2 * rely * dy + dyy
                    acc["sxy"][ok] += n * relx * rely + relx * dy + rely * dx + dxy
        n = acc["n"]
        enough = valid_q & (n >= self.cfg["min_points"])
        nn = np.where(enough, n, np.nan)
        phi = np.arctan2(acc["s"], acc["c"])  # flow course, clockwise from north
        ux, uy = np.cos(phi), -np.sin(phi)  # starboard axis of the flow
        mu = (acc["sx"] * ux + acc["sy"] * uy) / nn  # centroid offset from the query along u
        var = (ux * ux * acc["sxx"] + 2 * ux * uy * acc["sxy"] + uy * uy * acc["syy"]) / nn - mu * mu
        hdg = (np.degrees(phi - course_rad) + 180) % 360 - 180
        return {
            "logdens": np.where(valid_q, np.log1p(n / max(n_days, 1)), np.nan),
            "coher": np.hypot(acc["c"], acc["s"]) / nn,
            "hdg": np.where(enough, hdg, np.nan),
            "offset": -mu,
            "width": np.sqrt(np.clip(var, 0, None)),
        }


def _future_days(t0: pl.Series, step_s: int, n_future: int, map_days: set) -> list[tuple]:
    """Map days covered by each window's future (first to last forecast step); empty when outside the map."""
    first = (t0 + timedelta(seconds=step_s)).dt.date().to_list()
    last = (t0 + timedelta(seconds=step_s * n_future)).dt.date().to_list()
    return [tuple(sorted({a, b} & map_days)) for a, b in zip(first, last, strict=True)]


def fairway_features(hist: np.ndarray, t0: pl.Series, maps: FlowMaps, step_s: int, n_future: int,
                     cfg: dict) -> dict[str, np.ndarray]:
    """Fairway features for windows of one region (hist [n, obs, 4], t0 = anchor times)."""
    lat, lon, v, th = anchor_frame(hist, step_s)
    x, y = maps.xy(lat, lon)
    names = fairway_feature_names(cfg["ahead_min"])
    out = {k: np.full(len(hist), np.nan) for k in names}
    groups: dict[tuple, list[int]] = {}
    for i, key in enumerate(_future_days(t0, step_s, n_future, set(maps.by_day))):
        groups.setdefault(key, []).append(i)
    for key, idx in sorted(groups.items()):
        sel = np.asarray(idx)
        grid, n_days = maps.without(key)
        q = maps.query(grid, n_days, x[sel], y[sel], th[sel])
        for k in ("logdens", "coher", "hdg", "offset", "width"):
            out[f"flow_{k}_0"][sel] = q[k]
        for m in cfg["ahead_min"]:
            d = v[sel] * m * 60
            qa = maps.query(grid, n_days, x[sel] + d * np.sin(th[sel]), y[sel] + d * np.cos(th[sel]), th[sel])
            out[f"flow_logdens_{m}"][sel] = qa["logdens"]
            out[f"flow_hdg_{m}"][sel] = qa["hdg"]
            out[f"flow_offset_{m}"][sel] = qa["offset"]
    return out
