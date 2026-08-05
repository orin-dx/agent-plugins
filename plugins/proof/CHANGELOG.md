# Changelog — proof

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
- Subagents: proof-recon, proof-scanner, proof-adversary, proof-exit-gate
