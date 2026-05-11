"""Filesystem helpers for local-only batch processing."""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

from app.config import config, ensure_data_directories


def safe_filename(name: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return stem.strip("._") or "file"


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def timestamped_dir(base: Path, prefix: str) -> Path:
    directory = base / f"{safe_filename(prefix)}_{timestamp_slug()}"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def copy_to_uploads(input_path: str | Path) -> Path:
    ensure_data_directories()
    source = Path(input_path)
    target = config.upload_dir / f"{source.stem}_{timestamp_slug()}{source.suffix.lower()}"
    shutil.copy2(source, target)
    return target


def is_pdf(path: str | Path) -> bool:
    return Path(path).suffix.lower() in config.supported_pdf_extensions


def is_image(path: str | Path) -> bool:
    return Path(path).suffix.lower() in config.supported_image_extensions

