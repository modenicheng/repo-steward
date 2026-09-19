#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

from common import git_last_commit_epoch, tracked_files

DOC_SUFFIXES = {".md", ".mdx", ".rst"}
TEMP_STEMS = {"summary", "analysis", "implementation_notes", "fix_report", "refactor_report", "notes", "scratch"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def inventory(root: Path) -> dict:
    docs = []
    tracked = set(tracked_files(root))
    for rel in sorted(tracked):
        p = root / rel
        if p.suffix.lower() not in DOC_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        broken = []
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            dest = (p.parent / path_part).resolve()
            try:
                dest.relative_to(root.resolve())
            except ValueError:
                continue
            if not dest.exists():
                broken.append(target)
        stem = p.stem.lower().replace("-", "_").replace(" ", "_")
        docs.append({
            "path": rel,
            "headings": HEADING_RE.findall(text)[:20],
            "broken_local_links": broken,
            "temporary_name_signal": stem in TEMP_STEMS,
            "last_commit_epoch": git_last_commit_epoch(root, rel),
        })
    return {"documents": docs}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = inventory(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if not result["documents"]:
        print("docs-inventory: no tracked documents")
        return 0
    for doc in result["documents"]:
        flags = []
        if doc["temporary_name_signal"]:
            flags.append("temporary-name")
        if doc["broken_local_links"]:
            flags.append(f"broken-links={len(doc['broken_local_links'])}")
        suffix = "  [" + ", ".join(flags) + "]" if flags else ""
        print(doc["path"] + suffix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
