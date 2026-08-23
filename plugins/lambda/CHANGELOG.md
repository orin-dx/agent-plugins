# Changelog

— lambda

## [1.6.1] - 2026-08-23

### Fixed
- `needs_architecture` had no routing in the skill's `<context_management>` — unlike its `needs_context`/`spec_contradiction` siblings, a caller had no defined next step for it. Added the same re-entry sequence as `spec_contradiction`: wrap `architecture_escalation` into a single-finding `finding-report@1`, route to `canon/architect`, then `gate-spec` → `planner` (amend) → `challenger` before resuming.

## [1.6.0] - 2026-08-23

### Added
- **`implementer`**: default posture for any criterion whose value can be absent, wrong, or stale, especially at a process, crate, or serialization boundary — a sum type, discriminated union, or Result-shaped representation, not a raw value paired with a separate boolean. See `shared/references/boundary-value-shapes.md` (new).
- `needs_architecture` status and `architecture_escalation` output object — `implementer` reports these instead of implementing the unsafe shape when the safe one needs a change beyond the current task's own scope; escalates toward `canon:architect`.

## [1.5.0] - 2026-08-22

### Added
- **`reviewer`**: now flags doc comments or inline comments that restate a signature, narrate an alternative not taken, or pad a genuinely simple point — see `shared/references/code-comments.md`. Fresh-read backstop for `implementer`'s own comment-writing rule, since a rule stated once at the start of a long TDD loop can't be trusted to hold for the whole task.

### Changed
- **`implementer`**: writes doc/inline comments per `shared/references/code-comments.md` — states what the comment's reader needs, not a restated signature or narrated process.
- **`recon`**: `reasoning` scratchpad capped to 1-2 sentences — it's discarded, not read by a human, and this is mechanical enumeration.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `implementer`'s frontmatter description tightened; no routing behavior changed.

## [1.4.2] - 2026-08-21

### Fixed
- SKILL.md and README.md documented a fictional "Sub-skills" table (`lambda/implement`, `lambda/generate-tests`, `lambda/explain`, `lambda/refactor`) with slash-path names that look like independently invokable skills — lambda has exactly one skill directory, and no agent implements "generate-tests," "explain," or "refactor" as a distinct mode. Replaced with an honest description of the one real pipeline (recon → [implementer → mutator → reviewer] × N → exit-gate) and a Capability Gaps table naming which trigger phrases have no agent behind them.
- README's version line was stuck at 1.2.0 while `plugin.json` had already moved to 1.4.1.
### Changed
- README's plain-text pipeline is now a Mermaid diagram styled with the palette from `shared/references/orin-visual-standard.md`, with the per-task loop (`implementer` → `mutator` → `reviewer`) in its own subgraph, separate from the one-time `recon`/`exit-gate` bookends.

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
- `spec_contradiction` status in `implementer` output — emitted when an acceptance criterion contradicts observed system behavior rather than being merely hard to implement; carries a `contradiction` object naming the criterion_id, the spec's claim, and the observed behavior
- `spec_drift_warning` in the recon workspace manifest — computed by comparing the plan@1's `spec_hash` against the current spec file's content hash, surfacing when the spec changed after the plan was made
- Orchestration note in lambda SKILL.md for routing a `spec_contradiction` report to canon/correct, then resuming from an amended plan once the correction is gated
### Changed
- `exit-gate` now records a `spec_drifted_since_planning` gap in the verdict when spec_drift_warning is set — graceful degradation, consistent with existing spec_file_unset handling
- `recon` computes `spec_hash` comparisons over raw file bytes, not a parsed or re-serialized form, so identical spec content never produces a false drift warning
- Correction routing now passes the amended plan through challenger before lambda resumes, and escalates to a human if the same criterion_id contradicts a second time after correction
- `implementer` now records `criteria_evidence` per task on completion — exact test file/line and implementation file/line for every covers_criteria ID the task proves, captured as a byproduct of the TDD cycle it already runs
- `exit-gate` uses the aggregated `criteria_evidence` as pointers for targeted verification — it reads the exact named location instead of searching the codebase cold, but still independently confirms the criterion holds rather than trusting the pointer
### Fixed
- `implementer`, `reviewer`, `exit-gate`, and `recon` now carry the trust-boundary defense for workspace-reading agents (backstory priming, named failure mode, output EARS rule) — all four read files from the project under implementation and previously lacked the same injection-resistance guard adversary has had since its introduction
- Corrected the `<io>` section in lambda SKILL.md, which claimed lambda produces `changeset@1` — no lambda agent ever has; `changeset-analyzer` produces it. Lambda now documents that it produces per-task `criteria_evidence`, which the caller hands to delta when shipping
- `lambda` SKILL.md frontmatter version was stuck at 1.1.0 while `plugin.json` had already moved to 1.2.0 in the prior round — synced to 1.2.0

## [1.1.0] - 2026-08-10
### Added
- `spec_file_path` propagation through workspace manifest — recon accepts spec_file_path as input, verifies the file exists, and emits `spec_file_warning` when absent rather than failing hard
- `covers_criteria` support — implementer reads the acceptance criteria for a task's `covers_criteria` IDs from disk before writing tests when `spec_file_path` is available
### Changed
- `exit-gate` reads spec from disk at `spec_file_path` when available; graceful degradation with `spec_file_unset` coverage gap recorded in the verdict when absent
- `reviewer` is now language-aware — loads `rust-hazards.md` or `typescript-hazards.md` based on the workspace manifest `language` field instead of applying hardcoded Rust non-negotiables
### Fixed
- Lambda SKILL.md context management now correctly identifies `spec_file_path` source as `plan@1` (propagated there by planner from the spec) rather than `spec@1`

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
