# Changelog

— muse

## [1.0.1] - 2026-09-09

### Changed
- Agents now report material concerns directly with evidence, consequence, and calibrated confidence.

## [1.0.0] - 2026-08-27

### Added
- Initial release. Component specification plugin: turns UI/design intent into unambiguous, testable component specs — props, variants, per-state behavior, and accessibility criteria as testable propositions, gated before planning. One skill (`component`), three subagents (`drafter`, `auditor`, `exit-gate`). Reuses `spec@1`/`verdict@1` — no new schema. Tenth plugin in the Wisp-branded ecosystem. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).
