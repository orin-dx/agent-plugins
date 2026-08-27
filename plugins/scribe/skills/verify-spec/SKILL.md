---
name: verify-spec
description: >-
  Trigger when the user asks whether a spec matches its source: "is this grounded?", "does this spec match the requirement?", "check this spec against the requirement". Given a draft spec@1 plus the originating requirement@1 and optional research-report@1, checks whether each acceptance criterion is grounded in the source artifacts. Classifies criteria as supported, unsupported, or overfitted. Collects evidence only — does not produce a pass/fail verdict. Use before implementation, not after — for post-implementation drift, use scribe/spec-drift instead.
version: 2.0.0
---

# Scribe — Verify Spec

<overview>
Confirms a spec draft actually traces back to what the requirement (and research, if any) asked for — not whether the spec reads well, that's `scribe/audit-spec`'s job. Delegates to `verifier`, a neutral evidence collector with no pass/fail authority.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **verifier** | sonnet / medium | A draft spec@1 needs each acceptance criterion checked against its source requirement/research-report for grounding. |
</dispatch>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/requirement@1.json`, `shared/schemas/research-report@1.json`
</references>

<io>
**Consumes**: draft `spec@1`, originating `requirement@1`, optionally `research-report@1`
**Produces**: evidence report — supported / unsupported / overfitted per criterion. Route to `scribe/audit-spec`.
</io>
