"""Leakage-aware time-block split with independent transfer waterways.

A window belongs to a block only if its whole span (history start .. forecast end) lies
inside it; windows straddling a boundary, or ending after `test_end`, are labelled "excluded"
and never used. Windows outside the home region get transfer labels instead of train/val/test,
so every existing `split == "train"` selection stays home-only:

    home      train            val            test
    transfer  transfer_context transfer_val   transfer_test

`transfer_context` windows are never used to fit models; they cover the training period and
may only support context derived from historical traffic (e.g. V2 traffic-flow maps).
"""

from datetime import datetime, timedelta

import polars as pl

LOCKED_SPLITS = ("test", "transfer_test")
EVAL_SPLITS = ("val", "test", "transfer_val", "transfer_test")
TRANSFER_LABELS = {"train": "transfer_context", "val": "transfer_val", "test": "transfer_test"}


def resolve_boundaries(meta: pl.DataFrame, split_cfg: dict) -> tuple[datetime, datetime, datetime | None]:
    """(train_end, val_end, test_end); test_end is None when the test block is open-ended."""
    if split_cfg.get("train_end") and split_cfg.get("val_end"):
        parse = lambda s: datetime.fromisoformat(s).replace(tzinfo=meta["t0"].min().tzinfo)  # noqa: E731
        test_end = parse(split_cfg["test_end"]) if split_cfg.get("test_end") else None
        return parse(split_cfg["train_end"]), parse(split_cfg["val_end"]), test_end
    f_train, f_val = split_cfg["auto_fractions"]
    t_min, t_max = meta["t0"].min(), meta["t0"].max()
    total = t_max - t_min
    hour = lambda d: d.replace(minute=0, second=0, microsecond=0)  # noqa: E731
    return hour(t_min + total * f_train), hour(t_min + total * (f_train + f_val)), None


def assign_split(meta: pl.DataFrame, train_end, val_end, step_s: int, obs_steps: int, future_steps: int,
                 test_end=None, home_region: str | None = None):
    start = pl.col("t0") - timedelta(seconds=step_s * (obs_steps - 1))
    end = pl.col("t0") + timedelta(seconds=step_s * future_steps)
    in_test = (start >= val_end) if test_end is None else (start >= val_end) & (end <= test_end)
    block = (
        pl.when(end <= train_end).then(pl.lit("train"))
        .when((start >= train_end) & (end <= val_end)).then(pl.lit("val"))
        .when(in_test).then(pl.lit("test"))
        .otherwise(pl.lit("excluded"))
    )
    if home_region is not None and "region" in meta.columns:
        block = pl.when(pl.col("region") == home_region).then(block).otherwise(
            block.replace(TRANSFER_LABELS))
    return meta.with_columns(split=block)


def split_summary(meta: pl.DataFrame, train_end, val_end, test_end=None) -> dict:
    keys = ["split", "region"] if "region" in meta.columns else ["split"]
    counts = meta.group_by(keys).agg(n_windows=pl.len(), n_vessels=pl.col("mmsi").n_unique()).sort(keys)
    by_split = meta.group_by("split").agg(n_windows=pl.len(), n_vessels=pl.col("mmsi").n_unique()).sort("split")
    vessels = {s: set(meta.filter(pl.col("split") == s)["mmsi"]) for s in ("train", *EVAL_SPLITS)}
    summary = {
        "train_end_utc": str(train_end),
        "val_end_utc": str(val_end),
        "test_end_utc": str(test_end),
        "counts": {r["split"]: {"windows": r["n_windows"], "vessels": r["n_vessels"]} for r in by_split.to_dicts()},
        "vessel_overlap_with_train": {s: len(vessels["train"] & vessels[s]) for s in EVAL_SPLITS},
    }
    if "region" in meta.columns:
        summary["counts_by_region"] = {
            f"{r['split']}/{r['region']}": {"windows": r["n_windows"], "vessels": r["n_vessels"]}
            for r in counts.to_dicts()}
    return summary
