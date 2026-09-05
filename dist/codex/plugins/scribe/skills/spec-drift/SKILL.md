---
name: spec-drift
description: Compare a persisted specification with current implementation and tests to find covered, uncovered, and drifted criteria. Use for “check spec drift” or “does the code still match this spec?”.
---

# Detect specification drift

## Outcome

Produce a read-only criterion-by-criterion report grounded in current code and tests, not in historical approval or stale evidence pointers.

## Workflow

1. Read the spec from `spec_file_path` and validate it with `shared/schemas/spec@1.json`. Report an unset path as a coverage gap rather than silently using a stale pasted copy.
2. Inspect current implementation, tests, public interfaces, and relevant runtime behavior for each criterion. Use prior `criteria_evidence` only as a starting location.
3. Classify each criterion as `covered`, `uncovered`, or `drifted`. Cite the current file and line or test result that supports the classification.
4. Separate missing verification from behavioral drift. A test absence is not proof that behavior is absent.
5. Return the report without changing code or the spec. Recommend `scribe:correct-spec` only when the spec itself conflicts with verified reality.

## Contract

- Input schema: `shared/schemas/spec@1.json`
- Input location: `spec_file_path`, normally `docs/specs/<id>.json`
- Output: read-only drift report with per-criterion evidence

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `reviewer` for a non-overlapping criterion group and reconcile classifications in the primary agent.

For a wide spec, team members may inspect independent criterion groups with fixed file scopes. The primary agent owns final classification consistency. Smaller audits run completely in one agent.

## Boundaries

- Do not modify implementation, tests, or the persisted spec during diagnosis.
- Do not treat documentation claims as proof that a criterion is implemented.
