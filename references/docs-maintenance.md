# Documentation maintenance

Use this as the documentation sub-workflow. Its purpose is to prevent both missing documentation and documentation sprawl.

## Principle: one durable fact, one canonical owner

Do not copy the same setup command, architectural rule, or configuration truth into several long-lived documents. Pick one owner and let other documents link or summarize briefly.

A practical default role map:

- `README.md`: project purpose, quick start, primary entry points; not full architecture.
- `AGENTS.md`: instructions for agents/contributors, commands, constraints, repository conventions; not a duplicate README.
- `docs/architecture.md`: current system structure, boundaries, data flow, invariants; not historical discussion.
- `docs/decisions/*.md`: why important decisions were made; append historical decisions instead of rewriting history.
- `docs/development.md`: durable local development, test, debug, and release workflows.
- `CHANGELOG.md` or release notes: time-ordered user-visible change history.
- `docs/plans/`: temporary plans. Archive or delete them after completion instead of letting them masquerade as current architecture.

Do not force this exact layout when the repository already has clear roles. Preserve coherent local conventions.

## Workflow

### 1. Inventory documents

Identify durable docs, temporary plans, generated docs, duplicated guides, and files with unclear ownership.

For each durable doc, determine:

- intended audience;
- facts it canonically owns;
- source files/configuration that can invalidate those facts;
- whether another document repeats the same content.

### 2. Determine the change surface

For a code/config change, identify facts that may have changed:

- commands and flags;
- package names and paths;
- environment variables;
- public APIs;
- configuration schema;
- module boundaries;
- persistence/schema behavior;
- deployment or release workflow;
- user-facing behavior.

Do not open every document reflexively. Read the documents that own those facts.

### 3. Compare docs with sources of truth

Prefer executable/configured evidence over prose:

- manifests and scripts for commands;
- router/CLI declarations for interfaces;
- schemas/migrations for persistence;
- CI workflows for validation/release behavior;
- code boundaries for architecture claims.

Git recency is a drift signal, not proof. A source file changing after a document means “inspect this doc”, not “rewrite this doc”.

### 4. Apply a minimal patch

Correct stale facts without opportunistic rewriting. Preserve unaffected wording and structure unless the current structure itself causes duplication or confusion.

When two docs duplicate the same fact:

1. choose the canonical owner;
2. keep full detail there;
3. replace duplicate detail elsewhere with a short summary or link;
4. verify links and anchors.

### 5. Retire temporary documents

For completed plans, investigations, and implementation notes:

- delete them if they have no enduring value;
- archive them if historical reasoning matters;
- promote only durable conclusions into canonical docs;
- never leave a completed plan as a second source of current truth.

### 6. Verify

Check:

- links and referenced paths;
- commands that can be run cheaply;
- renamed symbols and configuration keys;
- examples affected by API changes;
- duplicate facts across durable docs;
- stale “planned”, “TODO”, “future”, or “not implemented” claims.

### 7. Record ownership only when useful

For repositories with recurring drift, create `.repo-steward.toml` mapping docs to source paths. Do not add it to tiny repositories that do not need machine-assisted drift checks.

Example:

```toml
[docs."README.md"]
sources = ["pyproject.toml", "src/cli/**"]
concerns = ["install", "entrypoints", "basic usage"]

[docs."docs/architecture.md"]
sources = ["src/**", "migrations/**"]
concerns = ["module boundaries", "data flow", "persistence"]
```

## Documentation anti-patterns

Avoid:

- `SUMMARY.md`, `ANALYSIS.md`, and task reports committed only because an agent produced them;
- README sections that duplicate detailed development docs;
- architecture documents describing intentions rather than current behavior without clearly marking them as proposals;
- duplicated command snippets that drift independently;
- giant “everything” docs that mix onboarding, design history, API reference, and operations;
- updating a timestamp without verifying content.
