---
name: proof
description: >-
  Trigger this skill when the user asks to perform a bug hunt, code audit, find bugs, security audit, defect scan, vulnerability scan, code review for bugs, or asks "what's wrong with this code." Activate for any codebase language — Rust, TypeScript, or JavaScript. This skill runs a 4-phase pipeline: (1) recon builds a verified module manifest and detects the primary language from Cargo.toml or package.json; (2) scanner reads language-specific hazard taxonomies from shared/references/rust.md or shared/references/typescript.md and identifies candidate bugs in live files only; (3) adversary attempts to refute each candidate by tracing control flow and trigger conditions — only unrebutted findings survive; (4) exit-gate independently verifies that all confirmed findings are resolved after remediation, checks for sibling gaps, and confirms the workspace still compiles and tests pass. Proof never reports bugs in dead or unreachable code. Output follows the finding-report@1 schema.
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

## 4-Phase Flow

```
proof-recon → proof-scanner → proof-adversary → proof-exit-gate
```

1. **Recon** — builds verified manifest: live files, dead files, entry points, language.
2. **Scan** — reads language-specific heuristics, emits candidate findings with file:line and trigger condition.
3. **Adversary** — reads actual code, traces control flow, refutes or confirms each candidate.
4. **Exit Gate** — after remediation, independently re-reads code from scratch, checks all confirmed findings are gone, scans for sibling gaps, verifies compile + tests.

---

## Language Detection

Recon inspects the workspace root:
- `Cargo.toml` present → language: `rust` → scanner loads `shared/references/rust.md`
- `package.json` present → language: `typescript` or `javascript` → scanner loads `shared/references/typescript.md`

---

## Dead Code Rule

Proof ONLY reports bugs in live, reachable code. Any file not traceable from an entry point is dead and excluded from all scanning and adversarial phases. This is enforced by the recon manifest.

---

## Output

All confirmed findings conform to the `finding-report@1` schema (`shared/schemas/finding-report@1.json`). The exit-gate verdict conforms to `verdict@1` (`shared/schemas/verdict@1.json`).
