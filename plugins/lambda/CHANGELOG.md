# Changelog — lambda

## [1.2.0] - 2026-08-11
### Added
- `spec_contradiction` status in `lambda-implementer` output — emitted when an acceptance criterion contradicts observed system behavior rather than being merely hard to implement; carries a `contradiction` object naming the criterion_id, the spec's claim, and the observed behavior
- `spec_drift_warning` in the lambda-recon workspace manifest — computed by comparing the plan@1's `spec_hash` against the current spec file's content hash, surfacing when the spec changed after the plan was made
- Orchestration note in lambda SKILL.md for routing a `spec_contradiction` report to canon/correct, then resuming from an amended plan once the correction is gated
### Changed
- `lambda-exit-gate` now records a `spec_drifted_since_planning` gap in the verdict when spec_drift_warning is set — graceful degradation, consistent with existing spec_file_unset handling
- `lambda-recon` computes `spec_hash` comparisons over raw file bytes, not a parsed or re-serialized form, so identical spec content never produces a false drift warning
- Correction routing now passes the amended plan through vector-challenger before lambda resumes, and escalates to a human if the same criterion_id contradicts a second time after correction
- `lambda-implementer` now records `criteria_evidence` per task on completion — exact test file/line and implementation file/line for every covers_criteria ID the task proves, captured as a byproduct of the TDD cycle it already runs
- `lambda-exit-gate` uses the aggregated `criteria_evidence` as pointers for targeted verification — it reads the exact named location instead of searching the codebase cold, but still independently confirms the criterion holds rather than trusting the pointer
### Fixed
- `lambda-implementer`, `lambda-reviewer`, `lambda-exit-gate`, and `lambda-recon` now carry the trust-boundary defense for workspace-reading agents (backstory priming, named failure mode, output EARS rule) — all four read files from the project under implementation and previously lacked the same injection-resistance guard proof-adversary has had since its introduction
- Corrected the `<io>` section in lambda SKILL.md, which claimed lambda produces `changeset@1` — no lambda agent ever has; `delta-changeset-analyzer` produces it. Lambda now documents that it produces per-task `criteria_evidence`, which the caller hands to delta when shipping
- `lambda` SKILL.md frontmatter version was stuck at 1.1.0 while `plugin.json` had already moved to 1.2.0 in the prior round — synced to 1.2.0

## [1.1.0] - 2026-08-10
### Added
- `spec_file_path` propagation through workspace manifest — lambda-recon accepts spec_file_path as input, verifies the file exists, and emits `spec_file_warning` when absent rather than failing hard
- `covers_criteria` support — lambda-implementer reads the acceptance criteria for a task's `covers_criteria` IDs from disk before writing tests when `spec_file_path` is available
### Changed
- `lambda-exit-gate` reads spec from disk at `spec_file_path` when available; graceful degradation with `spec_file_unset` coverage gap recorded in the verdict when absent
- `lambda-reviewer` is now language-aware — loads `rust-hazards.md` or `typescript-hazards.md` based on the workspace manifest `language` field instead of applying hardcoded Rust non-negotiables
### Fixed
- Lambda SKILL.md context management now correctly identifies `spec_file_path` source as `plan@1` (propagated there by vector-planner from the spec) rather than `spec@1`

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
- Subagents: lambda-recon, lambda-implementer, lambda-reviewer, lambda-exit-gate
