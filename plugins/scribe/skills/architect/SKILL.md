---
name: architect
description: >-
  Trigger when `finding-report@2`, `implementation-review@2`, or `implementation-result@1` identifies a structural defect class. Produce the smallest `spec@1` that makes recurrence impossible or machine-detectable through a type, API, boundary, invariant, lint, test, or CI rule.
version: 2.2.0
---

# Scribe — Architect

<overview>
Turn confirmed defect families into enforceable structural specs. Route every output through verify-spec, audit-spec, audit-architecture, and gate-spec before planning.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **architect** | claude-fable-5-1 / high | A confirmed defect family needs a structural boundary, domain model, or enforceable invariant. |
</dispatch>

<references>
`shared/schemas/finding-report@2.json`, `shared/schemas/implementation-review@2.json`, `shared/schemas/implementation-result@1.json`, `shared/schemas/spec@1.json`, and `shared/references/architecture-remediation.md`
</references>

<io>
**Consumes**: `finding-report@2`, `implementation-review@2`, or an architecture-escalating `implementation-result@1`.

**Produces**: one `spec@1` per structural boundary. Route through the full Scribe checks, Navigator, and Smith; after implementation passes, refresh the persisted architecture model.
</io>
