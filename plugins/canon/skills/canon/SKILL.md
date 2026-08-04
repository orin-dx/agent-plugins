---
name: canon
description: >-
  Trigger this skill when the user asks to write or draft a spec, says "spec this out", wants to check whether a spec is complete or unambiguous, says "review this spec", asks whether a spec matches the code ("has this drifted?", "is the spec still accurate?"), or has a PR and wants to know if the spec needs updating. Also activate when converting a requirement or research report into a structured specification document. This skill produces spec@1 artifacts where every acceptance criterion is a testable proposition — no TBDs, no ambiguous language. Criteria must be confirmable true or false from the outside; error cases carry their own dedicated criteria. Use canon to catch untestable language ("the system should be responsive"), ambiguous scope, missing error cases, and drift between a written spec and the actual implementation.
version: "1.0.0"
---

# canon — Specification Skill

<overview>
canon turns requirements and research reports into unambiguous, testable specifications. It enforces a single standard: a developer who reads the output spec must be able to write an implementation without asking a single clarifying question, and every acceptance criterion must translate directly to a test case.
</overview>

---

<sub_skills>

### canon/draft
Given a `requirement@1` and optionally a `research-report@1`, produce a `spec@1` draft with purpose, scope, non_goals, api_surface (if applicable), and acceptance criteria. All criteria are testable propositions; error cases are covered with `is_error_case: true`.

### canon/review
Given a `spec@1`, audit it for untestable criteria, ambiguous language, missing error cases, scope overlap, and incomplete sections. Returns a structured issue list with suggested fixes.

### canon/verify
Given a `spec@1` and a workspace path, check whether every acceptance criterion is implemented in code. Reports confirmed matches, mismatches (spec drift), and unverifiable claims that require runtime testing.

### canon/changeset
Given a `spec@1` and a set of code changes (diff or PR), determine whether the spec needs updating. Returns a precise list of stale or incorrect criteria with suggested rewrites.

</sub_skills>

---

<success_criteria>
A developer can read the spec and write the implementation without asking a single clarifying question. Every acceptance criterion translates directly to a test case.
</success_criteria>

---

<artifact_contracts>

**Consumes**: `requirement@1`, `research-report@1` (optional)

**Produces**: `spec@1`

</artifact_contracts>

---

<framework_references>
- [Agent Best Practices](../../../shared/agent-best-practices.md)
- [Spec Schema](../../../shared/schemas/spec@1.json)
- [Verdict Schema](../../../shared/schemas/verdict@1.json)
</framework_references>

---

<subagent_dispatch_matrix>

| Agent | Sub-skill | When to Delegate |
| :--- | :--- | :--- |
| **`canon-drafter`** | draft | Producing a new spec from a requirement or research report. |
| **`canon-auditor`** | review | Checking a spec for quality, completeness, and testability. |
| **`canon-verifier`** | verify | Detecting drift between a spec and actual code in a workspace. |
| **`canon-exit-gate`** | (gate) | Final pass/fail judgment before handing the spec to planning. |

</subagent_dispatch_matrix>
