from pathlib import Path

from file_upload_guard.file_page import build_extracted_text_package, build_file_page
from file_upload_guard.protocol import render_extracted_text, render_file_page


def test_build_file_page_returns_requested_page(tmp_path: Path):
    path = tmp_path / "notes.txt"
    path.write_text("alpha\nbeta\ngamma\ndelta\n", encoding="utf-8")

    package = build_file_page(path, page_number=2, page_size=12)
    rendered = render_file_page(package)

    assert f"FILE: {path}" in rendered
    assert "PAGE: 2/2" in rendered
    assert "LINES: 3-4" in rendered
    assert "gamma" in rendered


def test_build_extracted_text_package_uses_extractor_for_docx(tmp_path: Path):
    from docx import Document

    path = tmp_path / "report.docx"
    document = Document()
    document.add_paragraph("Board update")
    document.save(path)

    package = build_extracted_text_package(path)
    rendered = render_extracted_text(package)

    assert "SUCCESS: true" in rendered
    assert "Board update" in rendered
