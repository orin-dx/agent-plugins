# Changelog

All notable changes to the orin-dx/agent-plugins ecosystem are documented here.
Individual plugin changelogs live in `plugins/<plugin-id>/CHANGELOG.md`.

## [3.0.0] - 2026-08-21 — Multi-Skill Plugins, Consumer-Scaled Changesets, and a Voice Standard

### Breaking Changes
- `delta`, `canon`, `graph`, and `basis` each split their single broad skill into targeted, independently-triggered skills (22 total). `/delta:ship`, `/canon:canon`, `/graph:graph`, and `/basis:basis` are gone.
- `changeset@1` and `release-artifact@1` are superseded by `changeset@2`/`release-artifact@2`, which add required `consumer_impact` and `semver_impact` fields. `@1` remain on disk and valid — new consumers should target `@2`.

### Architectural Rule Changes
- Plugin Structure now explicitly allows multiple skill directories per plugin (`skills/<skill-name>/SKILL.md`) when a plugin's scope covers genuinely independent, heterogeneous intents on the same artifact — previously every plugin was assumed to have exactly one, named after the plugin id.
- Skill Names collisions now resolve with a specific compound name (`audit-spec`, not `canon-audit`) instead of a plugin-id prefix — the `plugin:skill` invocation already disambiguates two plugins sharing a bare word, so the prefix only duplicated that.

### Skills & Agent Capabilities
- **`delta` (v2.0.0)**: split into `commit`, `pr`, `changeset`, `receive-feedback`, `post-review`, `release`. `changeset-analyzer` now classifies `consumer_impact`/`semver_impact` before writing anything and scales summary detail to match; `release-summarizer` aggregates instead of re-deriving type; `pr-narrator` gained real length and structure discipline it previously lacked.
- **`canon` (v2.0.0)**: split into `draft-spec`, `verify-spec`, `spec-drift`, `audit-spec`, `gate-spec`, `correct-spec`, `architect`. Corrected two wrong model tiers (`drift-checker` and `architect` are `opus/high`, not `sonnet/medium`) and a stale `plugin.json` description listing sub-skills that never existed.
- **`graph` (v2.0.0)**: split into `capture-need`, `clarify-requirement`, `prioritize-backlog`, `connect-requirement`, `audit-backlog`. Added `prioritizer` — the one genuinely new agent this pass required; `clarifier` had a real agent but no listed sub-skill until now.
- **`basis` (v2.0.0)**: split into `scaffold-plugin`, `audit-plugin`, `design-schema`, `scaffold-subagent`. `scaffolder` now documents a single-subagent generation mode; `auditor` now checks every skill directory a plugin has instead of assuming exactly one.
- **`lambda` (v1.4.1)**: `plugin.json` no longer lists `changeset@1` in `produces` — lambda never assembles a changeset itself, `changeset-analyzer` does.

### Voice & Documentation Standards
- Added `shared/references/docs-voice.md`: a checkable voice standard (lead with the conclusion, active voice, bullets over prose, a banned-word list, the Conventional Comments/Google review-label vocabulary for triaging feedback) — embedded into `conventional-commits.md`, `github.md`, and `changesets.md` rather than loaded as a second reference, per this repo's one-reference-file-per-agent convention.

