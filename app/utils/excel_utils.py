from __future__ import annotations
from pathlib import Path

def autosize_columns(path:str | Path) -> None:
    from openpyxl import load_workbook
    workbook=load_workbook(path)
    for sheet in workbook.worksheets:
        for column_cells in sheet.columns:
            values=[str(cell.value) for cell in column_cells if cell.value is not None]
            if not values:
                continue
            width=min(max(len(value) for value in values) + 2, 48)
            sheet.column_dimensions[column_cells[0].column_letter].width = width
        workbook.save(path)