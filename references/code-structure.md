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

## Baseline first

Before structural changes, establish behavior with existing tests, a focused regression test, or a reproducible command. Refactoring without a baseline makes “cleanup” indistinguishable from accidental behavior change.

## Preferred refactoring order

1. Remove dead code and duplication with clear evidence.
2. Extract named local functions when they clarify phases without creating cross-file indirection.
3. Separate modules only when responsibilities or lifecycles are independently understandable.
4. Introduce interfaces/traits/protocols only when a real boundary needs them.
5. Move shared code only after two or more callers demonstrate stable shared behavior.
6. Re-run focused tests after each coherent step.

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
