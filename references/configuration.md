# Configuration

Repo Steward works without configuration. Add `.repo-steward.toml` only when repository-specific mappings or thresholds improve signal.

Start from `assets/repo-steward.toml`.

## Scan settings

```toml
[scan]
large_file_bytes = 1048576
root_file_warn = 20
warn_lines = 600
high_lines = 1000
ignore_paths = ["vendor/**"]
```

Thresholds are warning levels only.

## Documentation ownership

```toml
[docs."README.md"]
sources = ["package.json", "src/cli/**"]
concerns = ["install", "entrypoints"]

[docs."docs/architecture.md"]
sources = ["src/**", "migrations/**"]
concerns = ["module boundaries", "data flow"]
```

A source glob marks a document as a candidate for review when matching source files changed more recently in Git history.

Do not map every source file to every document. Broad mappings make drift checks noisy and useless.
