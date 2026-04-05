# codebuddyAgent Notes

## Goal

Use the universal `skills/file-upload-guard/SKILL.md` rules without redefining them.

## Adapter Guidance

- Load the universal skill text into the `codebuddyAgent` skill or agent profile.
- Expose the local CLI as shell commands or named tools.
- Treat the workflow as mandatory for any local project or local file request.

## Command Mapping

- Project overview: `file-upload-guard project-summary --root <ROOT_PATH>`
- File summary: `file-upload-guard file-summary --path <FILE_PATH>`
- File page: `file-upload-guard file-page --path <FILE_PATH> --page <PAGE_NUMBER>`
- Extract text: `file-upload-guard extract-text --path <FILE_PATH>`
