# scribe — Specification

**Stage:** Spec · **Output:** `spec@1` · **Version:** 3.1.0

Turns requirements into unambiguous, testable specs a developer can implement without a single clarifying question — and keeps them that way after implementation starts.

- **Drafts, audits, and gates** specs against that standard; an adversarial exit gate enforces it, default disposition fail
- **Checks whole-system architectural fit** against a persisted architecture model before a spec reaches the gate — not just internal consistency
- **Designs structural remediation specs** from ranger's defect-class findings
- **Detects drift** between a gated spec and the live codebase
- **Revises a gated spec** when implementation reveals it was wrong

Once gated, the spec is written to disk and committed — downstream agents read it from the file, never from conversation context.

Eight independently-triggered skills, not a linear pipeline — pick the one that matches the task.

---

## When to Use

- You have a `requirement@1` (and optionally a `research-report@1`) and are ready to write a spec
- You need to verify that a draft spec's acceptance criteria are grounded in the source requirement
- You want to audit a spec for vague criteria, missing error cases, or unverifiable claims
- You want to check whether a spec fits the codebase's actual module boundaries, canonical abstractions, and invariants — not just whether it's internally consistent
- You need a binding pass/fail gate on a spec before it enters planning
- ranger has returned a `finding-report@1` and the defect class requires a structural fix, not a patch
- You want to check whether the live codebase still matches a spec gated weeks or months ago
- implementer reported that a criterion contradicts observed system behavior and the spec itself needs correcting

