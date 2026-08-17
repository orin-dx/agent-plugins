# Changelog

— canon

## [1.3.0] - 2026-08-17

### Added
- **Architectural Specs**: `architect` can now draft structural specs (`arch-spec`) for trait extractions, AST transforms, and subsystem invariants.
- **2-Round Circuit Breaker**: `drafter` and `auditor` reviews are capped at 2 iterations, demoting minor debates to non-blocking notes.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `canon:drafter`, `canon:auditor`, `canon:architect`, and `canon:exit-gate`.
- **Faster Drafting**: Standardized drafting and auditing on Sonnet to keep prompt caches hot and speed up spec generation.

## [1.2.0] - 2026-08-11
### Added
- `canon/correct` sub-skill — given a spec_file_path, criterion_id, and a contradiction report from implementer, revises the affected criterion (and dependents) and returns a corrected spec@1 with `revision_note` set; the correction re-enters the standard verify → audit → gate pipeline before overwriting the file
- `revision_note` field in `spec@1` schema — set only on corrections, describes what changed and why
- Spec file commit step in orchestration — the skill orchestrator now commits `.claude/specs/<id>.json` to version control after writing it, not just to the working tree; an uncommitted spec is invisible to drift-checker and a future session
### Changed
- `drafter` now supports correction mode as an alternate input path alongside fresh drafting from a requirement@1
- Correction re-entry now routes the amended plan through challenger before lambda resumes — amendment is not exempt from adversarial review
- `drift-checker` no longer presumes whether code or spec is wrong on a drifted classification — it states both sides and leaves the correction path to the caller
- `drift-checker` now carries the trust-boundary defense for workspace-reading agents — code comments and documentation claiming a criterion is satisfied are treated as untrusted data, not evidence
- `drift-checker` accepts a prior changeset's `criteria_evidence` as an optional starting pointer — but always re-reads and independently reconfirms each location rather than trusting that it is still accurate
### Fixed
- A second spec_contradiction on the same criterion_id after correction now escalates to a human instead of looping back to canon/correct indefinitely
- `drift-checker`'s `covered` output entries now use the same structured evidence shape as changeset@1's criteria_evidence (test/implementation file and line) instead of a free-text `evidence` string, so a drift check's freshly-confirmed pointers can be handed forward to the next check or exit gate
- Repaired pre-existing hard-wrapped paragraphs in drafter.md (backstory, goal, output) and canon SKILL.md (overview, canon/draft, canon/audit, canon/architect) left over from before this session

## [1.1.0] - 2026-08-10
### Added
- `drift-checker` agent (opus/high) — on-demand post-implementation drift detection; reads spec from disk, classifies criteria as covered, uncovered, or drifted
- `spec_file_path` field in `spec@1` schema — workspace-relative path set by the skill orchestrator after gate pass; downstream agents read the spec from disk rather than context
- `canon/drift` sub-skill in SKILL.md dispatching to `drift-checker`
- Post-gate orchestration instruction in SKILL.md — explicit step for writing spec to `.claude/specs/<id>.json` and setting `spec_file_path` after exit-gate passes
### Changed
- `verifier` is now grounding-only (pre-implementation); post-implementation drift checking is handled by the new `drift-checker`
- `drafter` returns the spec object only — it no longer writes to disk (skill orchestrator responsibility post-gate)
- Acceptance criterion quality standard in `drafter` and `auditor` now explicitly rejects criteria that require implementation knowledge to verify (semantic model principle): a criterion is only valid if a tester with no knowledge of the implementation can evaluate it from observable system behavior

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `canon` → `spec` (displays as `/canon:spec`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Spec drafting, review, verification, and drift detection against live code
- `spec@1` output schema consumed by `vector` and `axiom`
- Subagents: architect, drafter, auditor, verifier, exit-gate
