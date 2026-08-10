# Changelog — canon

## [1.1.0] - 2026-08-10
### Added
- `canon-drift-checker` agent (opus/high) — on-demand post-implementation drift detection; reads spec from disk, classifies criteria as covered, uncovered, or drifted
- `spec_file_path` field in `spec@1` schema — workspace-relative path set by the skill orchestrator after gate pass; downstream agents read the spec from disk rather than context
- `canon/drift` sub-skill in SKILL.md dispatching to `canon-drift-checker`
- Post-gate orchestration instruction in SKILL.md — explicit step for writing spec to `.claude/specs/<id>.json` and setting `spec_file_path` after canon-exit-gate passes
### Changed
- `canon-verifier` is now grounding-only (pre-implementation); post-implementation drift checking is handled by the new `canon-drift-checker`
- `canon-drafter` returns the spec object only — it no longer writes to disk (skill orchestrator responsibility post-gate)
- Acceptance criterion quality standard in `canon-drafter` and `canon-auditor` now explicitly rejects criteria that require implementation knowledge to verify (semantic model principle): a criterion is only valid if a tester with no knowledge of the implementation can evaluate it from observable system behavior

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
- Subagents: canon-architect, canon-drafter, canon-auditor, canon-verifier, canon-exit-gate
