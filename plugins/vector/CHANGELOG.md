# Changelog — vector

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
- Subagents: vector-planner, vector-estimator, vector-challenger
