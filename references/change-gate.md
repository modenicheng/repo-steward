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

Large diffs, large files, TODOs, and doc recency are review signals, not automatic blockers.
