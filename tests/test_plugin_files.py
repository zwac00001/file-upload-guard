import json
from pathlib import Path


def test_plugin_manifest_declares_file_upload_guard_plugin():
    plugin_manifest = json.loads(
        Path("plugins/file-upload-guard/.codex-plugin/plugin.json").read_text(
            encoding="utf-8"
        )
    )

    assert plugin_manifest["name"] == "file-upload-guard"
    assert plugin_manifest["version"] == "0.1.0"
    assert plugin_manifest["skills"] == "./skills/"
    assert plugin_manifest["interface"]["displayName"] == "File Upload Guard"
    assert plugin_manifest["interface"]["category"] == "Coding"


def test_plugin_marketplace_exposes_file_upload_guard():
    marketplace = json.loads(
        Path(".agents/plugins/marketplace.json").read_text(encoding="utf-8")
    )

    plugin_entry = next(
        plugin for plugin in marketplace["plugins"] if plugin["name"] == "file-upload-guard"
    )

    assert plugin_entry["source"]["source"] == "local"
    assert plugin_entry["source"]["path"] == "./plugins/file-upload-guard"
    assert plugin_entry["policy"]["installation"] == "INSTALLED_BY_DEFAULT"
    assert plugin_entry["policy"]["authentication"] == "ON_INSTALL"
    assert plugin_entry["category"] == "Coding"


def test_plugin_skill_bundle_is_self_contained():
    skill_root = Path("plugins/file-upload-guard/skills/file-upload-guard")

    expected_files = [
        skill_root / "SKILL.md",
        skill_root / "agents" / "openai.yaml",
        skill_root / "scripts" / "run_file_upload_guard.py",
        skill_root / "scripts" / "file_upload_guard" / "cli.py",
        skill_root / "scripts" / "file_upload_guard" / "project_summary.py",
        skill_root / "scripts" / "file_upload_guard" / "file_summary.py",
        skill_root / "scripts" / "file_upload_guard" / "file_page.py",
        skill_root / "scripts" / "file_upload_guard" / "extractors.py",
    ]

    missing = [str(path) for path in expected_files if not path.exists()]
    assert not missing, f"Missing plugin bundled files: {missing}"


def test_plugin_skill_uses_path_to_skill_commands_and_discovery_metadata():
    skill_text = Path(
        "plugins/file-upload-guard/skills/file-upload-guard/SKILL.md"
    ).read_text(encoding="utf-8")

    assert "<path-to-skill>/scripts/run_file_upload_guard.py" in skill_text
    assert "bashPatterns:" in skill_text
    assert "retrieval:" in skill_text
    assert "Do not attach or upload the raw local file directly." in skill_text
