"""Leakage-aware time-block split.

A window belongs to a block only if its whole span (history start .. forecast end) lies
inside it; windows straddling a boundary are labelled "excluded" and never used.
"""

from datetime import datetime, timedelta

import polars as pl


def resolve_boundaries(meta: pl.DataFrame, split_cfg: dict) -> tuple[datetime, datetime]:
    if split_cfg.get("train_end") and split_cfg.get("val_end"):
        parse = lambda s: datetime.fromisoformat(s).replace(tzinfo=meta["t0"].min().tzinfo)  # noqa: E731
        return parse(split_cfg["train_end"]), parse(split_cfg["val_end"])
    f_train, f_val = split_cfg["auto_fractions"]
    t_min, t_max = meta["t0"].min(), meta["t0"].max()
    total = t_max - t_min
    hour = lambda d: d.replace(minute=0, second=0, microsecond=0)  # noqa: E731
    return hour(t_min + total * f_train), hour(t_min + total * (f_train + f_val))


def assign_split(meta: pl.DataFrame, train_end, val_end, step_s: int, obs_steps: int, future_steps: int):
    start = pl.col("t0") - timedelta(seconds=step_s * (obs_steps - 1))
    end = pl.col("t0") + timedelta(seconds=step_s * future_steps)
    return meta.with_columns(
        split=pl.when(end <= train_end).then(pl.lit("train"))
        .when((start >= train_end) & (end <= val_end)).then(pl.lit("val"))
        .when(start >= val_end).then(pl.lit("test"))
        .otherwise(pl.lit("excluded"))
    )


def split_summary(meta: pl.DataFrame, train_end, val_end) -> dict:
    counts = meta.group_by("split").agg(n_windows=pl.len(), n_vessels=pl.col("mmsi").n_unique())
    vessels = {s: set(meta.filter(pl.col("split") == s)["mmsi"]) for s in ("train", "val", "test")}
    return {
        "train_end_utc": str(train_end),
        "val_end_utc": str(val_end),
        "counts": {r["split"]: {"windows": r["n_windows"], "vessels": r["n_vessels"]} for r in counts.to_dicts()},
        "vessel_overlap": {
            "train_val": len(vessels["train"] & vessels["val"]),
            "train_test": len(vessels["train"] & vessels["test"]),
        },
    }
