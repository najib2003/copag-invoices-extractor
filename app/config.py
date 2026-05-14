from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(slots=True)
class AppConfig:
    base_dir: Path = field(default_factory=_project_root)
    data_dir: Path | None = None
    upload_dir: Path | None = None
    rendered_pages_dir: Path | None = None
    ocr_text_dir: Path | None = None
    extracted_json_dir: Path | None = None
    export_dir: Path | None = None
    log_dir: Path | None = None
    temp_dir: Path | None = None
    processed_dir: Path | None = None
    pdf_dpi: int = 300
    image_format: str = "png"
    paddle_lang: str = "fr"
    paddle_use_angle_cls: bool = True
    llm_model_name: str = "qwen2.5:7b"
    llm_base_url: str = "http://localhost:11434"
    llm_timeout_seconds: int = 600

    def __post_init__(self) -> None:
        self.base_dir = Path(self.base_dir)
        self.data_dir = Path(self.data_dir) if self.data_dir else self.base_dir / "data"
        self.upload_dir = Path(self.upload_dir) if self.upload_dir else self.data_dir / "uploads"
        self.rendered_pages_dir = (
            Path(self.rendered_pages_dir)
            if self.rendered_pages_dir
            else self.data_dir / "rendered_pages"
        )
        self.ocr_text_dir = Path(self.ocr_text_dir) if self.ocr_text_dir else self.data_dir / "ocr_text"
        self.extracted_json_dir = (
            Path(self.extracted_json_dir)
            if self.extracted_json_dir
            else self.data_dir / "extracted_json"
        )
        self.export_dir = Path(self.export_dir) if self.export_dir else self.data_dir / "exports"
        self.log_dir = Path(self.log_dir) if self.log_dir else self.data_dir / "logs"
        self.temp_dir = Path(self.temp_dir) if self.temp_dir else self.data_dir / "temp"
        self.processed_dir = (
            Path(self.processed_dir)
            if self.processed_dir
            else self.data_dir / "processed"
        )
        self.llm_model_name = os.getenv("OLLAMA_MODEL", self.llm_model_name)
        self.llm_base_url = os.getenv("OLLAMA_BASE_URL", self.llm_base_url)
        self.llm_timeout_seconds = _env_int("OLLAMA_TIMEOUT_SECONDS", self.llm_timeout_seconds)


def ensure_data_directories(config: AppConfig | None = None) -> None:
    """Create all data folders required by the pipeline."""

    cfg = config or AppConfig()
    for directory in (
        cfg.upload_dir,
        cfg.rendered_pages_dir,
        cfg.ocr_text_dir,
        cfg.extracted_json_dir,
        cfg.export_dir,
        cfg.log_dir,
        cfg.temp_dir,
        cfg.processed_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)


DEFAULT_CONFIG = AppConfig()
