from pathlib import Path


def test_skill_declares_mandatory_local_file_policy():
    skill_text = Path("skills/file-upload-guard/SKILL.md").read_text(encoding="utf-8")

    assert "This skill is mandatory" in skill_text
    assert "Do not attach or upload the raw local file directly." in skill_text
    assert "file-upload-guard project-summary" in skill_text
    assert "file-upload-guard file-page" in skill_text


def test_protocol_reference_lists_all_package_types():
    protocol_text = Path(
        "skills/file-upload-guard/references/protocol.md"
    ).read_text(encoding="utf-8")

    assert "Project overview package" in protocol_text
    assert "File summary package" in protocol_text
    assert "File page package" in protocol_text
    assert "Extracted text package" in protocol_text


def test_generic_platform_notes_document_root_level_project_summary_flags():
    generic_text = Path(
        "skills/file-upload-guard/references/platform-generic.md"
    ).read_text(encoding="utf-8")

    assert ".gitignore" in generic_text
    assert ".ignore" in generic_text
    assert "nested .gitignore" not in generic_text
    assert ".git/info/exclude" not in generic_text
    assert "--include-hidden" in generic_text
    assert "--ignore-dir" in generic_text
    assert "--ignore-file" in generic_text
    assert "--ignore-glob" in generic_text


def test_skill_bundle_includes_local_python_runner():
    skill_root = Path("skills/file-upload-guard")

    expected_files = [
        skill_root / "scripts" / "run_file_upload_guard.py",
        skill_root / "scripts" / "file-upload-guard.cmd",
        skill_root / "scripts" / "file_upload_guard" / "__init__.py",
        skill_root / "scripts" / "file_upload_guard" / "cli.py",
        skill_root / "scripts" / "file_upload_guard" / "project_summary.py",
        skill_root / "scripts" / "file_upload_guard" / "file_summary.py",
        skill_root / "scripts" / "file_upload_guard" / "file_page.py",
        skill_root / "scripts" / "file_upload_guard" / "extractors.py",
        skill_root / "scripts" / "file_upload_guard" / "io_utils.py",
        skill_root / "scripts" / "file_upload_guard" / "protocol.py",
    ]

    missing = [str(path) for path in expected_files if not path.exists()]
    assert not missing, f"Missing bundled skill files: {missing}"


def test_codebuddy_notes_reference_bundled_wrapper():
    codebuddy_text = Path(
        "skills/file-upload-guard/references/platform-codebuddy.md"
    ).read_text(encoding="utf-8")

    assert "scripts/file-upload-guard.cmd" in codebuddy_text
    assert "run_file_upload_guard.py" in codebuddy_text


def test_codex_notes_reference_installed_skill_root_and_python_runner():
    codex_text = Path(
        "skills/file-upload-guard/references/platform-codex.md"
    ).read_text(encoding="utf-8")

    assert "$CODEX_HOME/skills/file-upload-guard" in codex_text
    assert "run_file_upload_guard.py" in codex_text
    assert "Do not attach or upload the raw local file directly." in codex_text


def test_codex_openai_yaml_uses_interface_block_and_skill_prompt():
    openai_yaml = Path(
        "skills/file-upload-guard/agents/openai.yaml"
    ).read_text(encoding="utf-8")

    assert "interface:" in openai_yaml
    assert 'display_name: "File Upload Guard"' in openai_yaml
    assert "short_description:" in openai_yaml
    assert 'default_prompt: "Use $file-upload-guard' in openai_yaml
    assert "policy:" in openai_yaml
    assert "allow_implicit_invocation: true" in openai_yaml
