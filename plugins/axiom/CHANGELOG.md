# Changelog

— axiom

## [1.1.0] - 2026-08-17

### Added
- **Targeted Gate Re-checks**: `exit-gate` verifies only the specific blocker delta on retry runs, saving time and tokens.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `axiom:recon`, `axiom:verifier`, and `axiom:exit-gate`.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `axiom` → `gate` (displays as `/axiom:gate`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Cross-cutting verification gate usable at any pipeline stage
- recon → verify → exit-gate protocol with retry-with-feedback loop
- `verdict@1` output schema
- Subagents: recon, verifier, exit-gate
