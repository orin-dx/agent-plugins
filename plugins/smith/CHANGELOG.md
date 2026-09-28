# Changelog

— smith

## [2.4.4] - 2026-09-27

### Added
- Language-service evidence guidance: LSP diagnostics count as supporting boundary evidence only with a recorded backend identity/version, negotiated capability, and content-version match; the repository's compiler/type-checker/test remains the terminal check.

## [2.4.3] - 2026-09-27

### Changed
- Comment guidance sends a structural alternative not taken to a decision record; any other alternative still goes in the PR body.

## [2.4.2] - 2026-09-10

### Changed
- Implementation, review, mutation, boundary-value, and comment guidance now load through concern-first reference paths in both harnesses.

## [2.4.1] - 2026-09-09

### Changed
- Language tooling and boundary guidance now selects project-native capabilities by risk and records confirming, refuting, and missing evidence.
- Rust and TypeScript guidance no longer treats style preferences or predetermined designs as universal requirements; agents also apply the shared radical-candor rule.

## [2.4.0] - 2026-09-09

### Added
- Risk-matched mutation, property, fuzz, race, integration, environment, and boundary verification across Rust, TypeScript/JavaScript, Python, and Go.
- Versioned workspace, implementation, mutation, review, and verdict handoffs with explicit capabilities, semantic candidate sites, generators and oracles, coverage gaps, pending checks, and provenance.

### Changed
- Reviewer and exit-gate independently derive semantic sibling candidates instead of accepting a reported zero-match search.
- Exit approval requires current workspace and external-state evidence plus terminal results for every started check.

## [2.3.0] - 2026-09-09

### Added
- `implementation-review@1` replaces free-text sibling gaps with related instances, shared root cause, semantic-model evidence, architecture evidence, and an explicit disposition.
- Reviewer searches syntactic and semantic siblings. Scoped families return for repair or unification; structural families route to `scribe:architect`.
- A phase-specific review reference preserves language-hazard, architecture-smell, and comment checks through progressive loading.
- Reviews carry workspace, batch, requirement, spec, and plan lineage plus positive or negative evidence for both sibling searches.
- Schema rules keep review status consistent with must-fix issues, unresolved instances, and architecture escalations.

### Changed
- Exit-gate independently verifies every defect-family instance and disposition.

### Fixed
- Implementer now commits only when the caller records explicit user authorization, matching Smith's orchestration boundary.

## [2.2.0] - 2026-09-01

### Changed
- `implementer` may adapt the plan's exact code to a better-shaped approach at execution time, provided the same file targets, `covers_criteria`, and tests are still satisfied — the plan's code is a concrete baseline, not a transcript to copy verbatim. Deviations are recorded in `concerns`. See [ADR-009](../../docs/adr/009-implementer-shape-latitude.md).
- Bulletized `implementer`'s `<judgment>` section and fixed a stray formatting artifact in `navigator`'s README.

## [2.1.0] - 2026-09-01

### Changed
- Dropped mandatory write-test-first ordering. `implementer` designs the approach, writes the implementation, then writes tests proving each `covers_criteria` criterion — order no longer mandated. Test quality is still enforced by `mutator`'s mutation-testing gate. Rationale: a controlled comparison found no measurable quality advantage from write-test-first ordering, at 3–9x the token cost, and that it suppressed upfront design work ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)).

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `lambda` → `smith`; skill `lambda/lambda` → `smith/implement`. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [1.6.2] - 2026-08-23

### Fixed
- The `needs_architecture` → `finding-report@1` field mapping in `skills/lambda/SKILL.md` omitted `id` and `description`, both required by the schema — a caller following it literally would produce a schema-invalid finding. Added both fields.

## [1.6.1] - 2026-08-23

### Fixed
- `needs_architecture` had no routing in the skill's `<context_management>`. Added the same re-entry sequence as `spec_contradiction`: wrap into a single-finding `finding-report@1`, route to `canon/architect`, then `gate-spec` → `planner` (amend) → `challenger` before resuming.

## [1.6.0] - 2026-08-23

### Added
- **`implementer`**: default posture for any criterion whose value can be absent, wrong, or stale — a sum type or Result-shaped representation, not a raw value paired with a separate boolean. See `shared/references/boundary-value-shapes.md` (new).
- `needs_architecture` status and `architecture_escalation` output object — `implementer` reports these instead of implementing an unsafe shape when the fix needs a change beyond the task's scope; escalates to `canon:architect`.

