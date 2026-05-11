"""Recipient (DESTINATAIRE) name extraction from labeled invoice headers."""

from __future__ import annotations

import re

from app.constants import MOTS_CLES_DESTINATAIRE, MOTS_IGNORES_DESTINATAIRE
from app.models.ocr_result import OCRResult
from app.utils.regex_utils import normalize_for_search, normalize_text

# Labels that introduce the recipient's name — longest first to avoid prefix shadowing
_SKIP_AS_LABELS = {"monsieur", "madame", "m.", "mme", "mr", "mrs"}
_HEADER_LABELS: list[str] = sorted(
    {normalize_for_search(kw) for kw in MOTS_CLES_DESTINATAIRE if kw not in _SKIP_AS_LABELS},
    key=len,
    reverse=True,
)
# These word prefixes signal that the line itself IS the name (e.g. "M.PIERRE CHAPPELLE")
_NAME_PREFIXES = {"m.", "mme", "mme.", "mr", "mrs", "monsieur", "madame"}

# Table column headers that should never be returned as a recipient name
_TABLE_HEADERS = {"description", "quantite", "quantite", "prix", "total", "montant", "designation"}


def _norm(text: str) -> str:
    """Normalize for comparison: strip accents, lowercase, normalize apostrophes."""
    text = normalize_for_search(text)
    text = re.sub(r"[''ʼ`´]", "'", text)
    return text.strip(" :#-")


class RecipientExtractor:
    def extract(self, ocr_result: OCRResult) -> dict[str, object]:
        lines = ocr_result.sorted_lines()

        for index, line in enumerate(lines[:30]):
            search = _norm(line.text)

            # --- Strategy 1: line starts with a strong DESTINATAIRE label ---
            matched = self._match_label(search)
            if matched is not None:
                # Try to get value on the same line (after the label + separator)
                remainder = re.sub(rf"^{re.escape(matched)}\s*[:#-]?\s*", "", search).strip(" :#-")
                if remainder and self._is_plausible(remainder):
                    # Return original-casing version
                    raw_remainder = re.sub(
                        rf"(?i)^{re.escape(matched)}\s*[:#-]?\s*",
                        "",
                        normalize_text(line.text),
                    ).strip(" :#-")
                    return {
                        "value": raw_remainder or remainder,
                        "confidence": min(line.confidence + 0.15, 1.0),
                        "source": line.text,
                    }

                # Value is on the next line
                if index + 1 < len(lines):
                    next_line = lines[index + 1]
                    value = normalize_text(next_line.text).strip(" :#-")
                    if value and self._is_plausible(_norm(next_line.text)):
                        return {
                            "value": value,
                            "confidence": min(next_line.confidence + 0.10, 1.0),
                            "source": f"{line.text} {next_line.text}",
                        }

            # --- Strategy 2: line begins with a civility prefix (M., Mme, Mr…) ---
            first_word = search.split()[0] if search.split() else ""
            if first_word in _NAME_PREFIXES:
                value = normalize_text(line.text).strip(" :#-")
                if value and self._is_plausible(search):
                    return {"value": value, "confidence": line.confidence, "source": line.text}

        return {"value": None, "confidence": 0.0, "source": ""}

    @staticmethod
    def _match_label(search: str) -> str | None:
        """Return the matched label constant if the line starts with it, else None."""
        for label in _HEADER_LABELS:
            if search == label:
                return label
            # "label :" or "label:" or "label : value"
            if re.match(rf"^{re.escape(label)}\s*[:#-]", search):
                return label
        return None

    @staticmethod
    def _is_plausible(text: str) -> bool:
        if not text or len(text) < 2 or len(text) > 80:
            return False
        norm = normalize_for_search(text)
        # Reject table header words
        if norm in _TABLE_HEADERS:
            return False
        if norm in MOTS_IGNORES_DESTINATAIRE:
            return False
        # Reject emails, phone numbers, pure addresses
        if "@" in text or re.search(r"\d{5,}", text):
            return False
        digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
        return digit_ratio < 0.4
