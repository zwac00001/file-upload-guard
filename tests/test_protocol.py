from file_upload_guard.protocol import (
    ExtractedTextPackage,
    FilePagePackage,
    render_extracted_text,
    render_file_page,
)


def test_render_file_page_uses_stable_header():
    package = FilePagePackage(
        path="src/app.py",
        page_number=2,
        total_pages=3,
        line_start=21,
        line_end=40,
        char_start=120,
        char_end=240,
        truncated=True,
        content="print('hello')\n",
    )

    rendered = render_file_page(package)

    assert "FILE: src/app.py" in rendered
    assert "PAGE: 2/3" in rendered
    assert "LINES: 21-40" in rendered
    assert "CHARS: 120-240" in rendered
    assert "TRUNCATED: true" in rendered
    assert "CONTENT-BEGIN" in rendered
    assert "CONTENT-END" in rendered


def test_render_extracted_text_reports_failure_without_binary_bytes():
    package = ExtractedTextPackage(
        path="docs/spec.pdf",
        source_type="pdf",
        success=False,
        text=None,
        reason="No extractable text found",
    )

    rendered = render_extracted_text(package)

    assert "SOURCE: docs/spec.pdf" in rendered
    assert "SOURCE-TYPE: pdf" in rendered
    assert "SUCCESS: false" in rendered
    assert "REASON: No extractable text found" in rendered
    assert "ORIGINAL-BINARY-SENT: false" in rendered
