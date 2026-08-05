# Changelog

All notable changes to the orin-dx/agent-plugins ecosystem are documented here.
Individual plugin changelogs live in `plugins/<plugin-id>/CHANGELOG.md`.

## [2026-08-05]
### Fixed
- All `plugin.json` manifests: `author` changed to object, `skills`/`agents` changed to relative paths for Claude Code compatibility
- README: corrected org name (`orin-axi` → `orin-dx`) throughout
- README: corrected AGY native install command to use git URL format
### Changed
- Skill names renamed to lifecycle stage words to remove display redundancy (`/proof:proof` → `/proof:audit`, etc.)
- Agents directory renamed from `subagents/` to `agents/` across all plugins
### Added
- `.claude-plugin/marketplace.json` for Claude Code CLI marketplace compatibility
### Deprecated
- `bug-hunter-rust` — superseded by `proof`
- `bug-hunter-ts` — superseded by `proof`
- `agent-plugin-builder` — superseded by `basis`

## [2026-08-04]
### Added
- Full 9-plugin lifecycle ecosystem: graph, trace, canon, vector, lambda, axiom, delta, proof, basis
- Shared JSON schemas (`shared/schemas/`) for all inter-plugin handoffs
- Runtime reference guides (`shared/references/`) for Rust, TypeScript, conventional commits, GitHub, MCP
- Plugin READMEs for all 9 plugins
### Changed
- Subagent prompts: quality pass, schema fixes, description expansions (80–200 words)

## [2026-07-27]
### Added
- Initial release with `bug-hunter-rust` and `bug-hunter-ts`
- `agent-plugin-builder` meta-skill for scaffolding new plugins
- `shared/agent-best-practices.md` authoring manual
