# file-upload-guard

Universal local file analysis guard for agent platforms that cannot upload raw files directly.

## What It Includes

- A reusable skill at `skills/file-upload-guard/SKILL.md`
- A local CLI under `src/file_upload_guard`
- Thin wrapper notes for `codebuddyAgent` and Codex App under `adapters/`
- Specs, plan notes, and tests for the workflow

## Workflow

1. Start with a project overview:

```powershell
file-upload-guard project-summary --root <ROOT_PATH>
```

2. Summarize a file when the model needs more detail:

```powershell
file-upload-guard file-summary --path <FILE_PATH>
```

3. Send only the requested page when exact content is needed:

```powershell
file-upload-guard file-page --path <FILE_PATH> --page <PAGE_NUMBER>
```

4. Extract text before paging PDF or Word files:

```powershell
file-upload-guard extract-text --path <FILE_PATH>
```

## Repository Layout

```text
skills/file-upload-guard/   Universal skill and platform notes
src/file_upload_guard/      Local helper CLI implementation
adapters/                   Thin platform wrappers
docs/                       Design and implementation notes
tests/                      Regression tests
```

## Development

```powershell
.venv\Scripts\python.exe -m pytest tests -q
```
