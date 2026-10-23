"""V3 infrastructure: Marine Cadastre ingestion, per-region calendars, quantile model and conformal boxes."""

from datetime import UTC, datetime, timedelta

import numpy as np
import polars as pl
import pytest
import zstandard

from morva.evaluation.conformal import box_scores, conformal_offset, coverage
from morva.evaluation.splits import assign_calendar_split
from morva.ingestion.dma import DMA_COLUMNS
from morva.ingestion.marinecadastre import ingest_file

HEADER = ("mmsi,base_date_time,longitude,latitude,sog,cog,heading,vessel_name,imo,call_sign,vessel_type,status,"
          "length,width,draft,cargo,transceiver")
SALISH = dict(name="salish_sea", source="marinecadastre", lat_min=47.0, lat_max=48.8, lon_min=-124.7, lon_max=-122.2)


def test_marinecadastre_ingest_maps_schema_types_and_drops_class_b(tmp_path):
    rows = [
        "367000001,2025-09-24 00:00:00,-122.5,47.6,12.1,10.0,9,CARGO ONE,IMO1,CALL,70,0,190,30,9.1,70,A",
        "367000002,2025-09-24 00:01:00,-122.6,47.7,9.0,200.0,,TUG TWO,,,52,0,30,10,,52,A",
        "367000003,2025-09-24 00:02:00,-122.7,47.8,0.0,0.0,,UNKNOWN,,,,5,,,,,A",
        "367000004,2025-09-24 00:03:00,-122.7,47.8,5.0,90.0,,SMALL,,,37,,,,,,B",  # Class B: dropped
        "367000005,2025-09-24 00:04:00,-80.0,30.0,5.0,90.0,,ELSEWHERE,,,70,0,100,20,,,A",  # outside every box
    ]
    src = tmp_path / "ais-2025-09-24.csv.zst"
    src.write_bytes(zstandard.ZstdCompressor().compress(("\n".join([HEADER, *rows]) + "\n").encode()))
    rec = ingest_file(src, tmp_path / "interim", {"keep_transceivers": ["A"]}, [SALISH])
    df = pl.read_parquet(tmp_path / "interim" / "ais-2025-09-24.parquet")
    assert rec["rows_written"] == 3 and set(df["mmsi"]) == {367000001, 367000002, 367000003}
    assert df.columns == [*DMA_COLUMNS.values(), "region"] and (df["region"] == "salish_sea").all()
    assert dict(zip(df["mmsi"], df["ship_type"], strict=True)) == {
        367000001: "Cargo", 367000002: "Tug", 367000003: "Undefined"}
    assert df.filter(pl.col("mmsi") == 367000003)["nav_status"][0] == "Moored"
    assert df["t"].dtype == pl.Datetime("us", "UTC") and df["t"][0] == datetime(2025, 9, 24, tzinfo=UTC)


def test_calendar_split_uses_each_regions_own_year_and_a_calib_block():
    def cal(year):
        d = lambda m, day: datetime(year, m, day, tzinfo=UTC)  # noqa: E731
        return {"train_start": d(9, 19), "train_end": d(10, 7), "val_end": d(10, 12), "calib_end": d(10, 16),
                "test_end": d(10, 30)}

    anchors = {"home": 2026, "salish_sea": 2025}
    t0s = [(r, datetime(y, 9, 18, tzinfo=UTC) + timedelta(hours=h)) for r, y in anchors.items()
           for h in range(0, 24 * 43, 6)]
    meta = pl.DataFrame({"region": [r for r, _ in t0s], "t0": [t for _, t in t0s], "mmsi": [1] * len(t0s)})
    out = assign_calendar_split(meta, {"home": cal(2026), "salish_sea": cal(2025)}, "home", 60, 20, 60)
    home, us = out.filter(pl.col("region") == "home"), out.filter(pl.col("region") == "salish_sea")
    assert set(home["split"]) == {"train", "val", "calib", "test", "excluded"}
    assert set(us["split"]) == {"transfer_context", "transfer_val", "transfer_calib", "transfer_test", "excluded"}
    for df, c in ((home, cal(2026)), (us, cal(2025))):
        labelled = df.filter(pl.col("split") != "excluded")
        assert (labelled["t0"] - timedelta(minutes=19) >= c["train_start"]).all()
        assert (labelled["t0"] + timedelta(minutes=60) <= c["test_end"]).all()
        calib = df.filter(pl.col("split").str.ends_with("calib"))
        assert calib["t0"].min() - timedelta(minutes=19) >= c["val_end"]
        assert calib["t0"].max() + timedelta(minutes=60) <= c["calib_end"]
    # The same calendar dates give the same labels in both years
    assert (home["split"].str.replace("^transfer_", "").replace({"context": "train"})
            == us["split"].str.replace("^transfer_", "").replace({"context": "train"})).all()


