---
name: draft-spec
description: >-
  Trigger when the user asks to write or draft a spec: "spec this out", "draft a spec", "write a spec for this requirement". Given a requirement@1 and optionally a research-report@1, produces a spec@1 draft with purpose, scope, non_goals, api_surface (if applicable), and acceptance criteria. Every criterion is a testable proposition; error cases carry is_error_case: true. No TBDs anywhere in the document — genuinely unknown items go in non_goals or the reasoning scratchpad instead.
version: 2.0.0
---

# Canon — Draft Spec

<overview>
Turns a requirement (and optional research report) into a spec a developer could implement without asking a single clarifying question. Delegates to `drafter`. The draft is not final — it feeds `canon/verify-spec` and `canon/audit-spec` before `canon/gate-spec` decides pass or fail.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** | sonnet / medium | A requirement@1 (plus optional research-report@1) needs a first spec@1 draft. |
</dispatch>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: `requirement@1`, optionally `research-report@1`
**Produces**: `spec@1` draft (no disk write yet — that happens after `canon/gate-spec` passes). Route to `canon/verify-spec`.
</io>
