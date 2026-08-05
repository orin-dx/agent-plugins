# Changelog — canon

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
- Subagents: canon-drafter, canon-auditor, canon-verifier, canon-exit-gate
