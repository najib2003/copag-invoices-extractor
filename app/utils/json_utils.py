from __future__ import annotations

import json
from pathlib import Path

from app.utils.file_utils import ensure_parent


def save_json(data: dict, path: Path) -> Path:
    ensure_parent(path)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

