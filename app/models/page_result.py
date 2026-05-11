from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.models.extraction_result import ExtractionResult
from app.models.ocr_result import OCRResult


@dataclass
class PageResult:
    page_number: int
    image_path: Path
    original_ocr: OCRResult
    selected_ocr: OCRResult
    extraction_result: ExtractionResult
    fallback_results: list[OCRResult] = field(default_factory=list)
    fallback_used: bool = False
    status: str = "pending"
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def record(self):
        return self.extraction_result.record

    def add_note(self, note: str) -> None:
        if not note:
            return

        if note not in self.notes:
            self.notes.append(note)

        self.extraction_result.add_note(note)

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "image_path": str(self.image_path),
            "original_ocr": self.original_ocr.to_dict(),
            "selected_ocr": self.selected_ocr.to_dict(),
            "fallback_used": self.fallback_used,
            "fallback_results": [result.to_dict() for result in self.fallback_results],
            "extraction_result": self.extraction_result.to_dict(),
            "status": self.status,
            "notes": self.notes,
            "metadata": self.metadata,
        }
