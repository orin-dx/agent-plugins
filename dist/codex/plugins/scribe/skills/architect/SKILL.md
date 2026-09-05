---
name: architect
description: Specify a structural correction for a confirmed defect class when local patches cannot make the class impossible. Use after a `finding-report@1` reveals a boundary, type, or abstraction failure.
---

# Specify a structural correction

## Outcome

Turn a confirmed defect class into a `spec@1` that changes the relevant type, API, or architectural boundary rather than documenting a fragile patch pattern.

## Workflow

1. Validate the finding report with `shared/schemas/finding-report@1.json` and inspect cited live code, trigger conditions, and root cause.
2. Determine whether a structural constraint can prevent recurrence: canonical type, interface boundary, ownership rule, dependency direction, or enforceable invariant.
3. Draft a `spec@1` using `shared/schemas/spec@1.json`. Write acceptance criteria that prove the defect class is unrepresentable or rejected, including migration and error behavior where needed.
4. State non-goals so the structural correction does not become an unrelated redesign.
5. Route the draft through `scribe:verify-spec`, `scribe:audit-spec`, `scribe:audit-architecture`, and `scribe:gate-spec` before it reaches planning.

## Contract

- Input schema: `shared/schemas/finding-report@1.json`
- Output schema: `shared/schemas/spec@1.json`
- Optional model evidence: `shared/schemas/arch-model@1.json`
- Persistence after a pass: `docs/specs/<id>.json`

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `tracer` for each independent boundary and keep structural remedy selection with the primary `author`.

If a defect crosses independent subsystems, teammates may trace each boundary and its callers. The primary agent must choose one coherent structural remedy and author the spec. For a single boundary, work alone.

## Boundaries

- Do not prescribe a broad rewrite when an enforceable local boundary removes the defect class.
- Do not treat a plausible finding as confirmed without reproducing or reading its evidence.
