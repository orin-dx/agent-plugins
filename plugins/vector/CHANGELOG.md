# Changelog — vector

## [1.1.0] - 2026-08-10
### Added
- `covers_criteria` field per task in `plan@1` — every acceptance criterion ID from the spec must appear in at least one task; vector-planner sets it, vector-challenger enforces completeness
- `orphaned-criteria` check dimension in `vector-challenger` — plan fails when any acceptance criterion ID appears in no task's `covers_criteria`
- `spec_file_path` field propagated from `spec@1` into `plan@1` — vector-planner reads spec from disk when path is available, challenger reads spec from disk for orphaned-criteria check
### Changed
- `vector-planner` output EARS rules now include explicit instruction to read from `spec_file_path` when set and to create a task for any uncovered criterion

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
