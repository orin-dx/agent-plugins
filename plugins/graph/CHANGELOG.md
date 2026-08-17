# Changelog

— graph

## [1.2.0] - 2026-08-17

### Changed
- **Streamlined Intake**: Standardized requirement schema citations across intake and clarifier agents.

## [1.1.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `graph:intake`, `graph:clarifier`, and `graph:auditor`.
- **Direct Requirement Capture**: `intake` extracts testable acceptance criteria with zero conversational filler.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `graph` → `need` (displays as `/graph:need`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Requirement capture with GitHub Issues integration; extensible to Linear, Jira
- `requirement@1` output schema
- Subagents: intake, clarifier, auditor
