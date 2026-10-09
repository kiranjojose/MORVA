"""Prediction windows: resample each segment to a fixed step and cut (history, future) pairs.

Resampling is linear in time for lat/lon/SOG and circular for COG. A window is kept only
if no ORIGINAL reporting gap inside it exceeds `max_gap_s`, so interpolated points never
bridge real AIS outages (protocol rule: never treat interpolated gaps as observations).
"""

import numpy as np
import polars as pl

HIST_FEATURES = ("lat", "lon", "sog", "cog")


def _resample_segment(t, lat, lon, sog, cog, step_s):
    grid = np.arange(np.ceil(t[0] / step_s) * step_s, t[-1] + 1e-9, step_s)
    if len(grid) == 0:
        return None
    out = np.full((len(grid), 4), np.nan)
    out[:, 0] = np.interp(grid, t, lat)
    out[:, 1] = np.interp(grid, t, lon)
    ok = ~np.isnan(sog)
    if ok.sum() >= 2:
        out[:, 2] = np.interp(grid, t[ok], sog[ok])
    ok = ~np.isnan(cog)
    if ok.sum() >= 2:
        unwrapped = np.degrees(np.unwrap(np.radians(cog[ok])))
        out[:, 3] = np.interp(grid, t[ok], unwrapped) % 360
    # Original gap surrounding each grid time
    idx = np.clip(np.searchsorted(t, grid, side="right"), 1, len(t) - 1)
    gap = t[idx] - t[idx - 1]
    return grid, out, gap


def build_windows(tracks: pl.DataFrame, cfg: dict):
    """Returns (hist [n, obs_steps, 4], fut [n, future_steps, 2], meta DataFrame)."""
    step, n_obs, n_fut = cfg["step_s"], cfg["obs_steps"], cfg["future_steps"]
    stride, max_gap, min_sog = cfg["stride_steps"], cfg["max_gap_s"], cfg["min_mean_sog_kn"]
    span = n_obs + n_fut

    hists, futs, meta = [], [], []
    for (seg_id, mmsi), g in tracks.sort("t").group_by(["segment_id", "mmsi"], maintain_order=True):
        t = g["t"].dt.epoch("s").to_numpy().astype(float)
        if len(t) < 2:
            continue
        res = _resample_segment(
            t, g["lat"].to_numpy(), g["lon"].to_numpy(),
            g["sog"].to_numpy().astype(float), g["cog"].to_numpy().astype(float), step,
        )
        if res is None or len(res[0]) < span:
            continue
        grid, arr, gap = res
        bad = (gap > max_gap) | np.isnan(arr[:, :2]).any(axis=1)
        bad_cum = np.concatenate([[0], np.cumsum(bad)])
        for start in range(0, len(grid) - span + 1, stride):
            if bad_cum[start + span] - bad_cum[start] > 0:
                continue
            h = arr[start : start + n_obs]
            if np.isnan(h[:, 2]).all() or np.nanmean(h[:, 2]) < min_sog:
                continue
            hists.append(h)
            futs.append(arr[start + n_obs : start + span, :2])
            meta.append((int(seg_id), int(mmsi), grid[start + n_obs - 1]))

    if not hists:
        raise ValueError("No valid windows; check segmentation and window config.")
    meta_df = pl.DataFrame(
        {
            "sample_id": np.arange(len(meta), dtype=np.int64),
            "segment_id": [m[0] for m in meta],
            "mmsi": [m[1] for m in meta],
            "t0": [m[2] for m in meta],
        }
    ).with_columns(pl.from_epoch(pl.col("t0").cast(pl.Int64), time_unit="s").dt.replace_time_zone("UTC"))
    return np.stack(hists), np.stack(futs), meta_df
