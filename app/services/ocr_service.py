from __future__ import annotations
import os
from collections.abc import Mapping
from pathlib import Path
from typing  import Any

from app.config import config
from app.models.ocr_line import OCRLine
from app.models.ocr_result import OCRResult


class OCRService:
    def __init__(
            self,
            lang:str | None =None,
            use_angle_cls: bool | None =None,
            ocr_engine:Any | None =None,
            **Kwargs :Any,
    ) -> None :
        self.lang = lang or config.paddle_lang
        self.use_angle_cls = config.paddle_use_angle_cls if use_angle_cls is None else use_angle_cls
        self.kwargs = Kwargs
        self._ocr:Any | None = ocr_engine
        self._configure_paddle_environment()

    @property
    def engine(self) -> Any:
        if self._ocr is None:
            try:
                self._ocr=self._build_engine()
            except ImportError as exc:
                raise RuntimeError(
                    "PaddleOCR is required for OCR. Install requirements.txt before processing invoices."
                ) from exc
        return self._ocr

    def extract_image(self, image_path:str |Path,page_number:int=1, source: str = "original") -> OCRResult:
        path=Path(image_path)
        raw_result = self._run_engine(path)
        lines = [
            OCRLine(text=text.strip(), confidence=confidence, bbox=box, page_number=page_number, source=source)
            for box, text, confidence in self._iter_ocr_lines(raw_result)
            if text and text.strip()
        ]
        return OCRResult(
            lines=lines,
            source=source,
            image_path=path,
            page_number=page_number,
            metadata={"engine": "PaddleOCR", "raw_line_count": len(lines)},
        )
    
    def _build_engine(self) ->Any:
        from paddleocr import PaddleOCR
        try:
            return PaddleOCR(
                lang=self.lang,
                device=config.paddle_device,
                enable_mkldnn=config.paddle_enable_mkldnn,
                cpu_threads=config.paddle_cpu_threads,
                enable_hpi=False,
                text_detection_model_name=config.paddle_text_detection_model_name,
                text_recognition_model_name=config.paddle_text_recognition_model_name,
                text_det_limit_side_len=config.paddle_text_det_limit_side_len,
                text_recognition_batch_size=config.paddle_text_recognition_batch_size,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=self.use_angle_cls,
                **self.kwargs,
            )
        except Exception:
            return PaddleOCR(
                lang=self.lang,
                use_angle_cls=self.use_angle_cls,
                enable_mkldnn=config.paddle_enable_mkldnn,
                cpu_threads=config.paddle_cpu_threads,
                **self.kwargs,
            )
    def _run_engine(self, path: Path) -> Any:
        if hasattr(self.engine, "predict"):
            return self.engine.predict(str(path))
        return self.engine.ocr(str(path), cls=self.use_angle_cls)

    def _iter_ocr_lines(self, result: Any):
        if result is None:
            return

        if self._looks_like_paddleocr_v3_result(result):
            yield from self._iter_paddleocr_v3_lines(result)
            return

        if isinstance(result, tuple):
            result = list(result)

        if not isinstance(result, list):
            return

        for entry in result:
            if self._looks_like_ocr_line(entry):
                box = self._coerce_box(entry[0])
                text = str(entry[1][0])
                confidence = float(entry[1][1] or 0.0)
                yield box, text, confidence
            elif isinstance(entry, (list, tuple)):
                yield from self._iter_ocr_lines(entry)

    @staticmethod
    def _looks_like_ocr_line(entry: Any) -> bool:
        return (
            isinstance(entry, (list, tuple))
            and len(entry) >= 2
            and isinstance(entry[1], (list, tuple))
            and len(entry[1]) >= 2
            and isinstance(entry[1][0], str)
        )

    @staticmethod
    def _looks_like_paddleocr_v3_result(result: Any) -> bool:
        items = result if isinstance(result, (list, tuple)) else [result]
        return any(OCRService._paddleocr_v3_data(item) is not None for item in items)

    def _iter_paddleocr_v3_lines(self, result: Any):
        items = result if isinstance(result, (list, tuple)) else [result]
        for item in items:
            data = self._paddleocr_v3_data(item)
            if not isinstance(data, Mapping):
                continue

            texts = self._to_list(self._first_present(data, "rec_texts", "texts"))
            scores = self._to_list(self._first_present(data, "rec_scores", "scores"))
            polys = self._to_list(self._first_present(data, "rec_polys", "dt_polys"))
            texts = texts if texts is not None else []
            scores = scores if scores is not None else []
            polys = polys if polys is not None else []

            for index, text in enumerate(texts):
                confidence = float(scores[index]) if index < len(scores) else 0.0
                box = self._coerce_box(polys[index]) if index < len(polys) else None
                yield box, str(text), confidence

    @staticmethod
    def _paddleocr_v3_data(item: Any) -> Mapping[str, Any] | None:
        data = getattr(item, "res", None)
        if isinstance(data, Mapping):
            return data

        if isinstance(item, Mapping):
            nested = item.get("res")
            if isinstance(nested, Mapping):
                return nested
            if OCRService._has_paddleocr_v3_line_keys(item):
                return item

        json_data = getattr(item, "json", None)
        if callable(json_data):
            json_data = json_data()
        if isinstance(json_data, Mapping):
            nested = json_data.get("res")
            if isinstance(nested, Mapping):
                return nested
            if OCRService._has_paddleocr_v3_line_keys(json_data):
                return json_data

        return None

    @staticmethod
    def _has_paddleocr_v3_line_keys(data: Mapping[str, Any]) -> bool:
        return any(key in data for key in ("rec_texts", "texts", "rec_scores", "scores", "rec_polys", "dt_polys"))

    @staticmethod
    def _coerce_box(raw_box: Any) -> list[list[float]] | None:
        raw_box = OCRService._to_list(raw_box)
        if not isinstance(raw_box, (list, tuple)):
            return None
        box: list[list[float]] = []
        for point in raw_box:
            if isinstance(point, (list, tuple)) and len(point) >= 2:
                box.append([float(point[0]), float(point[1])])
        return box or None

    @staticmethod
    def _to_list(value: Any) -> Any:
        if hasattr(value, "tolist"):
            return value.tolist()
        return value

    @staticmethod
    def _first_present(data: dict[str, Any], *keys: str) -> Any:
        for key in keys:
            if key in data and data[key] is not None:
                return data[key]
        return None

    @staticmethod
    def _configure_paddle_environment() -> None:
        # PaddleOCR 3.x on Windows can hit a Paddle/oneDNN runtime error on
        # some CPU builds. Keep CPU inference on the plain Paddle path by
        # default; this is slower but more reliable for an offline business tool.
        if not config.paddle_enable_mkldnn:
            os.environ.setdefault("FLAGS_use_mkldnn", "0")
        os.environ.setdefault("OMP_NUM_THREADS", str(config.paddle_cpu_threads))
    