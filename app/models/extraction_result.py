from __future__ import annotations
from dataclasses import dataclass ,field
from typing import Any
from app.models.invoice_record import InvoiceRecord


@dataclass
class ExtractionResult:
    record: InvoiceRecord

    sources_champs:dict[str,str]=field(default_factory=dict)
    champs_manquants: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def confiances_champs(self) -> dict[str,float]:
        return self.record.field_confidences
    @property
    def confiance_moyenne_champs(self) -> float :
        values=[value for value in self.confiances_champs.values() if value is not None]
        if not values:
            return 0.0
        return sum(values)/len(values)
    
    def add_note(self, note: str) -> None:
       
            if not note:
                return

            if note not in self.notes:
                self.notes.append(note)

            self.record.add_note(note)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "record": self.record.to_dict(),
            "sources_champs": self.sources_champs,
            "champs_manquants": self.champs_manquants,
            "notes": self.notes,
            "confiance_moyenne_champs": round(self.confiance_moyenne_champs, 4),
            "metadata": self.metadata,
        }
