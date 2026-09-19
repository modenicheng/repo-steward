# Repo Steward

Repo Steward is an agent skill for keeping software repositories lean, coherent, and current while development continues.

It targets four forms of repository entropy:

- filesystem entropy: generated junk, caches, secrets, accidental binaries, temporary reports;
- code entropy: god modules, unclear responsibilities, duplication, wrong abstractions;
- documentation entropy: duplicated facts, stale commands, architecture drift, immortal plans;
- agent entropy: verbose comments, unnecessary Markdown artifacts, unrelated diffs, over-engineering.

The governing rule:

> Prefer deleting, consolidating, or reusing over adding.

## Install

Install with the [skills.sh](https://skills.sh) CLI:

```bash
npx skills add modenicheng/repo-steward
```

## Included workflows

`SKILL.md` routes tasks to focused references instead of loading one giant policy document. The documentation workflow in `references/docs-maintenance.md` defines canonical ownership, source-backed drift checks, minimal updates, deduplication, and plan retirement.

The bundled Python scripts use only the standard library and collect evidence rather than making destructive decisions:

```bash
python scripts/repo_scan.py /path/to/repo
python scripts/file_metrics.py /path/to/repo
python scripts/docs_inventory.py /path/to/repo
python scripts/docs_drift.py /path/to/repo
python scripts/diff_guard.py /path/to/repo --staged
```

Optional `.repo-steward.toml` configuration maps durable documents to source-of-truth paths. Start from `assets/repo-steward.toml`.

## Design stance

Repo Steward rejects several common AI coding failure modes:

- splitting cohesive files only because they are long;
- inventing interfaces and layers without actual pressure;
- creating a new document for every task;
- duplicating setup commands across README, AGENTS, and development docs;
- rewriting unrelated files while “cleaning up”;
- treating linter metrics as architecture decisions.

The skill composes with repository-specific `AGENTS.md`, CI, linters, formatters, and test suites instead of replacing them.

## Test

```bash
python -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