def test_conformal_offset_formula_and_box_scores():
    scores = np.arange(1, 10, dtype=float)[:, None]  # n = 9 calibration windows, one knot
    assert conformal_offset(scores, 0.8)[0] == 8.0  # k = ceil(10 * 0.8) = 8 -> 8th smallest
    assert np.isinf(conformal_offset(scores, 0.95)[0])  # k = 10 > n = 9: no finite offset is valid
    lo, hi = np.zeros((1, 1, 2)), np.ones((1, 1, 2))
    assert box_scores(lo, hi, np.array([[[0.5, 0.5]]]))[0, 0] < 0  # inside
    assert box_scores(lo, hi, np.array([[[0.5, 3.0]]]))[0, 0] == pytest.approx(2.0)  # worse axis counts


def test_conformal_boxes_reach_target_coverage_on_exchangeable_data():
    rng = np.random.default_rng(0)
    n, knots = 4000, 3
    y = rng.normal(0, [1.0, 2.0, 4.0], size=(2 * n, 2, knots)).transpose(0, 2, 1)  # [n, knots, 2]
    lo, hi = -0.5 * np.ones_like(y), 0.5 * np.ones_like(y)  # deliberately too narrow before calibration
    for level in (0.8, 0.9):
        off = conformal_offset(box_scores(lo[:n], hi[:n], y[:n]), level)
        cov = coverage(lo[n:], hi[n:], y[n:], off)
        assert (np.abs(cov - level) < 0.03).all(), cov
        assert (coverage(lo[n:], hi[n:], y[n:], np.zeros(knots)) < level).all()


def test_quantile_model_shapes_order_and_level_check():
    from morva.models.quantile import QuantileResidualGBM

    rng = np.random.default_rng(1)
    n, step = 400, 60
    lat0, lon0 = 55.5, 11.0
    hist = np.zeros((n, 20, 4))
    hist[:, :, 0] = lat0 + np.linspace(-0.05, 0, 20)[None, :] + rng.normal(0, 1e-4, (n, 20))
    hist[:, :, 1] = lon0
    hist[:, :, 2], hist[:, :, 3] = 10.0, 0.0
    fut = np.stack([lat0 + np.linspace(0.003, 0.05, 20)[None, :] + rng.normal(0, 2e-3, (n, 20)),
                    lon0 + rng.normal(0, 2e-3, (n, 20))], axis=-1)
    X = rng.normal(size=(n, 3))
    m = QuantileResidualGBM([5, 10, 20], [0.1, 0.5, 0.9], max_iter=20).fit(X, hist, fut, step)
    pred = m.predict(X)
    assert pred.shape == (n, 3, 2, 3) and (np.diff(pred, axis=-1) >= 0).all()
    lo, hi = m.interval(pred, 0.8)
    assert lo.shape == (n, 3, 2) and (hi >= lo).all()
    with pytest.raises(ValueError):
        m.interval(pred, 0.9)  # 0.05 / 0.95 not fitted
