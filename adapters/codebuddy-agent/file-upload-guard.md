# codebuddyAgent Wrapper

Use `skills/file-upload-guard/SKILL.md` as the source of truth.

This wrapper is mandatory for local project and local file analysis.

## Required Policy

- Do not attach or upload the raw local file directly.
- Run `file-upload-guard project-summary --root <ROOT_PATH>` first.
- Let `project-summary` honor root `.gitignore` and root `.ignore` before selecting files.
- Run `file-upload-guard file-summary --path <FILE_PATH>` before requesting exact content.
- Run `file-upload-guard file-page --path <FILE_PATH> --page <PAGE_NUMBER>` only after the model requests a page.
- Use `file-upload-guard extract-text --path <FILE_PATH>` for PDF and Word files.
