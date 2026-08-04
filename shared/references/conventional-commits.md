# Conventional Commits Reference

**Format:** `<type>(<scope>): <description>`

Types: `feat` `fix` `docs` `style` `refactor` `test` `chore` `perf` `ci` `build` `revert`

Breaking change: append `!` after type/scope, or add `BREAKING CHANGE:` footer.

## Rules

- Subject line: imperative mood, no period, under 72 characters
- Body (optional): explain the *why*, not the what. Wrap at 72 characters.
- Footer: `BREAKING CHANGE: <description>`, `Fixes #123`, `Refs #456`
- Scope is optional; when used, it names the module or component

## Examples

```
feat(delta): add changeset generation skill

fix(axiom): retry gate passes specific failure message to producer

docs(shared): add conventional-commits reference

refactor(proof): extract language detection into recon subagent

feat!: rename bug-hunter-rust to proof

BREAKING CHANGE: plugin ID changed from bug-hunter-rust to proof.
Update marketplace.json and skill trigger references.
```

## Commit Message Body

The body answers: why was this change needed? What problem does it solve?

Don't describe what the code does (the diff shows that). Write what a reviewer needs to understand the intent.

## Scope Conventions (this repo)

| Scope | Covers |
|---|---|
| `axiom` | axiom plugin and subagents |
| `proof` | proof plugin and subagents |
| `delta` | delta plugin and subagents |
| `graph` | graph plugin and subagents |
| `canon` | canon plugin and subagents |
| `trace` | trace plugin and subagents |
| `vector` | vector plugin and subagents |
| `lambda` | lambda plugin and subagents |
| `basis` | basis plugin and subagents |
| `shared` | shared schemas, references, agent-best-practices |