## [1.5.0] - 2026-08-22

### Added
- **`reviewer`**: flags doc/inline comments that restate a signature, narrate an alternative not taken, or pad a simple point — see `shared/references/code-comments.md`. Fresh-read backstop for `implementer`'s own comment rule.

### Changed
- **`implementer`**: writes comments per `shared/references/code-comments.md` — states what the reader needs, not a restated signature.
- **`recon`**: `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006.

## [1.4.2] - 2026-08-21

### Fixed
- SKILL.md/README.md documented a fictional four-skill "Sub-skills" table; `lambda` has exactly one skill directory. Replaced with an honest description of the real pipeline (recon → [implementer → mutator → reviewer] × N → exit-gate) and a Capability Gaps table.
- README's version line was stuck at 1.2.0 while `plugin.json` had moved to 1.4.1.

### Changed
- README's pipeline is now a Mermaid diagram, with the per-task loop in its own subgraph separate from the one-time `recon`/`exit-gate` bookends.

## [1.4.0] - 2026-08-17

### Changed
- **Modern Tool Guidance**: Standardized on targeted `rg`, `fd`, and `bat` inspection for faster test and symbol discovery during TDD loops.

## [1.3.0] - 2026-08-17

### Added
- **Batch Implementation**: `implementer` now builds and tests full module batches in one pass, slashing subagent spawns by ~85%.
- **Milestone Gates**: `mutator` and `reviewer` verify complete batch milestones instead of interrupting every small edit.
- **Lean Code Diffs**: Enforced minimal viable code generation to keep pull requests clean and maintainable.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `lambda:implementer`, `lambda:mutator`, `lambda:reviewer`, and `lambda:exit-gate`.
- **Quiet Test Output**: Filtered passing test runner logs to keep context windows lean and responsive.

## [1.2.0] - 2026-08-11
### Added
- `spec_contradiction` status in `implementer` output — emitted when a criterion contradicts observed system behavior; carries the criterion_id, the spec's claim, and the observed behavior
- `spec_drift_warning` in the recon workspace manifest — flags when the spec changed after the plan was made, via a `spec_hash` comparison
- Orchestration note for routing a `spec_contradiction` report to `canon/correct`, then resuming from an amended, re-gated plan
### Changed
- `exit-gate` records `spec_drifted_since_planning` as a gap when `spec_drift_warning` is set
- `recon` compares `spec_hash` over raw file bytes, so identical spec content never produces a false drift warning
- Correction routing passes the amended plan through `challenger`, and escalates to a human if the same criterion contradicts a second time
- `implementer` records `criteria_evidence` per task on completion — exact test/implementation file and line for every `covers_criteria` ID proven
- `exit-gate` uses aggregated `criteria_evidence` as pointers, but still independently confirms each criterion rather than trusting the pointer
### Fixed
- `implementer`, `reviewer`, `exit-gate`, and `recon` now carry the trust-boundary defense for workspace-reading agents — all four read project files and previously lacked the injection-resistance guard `adversary` already had
- `lambda` SKILL.md's `<io>` claimed it produces `changeset@1` — it doesn't; `changeset-analyzer` does. Documented that `lambda` produces per-task `criteria_evidence` instead
- `lambda` SKILL.md frontmatter version was stuck at 1.1.0 while `plugin.json` had moved to 1.2.0 — synced

## [1.1.0] - 2026-08-10
### Added
- `spec_file_path` propagation through the workspace manifest — recon verifies the file exists and emits `spec_file_warning` when absent instead of failing hard
- `covers_criteria` support — implementer reads a task's acceptance criteria from disk before writing tests when `spec_file_path` is available
### Changed
- `exit-gate` reads spec from disk when available; records `spec_file_unset` as a coverage gap when absent
- `reviewer` is now language-aware — loads `rust-hazards.md` or `typescript-hazards.md` from the workspace manifest's `language` field instead of assuming Rust
### Fixed
- Lambda SKILL.md's context management now correctly sources `spec_file_path` from `plan@1`, not `spec@1`

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `lambda` → `code` (displays as `/lambda:code`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- TDD implementation cycle: failing test → minimal code → passing → commit
- `axiom` exit-gate integration for verified handoff
- `changeset@1` output schema consumed by `delta` and `axiom`
- Subagents: recon, implementer, reviewer, exit-gate
