#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import git_last_commit_epoch, load_config, path_matches, run_git, tracked_files


def uncommitted_files(root: Path) -> set[str]:
    proc = run_git(root, "status", "--porcelain=v1", "-z")
    if proc.returncode != 0:
        return set()
    out = set()
    parts = proc.stdout.split("\0")
    i = 0
    while i < len(parts):
        item = parts[i]
        if not item:
            i += 1
            continue
        status = item[:2]
        path = item[3:]
        if status[0] in "RC" and i + 1 < len(parts) and parts[i + 1]:
            out.add(parts[i + 1])
            i += 2
        else:
            out.add(path)
            i += 1
    return out


def scan(root: Path) -> dict:
    config = load_config(root)
    mappings = config.get("docs", {})
    files = tracked_files(root)
    dirty = uncommitted_files(root)
    findings = []
    for doc_path, spec in mappings.items():
        doc_path = str(doc_path)
        sources = [str(p) for p in spec.get("sources", [])]
        matched = [p for p in files if any(path_matches(p, pat) for pat in sources)]
        if not (root / doc_path).exists():
            findings.append({"kind": "missing_document", "document": doc_path, "sources": matched[:20]})
            continue
        doc_ts = git_last_commit_epoch(root, doc_path)
        newer = []
        for src in matched:
            if src in dirty:
                newer.append({"path": src, "reason": "uncommitted_change"})
                continue
            src_ts = git_last_commit_epoch(root, src)
            if doc_ts is not None and src_ts is not None and src_ts > doc_ts:
                newer.append({"path": src, "reason": "newer_commit"})
        if newer:
            findings.append({
                "kind": "review_document",
                "document": doc_path,
                "concerns": spec.get("concerns", []),
                "changed_sources": newer,
            })
    return {"configured_documents": len(mappings), "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not result["configured_documents"]:
        print("docs-drift: no [docs] mappings in .repo-steward.toml")
    elif not result["findings"]:
        print("docs-drift: no drift candidates")
    else:
        for f in result["findings"]:
            print(f"review  {f['document']}: {f['kind']}")
            for s in f.get("changed_sources", [])[:10]:
                print(f"        {s['path']} ({s['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
