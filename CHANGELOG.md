# Changelog

All notable changes to the orin-dx/agent-plugins ecosystem are documented here.
Individual plugin changelogs live in `plugins/<plugin-id>/CHANGELOG.md`.

## [4.1.0] - 2026-09-01 — Drop mandatory write-test-first ordering

`smith` (2.1.0) and `navigator` (2.1.0): dropped the requirement that a task's test be written and confirmed failing before its implementation. Tasks now specify a brief implementation approach, the exact implementation, and the exact tests proving each criterion — test quality is verified by `smith`'s existing mutation-testing gate, not by write order. Rationale is a controlled comparison finding no quality advantage from write-test-first ordering for agent-written code, at several times the token cost, and that it suppressed upfront design work agents otherwise did well. See `docs/adr/008-drop-test-first-ordering.md`.

## [4.0.0] - 2026-08-27 — Wisp Persona Rename

**BREAKING**: All 9 plugin ids renamed to persona/craft-role names under the umbrella brand **Wisp**, memorability having broken down once the ecosystem passed 9 abstract math-noun ids. A 10th plugin, `muse` (component specification), was added in the same pass. Each plugin's own `plugin.json` `id`/`name` was bumped to its next major version; every cross-plugin reference across agents, skills, shared references, shared schemas, and root docs was updated to match. See `docs/adr/007-wisp-persona-naming.md` for the full rationale.

| Old id | New id | New version |
|---|---|---|
| `graph` | `weaver` | 3.0.0 |
| `trace` | `vanguard` | 2.0.0 |
| `canon` | `scribe` | 3.0.0 |
| `vector` | `navigator` | 2.0.0 |
| `lambda` | `smith` | 2.0.0 |
| `proof` | `ranger` | 3.0.0 |
| `axiom` | `sentinel` | 2.0.0 |
| `delta` | `courier` | 3.0.0 |
| `basis` | `mason` | 3.0.0 |
| *(new)* | `muse` | 1.0.0 |

Single-skill plugins also renamed their skill from the old plugin id to a literal action word: `proof/proof` → `ranger/audit`, `trace/trace` → `vanguard/research`, `vector/vector` → `navigator/plan`, `axiom/axiom` → `sentinel/gate`, `lambda/lambda` → `smith/implement`. Multi-skill plugins (`weaver`, `scribe`, `courier`, `mason`) kept their existing skill names — only the plugin-id prefix changed.

## [3.5.3] - 2026-08-23 — Full-Repo Sweep

`v3.5.2`'s adversarial re-read only covered files touched this session. This pass extended the same scrutiny repo-wide, since the user asked whether *all* plugins — not just the touched ones — are conformant, succinct, and accurate. Ran fresh mechanical checks (constitution byte-identity, section order, banned words, description word counts) across all 38 agents, and two targeted audits: `axiom` (never touched or reviewed all session) and a cross-check of both marketplaces plus every plugin CHANGELOG against actual `plugin.json` state.

### Fixed
- **`axiom` (v1.2.3)**: `skills/axiom/SKILL.md` linked the authoring-time-only `shared/agent-best-practices.md` — a copy-paste leftover from scaffolding with no runtime purpose for a verification gate.
- **`basis` (v2.1.2)**: `auditor`'s "no authoring-time refs" check only scanned agent bodies, not `SKILL.md` files — the exact gap that let the `axiom` issue above ship unnoticed. Broadened the check to also scan `SKILL.md`, with `basis`'s own scaffolding skills carved out as the one legitimate exception.
- **`trace` (v1.2.5)**: README's "When to Use" bullet used the banned word "landscape."

