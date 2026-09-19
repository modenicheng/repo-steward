---
name: repo-steward
description: Keep software repositories lean, coherent, and current while coding, refactoring, reviewing, or cleaning up. Use for repository hygiene audits, code-structure cleanup, oversized-file or god-module investigation, documentation organization and drift prevention, AI-output cleanup, legacy repository rehabilitation, and pre-commit or pre-PR quality gates. Prefer deleting, consolidating, or reusing over adding files, abstractions, dependencies, comments, reports, or documentation.
---

# Repo Steward

Reduce repository entropy without replacing one kind of mess with another.

The default objective is not “more structure”. It is the smallest coherent repository that preserves behavior, intent, and maintainability.

## Core principles

1. Prefer deleting, consolidating, or reusing over adding.
2. Treat metrics and thresholds as investigation signals, never automatic verdicts.
3. Preserve behavior before refactoring. Establish a baseline with tests, reproducible commands, or explicit observed behavior.
4. Keep changes inside the task boundary. Do not opportunistically rewrite unrelated code or docs.
5. Do not create a new document when an existing canonical document can own the fact.
6. One durable fact should have one canonical owner. Other docs may link or summarize briefly.
7. Explain why, not what. Avoid comments and prose that merely restate code.
8. Do not create abstraction without pressure: repeated behavior, multiple implementations, a stable boundary, or demonstrated complexity.
9. Do not split a cohesive file solely to satisfy a line-count threshold.
10. Never delete uncertain files, generated artifacts with unclear provenance, migrations, fixtures, lockfiles, or user data without confirming their role.

## Route to focused guidance

Load only the references needed for the task:

- Repository clutter, ignored files, secrets, generated outputs, accidental binaries, root-directory mess: `references/repository-hygiene.md`
- Oversized files, god modules, duplication, deep nesting, confusing boundaries, premature abstraction: `references/code-structure.md`
- README/docs/ADR/AGENTS organization, stale commands, duplicated facts, architecture drift, plan lifecycle: `references/docs-maintenance.md`
- Verbose AI comments, redundant prose, unnecessary reports, noisy final responses: `references/output-hygiene.md`
- Commit or PR readiness, diff focus, docs impact, validation commands: `references/change-gate.md`
- Existing repository already messy and needs staged rehabilitation: `references/legacy-cleanup.md`
- Machine-readable ownership/configuration for docs and scans: `references/configuration.md`

## Standard operating sequence

Choose a pass depth without expanding the agreed task boundary:

| Pass | When | Coverage |
|---|---|---|
| Quick | Before handoff after a substantial or cross-cutting edit, or when a focused hygiene check is requested | Relevant checks, changed-code structure, every new file, and affected canonical docs. |
| Full | Milestone or phase closeout, broad cleanup, PR-batch closeout, or explicit hygiene audit | Quick coverage plus contracts, dependency direction, configuration, and documentation consistency across the agreed scope; use independent review for broad or high-risk work when available. |

For either pass:

1. Read local rules: `AGENTS.md`, `CONTRIBUTING.md`, manifests, CI, formatter/linter configs, and relevant docs.
2. Establish the change boundary: identify behavior, files, modules, or docs actually required.
3. Inspect before editing: search for existing utilities, canonical docs, similar modules, and established naming. Resolve material ambiguity from repository evidence first. Ask only when unresolved alternatives materially change behavior, compatibility, or scope; use established low-impact defaults otherwise. Recommend a simpler approach when it meets the same requirements.
4. Define observable success using `references/change-gate.md#acceptance-evidence`. For non-trivial multi-step work, pair significant implementation steps with corresponding verification in the working plan. Discover authoritative test, typecheck, and build commands from repository rules, manifests, and CI; run the narrowest useful baseline checks and record pre-existing failures or unavailable checks.
5. Make the smallest coherent change, following surrounding style and conventions. Do not add options, extension points, configuration, or fallback paths for hypothetical requirements; retain error handling justified by real inputs, trust boundaries, or supported contracts.
6. Check entropy: ask whether the change added unnecessary files, concepts, dependencies, comments, docs, or duplicated facts.
7. Validate and close findings using `references/change-gate.md`: targeted tests first, broader checks when warranted. A full pass also loads the code-structure and documentation guidance above.
8. Inspect the diff: remove accidental churn, temporary artifacts, debug output, unrelated formatting, stale docs, and code made unused by this change.
9. Report compactly: state what changed, what was validated, and remaining risks. Do not generate a second implementation report unless requested.

## Deterministic helpers

Use scripts as evidence collectors; do not let them replace engineering judgment.

```bash
python scripts/repo_scan.py /path/to/repo
python scripts/file_metrics.py /path/to/repo
python scripts/docs_inventory.py /path/to/repo
python scripts/docs_drift.py /path/to/repo
python scripts/diff_guard.py /path/to/repo --staged
```

All scripts use the Python standard library only.

## Decision rules before adding things

Before adding an artifact, answer the matching question:

- File: does it have an independent responsibility or lifecycle?
- Abstraction: is there actual repeated behavior, more than one implementation, or a stable boundary that pays for indirection?
- Document: which existing canonical document should own this fact?
- Dependency: can the standard library or an existing dependency solve this adequately?
- Comment: does it explain intent, invariants, non-obvious constraints, or a surprising tradeoff?
- Report: did the user request a durable report, or is a concise final response enough?

If the answer is weak, do not add it.

## Repository output policy

Do not create files such as `SUMMARY.md`, `ANALYSIS.md`, `IMPLEMENTATION_NOTES.md`, `FIX_REPORT.md`, `REFACTOR_REPORT.md`, or similar disposable artifacts unless the user explicitly asks for a durable document or repository conventions require one.

Do not leave scratch scripts, copied logs, generated screenshots, debug dumps, benchmark outputs, editor backups, or temporary exports in the repository.

Do not rewrite entire files merely to normalize style when the task only needs a small repair.

## Cleanup safety

Classify cleanup candidates:

- Safe: editor backups, known caches, reproducible generated outputs, duplicate temporary reports with a confirmed canonical owner.
- Review: old scripts, archived plans, fixtures, snapshots, generated code, vendored content, local configuration.
- Protected: migrations, lockfiles, legal files, release metadata, user data, secrets requiring rotation, artifacts with unknown regeneration paths.

Automatically remove only clearly safe items when cleanup is requested. Preserve review/protected items unless the user authorizes removal.

## Completion standard

A successful stewardship pass leaves the repository easier to navigate and cheaper to maintain, without hiding complexity behind more files or more prose.
