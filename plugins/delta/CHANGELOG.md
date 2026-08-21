# Changelog

— delta

## [2.1.1] - 2026-08-21

### Changed
- `changeset-analyzer`'s topic-splitting judgment now checks `linked_spec`/`linked_plan`/`linked_requirement` first, then explicitly stated shared scope, falling back to diff-inferred shared cause only when neither applies — splitting on ambiguity alone is a rare fallback, not the default. Prompted by concern that the 2.1.0 split-by-topic change could over-fragment a deliberately-scoped effort (e.g. a themed feature batch or a testing push) into many tiny changesets. `shared/references/changesets.md` updated to match.

## [2.1.0] - 2026-08-21

### Added
- `changeset-analyzer` now checks whether a diff contains multiple independent topics before classifying anything, and emits one `changeset@2` per topic instead of one bundled entry — the normal single-PR case still produces exactly one changeset, unchanged. Prompted by a real incident in a sibling repo (`callisto`) where a large backlog/catch-up diff got bundled into one changeset spanning unrelated tracks, with package attribution guessed from a written summary instead of verified per-topic against the actual diff. `changeset-analyzer`'s output contract changes from a single object to an array of one-or-more; `delta/changeset`'s `<io>` section updated to match.

## [2.0.0] - 2026-08-20

### Breaking
- Single `ship` skill replaced by six targeted skills: `commit`, `pr`, `changeset`, `receive-feedback`, `post-review`, `release`. The old `delta/review` and `delta/receive` alias pair is gone — `receive-feedback` is now the one name for triaging incoming feedback. Anything invoking `/delta:ship` or `/delta:review` must switch to the new names.
- A follow-up pass renamed `receive` → `receive-feedback`: bare "receive" didn't say what, and this plugin already has a `post-review` right next to it for symmetry.
- `changeset-analyzer` and `release-summarizer` now produce and consume `changeset@2`/`release-artifact@2` instead of `@1`. `changeset@1`/`release-artifact@1` are unchanged and remain valid per this repo's schema-immutability rule — new consumers should target `@2`.
### Added
- `post-review` skill: mechanical, no new subagent. Posts an already-drafted review or reply via `gh pr review`/`gh pr comment`, gated by explicit confirmation. Drafting critique of someone else's PR stays out of scope for delta — that's the built-in `code-review` skill's job.
- `consumer_impact` and `semver_impact` fields on `changeset@2`, set by `changeset-analyzer` at authoring time instead of guessed later at release time. Changeset summary detail now scales with `semver_impact`.
- `docs-voice.md` reference — the repo's voice standard (banned words, sentence-length ceiling, inverted pyramid, Conventional Comments/Google review-label vocabulary), embedded into `conventional-commits.md`, `github.md`, and `changesets.md`.
### Changed
- `release-artifact@2.changesets[]` no longer redeclares a separate `type` field — it consumes `changeset@2.consumer_impact`/`semver_impact` directly. `release-summarizer` computes the release version as `max(semver_impact)` instead of re-deriving type from prose.

## [1.3.0] - 2026-08-17

### Changed
- **Direct Evidence Citations**: Formatted changeset evidence pointers with direct file and line references.

## [1.2.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `delta:pr-narrator`, `delta:changeset-analyzer`, and `delta:release-summarizer`.
- **Direct Code Pointers**: Changeset analysis connects directly to test and code evidence produced during implementation.

## [1.1.0] - 2026-08-11
### Added
- `criteria_evidence` field in `changeset@1` schema — per-criterion evidence trail (test file/line, implementation file/line); `changeset-analyzer` now accepts implementer's aggregated criteria_evidence as optional input and uses it directly instead of re-deriving locations from the diff
- `linked_requirement` field in `changeset@1` schema — propagated from the linked spec@1 or plan@1 when available
### Changed
- `changeset-analyzer` falls back to file-level (no line number) evidence when reconstructing from a diff alone rather than fabricating a line number it cannot verify

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
