from __future__ import annotations
from pathlib import Path
from typing import Any

def load_image_array(path: str | Path) -> Any:
    import cv2

    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return image


def save_image(path: str | Path, image: Any) -> Path:
    import cv2

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(target), image):
        raise ValueError(f"Could not write image: {target}")
    return target