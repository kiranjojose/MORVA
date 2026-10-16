"""SYNTHETIC DMA-format AIS generator, used only for smoke-testing the pipeline before
real data is available. Output is labelled synthetic and must never appear in results.

Includes deliberate defects the quality stage must catch: SOG sentinel (102.3),
heading sentinel (511), duplicate rows, a position spike, a long reporting gap,
moored vessels and a non-Class-A transmitter.
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl

from morva.geo import KNOT_MS, from_local_xy

TS_FMT = "%d/%m/%Y %H:%M:%S"


def _voyage(rng, mmsi, start, duration_s, report_s, lat0, lon0):
    n = int(duration_s / report_s)
    t = np.arange(n) * report_s + rng.uniform(0, report_s, n) * 0.2
    sog = np.clip(rng.uniform(8, 18) + np.cumsum(rng.normal(0, 0.02, n)), 2, 25)
    # Piecewise turn rate: mostly straight, occasional manoeuvres
    turn = np.zeros(n)
    for _ in range(rng.integers(1, 4)):
        i = rng.integers(0, n)
        turn[i : i + rng.integers(20, 120)] = rng.choice([-1, 1]) * rng.uniform(0.1, 0.6)
    cog = (rng.uniform(0, 360) + np.cumsum(turn * report_s)) % 360
    v = sog * KNOT_MS
    x = np.cumsum(v * np.sin(np.radians(cog)) * report_s)
    y = np.cumsum(v * np.cos(np.radians(cog)) * report_s)
    lat, lon = from_local_xy(x + rng.normal(0, 5, n), y + rng.normal(0, 5, n), lat0, lon0)
    return {
        "t": [start + timedelta(seconds=float(s)) for s in t],
        "mmsi": [mmsi] * n,
        "lat": lat,
        "lon": lon,
        "sog": np.round(sog + rng.normal(0, 0.1, n), 1),
        "cog": np.round((cog + rng.normal(0, 1.0, n)) % 360, 1),
        "heading": np.round(cog) % 360,
    }


def generate(out_csv: Path, n_vessels: int = 40, n_moored: int = 3, seed: int = 7) -> Path:
    rng = np.random.default_rng(seed)
    day = datetime(2025, 1, 1)
    parts = []
    for k in range(n_vessels):
        start = day + timedelta(seconds=float(rng.uniform(0, 18 * 3600)))
        parts.append(
            pl.DataFrame(
                _voyage(rng, 219_000_000 + k, start, rng.uniform(2, 5) * 3600, 10.0,
                        rng.uniform(55.2, 55.8), rng.uniform(10.9, 12.4))
            ).with_columns(
                ship_type=pl.lit(rng.choice(["Cargo", "Tanker", "Passenger", "Fishing"])),
                length=pl.lit(float(rng.integers(30, 300))),
            )
        )
    for k in range(n_moored):
        n = 2000
        t = [day + timedelta(seconds=30.0 * i) for i in range(n)]
        parts.append(pl.DataFrame({
            "t": t, "mmsi": [219_900_000 + k] * n,
            "lat": 55.68 + rng.normal(0, 2e-5, n), "lon": 12.6 + rng.normal(0, 2e-5, n),
            "sog": np.abs(rng.normal(0, 0.1, n)).round(1), "cog": rng.uniform(0, 360, n).round(1),
            "heading": np.full(n, 511.0),
        }).with_columns(ship_type=pl.lit("Cargo"), length=pl.lit(120.0)))

    df = pl.concat(parts, how="diagonal").sort("t")

    # Defects
    df = df.with_columns(
        sog=pl.when(pl.int_range(pl.len()) % 997 == 0).then(102.3).otherwise(pl.col("sog")),
        mobile_type=pl.lit("Class A"),
    )
    spike = df.filter(pl.col("mmsi") == 219_000_001).row(200, named=True)
    df = df.with_columns(
        lat=pl.when((pl.col("mmsi") == 219_000_001) & (pl.col("t") == spike["t"]))
        .then(pl.col("lat") + 0.5).otherwise(pl.col("lat"))
    )
    gap_vessel = df.filter(pl.col("mmsi") == 219_000_002)
    t_mid = gap_vessel["t"][len(gap_vessel) // 2]
    df = df.filter(~((pl.col("mmsi") == 219_000_002)
                     & pl.col("t").is_between(t_mid, t_mid + timedelta(minutes=40))))
    df = pl.concat([df, df.sample(50, seed=seed)])  # duplicates
    base = df.head(20).with_columns(mobile_type=pl.lit("Base Station"), mmsi=pl.lit(2_190_000, pl.Int64))
    df = pl.concat([df, base]).sort("t")

    out = df.select(
        pl.col("t").dt.strftime(TS_FMT).alias("# Timestamp"),
        pl.col("mobile_type").alias("Type of mobile"),
        pl.col("mmsi").alias("MMSI"),
        pl.col("lat").round(6).alias("Latitude"),
        pl.col("lon").round(6).alias("Longitude"),
        pl.lit("Under way using engine").alias("Navigational status"),
        pl.col("sog").alias("SOG"),
        pl.col("cog").alias("COG"),
        pl.col("heading").alias("Heading"),
        pl.lit("Unknown").alias("IMO"),
        pl.col("ship_type").alias("Ship type"),
        (pl.col("length") / 6).round(0).alias("Width"),
        pl.col("length").alias("Length"),
        pl.lit(None, pl.Float64).alias("Draught"),
    )
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out.write_csv(out_csv)
    return out_csv
