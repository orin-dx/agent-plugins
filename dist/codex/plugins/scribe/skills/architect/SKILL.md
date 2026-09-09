---
name: architect
description: Specify a structural correction when `finding-report@1` or `implementation-review@1` reveals a recurring defect class, missing domain model, or architectural gap.
---

# Specify a structural correction

## Outcome

Turn a confirmed defect class into a `spec@1` that makes recurrence impossible or machine-detectable.

## Decision standard

Validate the input against `shared/schemas/finding-report@1.json` or `shared/schemas/implementation-review@1.json`. Load `shared/references/architecture-remediation.md`, then the model and language evidence it selects.

Choose the smallest canonical type, domain operation, interface boundary, ownership rule, dependency direction, or invariant that prevents recurrence. Produce one `spec@1` per structural boundary using `shared/schemas/spec@1.json`. Each criterion must be enforceable by compilation, test, lint, or CI and cover required migration or error behavior.

Route completed specs through `scribe:verify-spec`, `scribe:audit-spec`, `scribe:audit-architecture`, and `scribe:gate-spec` in that order. After Navigator and Smith complete the structural change, run `scribe:audit-architecture` in refresh mode.

## Contract

- Input schemas: `shared/schemas/finding-report@1.json` and `shared/schemas/implementation-review@1.json`
- Output schema: `shared/schemas/spec@1.json`
- Optional model evidence: `shared/schemas/arch-model@1.json`
- Persistence after a pass: `docs/specs/<id>.json`

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `tracer` for each independent boundary and keep structural remedy selection with the primary `author`.

If a defect crosses independent subsystems, teammates may trace each boundary and its callers. The primary agent must choose one coherent structural remedy and author the spec. For a single boundary, work alone.

## Boundaries

- Do not prescribe a broad rewrite when an enforceable local boundary removes the defect class.
- Do not treat a plausible finding as confirmed without reproducing or reading its evidence.
