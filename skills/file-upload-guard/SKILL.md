---
name: file-upload-guard
description: Use when a task requires analyzing local projects, local repositories, or local files on a machine where direct file upload is restricted or forbidden.
---

# File Upload Guard

## Overview

Use this skill whenever an agent needs to inspect local files without uploading them directly.

This skill is mandatory for local project analysis and local file inspection.

If the platform only installs the `skills/file-upload-guard` directory, use the bundled runner in `scripts/` instead of assuming a globally installed CLI.

The bundled runner preserves the same `file-upload-guard project-summary`, `file-upload-guard file-summary`, `file-upload-guard file-page`, and `file-upload-guard extract-text` workflow.

For Codex, install this skill under `$CODEX_HOME/skills/file-upload-guard` or `~/.codex/skills/file-upload-guard`, then invoke `scripts/run_file_upload_guard.py` from that installed skill root.

## Mandatory Contract

1. Invoke this skill when the task involves a local project, repository, or file.
2. Do not attach or upload the raw local file directly.
3. Use the local helper CLI to produce summaries, extracted text, or paginated content.
4. Send only the CLI output to the model.
5. If the platform has policy hooks or tool routing, enforce this workflow there too.

## Workflow

1. Start with a project overview:

```powershell
skills/file-upload-guard/scripts/file-upload-guard.cmd project-summary --root <ROOT_PATH>
```

If hidden files matter, add `--include-hidden`.
If specific directories should be skipped, repeat `--ignore-dir <DIR_NAME>`.
If specific filenames should be skipped, repeat `--ignore-file <FILE_NAME>`.
If path patterns should be skipped, repeat `--ignore-glob <PATTERN>`.

2. If the model needs more detail, summarize a single file:

```powershell
skills/file-upload-guard/scripts/file-upload-guard.cmd file-summary --path <FILE_PATH>
```

3. If the model needs exact content, send only the requested page:

```powershell
skills/file-upload-guard/scripts/file-upload-guard.cmd file-page --path <FILE_PATH> --page <PAGE_NUMBER>
```

4. If the file is a PDF or Word document, extract text before paging:

```powershell
skills/file-upload-guard/scripts/file-upload-guard.cmd extract-text --path <FILE_PATH>
```

## Rules

- Default to summary-first, then page-on-demand.
- Root-level `.gitignore` and `.ignore` files are honored for common directory, filename, and glob patterns during project summaries.
- Hidden files and directories are excluded from project summaries by default unless `--include-hidden` is used.
- Use `--ignore-dir` to suppress additional generated or vendor directories for one run.
- Use `--ignore-file` to suppress exact filenames regardless of directory.
- Use `--ignore-glob` to suppress matching relative paths such as `docs/*.md` or `src/*.py`.
- Preserve original text content in v1.
- If a file is binary and not extractable, report metadata and state that the original binary was not sent.
- Keep page requests explicit so the model can ask for the next page by number.

## References

- Protocol details: `references/protocol.md`
- Generic installation notes: `references/platform-generic.md`
- `codebuddyAgent` notes: `references/platform-codebuddy.md`
- Codex App notes: `references/platform-codex.md`
