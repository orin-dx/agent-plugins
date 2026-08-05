# Changelog — delta

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `delta` → `ship` (displays as `/delta:ship`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Full shipping pipeline: commit, PR creation, review response, changeset, release notes
- `release-artifact@1` output schema
- Subagents: delta-commit-analyzer, delta-pr-narrator, delta-changeset-analyzer, delta-review-preprocessor, delta-release-summarizer