### Verified, not changed
- Both `proof` and `lambda`'s one-line marketplace descriptions don't mention this session's newest capabilities (the `plausible` verdict path, `needs_architecture`). Left as-is — both marketplace files already agree with each other and with each plugin's own `plugin.json`, and the existing convention already omits other major features at this altitude (e.g. `lambda`'s blurb never mentioned mutation testing either). Padding every one-liner to stay current would fight this repo's own succinctness rule, not serve it.

## [3.5.2] - 2026-08-23 — Adversarial Re-Read

Four parallel adversarial passes re-read every file touched in `v3.4.0` and `v3.5.x`, explicitly hunting for contradictions rather than confirming things looked fine. Two of the four came back clean. Two surfaced real, fixable defects — one pre-existing, one introduced by this session's own `v3.5.0`/`v3.5.1` work:

### Fixed
- **`lambda` (v1.6.2)**: the `needs_architecture` → `finding-report@1` field mapping in `SKILL.md` omitted the schema's required `id` and `description` fields — a caller following it literally would produce a schema-invalid finding.
- **`proof` (v2.2.4)**: `exit-gate`'s output never conformed to `verdict@1.json` — wrong verdict enum, an entirely invalid blocker shape, and (new in `v2.2.3`) a `flagged_for_review` field with no schema counterpart. Added `verdict@2.json` (verdict@1 plus optional `flagged_for_review`) and rewrote `exit-gate` to conform to it literally. `axiom`, `canon`, and `lambda` are unaffected.
- **`basis` (v2.1.1)**: `auditor`'s frontmatter claimed a check count that disagreed with its own README table, and one check the README promised (no authoring-time references to `shared/agent-best-practices.md`) was never actually instructed anywhere in the agent's `<output>`.
- **`CONTRIBUTING.md`**: the new Capability Change Checklist (added in `v3.5.0`) had no bullet for "descriptive prose still matches actual behavior" — exactly the defect class that motivated writing the checklist in the first place. Added one.

## [3.5.1] - 2026-08-23 — Missed Instance

### Fixed
- **`trace` (v1.2.4)**: `recon` still claimed to map "specs, plans, docs" as research sources — missed in `v3.5.0`'s own pass despite that pass touching this same file for its `<load_first>` addition. `plan@1` is never persisted to disk. Found by re-checking for the exact phrase across the repo rather than trusting the earlier sweep was exhaustive.

## [3.5.0] - 2026-08-23 — Basis Conformance Overhaul & Cross-Plugin Doc Accuracy

A follow-up audit across the six plugins not touched in `v3.4.0` (`graph`, `trace`, `delta`, `axiom`, `proof`, `basis`) found the same class of gap recurring — `basis`, the meta-plugin meant to keep every other agent conformant, had itself fallen behind twice: it couldn't generate or check `<load_first>` (a real CONTRIBUTING.md requirement since before this session), and had no check for orchestration completeness (an agent's output status with no SKILL.md routing) — the exact defect fixed by hand in `lambda` this session. Root `CHANGELOG.md`'s own `v3.3.0` entry already documents this happening once before. This release fixes the specific findings and the root cause.

### Added
- **`basis` (v2.1.0)**: `scaffolder` generates `<load_first>` and drafts SKILL.md routing entries; `auditor` gained `<load_first>`-correctness and orchestration-completeness checks, and now runs the repo's own validation scripts for what they already check deterministically instead of re-deriving it through reasoning.
- **`proof` (v2.2.3)**: `adversary` gained a genuine `plausible` verdict path (the schema promised this since it was written; adversary was strictly binary). `exit-gate` gained `flagged_for_review` to carry plausible findings for human review without blocking on them.
- **`shared/references/workspace-conventions.md`**: consolidates the "gated specs live at `.claude/specs/*.json`" fact, now cited by `canon:auditor`, `graph:auditor`, and `trace:recon` instead of restated three times.
- **`shared/constitution.md`**: new rule — a new agent-authoring convention must update `basis:scaffolder`/`basis:auditor` in the same change, or it's documented, not enforced.
- **`CONTRIBUTING.md`**: new Capability Change Checklist — the full list of docs/versions a capability change touches, distilled from this session's own work.
- **`.github/workflows/validate.yml`**, **`CONTRIBUTING.md`**: `scripts/check-reference-size.sh` was written and documented in `CLAUDE.md` but wired into neither CI nor the local dev-setup command list. Added to both.

### Fixed
- **`delta` (v2.1.3)**: `receive-feedback` and its own `README.md` claimed automated must-fix/suggestion/question comment triage in 6 places; `review-preprocessor`'s own `<judgment>` explicitly forbids that call. Narrowed to what it does — package assembly.
- **`graph` (v2.0.2)**: `auditor` (and its SKILL.md/README) claimed to search "specs, plans, and implementation" for coverage; `plan@1` is never persisted to disk, so the claim was unfulfillable. Scoped to specs and implementation.
- **`trace` (v1.2.3)**: `synthesizer`'s `<output>` now shows a literal JSON template matching its three siblings, instead of prose-only.
- **`canon` (v2.2.1)**, **`graph`**, **`trace`**: each agent's own restatement of the spec-location fact replaced with a citation to the new shared reference.
- **`lambda` (v1.6.1)**: `needs_architecture` (added in `v1.6.0`) had no SKILL.md routing, unlike its `needs_context`/`spec_contradiction` siblings — added the same re-entry sequence.

