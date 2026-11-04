# Data

`raw/`, `interim/` and `processed/` are git-ignored. Only `manifests/` is committed.

## Getting the DMA files
1. Open https://www.dma.dk/safety-at-sea/navigational-information/ais-data and follow the link to the historical AIS archive.
2. Read and record the terms of use in `docs/03_data_card.md`.
3. Download ONE daily file first (`aisdk-YYYY-MM-DD.zip`, several hundred MB zipped) into `data/raw/`.
4. `uv run morva manifest data/raw/aisdk-YYYY-MM-DD.zip --notes "..."`
5. `uv run morva ingest`. If the header differs from `DMA_COLUMNS` in `src/morva/ingestion/dma.py`, the error will show the real header.

Never edit files in `raw/`.

## Norwegian AIS (Kystverket Historisk AIS, V4)

Orders are placed by hand at https://hais.kystverket.no and arrive as a download link by email. Each zip holds one
Parquet file per day in `position/`, always named `hais_YYYY-MM-DD.snappy.parquet`, whatever the area. To keep
names unique, the folder is split by purpose:

```text
data/raw/no/
  orders/                    every zip exactly as delivered, renamed <order date>_<check|main|test>_<areas>.zip
  checks/                    files from one-day check orders, renamed hais_<day>_check_<areas>.snappy.parquet
  hais_YYYY-MM-DD.snappy.parquet   daily files from the main and test orders: the only files the pipeline reads
```

The `ingest` command reads only the daily files at the top of `data/raw/no/`; `orders/` and `checks/` are never
ingested. Main orders cover every V4 Norwegian area at once (up to 5 areas per order), so each day has one file.

When an order arrives:
1. Save the zip in `data/raw/no/orders/` (any name) and tell Claude, or do the rest by hand:
2. rename it as above and extract its `position/` files to `checks/` (renamed) or to the top level (main and test);
3. write manifests: `uv run morva --data-config configs/v4/data.yaml --exp-config configs/v4/experiment.yaml
   manifest --source kystverket <files> --notes "..."`.

Test-period days (16–29 Oct 2026) are ordered only after the V4 hypotheses are frozen.
