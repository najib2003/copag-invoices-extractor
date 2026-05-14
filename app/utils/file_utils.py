from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


def safe_filename(name: str) -> str:
    """Return a filesystem-safe filename."""

    cleaned = re.sub(r"\s+", "_", name.strip())
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "", cleaned)
    cleaned = cleaned.strip("._")
    return cleaned or "file"


def timestamp_slug() -> str:
    """Return a sortable timestamp including microseconds."""

    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def copy_to_uploads(
    input_path: Path,
    upload_dir: Path | None = None,
    output_name: str | None = None,
) -> Path:
    """Copy a file into the upload directory and return the destination path."""

    destination_dir = upload_dir or Path("data") / "uploads"
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / (output_name or safe_filename(input_path.name))
    ensure_parent(destination)
    shutil.copy2(input_path, destination)
    return destination

