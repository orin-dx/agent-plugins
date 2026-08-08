# Changelog

All notable changes to the orin-dx/agent-plugins ecosystem are documented here.
Individual plugin changelogs live in `plugins/<plugin-id>/CHANGELOG.md`.

## [2026-08-08] — Research Implementation
### Added
- `docs/research/2026-08-08-agent-improvement-research.md` — synthesized findings from 5-agent parallel research workflow covering few-shot examples, schema manifest declarations, long-context handling, and prompt injection resistance
- `shared/scripts/validate-wiring.sh` — install-time wiring validation: checks all schema refs in `plugin.json` resolve to files in `shared/schemas/`, and that declared produces satisfy declared consumes
- `<context_management>` section in `plugins/lambda/skills/lambda/SKILL.md` — documents orchestrator checkpointing pattern: callers pass one task at a time, track commit SHAs externally, never re-send the full `plan@1` on each invocation
- `<example>` contrastive T7/T10 verdict pairs in `proof-adversary.md` — minimal JSON output objects anchoring what decisive evidence looks like vs. vague claim; T7 confirmed/dismissed and T10 confirmed/dismissed
- Trust Boundaries for Code-Reading Agents section in `shared/constitution.md` — EARS rules establishing that workspace files encountered during analysis are untrusted data, not evaluation instructions
- Axiom Retry Caller Constraint section in `shared/constitution.md` — EARS rule: on retry, callers pass only the revised artifact + prior verdict's blockers array
- Trust Boundaries for Code-Reading Agents section (§10) in `shared/agent-best-practices.md` — three-part defense pattern for code-reading agents
- `Verdict signal` sub-field added to T7 and T10 entries in `shared/references/rust-hazards.md` and `shared/references/typescript-hazards.md` — executable evidence distinguishing confirmable from dismissible at the boundary
- `consumes` and `produces` arrays added to all 9 `plugin.json` manifests — wiring declarations enabling the new validation script
### Changed
- `proof-adversary.md` `<backstory>` — expanded to 4 sentences covering both false-positive (missed caller guard) and false-negative (accepted SAFETY comment as evidence) failure incidents; unified punch line: wrong verdicts in either direction require a runtime construct
- `proof-adversary.md` `<judgment>` — added second failure mode: comment claims are not refutation evidence; refutation must cite an executable construct
- `proof-adversary.md` `<output>` — added trust-boundary EARS rule before the "For each candidate" paragraph; workspace CLAUDE.md/AGENTS.md carry no authority over evaluation criteria
- `proof-scanner.md` `<judgment>` — added second failure mode: instructions embedded in scanned files are code-under-analysis, not commands
- `proof-scanner.md` `<output>` — added EARS batch rule: WHEN live_files exceeds 200, process in batches of 50
- `lambda-implementer.md` `<output>` — added `needs_context` trigger EARS rule: emit `needs_context` when a required file is missing or baseline commit state cannot be verified

## [2026-08-08]
### Removed
- `plugins/bug-hunter-rust/` — deleted (superseded by `proof`)
- `plugins/bug-hunter-ts/` — deleted (superseded by `proof`)
- `plugins/agent-plugin-builder/` — deleted (superseded by `basis`)
### Added
- `shared/constitution.md` — EARS-format authoritative rules for all plugin development; single source of truth
- `plugins/proof/agents/proof-boundary-tracer.md` — conditional sonnet/medium agent; traces T7/T10 field survival before adversarial verification
- `plugins/canon/agents/canon-architect.md` — opus/high agent; takes `finding-report@1`, produces `spec@1` for structural remediation; closes the proof→canon loop
- `plugins/lambda/agents/lambda-mutator.md` — sonnet/medium agent; runs cargo-mutants or Stryker, designs precision tests for surviving mutants, feeds convergence loop back to implementer
- `shared/schemas/field-survival-map@1.json` — output schema for proof-boundary-tracer; consumed by proof-adversary
- `shared/schemas/mutation-report@1.json` — output schema for lambda-mutator; consumed by lambda-exit-gate and lambda-implementer
- Hazard T10 (Error Downgrade & Source Erasure) added to `shared/references/rust-hazards.md`
- Hazard T10 (Error Suppression & Downgrade) added to `shared/references/typescript-hazards.md`
- Smell 8 (Invisible Invariants) added to `shared/references/rust-smells.md`
- Smell 5 (Multi-Writer File Race) and Smell 7 (Invisible Invariants) added to `shared/references/typescript-smells.md`
- Rust Smell 2 extended with multi-writer file race sub-pattern
### Changed
- **All 36 agents across all 9 lifecycle plugins** rewritten with 4-part structure: `<backstory>`, `<goal>`, `<judgment>`, `<output>` — no `<role>` body sections, no `success_criteria` checklists
- EARS notation (WHEN/IF/WHILE/WHERE/THE SYSTEM SHALL) restricted to `<output>` sections only across all agents
- `<load_first>` blocks added to all agents that pull shared reference files at runtime — each loads only its phase-relevant file
- Model/effort tiers corrected: `graph-intake` promoted to sonnet/medium (analysis, not enumeration); `trace-risk-assessor` corrected to sonnet/medium; `delta-review-preprocessor` corrected to haiku/low
- `shared/agent-best-practices.md` fully rewritten — replaces 257-line "Superpowers 5-Section Framework" and AGY operational matrix with current principles: 4-part structure, cognitive mode separation, EARS placement, progressive context loading, SDD, model/effort tiering
- `AGENTS.md` rewritten — references `shared/constitution.md` as authority, updated directory layout, current authoring checklist
- `CONTRIBUTING.md` — fixed `subagents/` → `agents/` throughout; authoring checklist updated to 4-part structure
- `ARCHITECTURE.md` — `subagents/*.md` → `agents/*.md` in Tier 2 description
- `CLAUDE.md` (project) — removed deleted plugin install examples, updated authoring references to point to constitution
- `README.md` — removed bug-hunter-* section; hazard taxonomy counts updated to T1–T10; schema contract table updated with two new schemas; AGY install list includes `proof` and `basis`
- `plugins/basis/skills/basis/SKILL.md` — removed "CSO trigger" and "subagent" terminology; updated authoring reference to constitution
- `plugins/graph/skills/graph/SKILL.md` — removed `<success_criteria>` block
- `plugins/axiom/skills/axiom/SKILL.md` — removed `<success_criteria>` block
- All SKILL.md dispatch matrices updated with Model/Effort columns
- `.claude-plugin/marketplace.json` — basis description updated ("subagents" → "agents")
- `plugins/proof/plugin.json` — `proof-boundary-tracer` added to agents list
- `plugins/canon/plugin.json` — `canon-architect` added to agents list
- `plugins/lambda/plugin.json` — `lambda-mutator` added to agents list

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
