---
name: gate
description: >-
  Trigger this skill when the user says "verify this", "check this spec", "check this plan", "check this requirement", "check this PR", "is this done?", "review this for completeness", "does this meet the criteria?", "gate this", or "quality check". Also activate before stage transitions: before starting implementation from a spec, before shipping from an implementation, before opening a PR from a branch. Applies to any stage artifact: requirements documents, design specs, implementation plans, code implementations, and pull requests. Do not activate for general question answering, code explanation, or exploratory work where no artifact boundary is being crossed. Activate when a defined artifact should be verified against stated criteria before downstream work proceeds. The axiom gate is the formal checkpoint: it either clears the artifact for the next stage or returns specific actionable blockers to the producing agent.
version: "1.0.0"
---

# Axiom Gate Skill

<overview>
Axiom is a cross-cutting verification gate. It runs whenever a stage artifact — requirement, spec, plan, implementation, or PR — must be confirmed against its criteria before the next stage begins. It does not generate artifacts; it only judges them.
</overview>

---

<when_to_activate>

Activate on any of these signals:

- Explicit gate request: "verify", "gate", "is this done?", "does this meet criteria?", "quality check"
- Stage transition: about to start implementation → gate the spec; about to open PR → gate the implementation
- Artifact type matches: requirement, spec, plan, implementation, PR

Do not activate for: general code questions, exploratory research, or authoring tasks where no artifact boundary is being crossed.

</when_to_activate>

---

<three_stage_flow>

### Stage 1 — Recon (haiku, low effort)
Inventory the artifact. Determine type, locate the file, enumerate the criteria it should be verified against (from a linked spec, requirement, or caller statement). Produce a structured manifest.

### Stage 2 — Verify (sonnet, medium effort)
Cross-reference the artifact against each criterion from the recon manifest. Find evidence for or against each. Produce a verification report with verified, failed, and unverifiable criteria.

### Stage 3 — Exit Gate (opus, high effort)
Produce the final verdict. Pass only if all criteria are verified with no unresolved failures. On fail, produce specific actionable blockers — not generic rejections. Each blocker must give the producing agent enough to make a targeted fix.

</three_stage_flow>

---

<axiom_protocol>

The protocol input is: `artifact_type`, `artifact_path`, `criteria` (explicit or derived from linked spec).

The protocol output is a `verdict@1` object: `pass` or `fail`, with `blockers` on failure and a `verdict_summary` for the orchestrator.

**Retry behavior**: Up to 3 retries. On each failure, the specific blockers are returned to the producing agent. At retry 3, escalate to the caller — do not loop indefinitely. Track `retry_count` in the verdict.

</axiom_protocol>

---

<sub_skills>

| Sub-skill | Artifact Type |
| :--- | :--- |
| `verify-requirement` | Requirements document |
| `verify-spec` | Design specification |
| `verify-plan` | Implementation plan |
| `verify-implementation` | Code implementation |
| `verify-pr` | Pull request |
| `exit-gate` | Final verdict assembly (all types) |

</sub_skills>

---

<success_criteria>

- **Pass**: all criteria confirmed verified, no unresolved failures. Downstream stage may proceed.
- **Fail**: one or more criteria unmet. Returns specific, actionable blockers. Producing agent must fix and resubmit. Gate does not proceed until pass or retry limit reached.

</success_criteria>

---

<framework_references>
- [Agent Best Practices](../../../shared/agent-best-practices.md)
- [Verdict Schema](../../../shared/schemas/verdict@1.json)
</framework_references>
