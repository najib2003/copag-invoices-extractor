from __future__ import annotations
from pathlib import Path

def count_pdf_pages(pdf_path: str |Path) -> int:
    import fitz
    with fitz.open(str(pdf_path)) as document:
        return document.page_count