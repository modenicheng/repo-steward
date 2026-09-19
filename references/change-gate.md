# Change gate

Use before commit, pull request, or handoff.

## Diff focus

Inspect changed files and ask:

- Does each changed hunk serve the requested task or a necessary prerequisite?
- Did formatting or generated output touch unrelated files?
- Did a cleanup silently change behavior?
- Did the change add temporary reports, logs, screenshots, dumps, or local config?
- Did a rename leave stale references?

Remove imports, variables, helpers, and references made unused by this change once their lack of remaining consumers is verified. Report pre-existing dead code outside the agreed scope rather than deleting it; an explicit cleanup task may include it, subject to the skill's cleanup safety rules.

Prefer explicit staging over indiscriminate `git add .` when repository state contains unrelated work.

## Acceptance evidence

Turn the requested outcome into an observable check before implementation:

- Bug repair: reproduce the reported failure with a focused test or command, then verify the repair against that same case.
- Validation change: check invalid inputs are rejected and supported valid inputs still succeed.
- Refactoring: establish equivalent behavior before and after, not merely a smaller file or a green unrelated suite.
- Documentation change: verify the affected facts against their authoritative source and check changed links; passing code tests alone does not establish prose correctness.

Use existing checks when they demonstrate the outcome; add focused coverage when they do not. After a failed check, investigate, make an in-scope correction, and rerun it. Do not weaken the criterion just to obtain a pass. If verification is unavailable or a repair needs a user decision, report the specific limitation rather than claiming completion.

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
