from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class OCRLine:
    text: str
    confidence: float
    bbox: list[list[float]] | None = None
    page_number: int | None = None
    source: str = "original"

    @property
    def top(self) -> float:
        if not self.bbox:
            return 0.0
        values = [point[1] for point in self.bbox if len(point) >= 2]
        return min(values) if values else 0.0

    @property
    def left(self) -> float:
        if not self.bbox:
            return 0.0
        values = [point[0] for point in self.bbox if len(point) >= 2]
        return min(values) if values else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "page_number": self.page_number,
            "source": self.source,
        }