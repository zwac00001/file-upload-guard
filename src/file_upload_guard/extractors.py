from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ExtractionResult:
    source_type: str
    success: bool
    text: str | None = None
    reason: str | None = None


def _load_pdf_reader():
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ImportError("Missing optional dependency 'pypdf' for PDF extraction") from exc

    return PdfReader


def _load_docx_document():
    try:
        from docx import Document
    except ImportError as exc:
        raise ImportError(
            "Missing optional dependency 'python-docx' for Word extraction"
        ) from exc

    return Document


def _extract_pdf_text(path: Path) -> str:
    PdfReader = _load_pdf_reader()
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def _extract_docx_text(path: Path) -> str:
    Document = _load_docx_document()
    document = Document(str(path))
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs if paragraph.text
    ).strip()


def extract_text_from_path(path: Path) -> ExtractionResult:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        try:
            text = _extract_pdf_text(path)
        except ImportError as exc:
            return ExtractionResult(source_type="pdf", success=False, reason=str(exc))
        if text:
            return ExtractionResult(source_type="pdf", success=True, text=text)
        return ExtractionResult(
            source_type="pdf",
            success=False,
            reason="No extractable text found",
        )

    if suffix == ".docx":
        try:
            text = _extract_docx_text(path)
        except ImportError as exc:
            return ExtractionResult(source_type="docx", success=False, reason=str(exc))
        if text:
            return ExtractionResult(source_type="docx", success=True, text=text)
        return ExtractionResult(
            source_type="docx",
            success=False,
            reason="No extractable text found",
        )

    return ExtractionResult(
        source_type=suffix.lstrip(".") or "unknown",
        success=False,
        reason=f"No extractor available for {suffix or '<no-ext>'}",
    )
