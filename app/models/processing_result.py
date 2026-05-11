from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models.invoice_record import InvoiceRecord
from app.models.page_result import PageResult


@dataclass
class ProcessingResult:
    input_file: Path
    pages: list[PageResult] = field(default_factory=list)
    export_path: Path | None = None
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def invoices(self) -> list[InvoiceRecord]:
        return [page.record for page in self.pages]

    def finish(self) -> None:
        self.finished_at = datetime.now()

    def summary(self) -> dict[str, Any]:
        records = self.invoices
        review_count = sum(1 for record in records if record.statut != "ok")
        fallback_count = sum(1 for page in self.pages if page.fallback_used)

        return {
            "input_file": self.input_file.name,
            "invoice_count": len(records),
            "review_count": review_count,
            "fallback_count": fallback_count,
            "export_path": str(self.export_path) if self.export_path else None,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_file": str(self.input_file),
            "export_path": str(self.export_path) if self.export_path else None,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "summary": self.summary(),
            "pages": [page.to_dict() for page in self.pages],
            "metadata": self.metadata,
        }
