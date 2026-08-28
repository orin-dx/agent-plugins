---
name: gate
description: >-
  Trigger this skill when the user says "verify this", "check this spec", "check this plan", "check this requirement", "check this PR", "is this done?", "review this for completeness", "does this meet the criteria?", "gate this", or "quality check" — also before stage transitions: starting implementation from a spec, shipping from an implementation, opening a PR from a branch. Applies to any stage artifact: requirements, specs, plans, implementations, PRs. Do not activate for general Q&A, code explanation, or exploratory work with no artifact boundary being crossed. The gate either clears the artifact for the next stage or returns specific, actionable blockers to the producing agent.
version: 1.2.0
---

# Sentinel Gate Skill

<overview>
Sentinel is a cross-cutting verification gate. It runs whenever a stage artifact — requirement, spec, plan, implementation, or PR — must be confirmed against its criteria before the next stage begins. It does not generate artifacts; it only judges them.
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

One skill, one three-agent pipeline, reused against whatever artifact type it's handed — requirement, spec, plan, implementation, PR, changeset, finding-report. `recon`'s job is exactly to work out what it's looking at and what criteria apply, so the same chain runs unchanged regardless of artifact type — there is no separate sub-skill or agent set per type.

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

<framework_references>
- [Verdict Schema](../../../shared/schemas/verdict@1.json)
</framework_references>
