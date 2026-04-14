from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


TEXT_ENCODINGS = ("utf-8", "utf-8-sig", "gb18030", "cp1252", "utf-16")


@dataclass(slots=True)
class TextPage:
    page_number: int
    total_pages: int
    line_start: int
    line_end: int
    char_start: int
    char_end: int
    content: str


def is_probably_binary(raw: bytes) -> bool:
    if not raw:
        return False
    if b"\x00" in raw:
        return True

    sample = raw[:1024]
    non_text_bytes = sum(byte < 9 or 13 < byte < 32 for byte in sample)
    return non_text_bytes / max(len(sample), 1) > 0.30


def read_text_file(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    if is_probably_binary(raw):
        raise ValueError(f"{path} appears to be binary")

    for encoding in TEXT_ENCODINGS:
        try:
            text = raw.decode(encoding).replace("\r\n", "\n").replace("\r", "\n")
            return text, encoding
        except UnicodeDecodeError:
            continue

    raise ValueError(f"{path} could not be decoded with the supported encodings")


def paginate_text(text: str, page_size: int = 7000) -> list[TextPage]:
    lines = text.splitlines(keepends=True) or [text]
    pages: list[TextPage] = []
    buffer: list[str] = []
    char_start = 0
    line_start = 1
    current_chars = 0

    for index, line in enumerate(lines, start=1):
        if buffer and current_chars + len(line) > page_size:
            content = "".join(buffer)
            pages.append(
                TextPage(
                    page_number=len(pages) + 1,
                    total_pages=0,
                    line_start=line_start,
                    line_end=index - 1,
                    char_start=char_start,
                    char_end=char_start + len(content),
                    content=content,
                )
            )
            char_start += len(content)
            line_start = index
            buffer = []
            current_chars = 0

        buffer.append(line)
        current_chars += len(line)

    if buffer:
        content = "".join(buffer)
        pages.append(
            TextPage(
                page_number=len(pages) + 1,
                total_pages=0,
                line_start=line_start,
                line_end=len(lines),
                char_start=char_start,
                char_end=char_start + len(content),
                content=content,
            )
        )

    total_pages = len(pages)
    for page in pages:
        page.total_pages = total_pages

    return pages
