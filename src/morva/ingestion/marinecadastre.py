"""NOAA/BOEM Marine Cadastre AIS ingestion (2025 daily format, `ais-2025-MM-DD.csv.zst`).

The files are already sampled at one minute and cover US waters. Each file is decompressed to a temporary CSV, read
as all-string columns, mapped to the same canonical schema as the DMA reader (`morva.ingestion.dma.DMA_COLUMNS`),
filtered to the regions of this source and to Class A transmitters, and written to `<interim>/<stem>.parquet`.

Numeric AIS ship-type codes are mapped to the DMA ship-type names, so `features.motion.SHIP_GROUPS` treats both
sources alike. Navigational-status codes are mapped to DMA's text values.
"""

import shutil
import tempfile
from pathlib import Path

import polars as pl
import zstandard

from morva.ingestion.dma import DMA_COLUMNS, FLOAT_COLS, filter_aoi

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"  # UTC
REQUIRED = ("mmsi", "base_date_time", "latitude", "longitude", "transceiver")

# Marine Cadastre 2025 column -> canonical column
MC_COLUMNS = {
    "base_date_time": "t", "mmsi": "mmsi", "latitude": "lat", "longitude": "lon", "status": "nav_status",
    "sog": "sog", "cog": "cog", "heading": "heading", "imo": "imo", "vessel_name": "name",
    "vessel_type": "ship_type", "width": "width", "length": "length", "draft": "draught",
}

_SINGLE_CODES = {
    30: "Fishing", 31: "Towing", 32: "Towing long/wide", 33: "Dredging", 34: "Diving", 35: "Military",
    36: "Sailing", 37: "Pleasure", 50: "Pilot", 51: "SAR", 52: "Tug", 53: "Port tender", 54: "Anti-pollution",
    55: "Law enforcement", 58: "Medical", 59: "Not party to conflict",
}
_CODE_RANGES = ((20, 29, "WIG"), (40, 49, "HSC"), (60, 69, "Passenger"), (70, 79, "Cargo"), (80, 89, "Tanker"),
                (90, 99, "Other"))
NAV_STATUS = {
    0: "Under way using engine", 1: "At anchor", 2: "Not under command", 3: "Restricted manoeuverability",
    4: "Constrained by her draught", 5: "Moored", 6: "Aground", 7: "Engaged in fishing", 8: "Under way sailing",
    15: "Unknown value",
}


def ship_type_name(code: pl.Expr) -> pl.Expr:
    """AIS ship-type code -> DMA ship-type name; missing or unknown codes -> "Undefined" (treated as missing)."""
    out = pl.lit("Undefined")
    for lo, hi, name in reversed(_CODE_RANGES):
        out = pl.when(code.is_between(lo, hi)).then(pl.lit(name)).otherwise(out)
    for c, name in _SINGLE_CODES.items():
        out = pl.when(code == c).then(pl.lit(name)).otherwise(out)
    return out


def scan_marinecadastre_csv(path: Path) -> pl.LazyFrame:
    lf = pl.scan_csv(path, infer_schema=False)
    present = set(lf.collect_schema().names())
    missing = [c for c in REQUIRED if c not in present]
    if missing:
        raise ValueError(f"{path.name}: missing expected Marine Cadastre columns {missing}; "
                         f"header is {sorted(present)}")
    code = pl.col("vessel_type").cast(pl.Int64, strict=False)
    status = pl.col("status").cast(pl.Int64, strict=False)
    lf = lf.with_columns(
        mobile_type=pl.when(pl.col("transceiver") == "A").then(pl.lit("Class A"))
        .when(pl.col("transceiver") == "B").then(pl.lit("Class B")).otherwise(pl.col("transceiver")),
        vessel_type=ship_type_name(code),
        status=status.replace_strict(NAV_STATUS, default=None, return_dtype=pl.String).fill_null(
            status.cast(pl.String)),
    ).rename({k: v for k, v in MC_COLUMNS.items() if k in present})
    absent = [pl.lit(None, pl.String).alias(c) for c in DMA_COLUMNS.values() if c not in lf.collect_schema().names()]
    lf = lf.with_columns(absent).select(list(DMA_COLUMNS.values()))
    return lf.with_columns(
        pl.col("t").str.strptime(pl.Datetime("us", "UTC"), TIMESTAMP_FORMAT, strict=False),
        pl.col("mmsi").cast(pl.Int64, strict=False),
        *[pl.col(c).cast(pl.Float64, strict=False) for c in FLOAT_COLS],
    )


def ingest_file(src: Path, out_dir: Path, source_cfg: dict, boxes: list[dict]) -> dict:
    """Convert one Marine Cadastre daily file (.csv.zst or .csv) to a region-filtered interim Parquet file."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.name.split('.')[0]}.parquet"
    keep = [{"A": "Class A", "B": "Class B"}.get(t, t) for t in source_cfg["keep_transceivers"]]
    with tempfile.TemporaryDirectory(dir=out_dir) as tmp:
        if src.suffix == ".zst":
            csv_path = Path(tmp) / "extracted.csv"
            with src.open("rb") as fin, csv_path.open("wb") as fout:
                with zstandard.ZstdDecompressor().stream_reader(fin) as reader:
                    shutil.copyfileobj(reader, fout, length=16 * 1024 * 1024)
        else:
            csv_path = src
        df = filter_aoi(scan_marinecadastre_csv(csv_path), boxes, keep).collect()
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
