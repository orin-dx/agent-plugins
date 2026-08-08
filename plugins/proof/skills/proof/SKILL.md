---
name: audit
description: >-
  Trigger this skill when the user asks to perform a bug hunt, code audit, find bugs, security audit, defect scan, vulnerability scan, code review for bugs, or asks "what's wrong with this code." Activate for any codebase language — Rust, TypeScript, or JavaScript. This skill runs a 5-phase pipeline: (1) recon builds a verified module manifest and detects the primary language from Cargo.toml or package.json; (2) scanner reads language-specific hazard taxonomies from shared/references/rust-hazards.md or shared/references/typescript-hazards.md and emits candidates in live files only; (3) boundary-tracer (conditional) traces field survival for T7 and T10 candidates; (4) adversary attempts to refute each candidate by tracing control flow — only unrebutted findings with concrete failing scenarios survive; (5) exit-gate independently re-reads code from scratch, checks for sibling gaps, confirms compile and tests pass, and escalates to human after 3 failed retries. Proof never reports bugs in dead or unreachable code. Output follows the finding-report@1 schema.
version: "2.0.0"
---

# proof — Cross-Language Bug-Hunting Skill

## Sub-skills

| Sub-skill | Purpose |
| :--- | :--- |
| `proof/scan` | Full hazard sweep across all categories in the workspace |
| `proof/focus` | Targeted scan — caller names one hazard category |
| `proof/verify` | Verify a single reported candidate bug |
| `proof/remediations` | Produce a structured fix plan from a finding-report |

---

## Pipeline

```
workspace → proof-recon → proof-scanner → [proof-boundary-tracer?] → proof-adversary → proof-exit-gate → finding-report@1
```

1. **Recon** — builds verified manifest: live files, dead files, entry points, language.
2. **Scan** — loads language-specific hazard reference, runs grep patterns against live files only, emits candidate@1 list.
3. **Boundary Tracer** *(conditional)* — traces field survival for T7 and T10 candidates. Skipped for all other taxonomies.
4. **Adversary** — reads actual code, traces control flow, tries to refute each candidate. Invoked once per candidate, never batched. Confirms only when a concrete failing scenario can be stated.
5. **Exit Gate** — after remediation, re-reads code from scratch, checks all confirmed findings are gone, scans for sibling gaps, verifies compile and tests. Escalates to human when retry_count exceeds 3.

---

## Dispatch Matrix

| Agent | Mode | Model / Effort | Loads | Input → Output |
| :--- | :--- | :--- | :--- | :--- |
| `proof-recon` | Workspace recon | haiku / low | — | workspace path → live/dead manifest + language |
| `proof-scanner` | Pattern matching | sonnet / medium | rust-hazards.md or typescript-hazards.md | manifest → candidate@1 list |
| `proof-boundary-tracer` | Data flow tracing | sonnet / medium | rust-hazards.md or typescript-hazards.md | T7/T10 candidate → field survival map. Conditional. |
| `proof-adversary` | Adversarial reasoning | opus / high | rust-hazards.md or typescript-hazards.md | candidate@1 (+ field map if T7/T10) → finding-report@1 entry or dismissal |
| `proof-exit-gate` | Exit verification | opus / high | — | finding-report@1 → verdict@1 |

---

## Language Detection

Recon inspects the workspace root:
- `Cargo.toml` present → language: `rust` → scanner and adversary load `shared/references/rust-hazards.md`
- `package.json` present → language: `typescript` or `javascript` → scanner and adversary load `shared/references/typescript-hazards.md`

---

## Dead Code Rule

Proof ONLY reports bugs in live, reachable code. Any file not traceable from an entry point is dead and excluded from all scanning and adversarial phases. This is enforced by the recon manifest.

---

## Output

All confirmed findings conform to the `finding-report@1` schema (`shared/schemas/finding-report@1.json`). The exit-gate verdict conforms to `verdict@1` (`shared/schemas/verdict@1.json`).
