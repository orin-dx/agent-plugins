---
name: gate
description: >-
  Trigger this skill when the user says "verify this", "check this spec", "check this plan", "check this requirement", "check this PR", "is this done?", "review this for completeness", "does this meet the criteria?", "gate this", or "quality check". Also activate before stage transitions: before starting implementation from a spec, before shipping from an implementation, before opening a PR from a branch. Applies to any stage artifact: requirements documents, design specs, implementation plans, code implementations, and pull requests. Do not activate for general question answering, code explanation, or exploratory work where no artifact boundary is being crossed. Activate when a defined artifact should be verified against stated criteria before downstream work proceeds. The axiom gate is the formal checkpoint: it either clears the artifact for the next stage or returns specific actionable blockers to the producing agent.
version: 1.2.0
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

| Stage | Agent | Model | Effort | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| 1 — Recon | `recon` | haiku | low | Inventory the artifact: type, location, criteria list, source files to read. No judgment. |
| 2 — Verify | `verifier` | sonnet | medium | Cross-reference each criterion against the source files. Classify as verified, failed, or unverifiable. Neutral — reports evidence only. |
| 3 — Exit Gate | `exit-gate` | opus | high | Produce the final verdict. Pass only if all criteria are verified with no unresolved failures. On fail, return specific actionable blockers. |

</three_stage_flow>

---

<axiom_protocol>

The protocol input is: `artifact_type`, `artifact_path`, `criteria` (explicit or derived from linked spec).

The protocol output is a `verdict@1` object: `pass` or `fail`, with `blockers` on failure and a `verdict_summary` for the orchestrator.

**Retry behavior**: Up to 3 retries. On each failure, the specific blockers are returned to the producing agent. At retry 3, escalate to the caller — do not loop indefinitely. Track `retry_count` in the verdict.

</axiom_protocol>

---

<sub_skills>

| Sub-skill | Artifact Type | Pipeline |
| :--- | :--- | :--- |
| `verify-requirement` | Requirements document | haiku/low → sonnet/medium → opus/high |
| `verify-spec` | Design specification | haiku/low → sonnet/medium → opus/high |
| `verify-plan` | Implementation plan | haiku/low → sonnet/medium → opus/high |
| `verify-implementation` | Code implementation | haiku/low → sonnet/medium → opus/high |
| `verify-pr` | Pull request | haiku/low → sonnet/medium → opus/high |
| `exit-gate` | Final verdict assembly (all types) | haiku/low → sonnet/medium → opus/high |

</sub_skills>

---

---

<framework_references>
- [Agent Best Practices](../../../shared/agent-best-practices.md)
- [Verdict Schema](../../../shared/schemas/verdict@1.json)
</framework_references>
