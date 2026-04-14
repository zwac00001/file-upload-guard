# Generic Platform Notes

## Installation

- Make the `file-upload-guard` CLI available on the local machine.
- Load `skills/file-upload-guard/SKILL.md` into the platform's reusable skill or system instruction mechanism.
- If the platform only copies the skill directory, call the bundled wrapper in `skills/file-upload-guard/scripts/file-upload-guard.cmd` or run `scripts/run_file_upload_guard.py` directly.

## Required Behavior

- Trigger the skill for any local project or file analysis task.
- Route project analysis through `file-upload-guard project-summary`.
- Automatically honor root-level `.gitignore` and `.ignore` entries for common directory, filename, and glob patterns.
- Add `--include-hidden` when the task explicitly needs dotfiles or hidden directories.
- Add `--ignore-dir <DIR_NAME>` and repeat it when extra generated or vendor directories should be excluded.
- Add `--ignore-file <FILE_NAME>` and repeat it when exact filenames should be excluded everywhere.
- Add `--ignore-glob <PATTERN>` and repeat it when relative path patterns should be excluded.
- Route single-file inspection through `file-upload-guard file-summary`.
- Route full-content requests through `file-upload-guard file-page`.
- Route PDF and Word inspection through `file-upload-guard extract-text`.

## Failure Handling

- If the CLI reports an extraction or paging error, relay that error as text.
- Do not fall back to direct raw file upload.
