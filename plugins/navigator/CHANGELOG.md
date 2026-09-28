# Changelog

— navigator

## [2.3.2] - 2026-09-10

### Fixed
- Codex planning now checks shared-interface siblings with the same syntax and architecture evidence as the Claude/AGY challenger.

### Changed
- Interface coverage now loads from the concern-first verification path and no longer describes semantic discovery as a deterministic grep pass.

## [2.3.1] - 2026-09-09

### Changed
- Agents now report material concerns directly with evidence, consequence, and calibrated confidence.
- Implementer discovery guidance now covers Rust, TypeScript/JavaScript, Python, and Go without assuming a language-specific abstraction.

## [2.3.0] - 2026-09-02

### Added
- Plan persistence: after `challenger` passes, the orchestrator writes `plan@1` to `docs/projects/<linked_spec>.json`, commits it, and sets `plan_file_path` — mirroring `scribe/gate-spec`. Previously `plan@1` was never persisted, so `weaver/audit-backlog` couldn't check plan coverage; now it can. An amended plan overwrites the same path.

## [2.2.0] - 2026-09-01

### Changed
- `planner`'s exact implementation code is now a concrete baseline, not a transcript `smith`'s implementer must copy — implementer may adapt shape if file targets, `covers_criteria`, and tests still hold. Task sizing changed from a clock-time estimate to "one reviewable unit sized to its Subsystem Batch's compilation boundary." See [ADR-009](../../docs/adr/009-implementer-shape-latitude.md).

## [2.1.0] - 2026-09-01

### Changed
- Dropped the requirement that every task specify a failing test before implementation. Tasks now specify approach, implementation, and tests proving each `covers_criteria` criterion, with no mandated order. See [ADR-008](../../docs/adr/008-drop-test-first-ordering.md) — a controlled comparison found no quality advantage from write-test-first ordering, at several times the token cost, and that it suppressed upfront design work.

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `vector` → `navigator`; skill `vector/vector` → `navigator/plan`. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [1.5.0] - 2026-08-23

### Added
- **`challenger`**: eighth review dimension, `interface-incompleteness` — flags a task that modifies one implementer of a shared trait/interface without covering every other known implementer or stating why not. Backed by a deterministic pre-scan (`shared/references/interface-implementers.md`, new).

## [1.4.2] - 2026-08-22

### Changed
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [1.4.1] - 2026-08-21

### Fixed
- SKILL.md/README.md documented a fictional four-skill "Sub-skills" list; `vector` has exactly one skill directory, and `vector/decompose` had no agent behind it at all. Replaced with an honest description: one skill, adaptive behavior, three agents.
- README's Subagents table listed `challenger` as `opus/high`; the agent's own frontmatter says `sonnet/medium`. Corrected.

### Changed
- README's pipeline is now a Mermaid flowchart, showing the challenger → planner feedback loop the prose already described.

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
- `spec_hash` field in `plan@1` — content hash at plan-creation time, compared by recon to detect post-planning spec changes
- `linked_requirement` field in `plan@1` — propagated from `spec@1` so the requirement-to-code chain is traceable
- Amend mode in `planner` — given a plan, a corrected spec, and the changed criterion_ids, patches only the affected tasks
### Changed
- `planner` computes `spec_hash` over raw file bytes, matching recon's comparison exactly
- An amended plan now passes through `challenger` before `lambda` resumes
### Fixed
- `vector` SKILL.md frontmatter version was stuck at 1.0.0 across two prior version bumps — synced, and its sub-skills/artifact-contracts sections updated to reflect actual behavior

## [1.1.0] - 2026-08-10
### Added
- `covers_criteria` field per task in `plan@1` — every acceptance criterion must appear in at least one task; `challenger` enforces completeness
- `orphaned-criteria` check dimension in `challenger`
- `spec_file_path` propagated from `spec@1` into `plan@1` for disk reads by both `planner` and `challenger`
### Changed
- `planner` output rules now instruct reading from `spec_file_path` when set and creating a task for any uncovered criterion

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
