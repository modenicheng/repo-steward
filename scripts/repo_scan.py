#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import ignored_by_config, load_config, tracked_files

RISKY_NAMES = {
    ".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json",
    "secrets.json", "secret.txt", "token.txt",
}
RISKY_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
JUNK_SUFFIXES = {".log", ".tmp", ".bak", ".orig", ".swp", ".swo"}
JUNK_PARTS = {"node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def scan(root: Path) -> dict:
    config = load_config(root)
    scan_cfg = config.get("scan", {})
    large_limit = int(scan_cfg.get("large_file_bytes", 1_048_576))
    root_warn = int(scan_cfg.get("root_file_warn", 20))
    findings: list[dict] = []
    files = [p for p in tracked_files(root) if not ignored_by_config(p, config)]

    root_files = [p for p in files if "/" not in p]
    if len(root_files) > root_warn:
        findings.append({"severity": "review", "kind": "root_clutter", "count": len(root_files), "limit": root_warn})

    for rel in files:
        p = root / rel
        lower_name = p.name.lower()
        parts = set(Path(rel).parts)
        if lower_name in RISKY_NAMES or p.suffix.lower() in RISKY_SUFFIXES:
            findings.append({"severity": "block", "kind": "risky_filename", "path": rel})
        if p.suffix.lower() in JUNK_SUFFIXES or parts & JUNK_PARTS:
            findings.append({"severity": "review", "kind": "tracked_junk", "path": rel})
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if size >= large_limit:
            findings.append({"severity": "review", "kind": "large_tracked_file", "path": rel, "bytes": size, "limit": large_limit})

    return {"root": str(root), "tracked_files": len(files), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result["findings"]:
            print("repo-scan: no findings")
        for f in result["findings"]:
            detail = f.get("path", f.get("count", ""))
            print(f"{f['severity']:>6}  {f['kind']:<20} {detail}")
    return 1 if any(f["severity"] == "block" for f in result["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
