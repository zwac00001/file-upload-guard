from pathlib import Path

from file_upload_guard.file_summary import build_file_summary
from file_upload_guard.protocol import render_file_summary


def test_build_file_summary_extracts_python_structure(tmp_path: Path):
    path = tmp_path / "service.py"
    path.write_text(
        "import os\n\n"
        "def run_job(name: str) -> str:\n"
        "    return name.upper()\n",
        encoding="utf-8",
    )

    package = build_file_summary(path)
    rendered = render_file_summary(package)

    assert f"FILE: {path}" in rendered
    assert "TYPE: text/x-python" in rendered
    assert "run_job" in rendered
    assert "import os" in rendered


def test_build_file_summary_falls_back_to_metadata_for_binary_files(tmp_path: Path):
    path = tmp_path / "image.bin"
    path.write_bytes(b"\x00\x01\x02\x03")

    package = build_file_summary(path)

    assert package.metadata_only is True
    assert "Binary file" in package.structure_lines[0]
