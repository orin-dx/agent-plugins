# Changesets Reference

Changesets are structured records of what changed and why, used to generate release notes and communicate changes to consumers.

## The changeset@2 Schema

Supersedes `changeset@1` (`shared/schemas/changeset@1.json`, still valid, now legacy) by adding required `consumer_impact` and `semver_impact`. `changeset-analyzer` produces `changeset@2` — see `shared/schemas/changeset@2.json`.

```json
{
  "summary": "Add cross-language recon agent to proof plugin",
  "consumer_impact": "new-capability",
  "semver_impact": "minor",
  "files_changed": ["plugins/proof/subagents/recon.md"],
  "tests_added": [],
  "acceptance_criteria_met": ["SPEC-001-AC-3", "SPEC-001-AC-4"],
  "breaking_changes": [],
  "commits": ["abc1234"],
  "linked_spec": "SPEC-001",
  "linked_plan": "PLAN-001"
}
```

## Consumer Impact Classification

Set at authoring time, per changeset — not guessed later at release time:

| `consumer_impact` | Meaning |
|---|---|
| `behavior-change` | An existing, observable behavior changed for someone outside this repo |
| `new-capability` | Something new is now possible that wasn't before |
| `internal-only` | No observable effect outside this repo (refactor, internal tooling, test-only) |

`release-summarizer` filters out `internal-only` entries automatically — they never need a human decision about inclusion.

## One Changeset Per Topic

A changeset is one coherent, single-sentence-describable change — not a diff, and not a file/package/commit count. Bundling unrelated topics and fragmenting one coherent effort are equally real failure modes.

What belongs together, in order of how much weight the signal carries:

1. **Shared `linked_spec`/`linked_plan`/`linked_requirement`** — a scope decision already made before the code existed, so it outweighs anything read from the diff. A testing push scoped as one requirement is one changeset even across every package.
2. **An explicitly stated shared scope** from whoever handed over the diff ("a coordinated testing push," "shipping these together") — trust it.
3. **Shared cause read from the diff**, only absent 1 and 2: does one part exist *because of* another (one changeset), or would each have happened independently (separate changesets)? An "and" joining two unrelated things is two changesets.

Check 1 and 2 before falling back to 3 — most real cases resolve there. Splitting on genuine ambiguity is a fallback, not a default; reaching for it first produces changeset sprawl. Verify a split topic's `consumer_impact`/`semver_impact`/`files_changed` against its own diff slice, not the whole batch's summary — note anything unresolved in `reasoning` rather than assigning it by guess.

## Voice

Separate *what changed* (factual) from *why* (one clause) — don't blend them. Detail scales with `semver_impact`: `patch`/`internal-only` gets one clause, `minor` gets one sentence plus an optional one-clause why, `major` requires each `breaking_changes` entry to state old behavior → new behavior → what the caller does about it. No banned words (*delve, leverage, seamless, robust, elevate, foster, unlock, empower, testament, pivotal, showcase, meticulous, game-changer, utilize*). Full standard: `shared/references/docs-voice.md`.

## Changeset vs. Commit Message

- **Commit message**: for developers reading git history. Explains the technical change.
- **Changeset summary**: for consumers of the package. Explains the user-visible impact.

Same change, two framings:
- Commit: `refactor(proof): extract language detection into recon subagent`
- Changeset: `Proof plugin now detects workspace language automatically before scanning`

## Release Notes Generation

The `delta/release` skill aggregates changeset summaries by `semver_impact` (breaking/feature/fix), filtering out `consumer_impact: internal-only` entries:

```markdown
## v2.0.0 (2026-08-04)

### Breaking Changes
- Plugin IDs renamed: bug-hunter-rust → proof, agent-plugin-builder → basis

### New Features
- axiom exit gate with retry-with-feedback for all stage transitions
- proof plugin with cross-language recon and adversarial verification

### Bug Fixes
- ...
```

## When to Write a Changeset

Write a changeset for every PR that:
- Adds a new skill or subagent
- Changes a subagent's model or effort tier
- Modifies a shared schema (always breaking if fields removed)
- Renames a plugin ID
- Changes the axiom protocol or retry behavior

Skip changesets for:
- Pure documentation changes
- Reference file updates
- Internal refactors with no behavioral change

**Check this list before reaching for the Semver Decision Guide below, not after.** The failure mode this guards against is real: rewriting a plugin's own self-description (fixing a fictional or stale claim in its `SKILL.md`/`README.md`) touches files but changes no behavior — it belongs on this skip list, not on the bump table. Jumping straight to "how much do I bump" skips the "should I bump at all" question the skip list exists to ask first. If nothing on the "when to write" list above applies and nothing changed for anyone outside this repo, stop here — no changeset, no version bump, no tag.

## Semver Decision Guide

This table is machine-enforced: `changeset-analyzer` sets `semver_impact` directly from it at authoring time. `release-summarizer` does not re-derive semver from prose — it takes `max(semver_impact)` across the changesets included in a release.

| Change | Version bump |
|---|---|
| Pure documentation or self-description fix, no behavior change | **none — see "Skip changesets for" above, do not bump** |
| New plugin, no schema change | minor |
| New field in existing schema (optional) | minor |
| Removed or renamed field in existing schema | major + new file |
| New schema file | minor |
| Bug fix in subagent prompt (changes actual behavior) | patch |
| New skill within existing plugin | minor |
| Renamed plugin ID | major |
