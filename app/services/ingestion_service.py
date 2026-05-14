from __future__ import annotations

import logging
from pathlib import Path

from app.config import AppConfig
from app.constants import SUPPORTED_EXTENSIONS
from app.utils.file_utils import copy_to_uploads, safe_filename, timestamp_slug

MAX_UPLOAD_STEM_LENGTH = 80


class IngestionService:
    """Validate and copy source documents into the uploads folder."""

    def __init__(self, config: AppConfig | None = None, logger: logging.Logger | None = None) -> None:
        self.config = config or AppConfig()
        self.logger = logger or logging.getLogger(__name__)

    def ingest(self, input_path: Path) -> Path:
        source = Path(input_path).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(f"Input file does not exist: {source}")
        if not source.is_file():
            raise ValueError(f"Input path is not a file: {source}")

        suffix = source.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ValueError(f"Unsupported file extension '{suffix}'. Supported: {supported}")

        safe_stem = safe_filename(source.stem)[:MAX_UPLOAD_STEM_LENGTH].rstrip("._-") or "file"
        uploaded_name = f"{safe_stem}_{timestamp_slug()}{suffix}"
        uploaded_path = copy_to_uploads(source, self.config.upload_dir, uploaded_name)
        self.logger.info("file uploaded: %s", uploaded_path)
        return uploaded_path
