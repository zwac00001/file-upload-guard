# file-upload-guard

Universal local file analysis guard for agent platforms that cannot upload raw files directly.

## What It Includes

- A reusable skill at `skills/file-upload-guard/SKILL.md`
- A Codex plugin bundle at `plugins/file-upload-guard/`
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
plugins/file-upload-guard/  Codex plugin bundle for auto-discovery
src/file_upload_guard/      Local helper CLI implementation
adapters/                   Thin platform wrappers
docs/                       Design and implementation notes
tests/                      Regression tests
```

## Development

```powershell
.venv\Scripts\python.exe -m pytest tests -q
```

## Codex Install

Copy `skills/file-upload-guard` to `$CODEX_HOME/skills/file-upload-guard` or `~/.codex/skills/file-upload-guard` when `CODEX_HOME` is unset.

Then invoke the bundled runner:

```powershell
python "$CODEX_HOME/skills/file-upload-guard/scripts/run_file_upload_guard.py" project-summary --root .
```

## Codex Plugin Install

For Codex's home-local plugin path, copy:

- `plugins/file-upload-guard/` to `~/plugins/file-upload-guard`
- `.agents/plugins/marketplace.json` to `~/.agents/plugins/marketplace.json`

After that, restart Codex so it reloads the local marketplace.

### Another Windows Machine

```powershell
git clone https://github.com/zwac00001/file-upload-guard.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\\plugins" | Out-Null
New-Item -ItemType Directory -Force "$env:USERPROFILE\\.agents\\plugins" | Out-Null

Copy-Item -LiteralPath ".\\file-upload-guard\\plugins\\file-upload-guard" -Destination "$env:USERPROFILE\\plugins" -Recurse -Force
Copy-Item -LiteralPath ".\\file-upload-guard\\.agents\\plugins\\marketplace.json" -Destination "$env:USERPROFILE\\.agents\\plugins\\marketplace.json" -Force

python -m pip install pypdf python-docx PyYAML
```

Then restart Codex and verify with:

```powershell
python "$env:USERPROFILE\\plugins\\file-upload-guard\\skills\\file-upload-guard\\scripts\\run_file_upload_guard.py" project-summary --root .
```

If the command prints `PROJECT-OVERVIEW`, the plugin bundle is installed correctly.

## Stronger Codex Defaults

If you want Codex to prefer this workflow for local file analysis tasks, add two local configs:

1. `~/.codex/config.toml`
   Add the skill path with `enabled = true`
2. `~/.codex/AGENTS.md`
   Add a rule that requires `$file-upload-guard` before local project or local file analysis

This strengthens default behavior for local file analysis, but it is not a guaranteed hard pre-hook for every unrelated command.
