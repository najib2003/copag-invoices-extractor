from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
 
from app.constants import COLONNES_AUDIT,COLONNES_EXPORT
from app.models.line_item import LineItem

@dataclass
class InvoiceRecord:
    nom_fichier :str
    numero_page :int

    nom_fournisseur: str | None=None
    total_ht : float | None=None
    tva : float | None=None
    ttc : float | None=None
    confiance_ocr: float = 0.0
    statut: str = "en_attente"

    line_items: list[LineItem]=field(default_factory=list)
    notes: list[str] =field(default_factory=list)

    field_confidences: dict[str, float]=field(default_factory=dict)
    metadata: dict[str,Any]=field(default_factory=dict)


    def add_note(self, note:str) -> None:
        if note and note not in self.notes:
            self.notes.append(note)
    
    
    def to_export_rows(self) -> list[dict[str,Any]]:
        if not self.line_items:
            row={
                 "nom_fournisseur": self.nom_fournisseur,
                "prix_unitaire": None,
                "quantite": None,
                "total": None,
                "total_ht": self.total_ht,
                "tva": self.tva,
                "ttc": self.ttc,
            }
            return[
                {column:row.get(column) for column in COLONNES_EXPORT}
            ]
            rows = []

        for line_item in self.line_items:
            row = line_item.to_export_row(
                nom_fournisseur=self.nom_fournisseur,
                total_ht=self.total_ht,
                tva=self.tva,
                ttc=self.ttc,
            )

            rows.append(
                {column: row.get(column) for column in COLONNES_EXPORT}
            )

        return rows


    def to_audit_row(self) -> dict[str, Any]:
        """
        Créer une ligne de contrôle/debug.

        Cette ligne n'est pas forcément l'export final.
        Elle sert à savoir si l'extraction s'est bien passée.
        """

        row = {
            "nom_fichier": self.nom_fichier,
            "numero_page": self.numero_page,
            "confiance_ocr": round(self.confiance_ocr, 4),
            "statut": self.statut,
            "notes": "; ".join(self.notes),
        }

        return {column: row.get(column) for column in COLONNES_AUDIT}

    def to_dict(self) -> dict[str, Any]:
        return {
            "nom_fichier": self.nom_fichier,
            "numero_page": self.numero_page,
            "nom_fournisseur": self.nom_fournisseur,
            "total_ht": self.total_ht,
            "tva": self.tva,
            "ttc": self.ttc,
            "confiance_ocr": round(self.confiance_ocr, 4),
            "statut": self.statut,
            "notes": self.notes,
            "line_items": [line_item.to_dict() for line_item in self.line_items],
            "field_confidences": self.field_confidences,
            "metadata": self.metadata,
        }