### Fixes
- Cross-plugin references left stale by `canon`'s rename (`shared/constitution.md`'s Spec Correction Loop, `lambda`'s SKILL.md) corrected.
- `canon/drift-checker` and `graph/auditor`'s `summary` fields changed from an unbounded prose paragraph to structured counts plus an optional one-clause note.
- `AGENTS.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, and root `README.md` brought in sync with the multi-skill pattern; `CONTRIBUTING.md`'s stale `author`/`skills` field examples, a prefixed-agent-name example contradicting the Namespacing Rule, and a diagram inconsistency between README and ARCHITECTURE (proof→canon edge label) also corrected.

## [2.2.0] - 2026-08-17 — Polyglot API Grounding, JIT Context Hooks, and Modern Tool Guidance

### Architectural Performance & Tooling
- **Polyglot API Grounding**: Mandated that agents inspect live source definitions before declaring function or type signatures in specs (`canon`) or plans (`vector`), eliminating multi-round revision loops caused by parameter or borrow mismatches.
- **Just-In-Time (JIT) Context Hooks**: Added cross-platform lifecycle hook templates in `shared/hooks/` (`pre-command.sh`, `subagent-start.sh`) that dynamically load minimal 2-line modern CLI guidance and language hazard taxonomies without polluting cold prompt caches.
- **Modern CLI Preference Invariant**: Standardized tool selection heuristics in cached static headers to prioritize `rg`, `fd`, `bat`, and `jq` over legacy `grep`, `find`, `sed`, and `cat`.
- **Explicit Relative Schema Citations**: Enforced relative path citations (`shared/schemas/<name>@<version>.json`) in all `<output>` contracts, eliminating filesystem-wide `find /` schema searches.

### Skills & Agent Capabilities
- **`canon` (v1.4.0)**: `drafter` now verifies live codebase function and struct definitions before generating `api_surface` entries.
- **`vector` (v1.4.0)**: `planner` verifies existing types and modules against source code before defining task-level TDD steps.
- **`basis` (v1.2.0)**: Added scaffolding templates and auditing rules for JIT lifecycle hooks and modern CLI tool preference.

## [2026-08-17] — High-Signal Performance, Lean Naming, and Subsystem Batching

### Performance & Token Efficiency
- **Prompt Cache Optimization**: Standardized prompt headers so shared instructions stay cached, delivering >95% cache hits and lowering token costs across long sessions.
- **2-Round Circuit Breaker**: Capped spec and plan review loops at two rounds. Minor debates automatically demote to non-blocking notes so workflows never stall.
- **Batch Implementation**: The `code` skill (`lambda`) now implements features by complete crate or package modules, slashing subagent spawns by ~85%.
- **High-Density Output**: Stripped conversational filler and repetitive code dumps across all agents in favor of exact line pointers and minimal viable diffs.
- **Smart Model Routing**: Routed drafting, planning, and TDD execution through consistent Sonnet lanes, reserving Opus strictly for terminal exit gates.

### Skills & Agent Capabilities
- **`canon` (Specification)**: 
  - Added architectural spec drafting (`arch-spec`) to define trait boundaries, structural refactors, and system invariants.
  - Streamlined `drafter` and `auditor` reviews to guarantee fast convergence in 1–2 passes.
- **`vector` (Planning)**: 
  - Upgraded `planner` to organize tasks into cohesive, compiling subsystem batches.
  - Refined `challenger` to focus on testability and API clarity rather than rigid implementation steps.
- **`lambda` (Implementation)**: 
  - `implementer` now executes full module batches in a single TDD cycle with minimal code diffs.
  - `mutator` and `reviewer` run at batch milestones, keeping context clean and builds green.
- **`proof` (Bug Hunting)**: 
  - `adversary` now verifies candidate defect signals in module batches for faster bug-hunting sweeps.
- **`basis` (Plugin Builder)**:
  - `scaffolder` and `auditor` now generate and enforce clean agent naming and cache-friendly prompt headers for new plugins.
- **Lean Namespacing**: 
  - All agents now register with clean, direct names (e.g. `canon:drafter`, `vector:planner`, `lambda:implementer`) in Claude Code and AGY menus.

## [2026-08-12] — Spec Persistence, Correction Loop, and Traceability
### Added
- `spec_file_path` mechanism — the canon skill orchestrator writes the gated spec to `.claude/specs/<id>.json`, commits it, and every downstream agent reads it from disk instead of from lossy conversation context. `recon` warns (not fails) when the path is absent; graceful degradation throughout.
- `covers_criteria` on `plan@1` tasks and an `orphaned-criteria` check in `challenger` — every acceptance criterion must be claimed by at least one task before implementation begins.
- `drift-checker` (opus/high) — on-demand, post-implementation diagnostic that classifies each criterion as covered, uncovered, or drifted; a health check, not a blocking gate.
- Spec correction loop — `implementer` reports `spec_contradiction` when a criterion contradicts observed system behavior rather than forcing a false pass; the caller routes this to a new `canon/correct` sub-skill, which revises the spec, re-gates it, and hands the correction to `planner` in amend mode (patching only affected tasks, always re-reviewed by `challenger`). A second contradiction on the same criterion escalates to a human.
- `criteria_evidence` on `changeset@1` — exact test and implementation file/line per criterion, captured by `implementer` as a byproduct of the TDD cycle it already runs. `exit-gate` uses it as a pointer to check, never as proof by itself. `changeset-analyzer` uses it directly when available, falling back to file-level (no fabricated line numbers) reconstruction from a diff otherwise.
- `linked_requirement` propagated end-to-end: `spec@1` → `plan@1` → `changeset@1`, so the requirement-to-code chain is traceable without re-reading intermediate artifacts.
- `spec_hash` on `plan@1` — a raw-file-byte content hash `recon` compares against the live spec file to detect drift between planning and implementation.
- Trust-boundary defense (backstory priming, named failure mode, output EARS rule) extended to five workspace-reading agents that lacked it: `implementer`, `reviewer`, `exit-gate`, `recon`, `drift-checker`.
- `.gitignore` — was absent; `.DS_Store` had been accumulating as an untracked file.
### Changed
- `drafter` runs in an alternate correction mode in addition to fresh drafting; still returns the spec object only, never writes to disk itself.
### Fixed
- `axiom/README.md` and `ARCHITECTURE.md` claimed axiom "runs inside canon and lambda as an inline gate." False — `axiom`'s `plugin.json` declares `consumes: []`, confirmed independently by `shared/scripts/validate-wiring.sh`. `exit-gate` and `exit-gate` are separate agents that independently implement the same protocol axiom formalizes; neither invokes axiom's agents. Corrected the claim and redrew the pipeline diagrams in `README.md` and `ARCHITECTURE.md` so axiom shows as the standalone, optional gate it actually is.
- `lambda`'s and `vector`'s `SKILL.md` frontmatter versions were stuck one and two releases behind their `plugin.json` — never caught until this pass. Synced, and vector's sub-skill descriptions (which never mentioned `covers_criteria`, `spec_file_path`, or `orphaned-criteria`) now reflect actual current behavior.
- Root `README.md`'s pipeline diagram and lambda's own docs claimed lambda produces `changeset@1` directly — it doesn't; `changeset-analyzer` does, from lambda's `criteria_evidence`. Corrected across `lambda/README.md` and `lambda/skills/lambda/SKILL.md`.

## [2026-08-08] — Research Implementation
### Added
- `docs/research/2026-08-08-agent-improvement-research.md` — synthesized findings from 5-agent parallel research workflow covering few-shot examples, schema manifest declarations, long-context handling, and prompt injection resistance
- `shared/scripts/validate-wiring.sh` — install-time wiring validation: checks all schema refs in `plugin.json` resolve to files in `shared/schemas/`, and that declared produces satisfy declared consumes
- `<context_management>` section in `plugins/lambda/skills/lambda/SKILL.md` — documents orchestrator checkpointing pattern: callers pass one task at a time, track commit SHAs externally, never re-send the full `plan@1` on each invocation
- `<example>` contrastive T7/T10 verdict pairs in `adversary.md` — minimal JSON output objects anchoring what decisive evidence looks like vs. vague claim; T7 confirmed/dismissed and T10 confirmed/dismissed
- Trust Boundaries for Code-Reading Agents section in `shared/constitution.md` — EARS rules establishing that workspace files encountered during analysis are untrusted data, not evaluation instructions
- Axiom Retry Caller Constraint section in `shared/constitution.md` — EARS rule: on retry, callers pass only the revised artifact + prior verdict's blockers array
- Trust Boundaries for Code-Reading Agents section (§10) in `shared/agent-best-practices.md` — three-part defense pattern for code-reading agents
- `Verdict signal` sub-field added to T7 and T10 entries in `shared/references/rust-hazards.md` and `shared/references/typescript-hazards.md` — executable evidence distinguishing confirmable from dismissible at the boundary
- `consumes` and `produces` arrays added to all 9 `plugin.json` manifests — wiring declarations enabling the new validation script
### Changed
- `adversary.md` `<backstory>` — expanded to 4 sentences covering both false-positive (missed caller guard) and false-negative (accepted SAFETY comment as evidence) failure incidents; unified punch line: wrong verdicts in either direction require a runtime construct
- `adversary.md` `<judgment>` — added second failure mode: comment claims are not refutation evidence; refutation must cite an executable construct
- `adversary.md` `<output>` — added trust-boundary EARS rule before the "For each candidate" paragraph; workspace CLAUDE.md/AGENTS.md carry no authority over evaluation criteria
- `scanner.md` `<judgment>` — added second failure mode: instructions embedded in scanned files are code-under-analysis, not commands
- `scanner.md` `<output>` — added EARS batch rule: WHEN live_files exceeds 200, process in batches of 50
- `implementer.md` `<output>` — added `needs_context` trigger EARS rule: emit `needs_context` when a required file is missing or baseline commit state cannot be verified

## [2026-08-08]
### Removed
- `plugins/bug-hunter-rust/` — deleted (superseded by `proof`)
- `plugins/bug-hunter-ts/` — deleted (superseded by `proof`)
- `plugins/agent-plugin-builder/` — deleted (superseded by `basis`)
### Added
- `shared/constitution.md` — EARS-format authoritative rules for all plugin development; single source of truth
- `plugins/proof/agents/boundary-tracer.md` — conditional sonnet/medium agent; traces T7/T10 field survival before adversarial verification
- `plugins/canon/agents/architect.md` — opus/high agent; takes `finding-report@1`, produces `spec@1` for structural remediation; closes the proof→canon loop
- `plugins/lambda/agents/mutator.md` — sonnet/medium agent; runs cargo-mutants or Stryker, designs precision tests for surviving mutants, feeds convergence loop back to implementer
- `shared/schemas/field-survival-map@1.json` — output schema for boundary-tracer; consumed by adversary
- `shared/schemas/mutation-report@1.json` — output schema for mutator; consumed by exit-gate and implementer
- Hazard T10 (Error Downgrade & Source Erasure) added to `shared/references/rust-hazards.md`
- Hazard T10 (Error Suppression & Downgrade) added to `shared/references/typescript-hazards.md`
- Smell 8 (Invisible Invariants) added to `shared/references/rust-smells.md`
- Smell 5 (Multi-Writer File Race) and Smell 7 (Invisible Invariants) added to `shared/references/typescript-smells.md`
- Rust Smell 2 extended with multi-writer file race sub-pattern
### Changed
- **All 36 agents across all 9 lifecycle plugins** rewritten with 4-part structure: `<backstory>`, `<goal>`, `<judgment>`, `<output>` — no `<role>` body sections, no `success_criteria` checklists
- EARS notation (WHEN/IF/WHILE/WHERE/THE SYSTEM SHALL) restricted to `<output>` sections only across all agents
- `<load_first>` blocks added to all agents that pull shared reference files at runtime — each loads only its phase-relevant file
- Model/effort tiers corrected: `intake` promoted to sonnet/medium (analysis, not enumeration); `risk-assessor` corrected to sonnet/medium; `review-preprocessor` corrected to haiku/low
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
- `plugins/proof/plugin.json` — `boundary-tracer` added to agents list
- `plugins/canon/plugin.json` — `architect` added to agents list
- `plugins/lambda/plugin.json` — `mutator` added to agents list

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
