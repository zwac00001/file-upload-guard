import os
import subprocess
import sys
from pathlib import Path

from docx import Document

from file_upload_guard.cli import build_parser, main


def test_parser_exposes_expected_subcommands():
    parser = build_parser()
    subparsers_action = next(
        action for action in parser._actions if getattr(action, "choices", None)
    )

    assert set(subparsers_action.choices) == {
        "project-summary",
        "file-summary",
        "file-page",
        "extract-text",
    }


def test_cli_project_summary_prints_rendered_output(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    exit_code = main(["project-summary", "--root", str(tmp_path)])

    assert exit_code == 0
    assert "PROJECT-OVERVIEW" in capsys.readouterr().out


def test_cli_project_summary_supports_include_hidden_and_ignore_dir(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    (github_dir / "workflow.yml").write_text("name: ci\n", encoding="utf-8")
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "bundle.js").write_text("console.log('bundle');\n", encoding="utf-8")

    exit_code = main(
        [
            "project-summary",
            "--root",
            str(tmp_path),
            "--include-hidden",
            "--ignore-dir",
            "dist",
        ]
    )

    assert exit_code == 0
    output = capsys.readouterr().out
    assert ".env" in output
    assert ".github/workflow.yml" in output
    assert "dist/bundle.js" not in output


def test_cli_project_summary_supports_ignore_file_and_ignore_glob(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    (reports_dir / "debug.log").write_text("debug\n", encoding="utf-8")
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "notes.md").write_text("# Notes\n", encoding="utf-8")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "app.py").write_text("print('skip me')\n", encoding="utf-8")
    (src_dir / "keep.txt").write_text("keep me\n", encoding="utf-8")

    exit_code = main(
        [
            "project-summary",
            "--root",
            str(tmp_path),
            "--ignore-file",
            "README.md",
            "--ignore-file",
            "debug.log",
            "--ignore-glob",
            "docs/*.md",
            "--ignore-glob",
            "src/*.py",
        ]
    )

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "README.md" not in output
    assert "reports/debug.log" not in output
    assert "docs/notes.md" not in output
    assert "src/app.py" not in output
    assert "src/keep.txt" in output


def test_cli_extract_text_prints_docx_content(tmp_path: Path, capsys):
    path = tmp_path / "brief.docx"
    document = Document()
    document.add_paragraph("Launch checklist")
    document.save(path)

    exit_code = main(["extract-text", "--path", str(path)])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "SUCCESS: true" in output
    assert "Launch checklist" in output


def test_python_module_entrypoint_prints_project_overview(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path("src").resolve())

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "file_upload_guard.cli",
            "project-summary",
            "--root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert completed.returncode == 0
    assert "PROJECT-OVERVIEW" in completed.stdout
