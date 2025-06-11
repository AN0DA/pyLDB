Generate a concise, Conventional Commit message for a Python library.

Follow these rules:
Use one of these types: chore, docs, feat, fix, refactor, style, test, revert, perf, ci, merge.
Use a short, lowercase imperative summary (max 72 chars) after type(scope):.
Scope is optional but can specify a module or feature.
Use a blank line before the detailed body (if needed).
Body explains what, why, and how (if relevant).
Use present tense and avoid personal pronouns.
Reference issues or PRs if relevant (e.g., “Closes #123”).
For breaking changes, add a BREAKING CHANGE: section.
Do not use WIP in commit messages.

Examples:
feat(core): add async support to BDL client
fix(visualization): correct axis label formatting
docs: update usage section in README
refactor: simplify config loading logic
