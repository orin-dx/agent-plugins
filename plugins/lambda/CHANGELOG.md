# Changelog — lambda

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `lambda` → `code` (displays as `/lambda:code`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- TDD implementation cycle: failing test → minimal code → passing → commit
- `axiom` exit-gate integration for verified handoff
- `changeset@1` output schema consumed by `delta` and `axiom`
- Subagents: lambda-recon, lambda-implementer, lambda-reviewer, lambda-exit-gate
