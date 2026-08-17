# Changelog

— proof

## [2.2.0] - 2026-08-17

### Changed
- **Fast Symbol Discovery**: Updated scanning and adversary workflows to use targeted `rg` patterns for symbol inspection.

## [2.1.0] - 2026-08-17

### Added
- **Module-Batched Sweeps**: `adversary` now audits candidate defect signals grouped by crate module in a single pass.
- **Dead-Code Pre-Filtering**: Automatically filters out inactive code before scanning to eliminate false alarms.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `proof:scanner`, `proof:adversary`, and `proof:exit-gate`.
- **Fast Candidate Refutation**: Routed initial candidate reviews to Sonnet, reserving Opus for the final binding exit gate.

## [2.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `proof` → `audit` (displays as `/proof:audit`)

## [2.0.0] - 2026-08-04
### Added
- Initial release, superseding `bug-hunter-rust` and `bug-hunter-ts`
- 4-phase pipeline: recon → scan → adversary → exit-gate
- Cross-language support: Rust, TypeScript, JavaScript
- Runtime language heuristics via `shared/references/rust.md` and `shared/references/typescript.md`
- `finding-report@1` output schema
- Subagents: recon, scanner, adversary, exit-gate
