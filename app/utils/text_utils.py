from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize text for comparison without changing the OCR source text."""

    normalized = text.replace("\u00a0", " ")
    normalized = unicodedata.normalize("NFKC", normalized)
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n\s+", "\n", normalized)
    return normalized.strip()
