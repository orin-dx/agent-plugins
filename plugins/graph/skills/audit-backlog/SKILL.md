---
name: audit-backlog
description: >-
  Trigger when the user asks about overall backlog health: "what's in the backlog", "audit the backlog", "what requirements are missing coverage". Cross-references all open requirement@1 objects against existing specs and implementation files. Returns per-requirement status (covered, partial, missing, duplicate) with evidence, plus a structured summary — per-status counts and an optional one-clause note, not a prose paragraph. Named audit-backlog rather than bare audit because that word is already proof's plugin-level skill name (code/bug auditing) — a different domain entirely.
version: 2.0.0
---

# Graph — Audit Backlog

<overview>
The full-backlog version of `graph/connect-requirement` — same agent, wider scope. Use this before planning to prevent duplicate or redundant work across the whole open backlog, not just one requirement.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | All open requirement@1 objects need cross-referencing against specs and implementation for coverage and duplicates. |
</dispatch>

<references>
`shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: all open `requirement@1` objects, workspace access
**Produces**: audit report — per-requirement status/evidence/duplicate_of, plus a backlog health summary. Read-only; does not modify any files.
</io>
