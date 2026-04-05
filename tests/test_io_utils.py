from pathlib import Path

from file_upload_guard.io_utils import is_probably_binary, paginate_text, read_text_file


def test_is_probably_binary_flags_null_bytes():
    assert is_probably_binary(b"\x00\x01hello") is True


def test_read_text_file_falls_back_to_cp1252(tmp_path: Path):
    path = tmp_path / "notes.txt"
    path.write_bytes(b"caf\xe9")

    text, encoding = read_text_file(path)

    assert text == "caf" + "\u00e9"
    assert encoding == "cp1252"


def test_paginate_text_preserves_ranges():
    text = "line1\nline2\nline3\nline4\n"

    pages = paginate_text(text, page_size=12)

    assert len(pages) == 2
    assert pages[0].page_number == 1
    assert pages[0].line_start == 1
    assert pages[0].line_end == 2
    assert pages[1].page_number == 2
    assert pages[1].line_start == 3
    assert pages[1].line_end == 4
