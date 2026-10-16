"""Dataset manifests: provenance record for every raw file (committed to git)."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def sha256(path: Path, chunk: int = 16 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def write_manifest(raw_file: Path, manifest_dir: Path, provider: str, url: str, notes: str = "") -> Path:
    manifest_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "file": raw_file.name,
        "provider": provider,
        "source_url": url,
        "size_bytes": raw_file.stat().st_size,
        "sha256": sha256(raw_file),
        "recorded_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "license_note": "Check provider terms before redistribution. Raw data is not committed.",
        "notes": notes,
    }
    out = manifest_dir / f"{raw_file.name}.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    return out
