from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProjectOverviewPackage:
    root: str
    tree_lines: list[str]
    file_counts: dict[str, int]
    key_files: list[str]
    summaries: dict[str, str]
    errors: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FileSummaryPackage:
    path: str
    source_type: str
    size_bytes: int
    line_count: int | None
    encoding: str | None
    preview: str
    structure_lines: list[str]
    metadata_only: bool = False
    errors: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FilePagePackage:
    path: str
    page_number: int
    total_pages: int
    line_start: int
    line_end: int
    char_start: int
    char_end: int
    truncated: bool
    content: str


@dataclass(slots=True)
class ExtractedTextPackage:
    path: str
    source_type: str
    success: bool
    text: str | None
    reason: str | None


def _render_list(title: str, values: list[str]) -> list[str]:
    lines = [f"{title}:"]
    lines.extend(f"- {value}" for value in values)
    return lines


def _render_mapping(title: str, values: dict[str, str]) -> list[str]:
    lines = [f"{title}:"]
    lines.extend(f"- {key}: {value}" for key, value in values.items())
    return lines


def render_project_overview(package: ProjectOverviewPackage) -> str:
    lines = [
        "PROJECT-OVERVIEW",
        f"ROOT: {package.root}",
        *_render_list("TREE", package.tree_lines),
        *_render_mapping(
            "FILE-COUNTS",
            {key: str(value) for key, value in package.file_counts.items()},
        ),
        *_render_list("KEY-FILES", package.key_files),
        *_render_mapping("SUMMARIES", package.summaries),
    ]

    if package.errors:
        lines.extend(_render_list("ERRORS", package.errors))

    return "\n".join(lines)


def render_file_summary(package: FileSummaryPackage) -> str:
    lines = [
        "FILE-SUMMARY",
        f"FILE: {package.path}",
        f"TYPE: {package.source_type}",
        f"SIZE-BYTES: {package.size_bytes}",
        f"LINE-COUNT: {package.line_count if package.line_count is not None else 'n/a'}",
        f"ENCODING: {package.encoding if package.encoding is not None else 'n/a'}",
        f"METADATA-ONLY: {'true' if package.metadata_only else 'false'}",
        "PREVIEW-BEGIN",
        package.preview,
        "PREVIEW-END",
        *_render_list("STRUCTURE", package.structure_lines),
    ]

    if package.errors:
        lines.extend(_render_list("ERRORS", package.errors))

    return "\n".join(lines)


def render_file_page(package: FilePagePackage) -> str:
    return "\n".join(
        [
            f"FILE: {package.path}",
            f"PAGE: {package.page_number}/{package.total_pages}",
            f"LINES: {package.line_start}-{package.line_end}",
            f"CHARS: {package.char_start}-{package.char_end}",
            f"TRUNCATED: {'true' if package.truncated else 'false'}",
            "CONTENT-BEGIN",
            package.content,
            "CONTENT-END",
        ]
    )


def render_extracted_text(package: ExtractedTextPackage) -> str:
    lines = [
        "EXTRACTED-TEXT",
        f"SOURCE: {package.path}",
        f"SOURCE-TYPE: {package.source_type}",
        f"SUCCESS: {'true' if package.success else 'false'}",
        "ORIGINAL-BINARY-SENT: false",
    ]

    if package.success and package.text is not None:
        lines.extend(["TEXT-BEGIN", package.text, "TEXT-END"])
    if package.reason is not None:
        lines.append(f"REASON: {package.reason}")

    return "\n".join(lines)