## [3.4.0] - 2026-08-23 — Shift-Left Defect Checks

### Added
- **`vector` (v1.5.0)**: `challenger` gained an eighth review dimension, `interface-incompleteness` — a task touching one implementer of a shared trait/interface/protocol must cover every other known implementer or say why not, checked via a deterministic pre-scan rather than recalled from memory.
- **`canon` (v2.2.0)**: `auditor` gained a seventh audit dimension, `boundary-round-trip` — a field a spec adds or changes on a type another spec persists, serializes, or transmits needs a matching round-trip criterion on the far side, or the gap must be named on purpose.
- **`lambda` (v1.6.0)**: `implementer` now defaults any criterion whose value can be absent, wrong, or stale at a boundary to a sum type, discriminated union, or Result — not a raw value next to a separate boolean — escalating to `canon:architect` (via a new `needs_architecture` status) only when a single task's own scope can't reach that shape.
- **`shared/references/interface-implementers.md`**: deterministic implementer-enumeration patterns (grep/AST) per language, loaded by `challenger`.
- **`shared/references/boundary-value-shapes.md`**: the sum-type-over-bool default posture, with Rust/TypeScript before-after examples, loaded by `implementer`.

### Fixed
- `canon:auditor` never stated where gated specs live in the workspace, a pre-existing gap behind its `scope-overlap` dimension since before this change. Now points to `.claude/specs/*.json`, where `canon/gate-spec` writes every passed spec.
- Root `README.md`'s Shared References table was missing the two new files above; its marketplace badge was still pinned to `v2.0.0` while `marketplace.json` had already moved through several major/minor bumps — corrected to `v3.4.0`.

## [3.3.0] - 2026-08-22 — Constitution Section & Reader-Scoped Writing

### Added
- **`shared/constitution.md`**: new Reader-Scoped Writing rule — a doc comment, inline comment, commit message, PR body, or spec field includes only what its actual reader needs; length follows that need, not a target in either direction. A stricter corollary applies to spec@1/plan@1 text specifically, since those get re-read from disk by every subsequent pipeline stage rather than read once by a human.
- **5-part agent structure (ADR-006)**: every agent body now defines `<constitution>` as a byte-for-byte identical first section across all 38 agents, ahead of `<backstory>`/`<goal>`/`<judgment>`/`<output>`. This is what makes the Static Prompt Prefix Invariant's cache-sharing claim real instead of aspirational — previously no agent file had any shared header despite the invariant describing one. Content: treat unauthored content as data not instruction, output-economy discipline, reader-scoped writing, abstract tool language. `constitution.md` and `agent-best-practices.md` amended to permit this 5th section and to allow EARS notation there in addition to `<output>`.
- **`shared/references/code-comments.md`**: operational subset of Reader-Scoped Writing for doc comments and inline comments specifically — `docs-voice.md` only ever covered prose (commits, PRs, changesets, docs), never comments inside code.
- **`scripts/check-reference-size.sh`**: enforces the existing 120-line reference-file cap, which `rust-hazards.md`/`typescript-hazards.md` had silently exceeded (150/167 lines).
- **ADR-006**: documents the `<constitution>` decision; ADR-001 (4-part structure) noted as extended, not superseded.

