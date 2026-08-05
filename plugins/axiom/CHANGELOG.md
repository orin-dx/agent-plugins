# Changelog — axiom

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
- Subagents: axiom-recon, axiom-verifier, axiom-exit-gate
