# Repository hygiene

Use this workflow to find physical repository clutter and accidental artifacts.

## Inspect

1. Identify the repository root and local ignore rules.
2. List tracked files before reasoning from the working tree. A generated file that is ignored is different from one already committed.
3. Inspect root-level files, large tracked files, likely secrets, caches, virtual environments, build outputs, logs, backups, temporary exports, notebook outputs, and duplicated generated artifacts.
4. Check whether generated artifacts have a documented regeneration path.
5. Separate source-controlled fixtures and snapshots from accidental outputs.

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
