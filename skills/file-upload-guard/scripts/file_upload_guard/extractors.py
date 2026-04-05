from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docx import Document
from pypdf import PdfReader


@dataclass(slots=True)
class ExtractionResult:
    source_type: str
    success: bool
    text: str | None = None
    reason: str | None = None


def _extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def _extract_docx_text(path: Path) -> str:
    document = Document(str(path))
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs if paragraph.text
    ).strip()


def extract_text_from_path(path: Path) -> ExtractionResult:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = _extract_pdf_text(path)
        if text:
            return ExtractionResult(source_type="pdf", success=True, text=text)
        return ExtractionResult(
            source_type="pdf",
            success=False,
            reason="No extractable text found",
        )

    if suffix == ".docx":
        text = _extract_docx_text(path)
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
