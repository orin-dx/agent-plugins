# Changelog

— weaver

## [3.0.3] - 2026-09-10

### Changed
- Backlog coverage now loads workspace conventions from the concern-first reference path.

## [3.0.2] - 2026-09-09

### Changed
- Agents now report requirement gaps and material concerns directly with evidence, consequence, and calibrated confidence.

## [3.0.1] - 2026-09-02

### Changed
- `auditor` can now check plan coverage, since `navigator/plan` persists `plan@1` to `docs/projects/<linked_spec>.json` as of `navigator` 2.3.0. `covered` status now also accepts a persisted plan with implementation underway.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `graph` → `weaver`. Skill names unchanged. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [2.0.2] - 2026-08-23

### Fixed
- `auditor` and its docs claimed coverage checking against "specs, plans, and implementation" — `plan@1` was never persisted anywhere, so plan coverage was never actually checkable. Scoped the claim down to specs and implementation.

### Added
- `auditor` gained a `<load_first>` citing `shared/references/workspace-conventions.md` — it previously had no stated location for gated specs.

## [2.0.1] - 2026-08-22

### Changed
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [2.0.0] - 2026-08-20

### Breaking
- Single `need` skill replaced by five targeted skills: `capture-need`, `clarify-requirement`, `prioritize-backlog`, `connect-requirement`, `audit-backlog`. `/graph:graph` must switch to the new names.
- `audit` collides with `proof`'s existing plugin-level skill — named `audit-backlog` instead.
- `auditor`'s `summary` field changed from a free-text string to a structured object. Anything reading it as a string will break.
### Added
- `prioritizer` agent (new) — ranks requirement@1 drafts by impact, urgency, and dependency order with a stated rationale.
- `graph/clarify-requirement` skill — `clarifier` had a real agent but was never listed as its own skill.
### Fixed
- `connect-requirement` and `audit-backlog` were previously two undifferentiated descriptions. Both now explicitly route to `auditor`, distinguished by scope (one requirement vs. the whole backlog).

## [1.2.0] - 2026-08-17

### Changed
- **Streamlined Intake**: Standardized requirement schema citations across intake and clarifier agents.

## [1.1.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `graph:intake`, `graph:clarifier`, and `graph:auditor`.
- **Direct Requirement Capture**: `intake` extracts testable acceptance criteria with zero conversational filler.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `graph` → `need` (displays as `/graph:need`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Requirement capture with GitHub Issues integration; extensible to Linear, Jira
- `requirement@1` output schema
- Subagents: intake, clarifier, auditor
