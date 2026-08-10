# Changelog — lambda

## [1.1.0] - 2026-08-10
### Added
- `spec_file_path` propagation through workspace manifest — lambda-recon accepts spec_file_path as input, verifies the file exists, and emits `spec_file_warning` when absent rather than failing hard
- `covers_criteria` support — lambda-implementer reads the acceptance criteria for a task's `covers_criteria` IDs from disk before writing tests when `spec_file_path` is available
### Changed
- `lambda-exit-gate` reads spec from disk at `spec_file_path` when available; graceful degradation with `spec_file_unset` coverage gap recorded in the verdict when absent
- `lambda-reviewer` is now language-aware — loads `rust-hazards.md` or `typescript-hazards.md` based on the workspace manifest `language` field instead of applying hardcoded Rust non-negotiables
### Fixed
- Lambda SKILL.md context management now correctly identifies `spec_file_path` source as `plan@1` (propagated there by vector-planner from the spec) rather than `spec@1`

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
