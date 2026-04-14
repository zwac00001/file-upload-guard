# Codex App Wrapper

Use `skills/file-upload-guard/SKILL.md` as the source of truth.

This wrapper is mandatory for local project and local file analysis.

Install the skill at `$CODEX_HOME/skills/file-upload-guard` or `~/.codex/skills/file-upload-guard` when `CODEX_HOME` is unset.

For Codex, prefer the bundled runner:

`python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py"`

## Required Policy

- Do not attach or upload the raw local file directly.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" project-summary --root <ROOT_PATH>` first.
- Let `project-summary` honor root `.gitignore` and root `.ignore` before selecting files.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-summary --path <FILE_PATH>` before requesting exact content.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-page --path <FILE_PATH> --page <PAGE_NUMBER>` only after the model requests a page.
- Use `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" extract-text --path <FILE_PATH>` for PDF and Word files.
