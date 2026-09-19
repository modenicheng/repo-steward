from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

DEFAULT_IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "target", "dist", "build",
}


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def is_git_repo(root: Path) -> bool:
    return run_git(root, "rev-parse", "--is-inside-work-tree").returncode == 0


def tracked_files(root: Path) -> list[str]:
    if is_git_repo(root):
        proc = run_git(root, "ls-files", "-z")
        if proc.returncode == 0:
            return sorted(p for p in proc.stdout.split("\0") if p)
    out: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in DEFAULT_IGNORED_DIRS for part in rel.parts):
            continue
        out.append(rel.as_posix())
    return sorted(out)


def load_config(root: Path) -> dict:
    path = root / ".repo-steward.toml"
    if not path.exists() or tomllib is None:
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return {}


def path_matches(path: str, pattern: str) -> bool:
    path = path.replace("\\", "/").lstrip("./")
    pattern = pattern.replace("\\", "/").lstrip("./")
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    if "**/" in pattern:
        prefix, suffix = pattern.split("**/", 1)
        if prefix and not path.startswith(prefix):
            return False
        return fnmatch.fnmatchcase(path, prefix + "*" + suffix) or fnmatch.fnmatchcase(path, prefix + suffix)
    return fnmatch.fnmatchcase(path, pattern)


def ignored_by_config(path: str, config: dict) -> bool:
    patterns = config.get("scan", {}).get("ignore_paths", [])
    return any(path_matches(path, str(p)) for p in patterns)


def git_last_commit_epoch(root: Path, path: str) -> int | None:
    if not is_git_repo(root):
        return None
    proc = run_git(root, "log", "-1", "--format=%ct", "--", path)
    text = proc.stdout.strip()
    return int(text) if proc.returncode == 0 and text.isdigit() else None
