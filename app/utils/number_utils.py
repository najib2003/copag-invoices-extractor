from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from numbers import Real


def safe_float(value) -> float | None:
    """Convert common French/Moroccan numeric strings to float."""

    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, Real):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("\u00a0", " ").replace(" ", "")
    text = re.sub(r"[^0-9,.\-]", "", text)
    if text in {"", "-", ".", ","}:
        return None

    comma_pos = text.rfind(",")
    dot_pos = text.rfind(".")
    if comma_pos != -1 and dot_pos != -1:
        if comma_pos > dot_pos:
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif comma_pos != -1:
        text = text.replace(",", ".")

    try:
        return float(Decimal(text))
    except (InvalidOperation, ValueError):
        return None


def numbers_close(a, b, tolerance: float = 0.05) -> bool:
    first = safe_float(a)
    second = safe_float(b)
    if first is None or second is None:
        return False
    return abs(first - second) <= tolerance

