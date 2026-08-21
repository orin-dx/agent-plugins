---
name: architect
description: >-
  Trigger when proof has returned a finding-report@1 and the confirmed defect class needs a structural fix — a change to the architecture, type system, interface boundary, or abstraction layer — rather than patches to individual instances. Given a finding-report@1, produces a spec@1 for the structural change that makes the defect class impossible or unrepresentable, not merely documented or harder to introduce. Acceptance criteria must be falsifiable at the type or API level.
version: 2.0.0
---

# Canon — Architect

<overview>
Closes the proof-to-design loop: proof surfaces what is broken, this skill specifies the structure that prevents it from being broken again. Delegates to `architect`. The output spec still goes through `canon/gate-spec` before feeding `vector` and `lambda` — architectural specs are not exempt from the gate.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **architect** | opus / high | A `finding-report@1`'s defect class calls for a structural fix — trait/type invariant or interface redesign — not instance patching. |
</dispatch>

<references>
`shared/schemas/finding-report@1.json`, `shared/schemas/spec@1.json`
</references>

<io>
**Consumes**: `finding-report@1` from `proof`
**Produces**: `spec@1` (or `arch-spec@1`) with trait/invariant contracts. Route to `canon/gate-spec`, then `vector` → `lambda`.
</io>