**Invoke with:** `"Write a spec for this requirement"`, `"Draft a spec based on this research"`, `"Verify this spec against the requirement"`, `"Audit this spec"`, `"Check this spec against our architecture"`, `"Gate this spec"`, `"Design the structural fix for this defect class"`, `"Check this spec for drift"`, `"Correct this spec — the criterion doesn't match reality"`

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install scribe
```

**AGY** — installs the full repo; see the [root README](../../README.md#install) for instructions.

**Codex** — see the [root Codex setup](../../README.md#codex), then run `codex plugin add scribe@wisp-plugins`.

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `scribe/draft-spec` | Drafts a `spec@1` from a `requirement@1` and optional `research-report@1` — no TBDs permitted | `drafter` |
| `scribe/verify-spec` | Checks that each acceptance criterion is grounded in the source requirement or research report | `verifier` |
| `scribe/spec-drift` | Checks whether the live codebase still implements every criterion in a gated spec — covered, uncovered, or drifted | `drift-checker` |
| `scribe/audit-spec` | Adversarially reviews a spec for vague criteria, missing error cases, and unverifiable claims | `auditor` |
| `scribe/audit-architecture` | Checks a spec against the workspace's persisted architecture model — boundary violations, competing abstractions, invariant conflicts; builds/refreshes the model on demand | `arch-auditor` |
| `scribe/gate-spec` | Binding pass/fail verdict before the spec enters planning; writes the passed spec to disk | `exit-gate` |
| `scribe/correct-spec` | Revises a previously gated spec after implementer reports a criterion contradicts observed system behavior | `drafter` (correction mode) |
| `scribe/architect` | Produces a structural remediation `spec@1` from a `finding-report@1` — eliminates the defect class, not the instances | `architect` |

`audit-spec` and `gate-spec` are not bare `audit`/`gate` — those words are already taken by `ranger` and `sentinel`'s own plugin-level skills. See `shared/constitution.md`'s Skill Names rule.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `drafter` | Drafter | sonnet / medium | Produces a `spec@1` from a `requirement@1` and optional `research-report@1`, or revises a gated spec in correction mode. No TBDs permitted. |
| `verifier` | Draft Verifier | sonnet / medium | Checks that acceptance criteria are grounded in the source artifacts (pre-implementation only). Neutral — collects evidence only. |
| `drift-checker` | Drift Detector | opus / high | On-demand, post-implementation: reads the spec from disk and the code from the workspace, classifies each criterion as covered, uncovered, or drifted. When a prior changeset's `criteria_evidence` is available, uses its pointers as a starting point but always independently re-verifies each one. |
| `auditor` | Auditor | sonnet / medium | Adversarially reviews the spec for vague criteria, missing error cases, ambiguous language, incomplete sections, unnecessary prose, and fields that cross into another spec (persisted, serialized, or transmitted) without a round-trip guarantee on the far side. |
| `arch-auditor` | System Architecture Auditor | claude-fable-5-1 / high | Checks a spec against the workspace's persisted `arch-model@1` for boundary violations, competing abstractions, and invariant conflicts — system scope, not spec scope. Also builds/refreshes the model itself in build mode. |
| `exit-gate` | Exit Gate | opus / high | Binding pass/fail verdict before the spec enters planning. Default disposition: fail. |
| `architect` | Architectural Remediator | claude-fable-5-1 / high | Takes a `finding-report@1` from ranger and produces a `spec@1` for the structural fix that eliminates the defect class. Reactive counterpart to `arch-auditor`. |

---

## Pipelines

**Standard drafting pipeline:**
```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10,ry:10,font-size:14px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10,ry:10,font-size:13px,font-weight:500;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10,ry:10,font-size:14px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10,ry:10,font-size:14px,font-weight:600;

    Req["requirement@1
    + research-report@1"] --> Draft["scribe/draft-spec
    drafter"]
    Draft --> Verify["scribe/verify-spec
    verifier"]
    Verify --> Audit["scribe/audit-spec
    auditor"]
    Audit --> ArchAudit["scribe/audit-architecture
    arch-auditor"]
    ArchAudit --> Gate["scribe/gate-spec
    exit-gate"]
    Gate -->|pass| Spec(["spec@1
    written + committed"])

    class Req source
    class Draft,Verify,Audit,ArchAudit engine
    class Gate router
    class Spec output
```

**On-demand drift check (maintenance, any time after implementation):**
```
spec_file_path + workspace root
  → scribe/spec-drift (drift-checker)
  → drift report (covered / uncovered / drifted)
```

**Correction pipeline (triggered by an implementer spec_contradiction report):**
```
spec_file_path + criterion_id + contradiction report
  → scribe/correct-spec (drafter, correction mode)
  → scribe/verify-spec → scribe/audit-spec → scribe/audit-architecture → scribe/gate-spec
  → [skill overwrites the same file, sets revision_note, commits]
  → corrected spec@1 → planner (amend mode) → smith resumes
```

**Architectural remediation pipeline (invoked after ranger):**
```
finding-report@1
  → scribe/architect (architect)
  → scribe/gate-spec (exit-gate)
  → spec@1 (architectural)
  → navigator → smith
```

`scribe/verify-spec` checks draft specs against their source artifacts pre-implementation — it does not detect drift after code exists; that is `scribe/spec-drift`'s job. `scribe/audit-spec` checks a spec on its own terms; `scribe/audit-architecture` checks it against the rest of the system — a spec can pass the first and still fail the second. `scribe/architect` is not part of the standard drafting pipeline: it is invoked when ranger returns a finding report and the root cause is structural.

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
| `spec_file_path` | no | Workspace-relative path where this spec is written on disk. Set by `scribe/gate-spec` after pass. |
| `revision_note` | no | Set only on a correction — what changed and why, citing the affected criterion_id |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

**`verdict@1`** — produced by `scribe/gate-spec` only; see `shared/schemas/verdict@1.json`

**`arch-audit@1`** — produced by `scribe/audit-architecture` (check mode); see `shared/schemas/arch-audit@1.json`

**`arch-model@1`** — the persisted architecture model, produced by `scribe/audit-architecture` (build mode) and written to `docs/architecture/model.json`; see `shared/schemas/arch-model@1.json`

---

## Exit Gate Conditions

`scribe/gate-spec` enforces four conditions on the spec itself — whole-system architectural fit is `scribe/audit-architecture`'s job, checked upstream, not re-litigated here. All four must pass:

1. Every acceptance criterion is a testable proposition (binary true/false from outside the system)
2. No TBDs remain
3. Error cases are marked `is_error_case: true`
4. Scope fits a single planning cycle

On fail, specific blockers are returned to `scribe/draft-spec` or `scribe/architect` for targeted retry. Maximum 3 retries before escalation to a human.

---

## Next Stage

Feed `spec@1` to **[navigator](../navigator/)** (implementation planning) or run it through **[sentinel](../sentinel/)** for standalone verification against an existing implementation.

When **[ranger](../ranger/)** produces a `finding-report@1`, feed it to `scribe/architect` to design the structural remediation before returning to navigator.
