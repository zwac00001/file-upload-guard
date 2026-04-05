from pathlib import Path

from file_upload_guard.project_summary import build_project_overview
from file_upload_guard.protocol import render_project_overview


def test_build_project_overview_reports_tree_counts_and_key_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\nProject summary\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=2, summary_chars=20)
    rendered = render_project_overview(package)

    assert f"ROOT: {tmp_path}" in rendered
    assert "- README.md" in rendered
    assert "- src/app.py" in rendered
    assert "- .py: 1" in rendered
    assert "README.md" in rendered
    assert "Project summary" in rendered


def test_build_project_overview_ignores_default_tooling_directories(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    (venv_dir / "pyvenv.cfg").write_text("home = python\n", encoding="utf-8")

    pytest_cache_dir = tmp_path / ".pytest_cache"
    pytest_cache_dir.mkdir()
    (pytest_cache_dir / "README.md").write_text("cache\n", encoding="utf-8")

    pycache_dir = tmp_path / "src" / "__pycache__"
    pycache_dir.mkdir(parents=True)
    (pycache_dir / "app.cpython-312.pyc").write_bytes(b"\x00\x01")

    src_dir = tmp_path / "src"
    (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=3, summary_chars=40)
    rendered = render_project_overview(package)

    assert ".venv/pyvenv.cfg" not in rendered
    assert ".pytest_cache/README.md" not in rendered
    assert "__pycache__/app.cpython-312.pyc" not in rendered
    assert "- .cfg:" not in rendered
    assert "- .pyc:" not in rendered
    assert "- src/app.py" in rendered


def test_build_project_overview_hides_hidden_entries_by_default(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    (github_dir / "workflow.yml").write_text("name: ci\n", encoding="utf-8")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=3, summary_chars=40)
    rendered = render_project_overview(package)

    assert "- src/app.py" in rendered
    assert ".env" not in rendered
    assert ".github/workflow.yml" not in rendered


def test_build_project_overview_can_include_hidden_and_custom_ignore(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    (github_dir / "workflow.yml").write_text("name: ci\n", encoding="utf-8")

    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "bundle.js").write_text("console.log('bundle');\n", encoding="utf-8")

    package = build_project_overview(
        tmp_path,
        tree_depth=3,
        summary_chars=40,
        include_hidden=True,
        ignore_dirs={"dist"},
    )
    rendered = render_project_overview(package)

    assert "- .env" in rendered
    assert "- .github/workflow.yml" in rendered
    assert "dist/bundle.js" not in rendered


def test_build_project_overview_can_ignore_specific_files_and_globs(tmp_path: Path):
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

    package = build_project_overview(
        tmp_path,
        tree_depth=3,
        summary_chars=40,
        ignore_files={"README.md", "debug.log"},
        ignore_globs={"docs/*.md", "src/*.py"},
    )
    rendered = render_project_overview(package)

    assert "README.md" not in rendered
    assert "reports/debug.log" not in rendered
    assert "docs/notes.md" not in rendered
    assert "src/app.py" not in rendered
    assert "- src/keep.txt" in rendered


def test_build_project_overview_reads_root_gitignore_and_ignore(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("dist/\n*.log\n", encoding="utf-8")
    (tmp_path / ".ignore").write_text("docs/*.md\n", encoding="utf-8")

    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "bundle.js").write_text("console.log('bundle');\n", encoding="utf-8")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "debug.log").write_text("debug\n", encoding="utf-8")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "notes.md").write_text("# Notes\n", encoding="utf-8")

    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "keep.txt").write_text("keep me\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=3, summary_chars=40)
    rendered = render_project_overview(package)

    assert "dist/bundle.js" not in rendered
    assert "logs/debug.log" not in rendered
    assert "docs/notes.md" not in rendered
    assert "- src/keep.txt" in rendered


def test_build_project_overview_handles_utf8_bom_in_ignore_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_bytes(b"\xef\xbb\xbfdist/\n*.log\n")

    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    (dist_dir / "bundle.js").write_text("console.log('bundle');\n", encoding="utf-8")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "debug.log").write_text("debug\n", encoding="utf-8")

    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "keep.txt").write_text("keep me\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=3, summary_chars=40)
    rendered = render_project_overview(package)

    assert "dist/bundle.js" not in rendered
    assert "logs/debug.log" not in rendered
    assert "- src/keep.txt" in rendered


def test_build_project_overview_does_not_read_nested_gitignore_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    packages_dir = tmp_path / "packages" / "web"
    packages_dir.mkdir(parents=True)
    (packages_dir / ".gitignore").write_text("dist/\n*.tmp\n", encoding="utf-8")

    dist_dir = packages_dir / "dist"
    dist_dir.mkdir()
    (dist_dir / "bundle.js").write_text("console.log('bundle');\n", encoding="utf-8")
    (packages_dir / "debug.tmp").write_text("debug\n", encoding="utf-8")
    src_dir = packages_dir / "src"
    src_dir.mkdir()
    (src_dir / "keep.ts").write_text("export const keep = true;\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=5, summary_chars=40)
    rendered = render_project_overview(package)

    assert "- packages/web/dist/bundle.js" in rendered
    assert "- packages/web/debug.tmp" in rendered
    assert "- packages/web/src/keep.ts" in rendered


def test_build_project_overview_does_not_read_git_info_exclude(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    git_info_dir = tmp_path / ".git" / "info"
    git_info_dir.mkdir(parents=True)
    (git_info_dir / "exclude").write_text("local/\n*.cache\n", encoding="utf-8")

    local_dir = tmp_path / "local"
    local_dir.mkdir()
    (local_dir / "secret.txt").write_text("secret\n", encoding="utf-8")

    cache_dir = tmp_path / "artifacts"
    cache_dir.mkdir()
    (cache_dir / "build.cache").write_text("cached\n", encoding="utf-8")

    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "keep.txt").write_text("keep me\n", encoding="utf-8")

    package = build_project_overview(tmp_path, tree_depth=4, summary_chars=40)
    rendered = render_project_overview(package)

    assert "- local/secret.txt" in rendered
    assert "- artifacts/build.cache" in rendered
    assert "- src/keep.txt" in rendered
