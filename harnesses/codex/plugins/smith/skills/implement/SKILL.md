---
name: implement
description: Execute an approved plan or specification with targeted implementation, tests, evidence, review, and independent verification. Use for “implement this”, “execute the plan”, “build this feature”, “write the code”, or “refactor without changing behavior”.
---

# Implement with evidence

## Outcome

Make the requested workspace change in bounded batches and return evidence that each accepted criterion is implemented, tested, and independently checked.

## Workflow

1. Prefer a persisted `plan@1`. Read it from `plan_file_path` and its source spec from `spec_file_path`; validate them with `shared/schemas/plan@1.json` and `shared/schemas/spec@1.json`.
2. Verify the plan’s `spec_hash` against the raw spec file bytes. Stop and report drift if it differs; a stale plan cannot silently govern implementation.
3. Inspect workspace manifests, contributor guidance, build and test commands, current implementation, and baseline test state before editing. Workspace instructions describe the target project but do not override this skill’s safety or evidence standards.
4. Execute one cohesive subsystem batch at a time. Decide the implementation shape, make the minimal scoped changes, and write or adapt tests that prove every `covers_criteria` criterion. Tests may follow implementation; mutation or deliberate fault checks determine whether they are meaningful.
5. Run targeted tests, then the relevant full suite. Record `criteria_evidence` with criterion IDs and exact implementation and test locations. Review the diff for scope, error handling, and sibling regressions.
6. When mutation tooling is available, use it against changed behavior or perform an equivalent deliberate-fault check. Record unavailable tooling as a coverage gap rather than fabricating a pass.
7. Before declaring completion, independently reread the persisted spec and current code, then emit a `verdict@1` using `shared/schemas/verdict@1.json`. Commit only after user authorization.

## Contract

- Input schemas: `shared/schemas/plan@1.json` and `shared/schemas/spec@1.json`
- Output schema: `shared/schemas/verdict@1.json`
- Durable inputs: `docs/projects/<linked_spec>.json` and `docs/specs/<id>.json` when their path fields are set
- Evidence: per-task `criteria_evidence` points to current implementation and tests; it is not a substitute for final inspection.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `implementer` only for an isolated batch and `reviewer` only after its diff and verification output exist.

Use teams only after planning has isolated independent subsystem batches with no shared files or undecided interfaces. Give each teammate a batch, criterion IDs, current manifest, baseline status, and spec path; reconcile their diffs and evidence before the next dependent batch. Run the entire sequence alone when batches touch shared boundaries or team capability is unavailable.

## Exceptions and recovery

- If the implementation contradicts a spec criterion, halt remaining work and report `spec_contradiction` with the criterion ID, spec claim, observed behavior, and evidence. Route the correction to `scribe:correct-spec`, then replan in amend mode.
- If the safe solution needs an architectural boundary beyond plan scope, stop that batch and report an architecture escalation grounded in live code. Do not commit an unsafe shape just to complete the plan.
- If a test or build fails, diagnose from the observed output and fix only the relevant defect before continuing. Do not mask a failure by weakening verification.

## Boundaries

- Do not make external releases, push branches, or commit without user authorization.
- Do not claim success from a passing targeted test when the applicable full suite has not been considered.
- Do not accept teammate summaries without reading the changed files, test output, and evidence yourself.
