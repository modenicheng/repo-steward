# Output hygiene

Use this guidance to reduce AI-generated clutter in code, docs, and final responses.

## Code comments

Keep comments that explain:

- non-obvious invariants;
- why a strange workaround exists;
- compatibility constraints;
- performance or safety tradeoffs;
- protocol or algorithm intent that code alone does not reveal.

Remove comments that merely narrate the next line, repeat names, or explain ordinary syntax.

## Documentation prose

Prefer concrete statements, commands, filenames, and behavior. Avoid ceremonial sections, marketing language, repeated summaries, and generic “best practices” prose with no repository-specific value.

Do not expand a short explanation into a taxonomy unless the taxonomy helps a real decision.

## Agent-created artifacts

Default to no persistent report. Return findings in the conversation unless the user requests a durable artifact or the repository convention requires one.

Before creating Markdown, ask whether an existing document owns the content. If yes, update it instead.

## Final response

Default structure:

1. what changed;
2. validation performed;
3. unresolved risks or intentionally deferred work.

Avoid narrating every command, repeating the task, or creating a long retrospective after a straightforward change.
