# codebuddyAgent Notes

## Goal

Use the universal `skills/file-upload-guard/SKILL.md` rules without redefining them.

## Adapter Guidance

- Load the universal skill text into the `codebuddyAgent` skill or agent profile.
- Prefer the bundled wrapper at `skills/file-upload-guard/scripts/file-upload-guard.cmd`.
- The wrapper delegates to `scripts/run_file_upload_guard.py`, so the skill remains usable even when the platform only copied the skill directory.
- Treat the workflow as mandatory for any local project or local file request.

## Command Mapping

- Project overview: `skills/file-upload-guard/scripts/file-upload-guard.cmd project-summary --root <ROOT_PATH>`
- File summary: `skills/file-upload-guard/scripts/file-upload-guard.cmd file-summary --path <FILE_PATH>`
- File page: `skills/file-upload-guard/scripts/file-upload-guard.cmd file-page --path <FILE_PATH> --page <PAGE_NUMBER>`
- Extract text: `skills/file-upload-guard/scripts/file-upload-guard.cmd extract-text --path <FILE_PATH>`
