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
