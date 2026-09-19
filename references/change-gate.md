# Change gate

Use before commit, pull request, or handoff.

## Diff focus

Inspect changed files and ask:

- Does every changed file serve the requested task?
- Did formatting or generated output touch unrelated files?
- Did a cleanup silently change behavior?
- Did the change add temporary reports, logs, screenshots, dumps, or local config?
- Did a rename leave stale references?

Prefer explicit staging over indiscriminate `git add .` when repository state contains unrelated work.

## Validation order

1. format/check only affected files when supported;
2. run focused unit/regression tests;
3. run typecheck/lint/build relevant to changed components;
4. run broader project checks when change scope warrants it;
5. inspect the final diff after tools modify files.

Do not claim checks passed if they did not run.

If a baseline check fails, distinguish pre-existing failures from regressions before continuing dependent cleanup. Fix in-scope regressions and rerun affected checks; report unrelated failures without claiming a clean gate.

## Independent review and closure

For a full pass, request a read-only independent reviewer when available. Supply the agreed scope, baseline commit or tag, current diff (including staged and unstaged edits), new files, relevant repository rules, and validation results. Review the affected files and their callers, not just changed lines. Use [code structure](code-structure.md) and [documentation maintenance](docs-maintenance.md) for the relevant criteria rather than duplicating a second checklist here.

Request evidence-backed findings as `file:line [P1|P2|P3] problem; suggested repair`; do not invent findings to fill categories. Resolve confirmed P1/P2 issues within scope before closing the gate, then rerun affected validation and review the repairs. If a repair requires destructive action, a contract change, or scope expansion, report it as blocked instead of proceeding without authorization. Put non-blocking P3 items in an existing issue/backlog mechanism or the final response, not a new report file.

When no independent reviewer is available, perform an explicit second pass and disclose that independence was unavailable. Do not describe self-review as independent review.

## Documentation impact

Check docs when the diff changes any durable fact: commands, config, API, paths, architecture, deployment, schemas, or user-visible behavior.

Do not update docs merely because source files changed.

## Blocking findings

Treat these as high-confidence blockers unless explicitly intended:

- secret/private-key material added to the diff;
- merge conflict markers;
- accidental debug dumps or local environment files;
- broken tests introduced by the change;
- generated artifact churn with no source change or explanation.

Large diffs, large files, TODOs, and doc recency are review signals, not automatic blockers. Review new TODO/FIXME/HACK markers in context against the change baseline; counts alone neither prove debt nor justify deleting useful markers. Respect an existing repository debt-baseline policy without introducing a second baseline system.
