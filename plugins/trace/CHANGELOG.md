# Changelog

— trace

## [1.2.2] - 2026-08-22

### Changed
- `recon`'s `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `trace`'s skill description tightened; no routing behavior changed.

## [1.2.1] - 2026-08-21

### Fixed
- `skills/trace/SKILL.md` and `README.md` each documented a "Sub-skills" list implying separately-invokable commands (`trace/question`/`trace/prior-art`/`trace/dependency`/`trace/risk` in one file, `trace/survey`/`trace/scan`/`trace/risk` in the other) — the two disagreed with each other, and both were fiction: trace has exactly one skill directory. Replaced both with one honest description of the real four-agent pipeline (recon → reader → synthesizer → risk-assessor), which narrows itself to what's asked instead of exposing named sub-modes.
- README's version line read `1.0.1`, already stale against `plugin.json`'s `1.2.0` before this fix.
### Changed
- README's pipeline section is now a Mermaid flowchart styled with the shared six-color palette (`shared/references/orin-visual-standard.md` §2), replacing the plain-text arrow chain.

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
