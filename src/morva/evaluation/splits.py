"""Leakage-aware time-block split with independent transfer waterways.

A window belongs to a block only if its whole span (history start .. forecast end) lies
inside it; windows straddling a boundary, or ending after `test_end`, are labelled "excluded"
and never used. Windows outside the home region get transfer labels instead of train/val/test,
so every existing `split == "train"` selection stays home-only:

    home      train            val            test
    transfer  transfer_context transfer_val   transfer_test

`transfer_context` windows are never used to fit models; they cover the training period and
may only support context derived from historical traffic (e.g. V2 traffic-flow maps).

V3 configs give each region a calendar (`split.calendars`) with a separate calibration block between validation and
test: train / val / calib / test, and transfer_context / transfer_val / transfer_calib / transfer_test.
"""

from datetime import datetime, timedelta

import polars as pl

LOCKED_SPLITS = ("test", "transfer_test")
EVAL_SPLITS = ("val", "test", "transfer_val", "transfer_test")
TRANSFER_LABELS = {"train": "transfer_context", "val": "transfer_val", "calib": "transfer_calib",
                   "test": "transfer_test"}
CALENDAR_BLOCKS = ("train_start", "train_end", "val_end", "calib_end", "test_end")
SYNTHETIC_CALENDAR_FRACTIONS = (0.6, 0.75, 0.85)  # train / val / calib ends as fractions of a region's time range


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


def resolve_calendars(meta: pl.DataFrame, split_cfg: dict, calendar_of: dict[str, str],
                      synthetic: bool = False) -> dict[str, dict[str, datetime]]:
    """Region -> block boundaries. Synthetic data have their own dates, so each region's range is cut by fraction."""
    tz = meta["t0"].dtype.time_zone
    if not synthetic:
        cals = {name: {k: datetime.fromisoformat(v).replace(tzinfo=meta["t0"].min().tzinfo) for k, v in c.items()}
                for name, c in split_cfg["calendars"].items()}
        return {region: cals[cal] for region, cal in calendar_of.items()}
    out = {}
    for region in calendar_of:
        t = meta.filter(pl.col("region") == region)["t0"]
        if t.is_empty():
            continue
        t_min, t_max = t.min(), t.max() + timedelta(seconds=1)
        span = t_max - t_min
        ends = [t_min + span * f for f in SYNTHETIC_CALENDAR_FRACTIONS]
        out[region] = dict(zip(CALENDAR_BLOCKS, [t_min - timedelta(days=1), *ends, t_max + timedelta(days=1)],
                               strict=True))
    assert tz is None or all(b.tzinfo is not None for c in out.values() for b in c.values())
    return out


def assign_calendar_split(meta: pl.DataFrame, bounds: dict[str, dict[str, datetime]], home_region: str,
                          step_s: int, obs_steps: int, future_steps: int) -> pl.DataFrame:
    """Label each window by its region's calendar. Windows outside every block, or straddling a boundary, are
    "excluded"; regions without a calendar are excluded entirely."""
    start = pl.col("t0") - timedelta(seconds=step_s * (obs_steps - 1))
    end = pl.col("t0") + timedelta(seconds=step_s * future_steps)
    label = pl.lit("excluded")
    for region, b in bounds.items():
        block = pl.lit("excluded")
        for name, lo, hi in reversed((("train", "train_start", "train_end"), ("val", "train_end", "val_end"),
                                      ("calib", "val_end", "calib_end"), ("test", "calib_end", "test_end"))):
            block = pl.when((start >= b[lo]) & (end <= b[hi])).then(pl.lit(name)).otherwise(block)
        if region != home_region:
            block = block.replace(TRANSFER_LABELS)
        label = pl.when(pl.col("region") == region).then(block).otherwise(label)
    return meta.with_columns(split=label)


def split_summary(meta: pl.DataFrame, train_end=None, val_end=None, test_end=None, boundaries=None) -> dict:
    keys = ["split", "region"] if "region" in meta.columns else ["split"]
    counts = meta.group_by(keys).agg(n_windows=pl.len(), n_vessels=pl.col("mmsi").n_unique()).sort(keys)
    by_split = meta.group_by("split").agg(n_windows=pl.len(), n_vessels=pl.col("mmsi").n_unique()).sort("split")
    split_counts = {r["split"]: {"windows": r["n_windows"], "vessels": r["n_vessels"]} for r in by_split.to_dicts()}
    vessels = lambda s: set(meta.filter(pl.col("split") == s)["mmsi"])  # noqa: E731
    if boundaries is None:  # V1/V2 layout, unchanged
        summary = {
            "train_end_utc": str(train_end),
            "val_end_utc": str(val_end),
            "test_end_utc": str(test_end),
            "counts": split_counts,
            "vessel_overlap_with_train": {s: len(vessels("train") & vessels(s)) for s in EVAL_SPLITS},
        }
    else:
        evaluated = sorted(set(meta["split"].unique()) - {"train", "excluded", "transfer_context"})
        summary = {
            "boundaries_utc": {r: {k: str(v) for k, v in b.items()} for r, b in boundaries.items()},
            "counts": split_counts,
            "vessel_overlap_with_train": {s: len(vessels("train") & vessels(s)) for s in evaluated},
        }
    if "region" in meta.columns:
        summary["counts_by_region"] = {
            f"{r['split']}/{r['region']}": {"windows": r["n_windows"], "vessels": r["n_vessels"]}
            for r in counts.to_dicts()}
    return summary
