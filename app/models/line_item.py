from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class LineItem:
    prix_unitaire : float | None=None
    quantite : float | None=None
    total :float | None=None
    confidence : float =0.0
    source : str=""

    def to_export_row(
            self,
            nom_fournisseur: str | None=None,
            total_ht: float | None = None,
        tva: float | None = None,
        ttc: float | None = None,
    ) -> dict[str, Any]:
        return {
            "nom_fournisseur": nom_fournisseur,
            "prix_unitaire": self.prix_unitaire,
            "quantite": self.quantite,
            "total": self.total,
            "total_ht": total_ht,
            "tva": tva,
            "ttc": ttc,
        }

    def to_dict(self) -> dict[str ,Any]:
        return{
            "prix_unitaire": self.prix_unitaire,
            "quantite": self.quantite,
            "total": self.total,
            "confidence": self.confidence,
            "source": self.source,
        }
    