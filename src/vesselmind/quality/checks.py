"""AIS quality protocol: null out sentinels, flag (never silently drop) suspicious points.

Flag columns (bool):
  flag_invalid_pos  lat/lon missing or out of range (incl. 91/181 "not available")
  flag_bad_mmsi     not a 9-digit ship MMSI with MID first digit 2-7
  flag_duplicate    repeated (mmsi, t); first occurrence kept unflagged
  flag_sog_high     reported SOG above plausible maximum
  flag_speed_spike  implied speed to BOTH neighbours exceeds threshold (isolated jump)
"""

import numpy as np
import polars as pl

from vesselmind.geo import KNOT_MS, haversine_m

FLAG_COLS = ["flag_invalid_pos", "flag_bad_mmsi", "flag_duplicate", "flag_sog_high", "flag_speed_spike"]
HARD_FLAGS = ["flag_invalid_pos", "flag_bad_mmsi", "flag_duplicate", "flag_speed_spike"]


def normalize_sentinels(df: pl.DataFrame) -> pl.DataFrame:
    """AIS 'not available' codes -> null: SOG 102.3, COG 360, heading 511."""
    return df.with_columns(
        sog=pl.when(pl.col("sog") >= 102.2).then(None).otherwise(pl.col("sog")),
        cog=pl.when((pl.col("cog") >= 360) | (pl.col("cog") < 0)).then(None).otherwise(pl.col("cog")),
        heading=pl.when((pl.col("heading") >= 360) | (pl.col("heading") < 0)).then(None).otherwise(pl.col("heading")),
    )


def _implied_speed_spike(df: pl.DataFrame, max_kn: float) -> np.ndarray:
    """Requires df sorted by (mmsi, t). Flags isolated jumps, not the points around them."""
    mmsi = df["mmsi"].to_numpy()
    t = df["t"].dt.epoch("s").to_numpy().astype(float)
    lat, lon = df["lat"].to_numpy(), df["lon"].to_numpy()
    n = len(df)
    speed_prev = np.full(n, np.nan)
    if n > 1:
        same = mmsi[1:] == mmsi[:-1]
        dt = np.maximum(t[1:] - t[:-1], 1.0)
        v = haversine_m(lat[:-1], lon[:-1], lat[1:], lon[1:]) / dt / KNOT_MS
        speed_prev[1:] = np.where(same, v, np.nan)
    speed_next = np.append(speed_prev[1:], np.nan)
    # Endpoint with only one neighbour: flag if that single implied speed is extreme
    prev_bad = np.nan_to_num(speed_prev, nan=-1) > max_kn
    next_bad = np.nan_to_num(speed_next, nan=-1) > max_kn
    has_prev, has_next = ~np.isnan(speed_prev), ~np.isnan(speed_next)
    return np.where(has_prev & has_next, prev_bad & next_bad, prev_bad | next_bad)


def add_flags(df: pl.DataFrame, max_implied_speed_kn: float, max_plausible_sog_kn: float) -> pl.DataFrame:
    df = df.sort(["mmsi", "t"]).with_columns(
        flag_invalid_pos=(
            pl.col("lat").is_null() | pl.col("lon").is_null()
            | ~pl.col("lat").is_between(-90, 90) | ~pl.col("lon").is_between(-180, 180)
        ),
        flag_bad_mmsi=~pl.col("mmsi").is_between(200_000_000, 799_999_999),
        flag_duplicate=pl.int_range(pl.len()).over(["mmsi", "t"]) > 0,
        flag_sog_high=pl.col("sog") > max_plausible_sog_kn,
    ).with_columns(pl.col("flag_sog_high").fill_null(False))

    # Spikes are computed on otherwise-valid points only, so duplicates don't mask them
    base_ok = ~pl.any_horizontal("flag_invalid_pos", "flag_bad_mmsi", "flag_duplicate")
    ok = df.filter(base_ok)
    spike = pl.Series("flag_speed_spike", _implied_speed_spike(ok, max_implied_speed_kn))
    ok = ok.with_columns(spike).select("mmsi", "t", "flag_speed_spike")
    return (
        df.join(ok, on=["mmsi", "t"], how="left", maintain_order="left")
        .with_columns(pl.col("flag_speed_spike").fill_null(False))
        .with_columns(pl.when(pl.col("flag_duplicate")).then(False).otherwise(pl.col("flag_speed_spike"))
                      .alias("flag_speed_spike"))
    )


def quality_report(raw: pl.DataFrame, flagged: pl.DataFrame) -> dict:
    n = len(flagged)
    report = {
        "rows": n,
        "vessels": flagged["mmsi"].n_unique(),
        "t_min_utc": str(flagged["t"].min()),
        "t_max_utc": str(flagged["t"].max()),
        "null_fraction_after_sentinels": {
            c: round(flagged[c].null_count() / max(n, 1), 4)
            for c in ("sog", "cog", "heading", "ship_type", "length", "width", "draught")
            if c in flagged.columns
        },
        "sentinel_counts_raw": {
            "sog_102.3": int((raw["sog"] >= 102.2).sum()),
            "heading_511": int((raw["heading"] >= 360).sum()),
            "cog_360": int((raw["cog"] >= 360).sum()),
        },
        "flags": {c: int(flagged[c].sum()) for c in FLAG_COLS},
        "rows_passing_hard_flags": int(flagged.filter(~pl.any_horizontal(HARD_FLAGS)).height),
    }
    dt = (
        flagged.filter(~pl.any_horizontal(HARD_FLAGS))
        .sort(["mmsi", "t"])
        .select(pl.col("t").diff().over("mmsi").dt.total_seconds().alias("dt"))
        .drop_nulls()["dt"]
    )
    if len(dt):
        report["report_interval_s_quantiles"] = {
            f"p{q}": float(dt.quantile(q / 100)) for q in (10, 50, 90, 99)
        }
    return report
