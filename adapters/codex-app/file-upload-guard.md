# Codex App Wrapper

Use `skills/file-upload-guard/SKILL.md` as the source of truth.

This wrapper is mandatory for local project and local file analysis.

Install the skill at `$CODEX_HOME/skills/file-upload-guard` or `~/.codex/skills/file-upload-guard` when `CODEX_HOME` is unset.

If you prefer the plugin path, install:

- `plugins/file-upload-guard/` to `~/plugins/file-upload-guard`
- `.agents/plugins/marketplace.json` to `~/.agents/plugins/marketplace.json`

For Codex, prefer the bundled runner:

`python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py"`

## Required Policy

- Do not attach or upload the raw local file directly.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" project-summary --root <ROOT_PATH>` first.
- Let `project-summary` honor root `.gitignore` and root `.ignore` before selecting files.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-summary --path <FILE_PATH>` before requesting exact content.
- Run `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" file-page --path <FILE_PATH> --page <PAGE_NUMBER>` only after the model requests a page.
- Use `python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" extract-text --path <FILE_PATH>` for PDF and Word files.

## Stronger Global Enforcement

To make Codex much more likely to use this workflow by default:

- add the skill path to `~/.codex/config.toml` with `enabled = true`
- add a global rule to `~/.codex/AGENTS.md` that requires `$file-upload-guard` before local project or local file analysis

This does not guarantee a hard pre-hook for every command, but it is the strongest repo-supported setup for Codex today.
