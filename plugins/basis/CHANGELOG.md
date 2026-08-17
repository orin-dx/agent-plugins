# Changelog

— basis

## [1.2.0] - 2026-08-17

### Added
- **JIT Hook Scaffolding**: Added reference hook generation in `shared/hooks/` for cross-platform lifecycle context injection.

## [1.1.0] - 2026-08-17

### Added
- **Lean Plugin Scaffolding**: `scaffolder` generates clean agent names without redundant plugin prefixes.
- **Cache-Aware Audits**: `auditor` checks that new plugin prompts follow static prefix caching standards.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `basis:scaffolder`, `basis:auditor`, and `basis:schema-designer`.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `basis` → `meta` (displays as `/basis:meta`)

## [1.0.0] - 2026-08-04
### Added
- Initial release, superseding `agent-plugin-builder`
- Plugin scaffolding, conformance auditing, and schema contract design
- Subagents: scaffolder, auditor, schema-designer
