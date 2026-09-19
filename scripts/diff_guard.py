#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import load_config, path_matches, run_git

RISKY_BASENAMES = {".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json", "secrets.json", "token.txt"}
RISKY_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
CONFLICT_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.M)


def changed_files(root: Path, staged: bool, base: str | None) -> list[str]:
    if staged:
        args = ("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    elif base:
        args = ("diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD")
    else:
        args = ("diff", "--name-only", "--diff-filter=ACMR")
    proc = run_git(root, *args)
    return [p for p in proc.stdout.splitlines() if p.strip()] if proc.returncode == 0 else []


def diff_text(root: Path, staged: bool, base: str | None) -> str:
    if staged:
        args = ("diff", "--cached", "--unified=0")
    elif base:
        args = ("diff", "--unified=0", f"{base}...HEAD")
    else:
        args = ("diff", "--unified=0")
    proc = run_git(root, *args)
    return proc.stdout if proc.returncode == 0 else ""


def numstat(root: Path, staged: bool, base: str | None) -> dict[str, int]:
    if staged:
        args = ("diff", "--cached", "--numstat")
    elif base:
        args = ("diff", "--numstat", f"{base}...HEAD")
    else:
        args = ("diff", "--numstat")
    proc = run_git(root, *args)
    out = {}
    if proc.returncode != 0:
        return out
    for line in proc.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        a, d, path = parts
        if a.isdigit() and d.isdigit():
            out[path] = int(a) + int(d)
    return out


def scan(root: Path, staged: bool = False, base: str | None = None) -> dict:
    files = changed_files(root, staged, base)
    stats = numstat(root, staged, base)
    blockers = []
    warnings = []
    for rel in files:
        p = Path(rel)
        if p.name.lower() in RISKY_BASENAMES or p.suffix.lower() in RISKY_SUFFIXES:
            blockers.append({"kind": "risky_file", "path": rel})
        if stats.get(rel, 0) >= 800:
            warnings.append({"kind": "large_diff", "path": rel, "changed_lines": stats[rel]})
    text = diff_text(root, staged, base)
    added = "\n".join(line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++"))
    if CONFLICT_RE.search(added):
        blockers.append({"kind": "conflict_marker_in_added_lines"})

    config = load_config(root)
    for doc, spec in config.get("docs", {}).items():
        sources = [str(x) for x in spec.get("sources", [])]
        touched = [f for f in files if any(path_matches(f, pat) for pat in sources)]
        if touched and str(doc) not in files:
            warnings.append({"kind": "docs_impact", "document": str(doc), "changed_sources": touched})

    return {"changed_files": files, "blockers": blockers, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--staged", action="store_true")
    group.add_argument("--base")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(Path(args.root).resolve(), args.staged, args.base)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for f in result["blockers"]:
            print("block  " + f["kind"] + ("  " + f["path"] if "path" in f else ""))
        for f in result["warnings"]:
            print("review " + f["kind"] + ("  " + f.get("path", f.get("document", ""))))
        if not result["blockers"] and not result["warnings"]:
            print("diff-guard: no findings")
    return 1 if args.strict and result["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
