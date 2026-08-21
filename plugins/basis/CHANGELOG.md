# Changelog

— basis

## [2.0.0] - 2026-08-20

### Breaking
- Single `meta` skill replaced by four targeted skills: `scaffold-plugin`, `audit-plugin`, `design-schema`, `scaffold-subagent`. Anything invoking `/basis:basis` must switch to the new per-skill names.
- `audit` was the natural bare-word name for the conformance-check skill but collides with `proof`'s existing plugin-level skill (`name: audit`) — named `audit-plugin` instead, per the constitution's Skill Names rule.
- A follow-up pass renamed `scaffold` → `scaffold-plugin`, `schema` → `design-schema`, `subagent` → `scaffold-subagent`: bare nouns/verbs left the object ambiguous in slash-command autocomplete, and `scaffold-plugin`/`scaffold-subagent` now read as siblings instead of `scaffold` sounding like the only "real" scaffolding skill.
### Added
- `basis/scaffold-subagent` skill: generates one conformant agent file for an existing plugin. `scaffolder.md` now documents a single-subagent mode (skips plugin.json/SKILL.md/symlink) alongside its existing full-plugin mode — no new agent needed, the old SKILL.md listed this sub-skill with no agent behind it.

## [1.2.0] - 2026-08-17

### Added
- **JIT Hook Scaffolding**: Added reference hook generation in `shared/hooks/` for cross-platform lifecycle context injection.

## [1.1.0] - 2026-08-17

### Added
- **Lean Plugin Scaffolding**: `scaffolder` generates clean agent names without redundant plugin prefixes.
- **Cache-Aware Audits**: `auditor` checks that new plugin prompts follow static prefix caching standards.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `basis:scaffolder`, `basis:auditor`, and `basis:schema-designer`.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `basis` → `meta` (displays as `/basis:meta`)

## [1.0.0] - 2026-08-04
### Added
- Initial release, superseding `agent-plugin-builder`
- Plugin scaffolding, conformance auditing, and schema contract design
- Subagents: scaffolder, auditor, schema-designer
