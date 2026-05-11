from __future__ import annotations
from typing import Iterable
from app.constants import COLONNES_EXPORT
from app.models.invoice_record import InvoiceRecord


def records_to_dataframe(records:Iterable[InvoiceRecord]):
    import pandas as pd

    rows=[ row for record in records for row in record.to_export_rows()]
    return pd.DataFrame(rows, columns=COLONNES_EXPORT)