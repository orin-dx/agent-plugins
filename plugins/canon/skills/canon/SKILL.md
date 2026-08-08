---
name: spec
description: >-
  Trigger this skill when the user asks to write or draft a spec, says "spec this out",
  wants to check whether a spec is complete or unambiguous, says "review this spec",
  asks whether a spec matches the source requirement ("is this grounded?"), asks for a
  structural fix after proof surfaces a defect class, or needs a pass/fail gate before
  planning. Also activate when converting a requirement or research report into a
  structured specification document, or when proof has returned a finding-report and the
  fix is architectural rather than a local patch. This skill produces spec@1 artifacts
  where every acceptance criterion is a testable proposition — no TBDs, no ambiguous
  language. Criteria must be confirmable true or false from the outside; error cases
  carry their own dedicated criteria. Use canon to catch untestable language ("the system
  should be responsive"), ambiguous scope, missing error cases, unsupported criteria, and
  defect classes that require structural elimination rather than instance patching.
version: "1.1.0"
---

# canon — Specification Skill

<overview>
canon turns requirements and research reports into unambiguous, testable specifications,
and turns defect class findings into architectural remediation specs. It enforces one
standard throughout: a developer who reads the output spec must be able to write an
implementation without asking a single clarifying question, and every acceptance
criterion must translate directly to a test case or type-level invariant check.
</overview>

---

<sub_skills>

### canon/draft
Given a `requirement@1` and optionally a `research-report@1`, produce a `spec@1` draft
with purpose, scope, non_goals, api_surface (if applicable), and acceptance criteria.
All criteria are testable propositions; error cases are covered with `is_error_case: true`.

### canon/verify
Given a draft `spec@1` plus the originating `requirement@1` and optional
`research-report@1`, check whether each acceptance criterion is grounded in the source
artifacts. Classifies criteria as supported, unsupported, or overfitted. Collects
evidence only — does not produce a pass/fail verdict.

### canon/audit
Given a `spec@1`, adversarially review it for untestable criteria, ambiguous language,
missing error cases, scope overlap, and incomplete sections. Returns a structured issue
list with specific rewritten suggested fixes.

### canon/gate
Given a `spec@1`, produce a binding pass/fail verdict before the spec enters planning.
Default disposition is fail. On fail, returns specific blockers the drafter can act on
without asking a follow-up question.

### canon/architect
Given a `finding-report@1` from proof, produce a `spec@1` for the structural change that
eliminates the defect class — not a patch of individual instances but the abstraction
boundary, type invariant, or interface redesign that makes the class impossible to
reintroduce. This sub-skill closes the proof-to-design loop.

</sub_skills>

---

<artifact_contracts>

**Consumes**: `requirement@1`, `research-report@1` (optional), `finding-report@1` (canon/architect only)

**Produces**: `spec@1`, `verdict@1` (canon/gate only)

</artifact_contracts>

---

<pipeline>

**Standard drafting pipeline:**
```
requirement@1 [+ research-report@1]
  → canon-drafter
  → canon-verifier
  → canon-auditor
  → canon-exit-gate
  → spec@1
```

**Architectural remediation pipeline (invoked after proof):**
```
finding-report@1
  → canon-architect
  → canon-exit-gate
  → spec@1 (architectural)
  → vector → lambda
```

`canon-architect` is not part of the standard drafting pipeline. It is invoked when
proof returns a `finding-report@1` and the root cause requires a structural fix. The
output spec feeds back into vector for planning.

</pipeline>

---

<framework_references>
- [Agent Best Practices](../../../shared/agent-best-practices.md)
- [Spec Schema](../../../shared/schemas/spec@1.json)
- [Verdict Schema](../../../shared/schemas/verdict@1.json)
- [Finding Report Schema](../../../shared/schemas/finding-report@1.json)
</framework_references>

---

<subagent_dispatch_matrix>

| Agent | Sub-skill | When to Delegate |
| :--- | :--- | :--- |
| **`canon-drafter`** | draft | Producing a new spec from a requirement or research report. |
| **`canon-verifier`** | verify | Checking that each acceptance criterion is grounded in the source artifacts. |
| **`canon-auditor`** | audit | Adversarial quality review for untestable language, ambiguity, and missing error cases. |
| **`canon-exit-gate`** | gate | Binding pass/fail judgment before handing the spec to planning. |
| **`canon-architect`** | architect | Designing the structural fix for a defect class surfaced by proof. |

</subagent_dispatch_matrix>
