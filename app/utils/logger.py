

from __future__ import annotations

import logging
from pathlib import Path

from app.config import config, ensure_data_directories


LOGGER_NAME = "copag_receipt_system"


def setup_logger(level: int = logging.INFO, log_file: Path | None = None) -> logging.Logger:
    ensure_data_directories()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_file or config.log_dir / "app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or LOGGER_NAME)

