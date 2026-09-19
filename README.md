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

[SKILL.md](SKILL.md) defines quick and full stewardship passes and routes tasks to focused guidance. The [documentation workflow](references/docs-maintenance.md) owns documentation maintenance; the [change gate](references/change-gate.md) owns acceptance evidence, validation, review, and finding closure.

The bundled Python scripts use only the standard library and collect evidence rather than making destructive decisions. Run these from the skill directory, passing the target repository path:

```bash
python scripts/repo_scan.py /path/to/repo
python scripts/file_metrics.py /path/to/repo
python scripts/docs_inventory.py /path/to/repo
python scripts/docs_drift.py /path/to/repo
python scripts/diff_guard.py /path/to/repo --staged
```

Git-backed scans cover tracked files; inspect untracked files separately. `diff_guard.py` checks unstaged changes by default and staged changes with `--staged`. Documentation drift checks use configured source mappings and Git history to suggest review candidates, not prove drift.

Optional [configuration](references/configuration.md) defines scan thresholds and documentation ownership. Start from [the template](assets/repo-steward.toml).

## Design stance

The [core principles](SKILL.md#core-principles) favor coherent responsibilities and canonical ownership over mechanical splitting or extra artifacts. The skill composes with repository-specific `AGENTS.md`, CI, linters, formatters, and test suites instead of replacing them.

## Test

```bash
python -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
