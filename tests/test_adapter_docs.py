from pathlib import Path


def test_codebuddy_adapter_points_to_universal_skill():
    text = Path("adapters/codebuddy-agent/file-upload-guard.md").read_text(
        encoding="utf-8"
    )

    assert "skills/file-upload-guard/SKILL.md" in text
    assert "file-upload-guard project-summary" in text
    assert "mandatory" in text.lower()


def test_codex_adapter_points_to_universal_skill():
    text = Path("adapters/codex-app/file-upload-guard.md").read_text(
        encoding="utf-8"
    )

    assert "skills/file-upload-guard/SKILL.md" in text
    assert "$CODEX_HOME/skills/file-upload-guard" in text
    assert "run_file_upload_guard.py" in text
    assert "Do not attach or upload the raw local file directly." in text
