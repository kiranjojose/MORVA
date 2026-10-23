"""Data sources and regions from the data configuration.

V1/V2 configs have one `source` (DMA) and every region uses it. V3 configs list several `sources` by name, and each
region names its `source` and its split `calendar`.
"""


def sources(data_cfg: dict) -> dict[str, dict]:
    """Source name -> source config (with `format` and `raw`)."""
    if "sources" in data_cfg:
        return data_cfg["sources"]
    return {"dma": {**data_cfg["source"], "format": "dma", "raw": data_cfg["paths"]["raw"]}}


def regions(data_cfg: dict) -> list[dict]:
    """Home AOI first, then the transfer waterways, each with its `source`. Boxes must not overlap."""
    default = next(iter(sources(data_cfg)))
    return [{"source": default, **r} for r in (data_cfg["aoi"], *data_cfg.get("transfer_aois", []))]
