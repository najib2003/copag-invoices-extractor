from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from app.constants import DATA_SUBDIRECTORIES

BASE_DIR = Path(__file__).parent.parent
DATA_DIR =BASE_DIR / "data"

@dataclass(frozen=True)
class AppConfig:
    base_dir: Path=BASE_DIR
    data_dir : Path=DATA_DIR
    upload_dir : Path= DATA_DIR / "uploads"
    rendered_pages_dir : Path = DATA_DIR / "rendered_pages"
    processed_dir : Path = DATA_DIR / "processsd"
    extracted_json_dir : Path =DATA_DIR/ "extracted_json"
    export_dir : Path =DATA_DIR/ "exports"
    temp_dir: Path = DATA_DIR/ "temp"
    log_dir: Path= DATA_DIR / "logs"

    paddle_lang: str ="fr"
    paddle_use_angle_cls: bool=False
    paddle_device: str= "cpu"
    paddle_enable_mkldnn: bool=False
    paddle_cpu_threads: int=4
    paddle_text_detection_model_name: str = "PP-OCRv5_mobile_det"
    paddle_text_recognition_model_name: str = "latin_PP-OCRv5_mobile_rec"
    paddle_text_det_limit_side_len: int = 960
    paddle_text_recognition_batch_size: int = 8
    pdf_render_dpi: int = 180
    ocr_confidence_threshold: float = 0.5
    minimum_ocr_lines: int = 0 #no minimum requirement for how many lines of text must be found 
    fallback_max_variants: int = 1
    default_export_name: str = "copag_invoice_export.xlsx"
    supported_pdf_extensions: set[str] = field(default_factory=lambda: {".pdf"})
    supported_image_extensions: set[str] = field(
        default_factory=lambda: {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
    )

config = AppConfig()


def ensure_data_directories() -> None:
    for directory_name in DATA_SUBDIRECTORIES:
        (config.data_dir / directory_name).mkdir(parents=True,exist_ok=True)