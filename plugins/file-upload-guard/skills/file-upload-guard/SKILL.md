---
name: file-upload-guard
description: Prevent raw local file uploads during local project and file analysis. Use when Codex needs to inspect a local repository, summarize a directory, read local files, or page file content instead of attaching files directly.
metadata:
  priority: 10
  bashPatterns:
    - '\b(Get-Content|cat|type|more)\b'
    - '\b(rg|ripgrep|findstr)\b'
  promptSignals:
    phrases:
      - "analyze this local project"
      - "analyze this repository"
      - "inspect local files"
      - "分析本地项目"
      - "分析这个仓库"
      - "不要上传文件"
      - "upload is restricted"
      - "direct file upload is forbidden"
    anyOf:
      - "local project"
      - "local repository"
      - "local file"
      - "project summary"
      - "file page"
    minScore: 6
retrieval:
  aliases:
    - file upload guard
    - local file guard
    - upload guard
    - project summary
  intents:
    - analyze a local project without uploading raw files
    - summarize a repository before reading exact files
    - page local file content instead of attaching files
    - extract document text before sending file content
---

# File Upload Guard

## Overview

Use this skill whenever Codex needs to inspect local files without uploading them directly.

This skill is mandatory for local project analysis and local file inspection.

In this plugin bundle, prefer the bundled helper at `<path-to-skill>/scripts/run_file_upload_guard.py`. If a global `file-upload-guard` CLI is already installed, treat it as equivalent.

## Mandatory Contract

1. Invoke this skill when the task involves a local project, repository, or file.
2. Do not attach or upload the raw local file directly.
3. Use the local helper CLI to produce summaries, extracted text, or paginated content.
4. Send only the CLI output to the model.
5. If the platform has policy hooks or tool routing, enforce this workflow there too.

## Workflow

1. Start with a project overview:

```powershell
python "<path-to-skill>/scripts/run_file_upload_guard.py" project-summary --root <ROOT_PATH>
```

If hidden files matter, add `--include-hidden`.
If specific directories should be skipped, repeat `--ignore-dir <DIR_NAME>`.
If specific filenames should be skipped, repeat `--ignore-file <FILE_NAME>`.
If path patterns should be skipped, repeat `--ignore-glob <PATTERN>`.

2. If the model needs more detail, summarize a single file:

```powershell
python "<path-to-skill>/scripts/run_file_upload_guard.py" file-summary --path <FILE_PATH>
```

3. If the model needs exact content, send only the requested page:

```powershell
python "<path-to-skill>/scripts/run_file_upload_guard.py" file-page --path <FILE_PATH> --page <PAGE_NUMBER>
```

4. If the file is a PDF or Word document, extract text before paging:

```powershell
python "<path-to-skill>/scripts/run_file_upload_guard.py" extract-text --path <FILE_PATH>
```

## Rules

- Default to summary-first, then page-on-demand.
- PDF and Word extraction additionally require `pypdf` and `python-docx` in the Python environment running `python`.
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
- Codex plugin notes: `references/platform-codex.md`
