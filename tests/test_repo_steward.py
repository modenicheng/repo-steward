import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import common
import diff_guard
import docs_drift
import docs_inventory
import file_metrics
import repo_scan


def git(root: Path, *args: str):
    return subprocess.run(["git", "-C", str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def init_repo(root: Path):
    git(root, "init", "-q")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.com")


def commit_all(root: Path, message: str, date: str | None = None):
    git(root, "add", ".")
    env = os.environ.copy()
    if date:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", message], env=env, check=True)


class RepoStewardTests(unittest.TestCase):
    def test_recursive_prefix_glob(self):
        self.assertTrue(common.path_matches("src/a/b.py", "src/**"))
        self.assertTrue(common.path_matches("src/x.py", "src/**"))
        self.assertFalse(common.path_matches("tests/x.py", "src/**"))

    def test_repo_scan_reports_sensitive_name_without_contents(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / ".env").write_text("TOP_SECRET=abc", encoding="utf-8")
            commit_all(root, "add env")
            result = repo_scan.scan(root)
            rendered = repr(result)
            self.assertIn("risky_filename", rendered)
            self.assertNotIn("TOP_SECRET", rendered)

    def test_file_metrics_threshold(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / "big.py").write_text("x=1\n" * 12, encoding="utf-8")
            commit_all(root, "big")
            result = file_metrics.scan(root, warn_lines=10, high_lines=20)
            self.assertEqual(result["findings"][0]["path"], "big.py")
            self.assertEqual(result["findings"][0]["severity"], "review")

    def test_docs_inventory_finds_broken_local_link(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / "README.md").write_text("# X\n[missing](docs/nope.md)\n", encoding="utf-8")
            commit_all(root, "docs")
            result = docs_inventory.inventory(root)
            self.assertEqual(result["documents"][0]["broken_local_links"], ["docs/nope.md"])

    def test_docs_drift_nested_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / "docs").mkdir()
            (root / "src").mkdir()
            (root / "docs" / "architecture.md").write_text("old", encoding="utf-8")
            (root / ".repo-steward.toml").write_text('[docs."docs/architecture.md"]\nsources=["src/**"]\n', encoding="utf-8")
            commit_all(root, "docs", "2026-01-01T00:00:00+00:00")
            (root / "src" / "a.py").write_text("print(1)", encoding="utf-8")
            commit_all(root, "code", "2026-01-02T00:00:00+00:00")
            result = docs_drift.scan(root)
            self.assertEqual(result["findings"][0]["document"], "docs/architecture.md")

    def test_diff_guard_warns_docs_impact(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / "src").mkdir()
            (root / "docs").mkdir()
            (root / "src" / "a.py").write_text("x=1\n", encoding="utf-8")
            (root / "docs" / "architecture.md").write_text("arch\n", encoding="utf-8")
            (root / ".repo-steward.toml").write_text('[docs."docs/architecture.md"]\nsources=["src/**"]\n', encoding="utf-8")
            commit_all(root, "base")
            (root / "src" / "a.py").write_text("x=2\n", encoding="utf-8")
            git(root, "add", "src/a.py")
            result = diff_guard.scan(root, staged=True)
            self.assertTrue(any(w["kind"] == "docs_impact" for w in result["warnings"]))

    def test_diff_guard_blocks_conflict_marker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_repo(root)
            (root / "a.txt").write_text("ok\n", encoding="utf-8")
            commit_all(root, "base")
            (root / "a.txt").write_text("<<<<<<< ours\nx\n=======\ny\n>>>>>>> theirs\n", encoding="utf-8")
            git(root, "add", "a.txt")
            result = diff_guard.scan(root, staged=True)
            self.assertTrue(any(b["kind"] == "conflict_marker_in_added_lines" for b in result["blockers"]))


if __name__ == "__main__":
    unittest.main()
