from pathlib import Path

from docx import Document

from file_upload_guard.extractors import extract_text_from_path


def test_extract_text_from_docx_reads_paragraphs(tmp_path: Path):
    path = tmp_path / "report.docx"
    document = Document()
    document.add_paragraph("Quarterly report")
    document.add_paragraph("Revenue increased")
    document.save(path)

    result = extract_text_from_path(path)

    assert result.success is True
    assert "Quarterly report" in result.text
    assert "Revenue increased" in result.text


def test_extract_text_from_unknown_suffix_reports_failure(tmp_path: Path):
    path = tmp_path / "archive.zip"
    path.write_bytes(b"PK\x03\x04")

    result = extract_text_from_path(path)

    assert result.success is False
    assert result.reason == "No extractor available for .zip"
