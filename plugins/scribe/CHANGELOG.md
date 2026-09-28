# Changelog

— scribe

## [3.3.3] - 2026-09-27

### Changed
- `scribe:architect` now loads decision-record guidance when an accepted record governs the area or the fix rejects a plausible alternative.

## [3.3.2] - 2026-09-10

### Changed
- Architecture and workspace guidance now load through concern-first reference paths in both harnesses.

## [3.3.1] - 2026-09-09

### Changed
- Architecture-smell guidance now starts from live responsibilities and invariants, tests competing explanations, and leaves implementation shape open unless evidence constrains it.
- Agents state structural concerns directly with evidence, consequence, and calibrated confidence.

## [3.3.0] - 2026-09-09

### Added
- Architecture remediation support for Python and Go structural smells.

### Changed
- `scribe:architect` consumes `finding-report@2`, `implementation-review@2`, and architecture-escalating `implementation-result@1` artifacts.
- `scribe:gate-spec` returns `verdict@3` with verified scope, coverage gaps, and pending checks.

## [3.2.0] - 2026-09-09

### Added
- `scribe:architect` now consumes Smith's `implementation-review@1` as well as Ranger's `finding-report@1`.
- Architectural remediation loads the persisted model location and language smells through one phase reference, then uses defect-family evidence to choose the smallest enforceable correction.
- Architect uses review workspace lineage for live inspection and carries requirement lineage into the structural spec.
- After Smith verifies a structural remediation, `scribe:audit-architecture` refreshes the persisted model with the new boundary and invariant.

## [3.1.0] - 2026-09-02

### Added
- **`scribe/audit-architecture`** (new skill, `arch-auditor` agent): checks a draft spec@1 against a persisted, workspace-wide `arch-model@1` for boundary violations, competing abstractions, and invariant conflicts — closing the gap where every existing check was spec-vs-spec or spec-vs-a-narrow-code-slice, never spec-vs-system. Runs between `scribe/audit-spec` and `scribe/gate-spec`; also builds/refreshes the model itself, bootstrapping when absent.
- New schemas `shared/schemas/arch-model@1.json` and `shared/schemas/arch-audit@1.json`.

### Changed
- Gated specs now write to `docs/specs/<id>.json` by default, replacing `.claude/specs/<id>.json`. Not breaking: prior `spec_file_path` values still resolve; only the default write location for new gates changed.
- **`architect`** moved from `opus/high` to `claude-fable-5-1/high`, matching the new `arch-auditor`'s tier for the same shape of whole-system reasoning.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `canon` → `scribe`. Skill names unchanged. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [2.2.1] - 2026-08-23

### Changed
- `auditor`'s `<load_first>` now cites `shared/references/workspace-conventions.md` instead of restating the spec-location fact inline.

## [2.2.0] - 2026-08-23

### Added
- **`auditor`**: seventh audit dimension, `boundary-round-trip` — flags a field a spec introduces or changes on a type another spec persists or transmits, when the far side has no matching round-trip criterion and the gap isn't named on purpose.

### Fixed
- `auditor` never stated where to find other gated specs for the `scope-overlap` check. Added `<load_first>` pointing to `<workspace_root>/.claude/specs/*.json`.

## [2.1.0] - 2026-08-22

### Added
- **`auditor`**: sixth audit dimension, `unnecessary-prose` — flags a fully testable, unambiguous criterion or section still wrapped in justification or hedging a downstream reader doesn't need. A spec is read from disk at every pipeline stage, so padding is a cost paid on every read.

### Changed
- **`drafter`**: judgment now names prose padding as its own failure mode, independent of testability.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [2.0.0] - 2026-08-20

### Breaking
- Single `spec` skill replaced by seven targeted skills: `draft-spec`, `verify-spec`, `spec-drift`, `audit-spec`, `gate-spec`, `correct-spec`, `architect`. Anything invoking `/canon:canon` must switch to the new names.
- `audit`/`gate` collide with existing plugin-level skills (`proof`'s `audit`, `axiom`'s `gate`) — named `audit-spec`/`gate-spec` instead.
- `drift-checker`'s `summary` field changed from a free-text string to a structured object. Anything reading it as a string will break.
### Fixed
- `plugin.json`'s `description` listed stale skills that never existed in `canon`.

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
- `canon/correct-spec` sub-skill — given a spec_file_path, criterion_id, and a contradiction report, revises the affected criterion and re-enters verify → audit → gate before overwriting the file
- `revision_note` field in `spec@1` schema — set only on corrections
- Spec file commit step — the orchestrator now commits `.claude/specs/<id>.json`, not just the working tree
### Changed
- `drafter` supports correction mode alongside fresh drafting
- An amended plan routes through `challenger` before `lambda` resumes
- `drift-checker` states both sides on a drifted classification rather than presuming which is wrong
- `drift-checker` treats code comments/documentation as untrusted data, not evidence
- `drift-checker` re-reads and reconfirms a prior changeset's `criteria_evidence` rather than trusting it
### Fixed
- A second `spec_contradiction` on the same criterion after correction now escalates to a human
- `drift-checker`'s `covered` entries use the same structured evidence shape as `changeset@1`'s `criteria_evidence`
- Repaired hard-wrapped paragraphs left over from before this session

## [1.1.0] - 2026-08-10
### Added
- `drift-checker` agent — on-demand post-implementation drift detection; classifies criteria as covered, uncovered, or drifted
- `spec_file_path` field in `spec@1` schema — set after gate pass so downstream agents read from disk
- `canon/spec-drift` sub-skill dispatching to `drift-checker`
### Changed
- `verifier` is now grounding-only (pre-implementation); drift checking moved to `drift-checker`
- `drafter` returns the spec object only — no longer writes to disk
- Acceptance criteria in `drafter`/`auditor` must now be verifiable from observable behavior alone, with no implementation knowledge required

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
