from pathlib import Path


def test_readme_describes_skill_and_cli_workflow():
    readme_text = Path("README.md").read_text(encoding="utf-8")

    assert "file-upload-guard" in readme_text
    assert "skills/file-upload-guard/SKILL.md" in readme_text
    assert "project-summary" in readme_text
    assert "file-summary" in readme_text
    assert "file-page" in readme_text
    assert "extract-text" in readme_text


def test_gitignore_excludes_local_env_and_cache_artifacts():
    gitignore_text = Path(".gitignore").read_text(encoding="utf-8")

    assert ".venv/" in gitignore_text
    assert ".pytest_cache/" in gitignore_text
    assert "__pycache__/" in gitignore_text
