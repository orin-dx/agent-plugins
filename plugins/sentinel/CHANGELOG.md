# Changelog

— sentinel

## [2.1.2] - 2026-09-10

### Fixed
- The gate skill's verdict-schema link now resolves from its nested skill directory.

## [2.1.1] - 2026-09-09

### Changed
- Agents now report blockers and material concerns directly with evidence, consequence, and calibrated confidence.

## [2.1.0] - 2026-09-09

### Changed
- Exit-gate returns `verdict@3`, separating blockers, coverage gaps, and unfinished checks.
- Mutable external evidence is refreshed near the verdict; started checks must reach a terminal result before pass.

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `axiom` → `sentinel`; skill `axiom/axiom` → `sentinel/gate`. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [1.2.3] - 2026-08-23

### Fixed
- `skills/axiom/SKILL.md` linked `shared/agent-best-practices.md` — an authoring-time-only guide with no runtime purpose for a verification gate. Copy-paste leftover from scaffolding.

## [1.2.2] - 2026-08-22

### Changed
- `recon`'s `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [1.2.1] - 2026-08-21

### Fixed
- `SKILL.md` and `README.md` documented two disagreeing "sub-skills" tables. Both were fiction: `axiom` has exactly one skill directory and one three-agent pipeline (`recon` → `verifier` → `exit-gate`). Replaced both with one consistent description.
- `README.md`'s version line said `1.0.1`; `plugin.json` was already at `1.2.0`. Corrected.
- Copy-paste typo in the standalone-installation note referring to `exit-gate` twice instead of naming `canon`'s and `lambda`'s.

### Changed
- `README.md`'s plain-text pipeline is now a Mermaid flowchart.

## [1.2.0] - 2026-08-17

### Changed
- **Direct Schema Paths**: Standardized explicit schema resolution in gate output contracts.

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
