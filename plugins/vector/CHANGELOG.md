# Changelog

— vector

## [1.5.0] - 2026-08-23

### Added
- **`challenger`**: eighth review dimension, `interface-incompleteness` — flags a task that modifies one implementer of a shared trait, interface, or protocol without covering every other known implementer or stating why not. Backed by a deterministic pre-scan (`shared/references/interface-implementers.md`, new) run before the agent's own reasoning, not recalled from memory.

## [1.4.2] - 2026-08-22

### Changed
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `planner`'s frontmatter description tightened; no routing behavior changed.

## [1.4.1] - 2026-08-21

### Fixed
- SKILL.md and README.md documented a fictional "Sub-skills" list (`vector/plan`, `vector/estimate`, `vector/challenge`, and SKILL.md additionally `vector/decompose`) that read like independently invokable skills — the way `delta/commit` or `canon/draft-spec` genuinely are, one directory per skill. `vector` has exactly one skill directory; nothing routes to those names. `vector/decompose` had no agent behind it at all — the Subsystem Batch grouping it described is something `planner` already does as part of producing the plan, not a separate mode. Replaced with an honest description: one skill, adaptive behavior, three agents.
- README's Subagents table listed `challenger` as `opus / high` — the actual agent frontmatter (`plugins/vector/agents/challenger.md`) says `sonnet / medium`. Corrected.
### Changed
- README's plain-text pipeline is now a Mermaid flowchart styled with the palette from `shared/references/orin-visual-standard.md`, and shows the challenger → planner feedback loop the prose already described but the old diagram didn't.

## [1.4.0] - 2026-08-17

### Added
- **Task Step Grounding**: `planner` inspects live source files before declaring signatures and types in implementation task steps.

## [1.3.0] - 2026-08-17

### Added
- **Subsystem Batches**: `planner` now groups implementation tasks by crate and package compilation boundaries.
- **Clearer Challenge Criteria**: `challenger` evaluates test coverage and API clarity without penalizing necessary implementation flexibility.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `vector:planner`, `vector:estimator`, and `vector:challenger`.
- **Hot Cache Planning**: Routed `challenger` through Sonnet to preserve cache sharing during draft planning iterations.

## [1.2.0] - 2026-08-11
### Added
- `spec_hash` field in `plan@1` schema — content hash of the spec file at plan-creation time, set by planner and compared by recon to detect spec changes after planning
- `linked_requirement` field in `plan@1` schema — propagated from spec@1.linked_requirement by planner so the requirement-to-code chain is traceable without re-reading the spec
- Amend mode in `planner` — given an existing plan@1, a corrected spec@1, and the criterion_ids that changed, patches only the tasks tied to affected criteria instead of re-decomposing the entire plan
### Changed
- `planner` computes `spec_hash` over the raw spec file bytes, not a parsed or re-serialized form, matching recon's comparison exactly
- An amended plan now passes through `challenger` before lambda resumes — amendment is not exempt from adversarial review
### Fixed
- `vector` SKILL.md frontmatter version was stuck at 1.0.0 while `plugin.json` had already moved to 1.1.0 and then 1.2.0 across the prior two rounds — synced to 1.2.0, and its sub_skills and artifact_contracts sections (which never mentioned covers_criteria, spec_file_path, or orphaned-criteria) now reflect actual current behavior

## [1.1.0] - 2026-08-10
### Added
- `covers_criteria` field per task in `plan@1` — every acceptance criterion ID from the spec must appear in at least one task; planner sets it, challenger enforces completeness
- `orphaned-criteria` check dimension in `challenger` — plan fails when any acceptance criterion ID appears in no task's `covers_criteria`
- `spec_file_path` field propagated from `spec@1` into `plan@1` — planner reads spec from disk when path is available, challenger reads spec from disk for orphaned-criteria check
### Changed
- `planner` output EARS rules now include explicit instruction to read from `spec_file_path` when set and to create a task for any uncovered criterion

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `vector` → `plan` (displays as `/vector:plan`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Spec decomposition into sequenced, TDD-ready implementation tasks with exact code and commit messages
- `plan@1` output schema consumed by `lambda`
- Subagents: planner, estimator, challenger
