---
name: audit-spec
description: >-
  Trigger when the user asks to review a spec's quality: "review this spec", "is this spec complete?", "audit this spec". Given a spec@1, adversarially reviews it for untestable criteria, ambiguous language, missing error cases, scope overlap with other specs, and incomplete sections. Returns a structured issue list with specific rewritten suggested fixes, not generic guidance. Named audit-spec rather than audit because the bare word audit is already proof's plugin-level skill name (code/bug auditing) — a different domain entirely.
version: 2.0.0
---

# Canon — Audit Spec

<overview>
Checks whether a spec, taken on its own terms, is complete, unambiguous, and implementable without a single clarifying question — a different question from `canon/verify-spec`'s "does it trace back to the requirement?". Delegates to `auditor`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | A spec@1 needs adversarial quality review before it enters `canon/gate-spec`. |
</dispatch>

<references>
`shared/schemas/spec@1.json`
</references>

<io>
**Consumes**: `spec@1`
**Produces**: issues array (criterion_id, type, description, suggested_fix per issue) plus an overall pass/fail verdict on spec quality (not the binding gate verdict — that's `canon/gate-spec`). Route to `canon/gate-spec`.
</io>
