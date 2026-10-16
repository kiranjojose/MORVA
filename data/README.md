# Data

`raw/`, `interim/` and `processed/` are git-ignored. Only `manifests/` is committed.

## Getting the DMA files
1. Open https://www.dma.dk/safety-at-sea/navigational-information/ais-data and follow the link to the historical AIS archive.
2. Read and record the terms of use in `docs/03_data_card.md`.
3. Download ONE daily file first (`aisdk-YYYY-MM-DD.zip`, several hundred MB zipped) into `data/raw/`.
4. `uv run morva manifest data/raw/aisdk-YYYY-MM-DD.zip --notes "..."`
5. `uv run morva ingest`. If the header differs from `DMA_COLUMNS` in `src/morva/ingestion/dma.py`, the error will show the real header.

Never edit files in `raw/`.
