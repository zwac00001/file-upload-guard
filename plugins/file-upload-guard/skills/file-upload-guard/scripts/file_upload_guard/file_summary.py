from __future__ import annotations

import mimetypes
import re
from pathlib import Path

from file_upload_guard.io_utils import read_text_file
from file_upload_guard.protocol import FileSummaryPackage


PYTHON_DEF_RE = re.compile(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.MULTILINE)
PYTHON_CLASS_RE = re.compile(r"^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.MULTILINE)


def _guess_source_type(path: Path, metadata_only: bool) -> str:
    if path.suffix.lower() == ".py":
        return "text/x-python"
    guessed, _ = mimetypes.guess_type(path.name)
    if guessed:
        return guessed
    return "application/octet-stream" if metadata_only else "text/plain"


def _preview(text: str, preview_lines: int) -> str:
    return "\n".join(text.splitlines()[:preview_lines])


def _python_structure(text: str) -> list[str]:
    structure: list[str] = []
    imports = [
        line.strip()
        for line in text.splitlines()
        if line.startswith(("import ", "from "))
    ]
    structure.extend(imports[:5])
    structure.extend(f"def {name}" for name in PYTHON_DEF_RE.findall(text))
    structure.extend(f"class {name}" for name in PYTHON_CLASS_RE.findall(text))
    return structure or ["No top-level symbols detected"]


def _generic_structure(path: Path, text: str) -> list[str]:
    if path.suffix.lower() == ".md":
        headings = [line.strip() for line in text.splitlines() if line.startswith("#")]
        return headings[:8] or ["No headings detected"]
    return ["Plain text content"]


def build_file_summary(path: Path, preview_lines: int = 12) -> FileSummaryPackage:
    size_bytes = path.stat().st_size

    try:
        text, encoding = read_text_file(path)
    except ValueError:
        return FileSummaryPackage(
            path=str(path),
            source_type=_guess_source_type(path, metadata_only=True),
            size_bytes=size_bytes,
            line_count=None,
            encoding=None,
            preview="",
            structure_lines=[f"Binary file: content withheld for {path.name}"],
            metadata_only=True,
        )

    structure = (
        _python_structure(text)
        if path.suffix.lower() == ".py"
        else _generic_structure(path, text)
    )

    return FileSummaryPackage(
        path=str(path),
        source_type=_guess_source_type(path, metadata_only=False),
        size_bytes=size_bytes,
        line_count=len(text.splitlines()),
        encoding=encoding,
        preview=_preview(text, preview_lines),
        structure_lines=structure,
    )
