# Changelog

— vanguard

## [2.0.2] - 2026-09-10

### Changed
- Research reconnaissance now loads workspace conventions from the concern-first reference path.

## [2.0.1] - 2026-09-09

### Changed
- Agents now report material concerns directly with evidence, consequence, and calibrated confidence.

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `trace` → `vanguard`; skill `trace/trace` → `vanguard/research`. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [1.2.5] - 2026-08-23

### Fixed
- README's "When to Use" bullet used the banned word "landscape". Reworded to "existing patterns and prior art".

## [1.2.4] - 2026-08-23

### Fixed
- `recon`'s `<goal>` still claimed to map "specs, plans, docs" as research sources. `plan@1` is never persisted to disk, so it was never a real source.

## [1.2.3] - 2026-08-23

### Added
- `recon` gained a `<load_first>` citing `shared/references/workspace-conventions.md` — it needed to map internal spec sources but had no stated location for them.

### Changed
- `synthesizer`'s `<output>` now shows a literal `research-report@1` JSON template, matching its three siblings.

## [1.2.2] - 2026-08-22

### Changed
- `recon`'s `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [1.2.1] - 2026-08-21

### Fixed
- `skills/trace/SKILL.md` and `README.md` documented two disagreeing "Sub-skills" lists. Both were fiction: `trace` has exactly one skill directory. Replaced both with one honest description of the real four-agent pipeline (recon → reader → synthesizer → risk-assessor).
- README's version line read `1.0.1`, already stale against `plugin.json`'s `1.2.0`.

### Changed
- README's pipeline section is now a Mermaid flowchart.

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
