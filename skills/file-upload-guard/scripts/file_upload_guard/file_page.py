from __future__ import annotations

from pathlib import Path

from file_upload_guard.extractors import extract_text_from_path
from file_upload_guard.io_utils import paginate_text, read_text_file
from file_upload_guard.protocol import ExtractedTextPackage, FilePagePackage


TEXT_EXTRACT_SUFFIXES = {".pdf", ".docx"}


def build_extracted_text_package(path: Path) -> ExtractedTextPackage:
    result = extract_text_from_path(path)
    return ExtractedTextPackage(
        path=str(path),
        source_type=result.source_type,
        success=result.success,
        text=result.text,
        reason=result.reason,
    )


def _text_for_paging(path: Path) -> str:
    if path.suffix.lower() in TEXT_EXTRACT_SUFFIXES:
        result = extract_text_from_path(path)
        if not result.success or result.text is None:
            raise ValueError(result.reason or f"Failed to extract text from {path}")
        return result.text

    text, _ = read_text_file(path)
    return text


def build_file_page(path: Path, page_number: int, page_size: int = 7000) -> FilePagePackage:
    text = _text_for_paging(path)
    pages = paginate_text(text, page_size=page_size)

    if page_number < 1 or page_number > len(pages):
        raise IndexError(f"Requested page {page_number} outside range 1-{len(pages)}")

    page = pages[page_number - 1]

    return FilePagePackage(
        path=str(path),
        page_number=page.page_number,
        total_pages=page.total_pages,
        line_start=page.line_start,
        line_end=page.line_end,
        char_start=page.char_start,
        char_end=page.char_end,
        truncated=page.total_pages > 1,
        content=page.content,
    )
