# canon — Specification

**Stage:** Spec · **Output:** `spec@1` · **Version:** 1.2.0

Drafts, audits, and gates unambiguous, testable specifications. Also designs structural remediation specs from proof's defect class findings, detects drift between a gated spec and the live codebase, and revises a gated spec when implementation reveals it was wrong. A spec that exits canon can be handed to a developer who has never spoken to the product team and implemented without clarifying questions. An adversarial exit gate enforces this guarantee — default disposition is fail. Once gated, the spec is written to disk and committed — downstream agents read it from its file, not from conversation context.

---

## When to Use

- You have a `requirement@1` (and optionally a `research-report@1`) and are ready to write a spec
- You need to verify that a draft spec's acceptance criteria are grounded in the source requirement
- You want to audit a spec for vague criteria, missing error cases, or unverifiable claims
- You need a binding pass/fail gate on a spec before it enters planning
- proof has returned a `finding-report@1` and the defect class requires a structural fix, not a patch
- You want to check whether the live codebase still matches a spec gated weeks or months ago
- lambda-implementer reported that a criterion contradicts observed system behavior and the spec itself needs correcting

**Invoke with:** `"Write a spec for this requirement"`, `"Draft a spec based on this research"`, `"Verify this spec against the requirement"`, `"Audit the spec for ambiguities"`, `"Gate this spec"`, `"Design the structural fix for this defect class"`, `"Check this spec for drift"`, `"Correct this spec — the criterion doesn't match reality"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `canon/draft` | Drafts a `spec@1` from a `requirement@1` and optional `research-report@1` — no TBDs permitted |
| `canon/verify` | Checks that each acceptance criterion is grounded in the source requirement or research report |
| `canon/drift` | Checks whether the live codebase still implements every criterion in a gated spec — covered, uncovered, or drifted |
| `canon/audit` | Adversarially reviews a spec for vague criteria, missing error cases, and unverifiable claims |
| `canon/gate` | Binding pass/fail verdict before the spec enters planning |
| `canon/correct` | Revises a previously gated spec after lambda-implementer reports a criterion contradicts observed system behavior |
| `canon/architect` | Produces a structural remediation `spec@1` from a `finding-report@1` — eliminates the defect class, not the instances |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `canon-drafter` | Drafter | sonnet / medium | Produces a `spec@1` from a `requirement@1` and optional `research-report@1`, or revises a gated spec in correction mode. No TBDs permitted. |
| `canon-verifier` | Draft Verifier | sonnet / medium | Checks that acceptance criteria are grounded in the source artifacts (pre-implementation only). Neutral — collects evidence only. |
| `canon-drift-checker` | Drift Detector | opus / high | On-demand, post-implementation: reads the spec from disk and the code from the workspace, classifies each criterion as covered, uncovered, or drifted. When a prior changeset's `criteria_evidence` is available, uses its pointers as a starting point but always independently re-verifies each one. |
| `canon-auditor` | Auditor | sonnet / medium | Adversarially reviews the spec for vague criteria, missing error cases, ambiguous language, and incomplete sections. |
| `canon-exit-gate` | Exit Gate | opus / high | Binding pass/fail verdict before the spec enters planning. Default disposition: fail. |
| `canon-architect` | Architectural Remediator | opus / high | Takes a `finding-report@1` from proof and produces a `spec@1` for the structural fix that eliminates the defect class. |

---

## Pipelines

**Standard drafting pipeline:**
```
requirement@1 [+ research-report@1]
  → canon-drafter
  → canon-verifier
  → canon-auditor
  → canon-exit-gate
  → [skill writes .claude/specs/<id>.json, commits it, sets spec_file_path]
  → spec@1
```

**On-demand drift pipeline (maintenance, any time after implementation):**
```
spec_file_path + workspace root
  → canon-drift-checker
  → drift report (covered / uncovered / drifted)
```

**Correction pipeline (triggered by a lambda-implementer spec_contradiction report):**
```
spec_file_path + criterion_id + contradiction report
  → canon-drafter (correction mode)
  → canon-verifier → canon-auditor → canon-exit-gate
  → [skill overwrites the same file, sets revision_note, commits]
  → corrected spec@1 → vector-planner (amend mode) → lambda resumes
```

**Architectural remediation pipeline (invoked after proof):**
```
finding-report@1
  → canon-architect
  → canon-exit-gate
  → spec@1 (architectural)
  → vector → lambda
```

`canon-verifier` checks draft specs against their source artifacts pre-implementation — it does not detect drift after code exists; that is `canon-drift-checker`'s job. `canon-architect` is not part of the standard drafting pipeline: it is invoked when proof returns a finding report and the root cause is structural.

---

## Exit Gate Conditions

The exit gate enforces four conditions. All must pass:

1. Every acceptance criterion is a testable proposition (binary true/false from outside the system)
2. No TBDs remain
3. Error cases are marked `is_error_case: true`
4. Scope fits a single planning cycle

On fail, specific blockers are returned to `canon-drafter` or `canon-architect` for
targeted retry. Maximum 3 retries before escalation to a human.

---

## Output Schemas

**`spec@1`** — see `shared/schemas/spec@1.json`

| Field | Required | Description |
| :--- | :--- | :--- |
| `id` | yes | Unique spec identifier |
| `purpose` | yes | One-sentence statement of what this spec accomplishes |
| `scope` | yes | What is in scope for this spec |
| `non_goals` | yes | Explicit list of what this spec does NOT cover |
| `acceptance_criteria` | yes | Array of testable propositions; each has `is_error_case` flag |
| `spec_file_path` | no | Workspace-relative path where this spec is written on disk. Set by the skill orchestrator after gate pass. |
| `revision_note` | no | Set only on a correction — what changed and why, citing the affected criterion_id |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

**`verdict@1`** — produced by `canon-exit-gate` only; see `shared/schemas/verdict@1.json`

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install canon
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed `spec@1` to **[vector](../vector/)** (implementation planning) or run it through
**[axiom](../axiom/)** for standalone verification against an existing implementation.

When **[proof](../proof/)** produces a `finding-report@1`, feed it to `canon-architect`
to design the structural remediation before returning to vector.
