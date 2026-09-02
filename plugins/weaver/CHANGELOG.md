# Changelog

— weaver

## [3.0.1] - 2026-09-02

### Changed
- `auditor` can now check plan coverage: `navigator/plan` persists `plan@1` to `docs/projects/<linked_spec>.json` as of `navigator` 2.3.0, so the "plan@1 is never persisted" caveat no longer holds. `covered` status now accepts a persisted plan with implementation underway as evidence, not only a gated spec plus shipped code. Affects `auditor`'s description, `<load_first>`, and status definitions; `audit-backlog`/`connect-requirement`/`README.md` claims about coverage sources are accurate again.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed from `graph` to `weaver` as part of the ecosystem-wide Wisp persona-naming rename — abstract math-noun plugin ids became hard to recall as the ecosystem grew past 9 plugins. This is the requirement definition plugin; no single-skill rename applies; skill names capture-need, clarify-requirement, prioritize-backlog, connect-requirement, and audit-backlog are unchanged. See `docs/adr/007-wisp-persona-naming.md` for the full rationale and old→new mapping. `plugin.json` `id`/`name` updated; every cross-plugin reference across the ecosystem updated to match.

## [2.0.2] - 2026-08-23

### Fixed
- `auditor`, both its `audit-backlog`/`connect-requirement` SKILL.md files, and `README.md` claimed coverage checking against "specs, plans, and implementation files" — `plan@1` is never persisted to disk anywhere in this pipeline, so plan coverage was never actually checkable. Scoped the claim down to specs and implementation.

### Added
- `auditor` gained a `<load_first>` citing the new `shared/references/workspace-conventions.md` — it previously had no stated location for gated specs on disk.

## [2.0.1] - 2026-08-22

### Changed
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `auditor`'s frontmatter description tightened; no routing behavior changed.

## [2.0.0] - 2026-08-20

### Breaking
- Single `need` skill replaced by five targeted skills: `capture-need`, `clarify-requirement`, `prioritize-backlog`, `connect-requirement`, `audit-backlog`. Anything invoking `/graph:graph` must switch to the new per-skill names.
- `audit` was the natural bare-word name for the backlog-coverage skill but collides with `proof`'s existing plugin-level skill (`name: audit`) — named `audit-backlog` instead, per the constitution's Skill Names rule.
- A follow-up pass renamed `capture` → `capture-need`, `clarify` → `clarify-requirement`, `prioritize` → `prioritize-backlog`, `connect` → `connect-requirement`: the plugin id `graph` doesn't hint at "requirement" the way `delta` hints at "shipping," so bare verbs left the object ambiguous in slash-command autocomplete.
- `auditor`'s `summary` field changed shape from a free-text string to a structured object (`covered_count`/`partial_count`/`missing_count`/`duplicate_count`/`note`). Anything consuming `graph/connect-requirement` or `graph/audit-backlog`'s output and reading `summary` as a string will break.
### Added
- `prioritizer` agent (new) — ranks requirement@1 drafts by impact, urgency, and dependency order with a stated rationale per ranking. No existing agent covered this; the old SKILL.md listed a `prioritize` sub-skill with no agent behind it.
- `graph/clarify-requirement` skill — `clarifier` had a real agent but was never listed in the old SKILL.md's sub-skills table. Given its own skill in this split.
### Fixed
- `graph/connect-requirement` and `graph/audit-backlog` were previously two undifferentiated sub-skill descriptions (one had no agent). Both now explicitly route to `auditor`, distinguished by scope: `connect-requirement` takes one requirement, `audit-backlog` sweeps the whole open backlog. `auditor.md`'s description documents both modes.

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
