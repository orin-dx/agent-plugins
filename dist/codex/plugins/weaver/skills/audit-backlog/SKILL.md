---
name: audit-backlog
description: Audit the health of a backlog of open requirements against specifications, plans, and implemented evidence. Use for “audit the backlog”, “what is missing coverage?”, or “what should we clean up?”.
---

# Audit the backlog

## Outcome

Deliver a read-only backlog health report with evidence for every open requirement and a compact aggregate summary.

## Workflow

1. Enumerate candidate requirement artifacts and validate each against `shared/schemas/requirement@1.json`.
2. Build an evidence map from requirements to specs, plans, tests, implementation, and issue state. Read candidates before assigning a status.
3. Classify each requirement as `covered`, `partial`, `missing`, or `duplicate`. Use `duplicate_of` only when the outcome and stakeholder materially coincide.
4. Report stale or unverifiable handoffs separately from missing implementation; an uncommitted or absent durable artifact is a coverage gap, not proof of absence.
5. Return counts by status plus the highest-leverage cleanup actions. Do not rewrite requirements as part of the audit.

## Contract

- Requirement schema: `shared/schemas/requirement@1.json`
- Related schemas: `shared/schemas/spec@1.json` and `shared/schemas/plan@1.json`
- Input: all open requirement artifacts and workspace evidence
- Output: a read-only audit report with per-requirement evidence and aggregate counts

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `recon` for an independent subsystem inventory and `reviewer` to check the resulting evidence map.

Use agent teams only to inspect independent, non-overlapping subsystem partitions. Give each teammate a fixed file scope and require evidence pointers. The primary agent reconciles duplicates and produces the sole final report. On small backlogs, work alone.

## Boundaries

- Never infer implementation coverage from a plan that has no verified code or tests.
- Never modify tracker state, requirements, specs, or plans during an audit.
