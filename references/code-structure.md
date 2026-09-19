# Code structure

Use this workflow for large files, god modules, duplication, tangled dependencies, or cleanup requests.

## Start from responsibility, not line count

A 900-line parser with one coherent grammar may be healthier than five 180-line files connected by indirection. Line count is a prompt to inspect, not a reason to split.

Investigate:

- multiple unrelated responsibilities in one module
- functions mixing orchestration, I/O, validation, policy, and formatting
- repeated logic that can diverge
- dependency cycles or imports that cross intended boundaries
- `utils`, `helpers`, or `common` modules accumulating unrelated behavior
- long functions caused by many conceptual phases
- deep conditionals that encode a state machine implicitly
- abstractions with one implementation and no real boundary pressure
- wrappers whose only purpose is to rename another function
- repeated validation or derivation of the same data, including hand-written checks already guaranteed by a schema validator
- silent internal fallbacks or swallowed errors that hide broken invariants; validate at trust boundaries and express internal guarantees with types or assertions where appropriate
- parallel replacement implementations or compatibility parameters added only to avoid updating old callers; preserve compatibility when it is a real supported contract

## State, contracts, and dependency direction

For a full pass, or changes touching these boundaries:

- Identify the authoritative owner of state, events, configuration, and derived data. A cache or projection is legitimate when its derivation and invalidation are clear; competing writable authorities are a finding, not every duplicate representation.
- Check declared schema/API/protocol compatibility rules before changing a frozen contract. Require the repository's approval, versioning, and migration process; do not silently turn cleanup into a breaking change.
- Check the repository's architecture tests, import rules, or documented layering. Ensure new directories are covered by those checks; when no automation exists, inspect representative imports across the affected boundary.
- When removing a capability, remove obsolete configuration keys and consumers within the supported compatibility policy. Ensure new keys have readers and documented defaults or explicit required-value validation.

## Baseline first

Before structural changes, establish behavior with existing tests, a focused regression test, or a reproducible command. Refactoring without a baseline makes “cleanup” indistinguishable from accidental behavior change.

## Preferred refactoring order

1. Remove dead code and duplication with clear evidence.
2. Extract named local functions when they clarify phases without creating cross-file indirection.
3. Separate modules only when responsibilities or lifecycles are independently understandable.
4. Introduce interfaces/traits/protocols only when a real boundary needs them.
5. Move shared code only after two or more callers demonstrate stable shared behavior.
6. Re-run focused tests after each coherent step.

When a structural prerequisite enables a behavior change, separate the move/refactor from the behavior change into reviewable steps, and separate commits when appropriate. Align tests with the new responsibility boundaries when splitting modules; keep shared integration coverage where it still tests a cohesive workflow.

## Anti-overengineering gate

Reject a proposed abstraction when all are true:

- only one implementation exists;
- the wrapper adds no invariant or boundary;
- call sites become harder to trace;
- the abstraction is justified only by hypothetical future needs.

Reject mechanical file splitting when the result increases navigation cost without reducing conceptual load.

## Size signals

Default investigation signals:

- source file around 600+ non-blank lines: inspect responsibilities
- source file around 1000+ non-blank lines: high-priority inspection
- function around 80+ lines: inspect phases and nesting

These are not failures. Repository-specific conventions override them.
