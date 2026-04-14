# Codex Plugin Notes

## Goal

Use the bundled `skills/file-upload-guard/SKILL.md` rules through a Codex plugin bundle.

## Adapter Guidance

- Keep `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/` together inside the plugin.
- Call the bundled local helper through the shell rather than attaching local files.
- Treat the workflow as mandatory for any local project or local file request.
- Do not attach or upload the raw local file directly.
- Use `<path-to-skill>/scripts/run_file_upload_guard.py` as the canonical runner path inside the plugin bundle.
- PDF and Word extraction additionally require `pypdf` and `python-docx` in the Python environment used by `python`.

## Command Mapping

- Project overview: `python "<path-to-skill>/scripts/run_file_upload_guard.py" project-summary --root <ROOT_PATH>`
- File summary: `python "<path-to-skill>/scripts/run_file_upload_guard.py" file-summary --path <FILE_PATH>`
- File page: `python "<path-to-skill>/scripts/run_file_upload_guard.py" file-page --path <FILE_PATH> --page <PAGE_NUMBER>`
- Extract text: `python "<path-to-skill>/scripts/run_file_upload_guard.py" extract-text --path <FILE_PATH>`
