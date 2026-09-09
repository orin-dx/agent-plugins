---
name: audit
description: >-
  Activate for bug hunts, security audits, suspected defects, or post-remediation checks in Rust, TypeScript, or JavaScript. Build a live-code manifest, scan the matching hazard taxonomy, trace boundary fields when required, and try to refute every candidate. Report only reachable confirmed or plausible defects. Group confirmed findings by shared root cause; when repeated defects suggest a missing domain concept or architectural constraint, route the report to `scribe:architect` before remediation. Verify fixes, syntactic siblings, semantic siblings, compilation, and tests before closing.
version: 2.3.0
---

# Ranger — Cross-Language Bug Hunting

## Modes

- Full sweep: scan every hazard taxonomy.
- Targeted scan: scan the named category.
- Candidate verification: send the supplied candidate directly to adversary.
- Post-remediation check: run exit-gate against prior findings.

## Pipeline

```text
workspace → recon → scanner → [boundary-tracer] → adversary → finding-report@1 → exit-gate
```

1. `recon` inventories live files, entry points, and language. Dead code leaves the pipeline.
2. `scanner` loads the matching hazard reference and emits `candidate@1` without judgment.
3. `boundary-tracer` produces `field-survival-map@1` for T7 and T10 candidates.
4. `adversary` handles one candidate per invocation. It confirms only a reachable failing scenario; external uncertainty produces `plausible`.
5. The caller aggregates findings into `finding-report@1` and evaluates the defect-family route below.
6. After remediation, `exit-gate` verifies findings, related instances, compilation, and tests; it emits `verdict@2`.

## Defect-family route

Treat confirmed findings with the same root cause, domain responsibility, or failure state as one possible defect family. Search beyond copied syntax: equivalent behavior may use different names, control flow, or language.

When a family suggests a missing concept, state, operation, boundary, abstraction, invariant, or enforcement mechanism, pass the complete `finding-report@1` to `scribe:architect` before remediation. Scribe inspects the semantic model and architecture, then specifies the smallest enforceable correction. Local or unrelated findings remain ordinary remediation work.

## Dispatch

| Agent | Mode | Tier | Input → output |
| :--- | :--- | :--- | :--- |
| `recon` | Enumeration | haiku / low | workspace → live/dead manifest |
| `scanner` | Pattern matching | sonnet / medium | manifest → `candidate@1` |
| `boundary-tracer` | Data-flow tracing | sonnet / medium | T7/T10 candidate → `field-survival-map@1` |
| `adversary` | Adversarial judgment | opus / high | one candidate → finding or dismissal |
| `exit-gate` | Binding verification | opus / high | `finding-report@1` → `verdict@2` |

## Contracts

- Candidates: `shared/schemas/candidate@1.json`
- Boundary evidence: `shared/schemas/field-survival-map@1.json`
- Findings: `shared/schemas/finding-report@1.json`
- Exit verdict: `shared/schemas/verdict@2.json`

Plausible findings pass to `flagged_for_review`; they never become remediation blockers without confirmation.
