# Changelog

— sentinel

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed from `axiom` to `sentinel` as part of the ecosystem-wide Wisp persona-naming rename — abstract math-noun plugin ids became hard to recall as the ecosystem grew past 9 plugins. This is the verification gate plugin; its skill also renamed from `axiom/axiom` to `sentinel/gate`. See `docs/adr/007-wisp-persona-naming.md` for the full rationale and old→new mapping. `plugin.json` `id`/`name` updated; every cross-plugin reference across the ecosystem updated to match.

## [1.2.3] - 2026-08-23

### Fixed
- `skills/axiom/SKILL.md` linked `shared/agent-best-practices.md` — an authoring-time-only guide with no legitimate runtime purpose for a verification gate, unlike `basis`'s scaffolding skills where it's the actual job. Copy-paste leftover from scaffolding. Found by an adversarial audit of the one plugin untouched all session.

## [1.2.2] - 2026-08-22

### Changed
- `recon`'s `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human, mechanical enumeration doesn't need more.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. No routing or output behavior changed.

## [1.2.1] - 2026-08-21

### Fixed
- `SKILL.md` and `README.md` each documented a "sub-skills" table, and the two disagreed with each other — `SKILL.md` listed six (`verify-requirement`, `verify-spec`, `verify-plan`, `verify-implementation`, `verify-pr`, `exit-gate`), `README.md` listed two (`axiom/gate`, `axiom/verify`). Both were fiction: axiom has exactly one skill directory and one three-agent pipeline (`recon` → `verifier` → `exit-gate`), reused unchanged against whatever artifact type it's handed. Replaced both with one consistent description.
- `README.md`'s version line said `1.0.1`; `plugin.json` was already at `1.2.0`. Corrected.
- Copy-paste typo in `README.md`'s standalone-installation note ("`exit-gate` and `exit-gate` are separate agents") — meant canon's and lambda's own exit-gate agents.
### Changed
- `README.md`'s plain-text pipeline is now a Mermaid flowchart styled with `orin-visual-standard.md`'s palette, matching how `ARCHITECTURE.md`'s axiom-gate-protocol diagram already renders it.

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
