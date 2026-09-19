# Legacy repository cleanup

Use when the repository already contains accumulated mess. Do not attempt a mega-refactor in one pass.

## Phase 1: survey

Collect evidence on:

- repository clutter and generated artifacts;
- large or multi-responsibility modules;
- duplicated logic;
- stale and duplicated docs;
- outdated dependencies only when dependency work is in scope;
- failing or missing validation paths;
- hotspots repeatedly changed together.

Produce a short prioritized plan. Avoid generating a permanent audit document unless requested.

## Phase 2: stabilize

Before structural cleanup:

- identify critical behavior;
- add focused regression coverage where absence of tests would make cleanup unsafe;
- document only non-obvious execution steps required to validate changes.

## Phase 3: clean in coherent slices

Preferred slice order:

1. obvious accidental artifacts;
2. dead code with evidence;
3. duplicated facts/docs;
4. local structural refactors with tests;
5. module boundary changes;
6. larger architectural work only if still justified.

Each slice should leave the repository valid and reviewable.

## Phase 4: prevent relapse

Add automation only for repeatable high-signal checks. Do not turn every cleanup observation into a new CI rule.

Good candidates include secret scanning, format/lint/test gates, generated-file checks, and selected documentation drift mappings.
