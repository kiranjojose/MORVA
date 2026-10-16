"""Config loading. Configs are plain YAML so every run is reproducible from files in git."""

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    with path.open() as f:
        return yaml.safe_load(f)


def project_path(relative: str | Path) -> Path:
    p = Path(relative)
    return p if p.is_absolute() else PROJECT_ROOT / p
