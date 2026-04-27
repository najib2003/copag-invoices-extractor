from dataclasses import dataclass
from typing import Any

@dataclass
class OCRLine:
    text: str
    confidence : float
    bbox :  list[list[float]] | None = None
    page_number :int | None =None
    source :str= "original"


    @property
    def top(self) -> float :
        if not self.bbox:
            return 0.0
        return min(point[1] for point in self.bbox if len(point) >=2)
    
    @property
    def left(self) -> float:
        if not self.bbox:
            return 0.0
        return min(point[0] for point in self.bbox if len(point) >=2)
    
    def to_dict(self) ->dict[str,Any]:
        return{
            "text": self.text ,
            "confidence": self.confidence,
            "bbox" :self.bbox,
            "page_number":self.page_number,
            "source": self.source,
        }