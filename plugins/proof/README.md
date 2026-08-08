# proof — Adversarial Bug Hunting

**Stage:** Cross-cutting · **Output:** `finding-report@1` · **Version:** 2.0.0

Adversarial bug hunting on live code. Builds a reachability manifest to exclude dead code from scanning, sweeps live files against language-specific hazard taxonomies, optionally traces data flow for intent-capture and error-downgrade candidates, then adversarially refutes each candidate — a finding is confirmed only when no refutation can be constructed and a concrete failing scenario can be stated. Gates the output through an exit verifier before producing `finding-report@1`.

Works on Rust, TypeScript, and JavaScript codebases. Language is auto-detected from `Cargo.toml` or `package.json`.

---

## When to Use

- You want a thorough bug hunt across the codebase before a release
- You suspect a specific hazard category (e.g. unsafe memory, unhandled promises) and want a targeted scan
- You have a candidate bug report and want adversarial verification before acting on it
- You want to confirm all findings are resolved after remediation

**Invoke with:** `"Hunt for bugs"`, `"Security audit"`, `"Find vulnerabilities"`, `"Scan for unhandled promises"`, `"Audit this for memory safety issues"`, `"Verify this bug report"`, `"Check what's still broken after my fixes"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `proof/scan` | Full hazard sweep across all categories in the workspace |
| `proof/focus` | Targeted scan — caller names one hazard category |
| `proof/verify` | Adversarially verify a single reported candidate bug |
| `proof/remediations` | Produce a structured fix plan from a finding report |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `proof-recon` | Workspace Recon | haiku / low | Traces imports from entry points to build a verified live/dead file manifest. All downstream agents operate only on live files. |
| `proof-scanner` | Hazard Scanner | sonnet / medium | Loads language-specific hazard taxonomies, runs grep patterns against live files, emits every match as a candidate@1 entry. No filtering — exhaustiveness is the goal. |
| `proof-boundary-tracer` | Data Flow Tracer | sonnet / medium | Conditional. Invoked for T7 and T10 candidates only. Traces each field of the flagged struct or type from construction site to execution boundary and produces a field survival map for the adversary. |
| `proof-adversary` | Adversarial Verifier | opus / high | Invoked once per candidate. Tries hard to refute before confirming. Runs a one-time constitution sweep for Invisible Invariants. Confirms only when a concrete failing scenario can be stated. |
| `proof-exit-gate` | Exit Verifier | opus / high | Re-reads all affected code from scratch after remediation. Checks resolved findings, scans for sibling gaps, verifies compile and tests. Escalates to human when retry_count exceeds 3. |

---

## Pipeline

```
workspace → proof-recon → proof-scanner → [proof-boundary-tracer?] → proof-adversary → proof-exit-gate → finding-report@1
```

`proof-boundary-tracer` is conditional — invoked only when the scanner produces T7 (write-only fields / intent-capture discard) or T10 (error downgrade) candidates.

---

## Dead Code Exclusion

`proof-recon` traces imports from all declared entry points to build a verified live file set. Any file not reachable from any entry point is classified as dead and excluded from all scanning and adversarial phases. This eliminates false positives from unused code paths — proof only reports bugs that can actually be triggered.

---

## Language Detection

Recon inspects the workspace root automatically:

| File found | Language | Hazard reference loaded |
| :--- | :--- | :--- |
| `Cargo.toml` | Rust | `shared/references/rust-hazards.md` |
| `package.json` | TypeScript / JavaScript | `shared/references/typescript-hazards.md` |

---

## Output Schema

`finding-report@1` — see `shared/schemas/finding-report@1.json`

Each confirmed finding requires:

| Field | Description |
| :--- | :--- |
| `id` | Unique finding identifier |
| `description` | What the bug is |
| `file` | File path |
| `line` | Line number |
| `severity` | `critical`, `high`, `medium`, or `low` |
| `trigger_condition` | The exact condition under which the bug fires |
| `root_cause` | Why it exists |
| `verdict` | `confirmed` |

---

## References

| File | Contents | Loaded by |
| :--- | :--- | :--- |
| `shared/references/rust-hazards.md` | Rust hazard taxonomies T1-T10, grep patterns, NAPI boundary rules | proof-scanner, proof-boundary-tracer, proof-adversary (Rust workspaces) |
| `shared/references/typescript-hazards.md` | TypeScript hazard taxonomies T1-T10, grep patterns, unhandled promise patterns | proof-scanner, proof-boundary-tracer, proof-adversary (TS/JS workspaces) |
| `shared/schemas/candidate@1.json` | Scanner output shape | — |
| `shared/schemas/finding-report@1.json` | Adversary and exit-gate output shape | — |
| `shared/schemas/verdict@1.json` | Exit-gate verdict shape | — |

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install proof
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Integration

`finding-report@1` feeds into **[delta](../delta/)** — the release summarizer rolls confirmed findings into release notes. Run proof before cutting any release.
