"""Kystverket Historisk AIS (HAIS) ingestion (`hais_YYYY-MM-DD.snappy.parquet`, from https://hais.kystverket.no).

An order is delivered as a zip whose `position/` folder holds one Parquet file per day; the extracted Parquet file is
the raw file. Positions are full-rate (Class A moving vessels report every 6-7 s in the 24 Sep 2026 sample). The file
carries a Spark `geometry` column whose Parquet logical type Polars cannot read, so it is read with PyArrow and the
geometry is never loaded.

Rows are mapped to the same canonical schema as the DMA reader (`morva.ingestion.dma.DMA_COLUMNS`), filtered to the
regions of this source, to Class A and to the configured data sources (`G` shore stations, `S` satellite), and
written to `<interim>/<stem>.parquet`.

The position file has no static or voyage fields: name, IMO, ship type, dimensions, draught and destination are null.
`rate_of_turn` is the encoded AIS ROT indicator, not degrees per minute, and is not used downstream, so `rot` is null.
"""

from pathlib import Path

import polars as pl
import pyarrow.parquet as pq

from morva.ingestion.dma import DMA_COLUMNS, filter_aoi
from morva.ingestion.marinecadastre import NAV_STATUS

REQUIRED = ("date_time_utc", "mmsi", "latitude", "longitude", "ais_class")

# HAIS column -> canonical column
HAIS_COLUMNS = {
    "date_time_utc": "t", "mmsi": "mmsi", "latitude": "lat", "longitude": "lon", "status": "nav_status",
    "speed_over_ground": "sog", "course_over_ground": "cog", "true_heading": "heading",
}


def read_hais_parquet(path: Path, keep_data_sources: list[str]) -> pl.LazyFrame:
    present = set(pq.ParquetFile(path).schema_arrow.names)
    missing = [c for c in REQUIRED if c not in present]
    if missing:
        raise ValueError(f"{path.name}: missing expected HAIS columns {missing}; columns are {sorted(present)}")
    cols = [c for c in (*HAIS_COLUMNS, "ais_class", "data_source") if c in present]
    lf = pl.from_arrow(pq.read_table(path, columns=cols)).lazy()
    if "data_source" in present:
        lf = lf.filter(pl.col("data_source").is_in(keep_data_sources))
    status = pl.col("status").cast(pl.Int64, strict=False)
    lf = lf.with_columns(
        mobile_type=pl.when(pl.col("ais_class") == "A").then(pl.lit("Class A"))
        .when(pl.col("ais_class") == "B").then(pl.lit("Class B")).otherwise(pl.col("ais_class")),
        status=status.replace_strict(NAV_STATUS, default=None, return_dtype=pl.String).fill_null(
            status.cast(pl.String)),
    ).rename({k: v for k, v in HAIS_COLUMNS.items() if k in present})
    absent = [pl.lit(None, pl.String).alias(c) for c in DMA_COLUMNS.values() if c not in lf.collect_schema().names()]
    lf = lf.with_columns(absent).select(list(DMA_COLUMNS.values()))
    return lf.with_columns(
        pl.col("t").cast(pl.Datetime("us")).dt.replace_time_zone("UTC"),
        pl.col("mmsi").cast(pl.Int64),
        *[pl.col(c).cast(pl.Float64, strict=False) for c in ("lat", "lon", "sog", "cog", "heading")],
        *[pl.col(c).cast(pl.Float64) for c in ("rot", "width", "length", "draught")],
    )


def ingest_file(src: Path, out_dir: Path, source_cfg: dict, boxes: list[dict]) -> dict:
    """Convert one HAIS daily Parquet file to a region-filtered interim Parquet file."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.name.split('.')[0]}.parquet"
    keep = [{"A": "Class A", "B": "Class B"}.get(t, t) for t in source_cfg["keep_ais_classes"]]
    lf = read_hais_parquet(src, source_cfg.get("keep_data_sources", ["G"]))
    df = filter_aoi(lf, boxes, keep).collect()
    unique = df.unique(maintain_order=True)
    unique.write_parquet(out_path)
    return {
        "source": src.name,
        "interim": out_path.name,
        "rows_in_aoi": len(df),
        "exact_duplicates_removed": len(df) - len(unique),
        "rows_written": len(unique),
        "rows_written_by_region": dict(sorted(unique["region"].value_counts().iter_rows())),
    }
