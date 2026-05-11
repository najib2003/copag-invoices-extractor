from __future__ import annotations
from pathlib import Path
from app.utils.file_utils import copy_to_uploads, is_image,is_pdf


class IngestionService:
    def is_supported(self, input_path:str|Path) -> bool:
        return is_pdf(input_path) or is_image(input_path)
    
    def detect_type(self, input_path: str | Path) -> str:
        path = Path(input_path)
        if is_pdf(path):
            return "pdf"
        if is_image(path):
            return "image"
        raise ValueError(f"Unsupported input file type: {path.suffix}")

    def prepare_input(self, input_path: str | Path, copy_to_local_uploads: bool = False) -> Path:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        if not self.is_supported(path):
            raise ValueError(f"Unsupported input file type: {path.suffix}")
        return copy_to_uploads(path) if copy_to_local_uploads else path
