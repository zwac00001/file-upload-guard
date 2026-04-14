# Codex App Notes

## Goal

Use the universal `skills/file-upload-guard/SKILL.md` rules through a Codex App skill wrapper.

## Installation

- Install this folder into `$CODEX_HOME/skills/file-upload-guard`.
- If `CODEX_HOME` is unset, use `~/.codex/skills/file-upload-guard`.
- Keep `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/` together so Codex can discover the skill and its bundled runner.
- Prefer the bundled Python runner at `$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py` instead of assuming a globally installed `file-upload-guard` command.
- PDF and Word extraction additionally require `pypdf` and `python-docx` in the Python environment used by `python`.

## Adapter Guidance

- Install the universal skill into the Codex skill search path.
- Call the bundled local helper through the shell rather than attaching local files.
- Treat the workflow as mandatory for any local project or local file request.
- Do not attach or upload the raw local file directly.

## Command Mapping

- Project overview: `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" project-summary --root <ROOT_PATH>`
- File summary: `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-summary --path <FILE_PATH>`
- File page: `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-page --path <FILE_PATH> --page <PAGE_NUMBER>`
- Extract text: `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" extract-text --path <FILE_PATH>`
