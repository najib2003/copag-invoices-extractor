
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.models.ocr_line import OCRLine


@dataclass
class OCRResult:
    lines: list[OCRLine] = field(default_factory=list)
    source: str = "original"
    image_path: Path | None = None
    page_number: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def raw_text(self) -> str:
        return "\n".join(line.text for line in self.lines if line.text)

    @property
    def average_confidence(self) -> float:
        if not self.lines:
            return 0.0
        return sum(line.confidence for line in self.lines) / len(self.lines)

    @property
    def line_count(self) -> int:
        return len(self.lines)

    def sorted_lines(self) -> list[OCRLine]:
        return sorted(self.lines, key=lambda line: (line.page_number or 0, line.top, line.left))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "image_path": str(self.image_path) if self.image_path else None,
            "page_number": self.page_number,
            "average_confidence": self.average_confidence,
            "line_count": self.line_count,
            "raw_text": self.raw_text,
            "lines": [line.to_dict() for line in self.lines],
            "metadata": self.metadata,
        }


