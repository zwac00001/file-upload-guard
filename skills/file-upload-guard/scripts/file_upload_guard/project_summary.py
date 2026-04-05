from __future__ import annotations

import fnmatch
import os
from collections import Counter
from pathlib import Path

from file_upload_guard.io_utils import read_text_file
from file_upload_guard.protocol import ProjectOverviewPackage


HIGH_VALUE_FILES = {
    "README.md",
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "go.mod",
    "Cargo.toml",
    "Makefile",
}

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
}


def _load_root_ignore_patterns(root: Path) -> tuple[set[str], set[str], set[str]]:
    ignore_dirs: set[str] = set()
    ignore_files: set[str] = set()
    ignore_globs: set[str] = set()

    for name in (".gitignore", ".ignore"):
        path = root / name
        if not path.is_file():
            continue

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.lstrip("\ufeff").strip().replace("\\", "/")
            if not line or line.startswith("#") or line.startswith("!"):
                continue

            normalized = line
            while normalized.startswith("./"):
                normalized = normalized[2:]
            normalized = normalized.lstrip("/")
            if not normalized:
                continue

            if normalized.endswith("/"):
                directory_pattern = normalized.rstrip("/")
                if directory_pattern and "/" not in directory_pattern and not any(
                    token in directory_pattern for token in "*?[]"
                ):
                    ignore_dirs.add(directory_pattern)
                elif directory_pattern:
                    ignore_globs.add(f"{directory_pattern}/*")
                continue

            if "/" not in normalized and not any(
                token in normalized for token in "*?[]"
            ):
                ignore_files.add(normalized)
                continue

            ignore_globs.add(normalized)

    return ignore_dirs, ignore_files, ignore_globs


def _iter_files(
    root: Path,
    *,
    include_hidden: bool,
    ignore_dirs: set[str],
    ignore_files: set[str],
    ignore_globs: set[str],
) -> list[Path]:
    files: list[Path] = []

    for current_root, directories, filenames in os.walk(root, topdown=True):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in ignore_dirs
            and (include_hidden or not directory.startswith("."))
        )

        current_path = Path(current_root)
        for filename in sorted(filenames):
            if not include_hidden and filename.startswith("."):
                continue

            path = current_path / filename
            relative_path = str(path.relative_to(root)).replace("\\", "/")

            if filename in ignore_files:
                continue
            if any(
                fnmatch.fnmatch(relative_path, pattern)
                or fnmatch.fnmatch(filename, pattern)
                for pattern in ignore_globs
            ):
                continue

            files.append(path)

    return files


def _tree_lines(paths: list[Path], root: Path, tree_depth: int) -> list[str]:
    lines: list[str] = []

    for path in paths:
        relative = path.relative_to(root)
        if len(relative.parts) > tree_depth:
            continue
        lines.append(str(relative).replace("\\", "/"))

    return lines


def _file_counts(paths: list[Path]) -> dict[str, int]:
    counter: Counter[str] = Counter()

    for path in paths:
        suffix = path.suffix.lower() or "<no-ext>"
        counter[suffix] += 1

    return dict(sorted(counter.items()))


def _key_files(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.name in HIGH_VALUE_FILES]


def _summaries(
    paths: list[Path],
    root: Path,
    summary_chars: int,
) -> tuple[dict[str, str], list[str]]:
    summaries: dict[str, str] = {}
    errors: list[str] = []

    for path in paths:
        try:
            text, _ = read_text_file(path)
            normalized_lines = [
                line.lstrip("# ").strip()
                for line in text.splitlines()
                if line.strip()
            ]
            collapsed = " ".join(normalized_lines)
            summaries[str(path.relative_to(root)).replace("\\", "/")] = collapsed[
                :summary_chars
            ]
        except ValueError as exc:
            errors.append(str(exc))

    return summaries, errors


def build_project_overview(
    root: Path,
    tree_depth: int = 3,
    summary_chars: int = 160,
    include_hidden: bool = False,
    ignore_dirs: set[str] | None = None,
    ignore_files: set[str] | None = None,
    ignore_globs: set[str] | None = None,
) -> ProjectOverviewPackage:
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise ValueError(f"{root} is not a directory")

    resolved_ignore_dirs = set(IGNORED_DIRECTORY_NAMES)
    if ignore_dirs is not None:
        resolved_ignore_dirs.update(ignore_dirs)
    resolved_ignore_files = set(ignore_files or set())
    resolved_ignore_globs = set(ignore_globs or set())

    auto_ignore_dirs, auto_ignore_files, auto_ignore_globs = _load_root_ignore_patterns(
        root
    )
    resolved_ignore_dirs.update(auto_ignore_dirs)
    resolved_ignore_files.update(auto_ignore_files)
    resolved_ignore_globs.update(auto_ignore_globs)

    files = _iter_files(
        root,
        include_hidden=include_hidden,
        ignore_dirs=resolved_ignore_dirs,
        ignore_files=resolved_ignore_files,
        ignore_globs=resolved_ignore_globs,
    )
    key_files = _key_files(files)
    summaries, errors = _summaries(key_files, root, summary_chars)

    return ProjectOverviewPackage(
        root=str(root),
        tree_lines=_tree_lines(files, root, tree_depth),
        file_counts=_file_counts(files),
        key_files=[str(path.relative_to(root)).replace("\\", "/") for path in key_files],
        summaries=summaries,
        errors=errors,
    )
