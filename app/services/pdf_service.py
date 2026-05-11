"""Local PDF rendering with PyMuPDF."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import config
from app.utils.file_utils import timestamped_dir


class PDFRenderError(RuntimeError):
    """Raised when a PDF can be opened but not rendered safely."""


@dataclass(frozen=True)
class PDFInfo:
    path: Path
    page_count: int
    is_encrypted: bool
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "page_count": self.page_count,
            "is_encrypted": self.is_encrypted,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class RenderedPDFPage:
    page_number: int
    image_path: Path
    width: int
    height: int
    dpi: int
    source_pdf: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "image_path": str(self.image_path),
            "width": self.width,
            "height": self.height,
            "dpi": self.dpi,
            "source_pdf": str(self.source_pdf),
        }


class PDFService:
    min_render_dpi = 72
    max_render_dpi = 600

    def render_pdf_to_images(
        self,
        pdf_path: str | Path,
        output_dir: str | Path | None = None,
        dpi: int | None = None,
        pages: Iterable[int] | None = None,
        max_pages: int | None = None,
        password: str | None = None,
    ) -> list[Path]:
        return [
            rendered_page.image_path
            for rendered_page in self.render_pdf_pages(
                pdf_path,
                output_dir=output_dir,
                dpi=dpi,
                pages=pages,
                max_pages=max_pages,
                password=password,
            )
        ]

    def render_pdf_pages(
        self,
        pdf_path: str | Path,
        output_dir: str | Path | None = None,
        dpi: int | None = None,
        pages: Iterable[int] | None = None,
        max_pages: int | None = None,
        password: str | None = None,
    ) -> list[RenderedPDFPage]:
        path = self._validate_pdf_path(pdf_path)
        render_dpi = self._resolve_dpi(dpi)
        fitz = self._import_fitz()

        target_dir = Path(output_dir) if output_dir else timestamped_dir(config.rendered_pages_dir, path.stem)
        target_dir.mkdir(parents=True, exist_ok=True)
        scale = render_dpi / 72
        matrix = fitz.Matrix(scale, scale)
        rendered_pages: list[RenderedPDFPage] = []

        try:
            document = fitz.open(str(path))
        except Exception as exc:
            raise PDFRenderError(f"Could not open PDF: {path}") from exc

        with document:
            self._authenticate_if_needed(document, password, path)
            if document.page_count <= 0:
                raise PDFRenderError(f"PDF has no pages: {path}")
            page_indexes = self._resolve_page_indexes(document.page_count, pages, max_pages)
            for page_index in page_indexes:
                page_number = page_index + 1
                page = document.load_page(page_index)
                pixmap = page.get_pixmap(matrix=matrix, alpha=False)
                image_path = target_dir / f"page_{page_number:04d}.png"
                try:
                    pixmap.save(str(image_path))
                except Exception as exc:
                    raise PDFRenderError(f"Could not render page {page_number} from PDF: {path}") from exc
                rendered_pages.append(
                    RenderedPDFPage(
                        page_number=page_number,
                        image_path=image_path,
                        width=int(getattr(pixmap, "width", 0) or 0),
                        height=int(getattr(pixmap, "height", 0) or 0),
                        dpi=render_dpi,
                        source_pdf=path,
                    )
                )
        return rendered_pages

    def get_pdf_info(self, pdf_path: str | Path, password: str | None = None) -> PDFInfo:
        path = self._validate_pdf_path(pdf_path)
        fitz = self._import_fitz()
        try:
            document = fitz.open(str(path))
        except Exception as exc:
            raise PDFRenderError(f"Could not open PDF: {path}") from exc

        with document:
            self._authenticate_if_needed(document, password, path)
            return PDFInfo(
                path=path,
                page_count=int(document.page_count),
                is_encrypted=bool(getattr(document, "is_encrypted", False)),
                metadata=dict(getattr(document, "metadata", {}) or {}),
            )

    def _validate_pdf_path(self, pdf_path: str | Path) -> Path:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        if path.suffix.lower() not in config.supported_pdf_extensions:
            raise ValueError(f"Unsupported PDF file extension: {path.suffix or '<none>'}")
        if not path.is_file():
            raise ValueError(f"PDF path is not a file: {path}")
        return path

    def _resolve_dpi(self, dpi: int | None) -> int:
        render_dpi = int(config.pdf_render_dpi if dpi is None else dpi)
        if render_dpi < self.min_render_dpi:
            raise ValueError(f"PDF render dpi must be at least {self.min_render_dpi}: {render_dpi}")
        if render_dpi > self.max_render_dpi:
            raise ValueError(f"PDF render dpi must be at most {self.max_render_dpi}: {render_dpi}")
        return render_dpi

    @staticmethod
    def _import_fitz():
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError(
                "PyMuPDF is required for local PDF rendering. Install requirements.txt."
            ) from exc
        return fitz

    @staticmethod
    def _authenticate_if_needed(document, password: str | None, path: Path) -> None:
        needs_password = bool(getattr(document, "needs_pass", False))
        if not needs_password:
            return
        authenticated = document.authenticate(password or "")
        if not authenticated:
            raise PermissionError(f"PDF is encrypted and needs a password: {path}")

    @staticmethod
    def _resolve_page_indexes(
        page_count: int,
        pages: Iterable[int] | None,
        max_pages: int | None,
    ) -> list[int]:
        if pages is None:
            selected = list(range(page_count))
        else:
            selected = []
            seen = set()
            for page_number in pages:
                if not isinstance(page_number, int):
                    raise TypeError(f"PDF page number must be an integer: {page_number!r}")
                if page_number < 1 or page_number > page_count:
                    raise ValueError(f"PDF page number out of range 1..{page_count}: {page_number}")
                page_index = page_number - 1
                if page_index not in seen:
                    seen.add(page_index)
                    selected.append(page_index)

        if max_pages is not None:
            if max_pages < 1:
                raise ValueError(f"max_pages must be at least 1: {max_pages}")
            selected = selected[:max_pages]

        if not selected:
            raise ValueError("No PDF pages selected for rendering")
        return selected
