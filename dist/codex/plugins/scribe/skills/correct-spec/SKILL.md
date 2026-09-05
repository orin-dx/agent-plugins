---
name: correct-spec
description: Correct a persisted specification when implementation evidence proves a criterion contradicts the live system. Use after a `spec_contradiction`, not for ordinary implementation difficulty.
---

# Correct a contradictory specification

## Outcome

Revise only the affected criteria and dependent plan implications while preserving the spec identity, durable path, and audit trail.

## Workflow

1. Read the spec from its `spec_file_path`; validate it using `shared/schemas/spec@1.json`.
2. Inspect the contradiction report and live workspace behavior. Confirm that the conflict is real rather than a missing implementation step or a misunderstood test.
3. Identify the affected criterion and dependent criteria. Amend only the necessary text, set `revision_note`, and retain the same spec ID and file path.
4. Run the corrected draft through `scribe:verify-spec`, `scribe:audit-spec`, `scribe:audit-architecture`, and `scribe:gate-spec`.
5. After a passing gate and user authorization, overwrite the existing `docs/specs/<id>.json` artifact, commit it, and send its changed criterion IDs to `navigator:plan` in amend mode.

## Contract

- Input schema: `shared/schemas/spec@1.json`
- Output schema: `shared/schemas/spec@1.json`
- Durable path: the existing `spec_file_path`, normally `docs/specs/<id>.json`
- Follow-on: amended `shared/schemas/plan@1.json` must go through planning review before implementation resumes.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `tracer` only for independent contradictory paths and keep the correction itself with the primary `author`.

This is a narrow evidence-and-judgment task; work alone by default. Use a teammate only when the contradiction spans independent code paths, and reconcile evidence before editing the spec.

## Boundaries

- Do not correct the spec for the same criterion twice without escalating to the user.
- Do not overwrite the persisted file or commit without user authorization.
- Do not continue implementation against a criterion confirmed to be contradictory.
