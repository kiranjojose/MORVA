"""V4 infrastructure: Kystverket HAIS ingestion."""

from datetime import UTC, datetime
from decimal import Decimal

import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq

from morva.ingestion.dma import DMA_COLUMNS
from morva.ingestion.kystverket import ingest_file

BERGEN = dict(name="bergen", source="kystverket", lat_min=60.0, lat_max=61.0, lon_min=4.5, lon_max=5.6)


def _hais_file(path, rows):
    """Write rows in the HAIS position schema (decimal SOG/COG, ns timestamps, binary geometry)."""
    names = ["date_time_utc", "mmsi", "longitude", "latitude", "status", "course_over_ground", "true_heading",
             "speed_over_ground", "rate_of_turn", "maneuvre", "data_source", "ais_class", "msg_type"]
    cols = dict(zip(names, map(list, zip(*rows, strict=True)), strict=True))
    table = pa.table({
        "date_time_utc": pa.array(cols["date_time_utc"], pa.timestamp("ns")),
        "mmsi": pa.array(cols["mmsi"], pa.int32()),
        "longitude": pa.array(cols["longitude"], pa.float64()),
        "latitude": pa.array(cols["latitude"], pa.float64()),
        "status": pa.array(cols["status"], pa.int8()),
        "course_over_ground": pa.array([Decimal(str(v)) for v in cols["course_over_ground"]], pa.decimal128(6, 2)),
        "true_heading": pa.array(cols["true_heading"], pa.int16()),
        "speed_over_ground": pa.array([Decimal(str(v)) for v in cols["speed_over_ground"]], pa.decimal128(6, 2)),
        "rate_of_turn": pa.array(cols["rate_of_turn"], pa.int8()),
        "maneuvre": pa.array(cols["maneuvre"], pa.int8()),
        "data_source": pa.array(cols["data_source"], pa.string()),
        "ais_class": pa.array(cols["ais_class"], pa.string()),
        "msg_type": pa.array(cols["msg_type"], pa.int8()),
        "geometry": pa.array([b"\x01"] * len(rows), pa.binary()),
    })
    pq.write_table(table, path)


def test_hais_ingest_maps_schema_and_keeps_shore_class_a_in_region(tmp_path):
    t0 = datetime(2026, 9, 24, 0, 0, 4)
    rows = [
        (t0, 257000001, 5.1, 60.3, 0, 182.5, 181, 12.3, 0, 0, "G", "A", 1),
        (t0, 257000002, 5.2, 60.4, 5, 360.0, 511, 0.0, -128, 0, "G", "A", 3),   # moored, sentinels kept raw
        (t0, 257000003, 5.3, 60.5, 0, 90.0, 90, 10.0, 0, 0, "S", "A", 27),      # satellite: dropped by default
        (t0, 257000004, 5.3, 60.5, 15, 90.0, 511, 6.0, 0, 0, "G", "B", 18),     # Class B: dropped
        (t0, 257000005, 10.6, 59.3, 0, 90.0, 90, 10.0, 0, 0, "G", "A", 1),      # outside the box
    ]
    src = tmp_path / "hais_2026-09-24.snappy.parquet"
    _hais_file(src, rows)
    rec = ingest_file(src, tmp_path / "interim", {"keep_ais_classes": ["A"]}, [BERGEN])
    df = pl.read_parquet(tmp_path / "interim" / "hais_2026-09-24.parquet")
    assert rec["rows_written"] == 2 and set(df["mmsi"]) == {257000001, 257000002}
    assert df.columns == [*DMA_COLUMNS.values(), "region"] and (df["region"] == "bergen").all()
    first = df.filter(pl.col("mmsi") == 257000001).row(0, named=True)
    assert first["sog"] == 12.3 and first["cog"] == 182.5 and first["heading"] == 181.0
    assert first["nav_status"] == "Under way using engine" and first["ship_type"] is None and first["rot"] is None
    moored = df.filter(pl.col("mmsi") == 257000002).row(0, named=True)
    assert moored["nav_status"] == "Moored" and moored["cog"] == 360.0 and moored["heading"] == 511.0
    assert df["t"].dtype == pl.Datetime("us", "UTC") and df["t"][0] == datetime(2026, 9, 24, 0, 0, 4, tzinfo=UTC)

    rec = ingest_file(src, tmp_path / "interim2", {"keep_ais_classes": ["A"], "keep_data_sources": ["G", "S"]},
                      [BERGEN])
    assert rec["rows_written"] == 3
