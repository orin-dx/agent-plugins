# Changelog

— delta

## [1.3.0] - 2026-08-17

### Changed
- **Direct Evidence Citations**: Formatted changeset evidence pointers with direct file and line references.

## [1.2.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `delta:pr-narrator`, `delta:changeset-analyzer`, and `delta:release-summarizer`.
- **Direct Code Pointers**: Changeset analysis connects directly to test and code evidence produced during implementation.

## [1.1.0] - 2026-08-11
### Added
- `criteria_evidence` field in `changeset@1` schema — per-criterion evidence trail (test file/line, implementation file/line); `changeset-analyzer` now accepts implementer's aggregated criteria_evidence as optional input and uses it directly instead of re-deriving locations from the diff
- `linked_requirement` field in `changeset@1` schema — propagated from the linked spec@1 or plan@1 when available
### Changed
- `changeset-analyzer` falls back to file-level (no line number) evidence when reconstructing from a diff alone rather than fabricating a line number it cannot verify

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
- Subagents: commit-analyzer, pr-narrator, changeset-analyzer, review-preprocessor, release-summarizer
