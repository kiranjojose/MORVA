"""Danish Maritime Authority (DMA) historical AIS ingestion.

Raw files are never modified. A zip is extracted to a temporary CSV, read as all-string
columns (DMA uses text such as "Unknown" in numeric fields), cast leniently, filtered to
the AOI and allowed mobile types, and written to `data/interim/<stem>.parquet`.
"""

import shutil
import tempfile
import zipfile
from pathlib import Path

import polars as pl

# DMA header name -> canonical name. Verify against the real file header on first download.
DMA_COLUMNS = {
    "# Timestamp": "t",
    "Type of mobile": "mobile_type",
    "MMSI": "mmsi",
    "Latitude": "lat",
    "Longitude": "lon",
    "Navigational status": "nav_status",
    "ROT": "rot",
    "SOG": "sog",
    "COG": "cog",
    "Heading": "heading",
    "IMO": "imo",
    "Name": "name",
    "Ship type": "ship_type",
    "Width": "width",
    "Length": "length",
    "Draught": "draught",
    "Destination": "destination",
}

FLOAT_COLS = ["lat", "lon", "rot", "sog", "cog", "heading", "width", "length", "draught"]


def _cast(lf: pl.LazyFrame, timestamp_format: str) -> pl.LazyFrame:
    return lf.with_columns(
        pl.col("t").str.strptime(pl.Datetime("us", "UTC"), timestamp_format, strict=False),
        pl.col("mmsi").cast(pl.Int64, strict=False),
        *[pl.col(c).cast(pl.Float64, strict=False) for c in FLOAT_COLS],
    )


def scan_dma_csv(path: Path, timestamp_format: str) -> pl.LazyFrame:
    lf = pl.scan_csv(path, infer_schema=False)
    present = set(lf.collect_schema().names())
    missing = [c for c in ("# Timestamp", "MMSI", "Latitude", "Longitude") if c not in present]
    if missing:
        raise ValueError(f"{path.name}: missing expected DMA columns {missing}; header is {sorted(present)}")
    mapping = {k: v for k, v in DMA_COLUMNS.items() if k in present}
    # Absent optional columns become typed nulls so the canonical schema is always the same
    absent = [pl.lit(None, pl.String).alias(v) for k, v in DMA_COLUMNS.items() if k not in present]
    lf = lf.select(list(mapping)).rename(mapping).with_columns(absent).select(list(DMA_COLUMNS.values()))
    return _cast(lf, timestamp_format)


def filter_aoi(lf: pl.LazyFrame, aoi: dict, keep_mobile_types: list[str]) -> pl.LazyFrame:
    return lf.filter(
        pl.col("lat").is_between(aoi["lat_min"], aoi["lat_max"])
        & pl.col("lon").is_between(aoi["lon_min"], aoi["lon_max"])
        & pl.col("mobile_type").is_in(keep_mobile_types)
    )


def ingest_file(src: Path, out_dir: Path, data_cfg: dict) -> Path:
    """Convert one DMA zip/CSV to an AOI-filtered interim Parquet file. Returns its path."""
    src_cfg, aoi = data_cfg["source"], data_cfg["aoi"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.name.split('.')[0]}.parquet"

    with tempfile.TemporaryDirectory(dir=out_dir) as tmp:
        if src.suffix == ".zip":
            with zipfile.ZipFile(src) as zf:
                members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
                if len(members) != 1:
                    raise ValueError(f"{src.name}: expected exactly one CSV inside, found {members}")
                csv_path = Path(tmp) / "extracted.csv"
                with zf.open(members[0]) as fin, csv_path.open("wb") as fout:
                    shutil.copyfileobj(fin, fout, length=16 * 1024 * 1024)
        else:
            csv_path = src

        lf = filter_aoi(scan_dma_csv(csv_path, src_cfg["timestamp_format"]), aoi, src_cfg["keep_mobile_types"])
        lf.sink_parquet(out_path)
    return out_path
