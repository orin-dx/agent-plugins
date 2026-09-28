# Changelog

— courier

## [3.0.3] - 2026-09-10

### Changed
- Commit, PR, review, changeset, release, and voice guidance now load through concern-first reference paths in both harnesses.
- Changeset documentation now names the exact delivery reference instead of a bare filename.

## [3.0.2] - 2026-09-09

### Changed
- `courier/pr` 2.0.1 now reports observed verification and unresolved gaps, omits empty sections, and separates independent topics.
- Agents state material concerns directly with evidence, consequence, and calibrated confidence.

## [3.0.1] - 2026-09-09

### Fixed
- Codex packaging now includes the voice guide loaded by Courier's runtime changeset guidance.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `delta` → `courier`. Skill names unchanged. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [2.1.3] - 2026-08-23

### Fixed
- `receive-feedback` and `README.md` claimed `review-preprocessor` categorizes incoming comments as must-fix/suggestion/question. It never did — its `<judgment>` forbids that call. Narrowed all claims to what it actually does: assemble a review package; the caller applies `shared/references/github.md`'s vocabulary by hand.

## [2.1.2] - 2026-08-22

### Changed
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [2.1.1] - 2026-08-21

### Changed
- `changeset-analyzer`'s topic-splitting now checks a linked spec/plan/requirement first, then explicit stated scope, falling back to diff-inferred cause only when neither applies — splitting on ambiguity alone is a rare fallback, not the default. Prevents the 2.1.0 split-by-topic change from over-fragmenting a deliberately-scoped effort.

## [2.1.0] - 2026-08-21

### Added
- `changeset-analyzer` now checks for multiple independent topics in a diff and emits one `changeset@2` per topic instead of one bundled entry; a normal single-PR diff still produces exactly one. Prompted by a real incident (sibling repo `callisto`) where a backlog/catch-up diff got bundled into one changeset spanning unrelated tracks. Output contract changes from a single object to an array of one-or-more.

## [2.0.0] - 2026-08-20

### Breaking
- Single `ship` skill replaced by six targeted skills: `commit`, `pr`, `changeset`, `receive-feedback`, `post-review`, `release`. `/delta:ship` and `/delta:review` must switch to the new names.
- `changeset-analyzer`/`release-summarizer` now produce/consume `changeset@2`/`release-artifact@2`. `@1` remain valid and unchanged; new consumers should target `@2`.
### Added
- `post-review` skill: posts an already-drafted review via `gh pr review`/`gh pr comment`, gated by explicit confirmation. Drafting critique of someone else's PR stays out of scope — that's `code-review`'s job.
- `consumer_impact`/`semver_impact` fields on `changeset@2`, set by `changeset-analyzer` at authoring time instead of guessed later. Summary detail scales with `semver_impact`.
- `docs-voice.md` reference — banned words, sentence-length ceiling, review-label vocabulary — embedded into the commit/PR/changeset references.
### Changed
- `release-artifact@2.changesets[]` consumes `consumer_impact`/`semver_impact` directly instead of redeclaring a `type` field; release version computed as `max(semver_impact)`.

## [1.3.0] - 2026-08-17

### Changed
- **Direct Evidence Citations**: Formatted changeset evidence pointers with direct file and line references.

## [1.2.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `delta:pr-narrator`, `delta:changeset-analyzer`, and `delta:release-summarizer`.
- **Direct Code Pointers**: Changeset analysis connects directly to test and code evidence produced during implementation.

## [1.1.0] - 2026-08-11
### Added
- `criteria_evidence` field in `changeset@1` — per-criterion evidence trail; `changeset-analyzer` accepts implementer's aggregated evidence directly instead of re-deriving it
- `linked_requirement` field in `changeset@1` — propagated from the linked spec/plan when available
### Changed
- `changeset-analyzer` falls back to file-level evidence rather than fabricating an unverifiable line number

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `delta` → `ship` (displays as `/delta:ship`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Full shipping pipeline: commit, PR creation, review response, changeset, release notes
- `release-artifact@1` output schema
- Subagents: commit-analyzer, pr-narrator, changeset-analyzer, review-preprocessor, release-summarizer
