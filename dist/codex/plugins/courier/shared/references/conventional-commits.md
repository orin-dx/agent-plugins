# Conventional Commits Reference

**Format:** `<type>(<scope>): <description>`

Types: `feat` `fix` `docs` `style` `refactor` `test` `chore` `perf` `ci` `build` `revert`

Breaking change: append `!` after type/scope, or add `BREAKING CHANGE:` footer.

## Rules

- Subject line: imperative mood, no period, under 72 characters
- Body (optional): explain the *why*, not the what. Do not artificially wrap lines — one paragraph per line, let the terminal/renderer soft-wrap.
- Footer: `BREAKING CHANGE: <description>`, `Fixes #123`, `Refs #456`
- Scope is optional; when used, it names the module or component

## Examples

```
feat(courier): add changeset generation skill

fix(sentinel): retry gate passes specific failure message to producer

docs(shared): add conventional-commits reference

refactor(ranger): extract language detection into recon subagent

feat!: rename bug-hunter-rust to proof

BREAKING CHANGE: plugin ID changed from bug-hunter-rust to proof.
Update marketplace.json and skill trigger references.

feat!: rename proof to ranger

BREAKING CHANGE: plugin ID changed from proof to ranger.
Update marketplace.json and skill trigger references.
```

## Commit Message Body

The body answers: why was this change needed? What problem does it solve?

Don't describe what the code does (the diff shows that). Write what a reviewer needs to understand the intent.

## Voice

Active voice, imperative mood. If a sentence keeps running, it's usually doing two jobs — split it rather than trimming words to make it fit. No banned words: *delve, leverage, seamless, robust, elevate, foster, unlock, empower, testament, pivotal, showcase, meticulous, game-changer, utilize* (use "use"). Full standard: `shared/references/docs-voice.md`.

## Scope Conventions (this repo)

| Scope | Covers |
|---|---|
| `sentinel` | sentinel plugin and subagents |
| `ranger` | ranger plugin and subagents |
| `courier` | courier plugin and subagents |
| `weaver` | weaver plugin and subagents |
| `scribe` | scribe plugin and subagents |
| `vanguard` | vanguard plugin and subagents |
| `navigator` | navigator plugin and subagents |
| `smith` | smith plugin and subagents |
| `mason` | mason plugin and subagents |
| `muse` | muse plugin and subagents |
| `shared` | shared schemas, references, agent-best-practices |
