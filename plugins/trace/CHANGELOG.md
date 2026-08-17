# Changelog

— trace

## [1.2.0] - 2026-08-17

### Changed
- **Targeted Research Lookups**: Uses `rg` and `bat` patterns for fast, windowed codebase evidence gathering.

## [1.1.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `trace:reader`, `trace:risk-assessor`, and `trace:synthesizer`.
- **High-Density Research**: `synthesizer` structures findings around exact file pointers and clear evidence assumptions.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `trace` → `research` (displays as `/trace:research`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Evidence-based research pipeline distinguishing confirmed findings from assumptions
- `research-report@1` output schema consumed by `canon`
- Subagents: recon, reader, synthesizer, risk-assessor
