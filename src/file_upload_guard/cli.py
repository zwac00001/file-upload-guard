from __future__ import annotations

import argparse
from pathlib import Path

from file_upload_guard.file_page import build_extracted_text_package, build_file_page
from file_upload_guard.file_summary import build_file_summary
from file_upload_guard.project_summary import build_project_overview
from file_upload_guard.protocol import (
    render_extracted_text,
    render_file_page,
    render_file_summary,
    render_project_overview,
)


SUBCOMMANDS = (
    "project-summary",
    "file-summary",
    "file-page",
    "extract-text",
)


def _handle_project_summary(args: argparse.Namespace) -> str:
    package = build_project_overview(
        Path(args.root),
        tree_depth=args.tree_depth,
        summary_chars=args.summary_chars,
        include_hidden=args.include_hidden,
        ignore_dirs=set(args.ignore_dir),
        ignore_files=set(args.ignore_file),
        ignore_globs=set(args.ignore_glob),
    )
    return render_project_overview(package)


def _handle_file_summary(args: argparse.Namespace) -> str:
    package = build_file_summary(Path(args.path), preview_lines=args.preview_lines)
    return render_file_summary(package)


def _handle_file_page(args: argparse.Namespace) -> str:
    package = build_file_page(
        Path(args.path),
        page_number=args.page,
        page_size=args.page_size,
    )
    return render_file_page(package)


def _handle_extract_text(args: argparse.Namespace) -> str:
    package = build_extracted_text_package(Path(args.path))
    return render_extracted_text(package)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="file-upload-guard")
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_parser = subparsers.add_parser("project-summary")
    project_parser.add_argument("--root", required=True)
    project_parser.add_argument("--tree-depth", type=int, default=3)
    project_parser.add_argument("--summary-chars", type=int, default=160)
    project_parser.add_argument("--include-hidden", action="store_true")
    project_parser.add_argument("--ignore-dir", action="append", default=[])
    project_parser.add_argument("--ignore-file", action="append", default=[])
    project_parser.add_argument("--ignore-glob", action="append", default=[])
    project_parser.set_defaults(handler=_handle_project_summary)

    summary_parser = subparsers.add_parser("file-summary")
    summary_parser.add_argument("--path", required=True)
    summary_parser.add_argument("--preview-lines", type=int, default=12)
    summary_parser.set_defaults(handler=_handle_file_summary)

    page_parser = subparsers.add_parser("file-page")
    page_parser.add_argument("--path", required=True)
    page_parser.add_argument("--page", type=int, required=True)
    page_parser.add_argument("--page-size", type=int, default=7000)
    page_parser.set_defaults(handler=_handle_file_page)

    extract_parser = subparsers.add_parser("extract-text")
    extract_parser.add_argument("--path", required=True)
    extract_parser.set_defaults(handler=_handle_extract_text)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output = args.handler(args)
    except (FileNotFoundError, IndexError, ValueError) as exc:
        parser.exit(status=1, message=f"error: {exc}\n")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
