"""Track segmentation: split each vessel's points into contiguous segments at reporting gaps."""

import polars as pl

from morva.quality.checks import HARD_FLAGS


def segment_tracks(df: pl.DataFrame, gap_s: float, min_points: int, min_duration_s: float) -> pl.DataFrame:
    """Drop hard-flagged points (if flag columns are present), start a new segment when the gap exceeds `gap_s` or
    the vessel changes `region` (if present), and keep segments with enough points and duration. Adds integer
    `segment_id`."""
    flags = [c for c in HARD_FLAGS if c in df.columns]  # absent when given already-clean points
    clean = (df.filter(~pl.any_horizontal(flags)) if flags else df).sort(["mmsi", "t"])
    new = (pl.col("mmsi") != pl.col("mmsi").shift(1)) | (pl.col("t").diff().dt.total_seconds() > gap_s)
    if "region" in clean.columns:  # a segment never spans two areas, so every window has exactly one region
        new = new | (pl.col("region") != pl.col("region").shift(1))
    clean = clean.with_columns(
        _new=new.fill_null(True)
    ).with_columns(segment_id=pl.col("_new").cum_sum().cast(pl.Int64)).drop("_new")

    stats = clean.group_by("segment_id").agg(
        n=pl.len(), dur=(pl.col("t").max() - pl.col("t").min()).dt.total_seconds()
    )
    keep = stats.filter((pl.col("n") >= min_points) & (pl.col("dur") >= min_duration_s))["segment_id"]
    return clean.filter(pl.col("segment_id").is_in(keep.implode()))


def vessel_table(df: pl.DataFrame) -> pl.DataFrame:
    """One row per MMSI with static attributes and a count of inconsistent ship-type reports."""
    agg = [pl.len().alias("n_points")]
    if "ship_type" in df.columns:
        # DMA writes "Undefined" on rows where no static message was merged; it is missing, not a type
        known = pl.col("ship_type").filter(pl.col("ship_type").is_not_null() & (pl.col("ship_type") != "Undefined"))
        agg += [
            known.mode().first().alias("ship_type"),
            known.n_unique().alias("n_ship_type_values"),
        ]
    for c in ("length", "width", "draught"):
        if c in df.columns:
            agg.append(pl.col(c).filter(pl.col(c) > 0).median().alias(c))
    return df.group_by("mmsi").agg(agg).sort("mmsi")
