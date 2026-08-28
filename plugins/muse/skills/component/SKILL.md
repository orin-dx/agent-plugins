---
name: component
description: >-
  Trigger when the user asks to spec a UI component: "spec this component", "draft a component spec", "write a spec for this design", "audit this component spec", "is this component spec ready?", "gate this component spec". Given a requirement@1 or free-text design intent, produces a spec@1 covering props, variants, per-state observable behavior, and accessibility criteria as testable propositions. Every criterion is falsifiable from outside the implementation; error cases and invalid prop combinations carry is_error_case: true. No TBDs anywhere in the document — genuinely unknown items go in non_goals or the reasoning scratchpad instead. Gated by a binding exit gate before the spec proceeds to planning.
version: 1.0.0
---

# Muse — Component Spec Skill

<overview>
Turns UI or design intent into a component spec a developer could implement — including its accessibility behavior — without asking a single clarifying question. One skill, one draft-audit-gate pipeline, reused unchanged regardless of which component is being specified. Muse audits the spec, not the implementation; for code-level accessibility hazard scanning after the component is built, see `ranger`'s accessibility hazard taxonomy.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** | sonnet / medium | A requirement@1 (or design intent) needs a first spec@1 draft covering props, variants, states, and accessibility criteria. |
| **auditor** | sonnet / medium | A drafted spec@1 needs adversarial review for missing states, missing accessibility criteria, or unmarked invalid prop combinations. |
| **exit-gate** | opus / high | An audited spec@1 needs a terminal binding pass/fail verdict before it proceeds to `navigator` for planning. |
</dispatch>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/verdict@1.json`
</references>

<io>
**Consumes**: `requirement@1`, or free-text design intent describing the component
**Produces**: `spec@1` (persisted to disk only after `exit-gate` passes) and, on failure, a `verdict@1` with blockers routed back to `drafter`. On pass, route the persisted `spec@1` — with `spec_file_path` set — to `navigator`.
</io>

<circuit_breaker>
Drafter → auditor review loops are capped at 2 iterations before reaching the exit gate. On round 2, unresolved debates about naming or phrasing are demoted to non-blocking notes rather than looping further. The exit gate itself allows up to 3 retries before escalating to a human reviewer.
</circuit_breaker>
