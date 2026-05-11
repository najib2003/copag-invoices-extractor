from __future__ import annotations
import re
import unicodedata
from typing import Iterable

def normalize_texte(txt:str) -> str:
    text =unicodedata.normalize("NFKD",txt or "")
    text =txt.encode("ascii","ignore").decode("ascii")
    return re.sub(r"[ \t]+", " ", txt.replace("\xa0", " ")).strip()

def normalize_for_search(text:str) -> str:
    return normalize_texte(text).lower()

def clean_label_value(value: str) ->str:
    value = re.sub(r"^[\s:#\-nNo.]+", "", value or "", flags=re.IGNORECASE)
    return value.strip(" :#-")

def parse_amount(value: object) -> float | None:
    if value is None:
        return None
    text = normalize_texte(str(value))
    text = re.sub(r"[^\d,.\-]", "", text)
    if not text or text in {"-", ".", ","}:
        return None
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None

def amount_candidates(line: str) -> list[float]:
    matches = re.findall(r"[-+]?(?:\d[\d\s.,]*|[.,]\d+)", normalize_texte(line))
    values = [parse_amount(match) for match in matches]
    return [value for value in values if value is not None]


def first_regex_group(patterns: Iterable[str], text: str, flags: int = re.IGNORECASE) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return clean_label_value(match.group(1))
    return None