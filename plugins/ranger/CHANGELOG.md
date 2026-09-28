# Changelog

— ranger

## [3.2.3] - 2026-09-27

### Changed
- The adversary constitution sweep now follows `CLAUDE.md`/`AGENTS.md`'s `@` imports and reads the nearest nested instruction file for the analyzed paths, still extracting only stated invariants.

## [3.2.2] - 2026-09-10

### Changed
- Runtime hazard paths now use the concern-first reference tree.
- Scanner documentation now describes candidate-signal enumeration without assuming every reference supplies a literal grep command.
- Adversary and boundary-tracer name every selectable hazard reference exactly.

## [3.2.1] - 2026-09-09

### Changed
- Hazard references now distinguish candidate signals from confirmation and refutation across Rust, TypeScript/JavaScript, Python, and Go.
- Agents apply the shared radical-candor rule; style preferences no longer masquerade as verified defects.

## [3.2.0] - 2026-09-09

### Added
- Python and Go hazard and boundary packs alongside Rust and TypeScript/JavaScript.
- `candidate-assessment@1` makes per-candidate confirmation, plausibility, and dismissal schema-valid. `finding-report@2` records languages and structural families; `verdict@3` records verified scope, gaps, and pending checks.

### Changed
- Recon emits a provenance-aware workspace manifest. Exit-gate independently derives semantic sibling candidates and verifies the relevant execution boundary against current state.

## [3.1.0] - 2026-09-09

### Added
- Defect-family routing groups confirmed findings by shared root cause or domain behavior and sends structural families to `scribe:architect` before remediation.
- Exit verification now searches syntactic and semantic siblings across live modules and requires structural assessment for repeated families.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `proof` → `ranger`; skill `proof/proof` → `ranger/audit`. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [2.2.4] - 2026-08-23

### Fixed
- `exit-gate`'s output never conformed to `verdict@1.json`: wrong enum values (`approved|blocked` vs the schema's `pass|fail`) and an illegal blocker shape — every verdict this agent produced was schema-invalid. `axiom`, `canon`, and `lambda` already used the schema correctly. Since schema versions are immutable, added `verdict@2.json` (`verdict@1` plus an optional `flagged_for_review` array) and rewrote `exit-gate`'s output to conform; the other three plugins are unaffected.

## [2.2.3] - 2026-08-23

### Added
- **`adversary`**: genuine `plausible` verdict path — previously strictly binary (confirm-with-scenario or refute), now emits `plausible` when reachability depends on state outside the code rather than stretching thin evidence into `confirmed`.
- **`exit-gate`**: `flagged_for_review` in the verdict output — carries `plausible` findings forward for human judgment.

### Fixed
- `README.md`'s Output Schema table documented only `verdict: confirmed`; corrected to cover both values.

## [2.2.2] - 2026-08-22

### Changed
- **Hazard reference split**: T7/T10 content extracted into dedicated `*-hazards-t7-t10.md` files, both now under the 120-line cap. `boundary-tracer` and `adversary` load only the relevant file per candidate instead of the full set; `scanner`/`reviewer` still load both where needed. Also removed a dead, unreferenced Workspace Discovery section — `recon`'s manifest already covers it.

### Fixed
- `skills/proof/SKILL.md`'s dispatch matrix mistagged `adversary` as `sonnet/medium`; frontmatter has always been `opus/high`.

## [2.2.1] - 2026-08-21

### Fixed
- `SKILL.md`/`README.md` documented a fictional four-skill "Sub-skills" table; `proof` has exactly one skill directory. Replaced with an honest description of the one adaptive pipeline.
- `README.md`'s version line said `2.0.0` while `plugin.json` said `2.2.0`. Synced.

### Changed
- `README.md`'s pipeline diagram is now a styled Mermaid flowchart.

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
