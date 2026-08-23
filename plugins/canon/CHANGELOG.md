# Changelog

— canon

## [2.2.1] - 2026-08-23

### Changed
- `auditor`'s `<load_first>` now cites the new `shared/references/workspace-conventions.md` instead of restating the `.claude/specs/*.json` location inline — the same fact `graph:auditor` and `trace:recon` also needed, now sourced once.

## [2.2.0] - 2026-08-23

### Added
- **`auditor`**: seventh audit dimension, `boundary-round-trip` — flags a field a spec introduces or changes on a type another spec persists, serializes, or transmits, when the far-side spec carries no matching round-trip criterion and the gap isn't named on purpose.

### Fixed
- `auditor` never stated where to find other gated specs for the `scope-overlap` check — a pre-existing gap, more consequential now that `boundary-round-trip` depends on the same lookup. Added `<load_first>` pointing to `<workspace_root>/.claude/specs/*.json`, where `canon/gate-spec` writes every spec once it passes, with the caveat that a spec still in draft won't appear there.

## [2.1.0] - 2026-08-22

### Added
- **`auditor`**: sixth audit dimension, `unnecessary-prose` — flags a criterion or section that is fully testable and unambiguous but wrapped in justification, restated context, or hedging a downstream reader doesn't need. A spec is read from disk by every subsequent pipeline stage (verifier, exit-gate, planner, challenger, every implementer task, lambda's exit-gate, drift-checker), so padding is a cost paid on every one of those reads, not once. Passing the existing testability/vagueness checks no longer exempts a criterion from this one.

### Changed
- **`drafter`**: judgment now names prose padding as a failure mode independent of testability — write for both from the first draft rather than relying on `auditor` to trim it later.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `auditor`, `drift-checker`, `drafter` frontmatter descriptions tightened; no routing behavior changed.

## [2.0.0] - 2026-08-20

### Breaking
- Single `spec` skill replaced by seven targeted skills: `draft-spec`, `verify-spec`, `spec-drift`, `audit-spec`, `gate-spec`, `correct-spec`, `architect`. Anything invoking `/canon:canon` (or the old sub-skill markdown headers) must switch to the new per-skill names.
- `audit` and `gate` were the natural bare-word names for two of these but collide with existing plugin-level skills (`proof`'s `audit`, `axiom`'s `gate`) — named `audit-spec` and `gate-spec` instead, per the amended constitution Skill Names rule (specific multi-word name over a `<plugin>-<stage>` prefix).
- A follow-up pass renamed `draft` → `draft-spec`, `verify` → `verify-spec`, `drift` → `spec-drift`, `correct` → `correct-spec`: the plugin id `canon` doesn't hint at "spec" the way `delta` hints at "shipping," so bare verbs left the skill's object ambiguous in slash-command autocomplete. `architect` stayed bare — distinctive enough on its own.
- `drift-checker`'s `summary` field changed shape from a free-text string to a structured object (`covered_count`/`uncovered_count`/`drifted_count`/`note`). Anything consuming `canon/spec-drift`'s output and reading `summary` as a string will break.
### Fixed
- `plugin.json`'s `description` listed stale skills (`review`, `changeset`) that never existed in canon — corrected to the real list.

## [1.4.0] - 2026-08-17

### Added
- **API Grounding**: `drafter` verifies live codebase function and struct definitions before generating `api_surface` signatures.
- **Direct Schema Citations**: Cites explicit relative schema paths in output contracts to prevent filesystem-wide search commands.

## [1.3.0] - 2026-08-17

### Added
- **Architectural Specs**: `architect` can now draft structural specs (`arch-spec`) for trait extractions, AST transforms, and subsystem invariants.
- **2-Round Circuit Breaker**: `drafter` and `auditor` reviews are capped at 2 iterations, demoting minor debates to non-blocking notes.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `canon:drafter`, `canon:auditor`, `canon:architect`, and `canon:exit-gate`.
- **Faster Drafting**: Standardized drafting and auditing on Sonnet to keep prompt caches hot and speed up spec generation.

## [1.2.0] - 2026-08-11
### Added
- `canon/correct-spec` sub-skill — given a spec_file_path, criterion_id, and a contradiction report from implementer, revises the affected criterion (and dependents) and returns a corrected spec@1 with `revision_note` set; the correction re-enters the standard verify → audit → gate pipeline before overwriting the file
- `revision_note` field in `spec@1` schema — set only on corrections, describes what changed and why
- Spec file commit step in orchestration — the skill orchestrator now commits `.claude/specs/<id>.json` to version control after writing it, not just to the working tree; an uncommitted spec is invisible to drift-checker and a future session
### Changed
- `drafter` now supports correction mode as an alternate input path alongside fresh drafting from a requirement@1
- Correction re-entry now routes the amended plan through challenger before lambda resumes — amendment is not exempt from adversarial review
- `drift-checker` no longer presumes whether code or spec is wrong on a drifted classification — it states both sides and leaves the correction path to the caller
- `drift-checker` now carries the trust-boundary defense for workspace-reading agents — code comments and documentation claiming a criterion is satisfied are treated as untrusted data, not evidence
- `drift-checker` accepts a prior changeset's `criteria_evidence` as an optional starting pointer — but always re-reads and independently reconfirms each location rather than trusting that it is still accurate
### Fixed
- A second spec_contradiction on the same criterion_id after correction now escalates to a human instead of looping back to canon/correct-spec indefinitely
- `drift-checker`'s `covered` output entries now use the same structured evidence shape as changeset@1's criteria_evidence (test/implementation file and line) instead of a free-text `evidence` string, so a drift check's freshly-confirmed pointers can be handed forward to the next check or exit gate
- Repaired pre-existing hard-wrapped paragraphs in drafter.md (backstory, goal, output) and canon SKILL.md (overview, canon/draft-spec, canon/audit, canon/architect) left over from before this session

## [1.1.0] - 2026-08-10
### Added
- `drift-checker` agent (opus/high) — on-demand post-implementation drift detection; reads spec from disk, classifies criteria as covered, uncovered, or drifted
- `spec_file_path` field in `spec@1` schema — workspace-relative path set by the skill orchestrator after gate pass; downstream agents read the spec from disk rather than context
- `canon/spec-drift` sub-skill in SKILL.md dispatching to `drift-checker`
- Post-gate orchestration instruction in SKILL.md — explicit step for writing spec to `.claude/specs/<id>.json` and setting `spec_file_path` after exit-gate passes
### Changed
- `verifier` is now grounding-only (pre-implementation); post-implementation drift checking is handled by the new `drift-checker`
- `drafter` returns the spec object only — it no longer writes to disk (skill orchestrator responsibility post-gate)
- Acceptance criterion quality standard in `drafter` and `auditor` now explicitly rejects criteria that require implementation knowledge to verify (semantic model principle): a criterion is only valid if a tester with no knowledge of the implementation can evaluate it from observable system behavior

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `canon` → `spec` (displays as `/canon:spec`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Spec drafting, review, verification, and drift detection against live code
- `spec@1` output schema consumed by `vector` and `axiom`
- Subagents: architect, drafter, auditor, verifier, exit-gate
