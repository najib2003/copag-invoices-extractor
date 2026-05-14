from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.models.ocr_line import OCRLine


@dataclass(slots=True)
class OCRResult:
    lines: list[OCRLine]
    source: str = "original"
    image_path: Path | None = None
    page_number: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def raw_text(self) -> str:
        return "\n".join(line.text for line in self.sorted_lines())

    @property
    def average_confidence(self) -> float:
        if not self.lines:
            return 0.0
        return sum(line.confidence for line in self.lines) / len(self.lines)

    @property
    def line_count(self) -> int:
        return len(self.lines)

    def sorted_lines(self) -> list[OCRLine]:
        return sorted(self.lines, key=lambda line: (line.top, line.left))

    def to_dict(self) -> dict[str, Any]:
        return {
            "lines": [line.to_dict() for line in self.sorted_lines()],
            "source": self.source,
            "image_path": str(self.image_path) if self.image_path else None,
            "page_number": self.page_number,
            "metadata": self.metadata,
            "raw_text": self.raw_text,
            "average_confidence": self.average_confidence,
            "line_count": self.line_count,
        }