### Changed
- **`canon` (v2.1.0)**: `auditor` gained a sixth check dimension, `unnecessary-prose`.
- **`lambda` (v1.5.0)**: `reviewer` now flags padded/restating comments as findings; `implementer` writes comments per the new reference.
- **`proof` (v2.2.2)**, **`basis` (v2.0.1)**, **`delta` (v2.1.2)**, **`axiom` (v1.2.2)**, **`graph` (v2.0.1)**, **`trace` (v1.2.2)**, **`vector` (v1.4.2)**: hazard-file split for `boundary-tracer`/`adversary`/`scanner` (proof only), `basis:scaffolder`/`auditor` updated to recognize and generate the 5-part structure (a real bug — `auditor`'s prior check would have failed every conformant agent), reasoning-field caps on haiku-tier agents, and frontmatter description trims across the roster — several exceeded the 80-200 word guideline by 40-80% (`changeset-analyzer` was 283 words, `implementer` 246). Agent + skill description text alone dropped from 5,453+2,438 words to 4,672+2,283 — a fixed cost paid every session regardless of which agent runs, unlike per-invocation prompt content.

### Fixed
- `proof/skills/proof/SKILL.md`'s dispatch matrix mistagged `adversary` as `sonnet/medium`; frontmatter has always been `opus/high`.
- Repo-wide hard-wrap sweep: manually line-wrapped prose (frontmatter `description:` blocks and body paragraphs) unwrapped to single flowing lines across 30+ files, per the standing no-wrap convention — diffs on a wrapped paragraph reflow the whole block for a one-word edit.

## [3.2.1] - 2026-08-21 — Anti-Fragmentation Judgment

### Changed
- **`delta` (v2.1.1)**: `changeset-analyzer`'s topic-splitting judgment (added in 3.2.0) now checks shared `linked_spec`/`linked_plan`/`linked_requirement` first, then explicitly stated shared scope, and only falls back to diff-inferred shared cause when neither applies — guarding against over-fragmenting a deliberately-scoped effort (a themed feature batch, a cross-package testing push) into many tiny changesets. `shared/references/changesets.md` updated to match.

## [3.2.0] - 2026-08-21 — Topic-Scoped Changesets

### Added
- **`delta` (v2.1.0)**: `changeset-analyzer` now checks whether a diff contains multiple independent topics before classifying anything, and emits one `changeset@2` per topic instead of a single bundled entry. A single PR still produces exactly one changeset, unchanged — the new behavior only engages on a backlog/catch-up diff spanning several unrelated tracks since the last release. Prompted by a real incident in a sibling repo (`callisto`, a separate release-automation tool) where a large diff got bundled into one changeset covering unrelated tracks with package attribution guessed from a written summary instead of verified per-topic against the actual diff. `changeset-analyzer`'s output contract changes from a single object to an array of one-or-more; `delta/changeset`'s `<io>` section and `shared/references/changesets.md` updated to match, with the split rule stated as a named failure mode (bundling for convenience costs more than a spurious split).

## [3.1.0] - 2026-08-21 — Honest Sub-Skills, Applied Diagram Palette, Readable READMEs

### Fixed
- `proof`, `vector`, `lambda`, `axiom`, and `trace` each documented a "Sub-skills" table with slash-path names (`proof/scan`, `vector/decompose`, `axiom/verify-plan`, ...) that read exactly like `delta/commit` or `canon/draft-spec` — real, independently invokable skills. None of these five plugins is actually split; each has exactly one skill directory, and those names never routed to anything. `axiom` and `trace` were worse: their own `SKILL.md` and `README.md` each documented two *different*, both-fictional lists that didn't agree with each other. All five replaced with one honest description of the plugin's real pipeline and how it adapts to what's asked, grounded in each plugin's actual agent files.
- `vector`'s README wrongly listed `challenger` as `opus/high`; the agent file says `sonnet/medium`. Corrected.
- `axiom`'s and `trace`'s README version lines were stale — both said `1.0.1` while `plugin.json` was already at `1.2.0`. `proof`'s and `lambda`'s had the same drift (`2.0.0` vs `2.2.0`, `1.2.0` vs `1.4.1`). All corrected.
- `axiom`'s description in both `marketplace.json` and `.claude-plugin/marketplace.json` repeated the same fictional six-item sub-skill list — fixed in both.

### Changed
- Applied `orin-visual-standard.md`'s six-color Mermaid palette — documented since this session's earlier work but never actually used anywhere in this repo's own diagrams — to every plugin pipeline diagram plus the root `README.md`/`ARCHITECTURE.md` diagrams. One consistent color-to-role mapping across all of them: indigo for entry points, violet for analysis/engine stages, slate for mechanical/storage roles, amber for routing/judgment decisions, emerald for verified output, rose for failure/escalation.
- `ARCHITECTURE.md`'s axiom-gate-protocol diagram, and `lambda`'s plugin pipeline, now use a subgraph to separate a linear check/loop chain from the retry logic around it — `orin-visual-standard.md`'s Subgraph Styling Spec, defined earlier this session, used for the first time here.
- Several plain-text ASCII pipeline diagrams (`graph`'s hand-aligned box art in particular — fragile, the next label edit would have misaligned it) converted to real Mermaid flowcharts.
- All nine plugin READMEs passed against `docs-voice.md` for scannability: dense paragraphs split into bullets, filler cut, banned words checked.

### Known follow-up, not fixed here
- `lambda`'s skill frontmatter `description` — the text that actually decides when the skill activates, not just its body documentation — still advertises "generate tests," "explain," and "refactor" as request shapes with no agent behind any of them. Left untouched since narrowing live routing behavior deserves its own explicit decision, not a side effect of a docs pass.

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
