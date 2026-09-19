# Repository hygiene

Use this workflow to find physical repository clutter and accidental artifacts.

## Inspect

1. Identify the repository root and local ignore rules.
2. List tracked files and non-ignored untracked files separately (`git ls-files --others --exclude-standard`). Inspect new files before staging as well as the diff. A generated file that is ignored is different from one already committed.
3. Inspect root-level files, large tracked files, likely secrets, caches, virtual environments, build outputs, logs, backups, temporary exports, notebook outputs, and duplicated generated artifacts.
4. Check whether generated artifacts have a documented regeneration path.
5. Separate source-controlled fixtures and snapshots from accidental outputs.

In Git repositories, the inventory/scan helpers enumerate tracked files only; separately inspect untracked files rather than treating a clean scan as complete coverage. `repo_scan.py` supplies name, path, and size signals, not proof of provenance or safe deletion. Regeneration paths, fixture intent, and overlapping configuration still require inspection.

## Signals worth checking

- `*.log`, `*.tmp`, `*.bak`, `*.orig`, swap files, editor autosaves
- `.env`, credential-like names, private keys, token dumps
- `node_modules`, `.venv`, `target`, `dist`, `build`, coverage outputs, caches
- large binaries where source or release storage would be more appropriate
- root directories containing unrelated scratch files or one-off scripts
- generated assets whose source is missing
- duplicate config files with overlapping ownership

## Do not over-clean

Do not delete lockfiles, migrations, fixtures, snapshots, vendored assets, generated source, model files, notebooks, or binaries merely because they are large. First determine whether they are intentional repository inputs.

Do not impose a generic `src/` layout on a repository whose current layout is coherent.

## Repair order

1. Remove clearly accidental tracked junk.
2. Add or tighten ignore rules only for genuinely generated/local artifacts.
3. Move intentional but misplaced files only when the new location clarifies ownership.
4. Consolidate duplicates after identifying a canonical owner.
5. Document regeneration only when it is non-obvious and durable.
6. Re-run the scan and inspect the diff.
