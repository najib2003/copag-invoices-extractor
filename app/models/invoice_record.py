from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.models.line_item import LineItem


@dataclass(slots=True)
class InvoiceRecord:
    pdf_file_name: str | None = None
    page_number: int | None = None
    nom_destinataire: str | None = None
    nom_fournisseur: str | None = None
    numero_facture: str | None = None
    date_facture: str | None = None
    total_ht: float | None = None
    tva: float | None = None
    ttc: float | None = None
    currency: str | None = None
    line_items: list[LineItem | dict[str, Any]] = field(default_factory=list)
    ocr_confidence: float | None = None
    status: str = "ok"
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = [
            item.to_dict() if isinstance(item, LineItem) else dict(item)
            for item in self.line_items
        ]
        return {
            "pdf_file_name": self.pdf_file_name,
            "page_number": self.page_number,
            "nom_destinataire": self.nom_destinataire,
            "nom_fournisseur": self.nom_fournisseur,
            "numero_facture": self.numero_facture,
            "date_facture": self.date_facture,
            "total_ht": self.total_ht,
            "tva": self.tva,
            "ttc": self.ttc,
            "currency": self.currency,
            "line_items": items,
            "ocr_confidence": self.ocr_confidence,
            "status": self.status,
            "notes": self.notes,
            "metadata": self.metadata,
        }
