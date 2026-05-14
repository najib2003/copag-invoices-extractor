from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class LineItem:
    designation: str | None = None
    qte: float | None = None
    prix: float | None = None
    prix_unitaire_ht: float | None = None
    total: float | None = None
    total_ht: float | None = None
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "designation": self.designation,
            "qte": self.qte,
            "prix": self.prix,
            "prix_unitaire_ht": self.prix_unitaire_ht,
            "total": self.total,
            "total_ht": self.total_ht,
            "confidence": self.confidence,
        }

