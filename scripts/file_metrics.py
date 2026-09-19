#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import ignored_by_config, load_config, tracked_files

SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".rs", ".go", ".py",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".java", ".kt", ".kts", ".cs",
    ".rb", ".php", ".swift", ".scala", ".zig", ".lua", ".sh", ".bash",
}


def count_lines(path: Path) -> tuple[int, int] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    lines = text.splitlines()
    return len(lines), sum(1 for line in lines if line.strip())


def scan(root: Path, warn_lines: int | None = None, high_lines: int | None = None) -> dict:
    config = load_config(root)
    cfg = config.get("scan", {})
    warn = int(warn_lines or cfg.get("warn_lines", 600))
    high = int(high_lines or cfg.get("high_lines", 1000))
    findings = []
    for rel in tracked_files(root):
        if ignored_by_config(rel, config) or (root / rel).suffix.lower() not in SOURCE_SUFFIXES:
            continue
        counts = count_lines(root / rel)
        if counts is None:
            continue
        total, nonblank = counts
        if nonblank >= warn:
            findings.append({
                "severity": "high" if nonblank >= high else "review",
                "path": rel,
                "lines": total,
                "nonblank_lines": nonblank,
            })
    findings.sort(key=lambda x: x["nonblank_lines"], reverse=True)
    return {"warn_lines": warn, "high_lines": high, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--warn-lines", type=int)
    ap.add_argument("--high-lines", type=int)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(Path(args.root).resolve(), args.warn_lines, args.high_lines)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif not result["findings"]:
        print("file-metrics: no size signals")
    else:
        for f in result["findings"]:
            print(f"{f['severity']:>6}  {f['nonblank_lines']:>6} nonblank  {f['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
