# proof — Adversarial Bug Hunting

**Stage:** Cross-cutting · **Output:** `finding-report@1` · **Version:** 2.0.0

Adversarial bug hunting on live code. Builds a reachability manifest to exclude dead code from scanning, sweeps live files against language-specific hazard taxonomies, then adversarially refutes each candidate — a finding is confirmed only when no refutation can be constructed. Gates the output through an exit verifier before producing `finding-report@1`.

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
| `proof-recon` | Module Manifest Builder | haiku / low | Traces imports from entry points to build a live/dead file manifest. Scanners only operate on live files. |
| `proof-scanner` | Hazard Scanner | sonnet / medium | Scans live files for bug patterns across 6 hazard taxonomies. Returns candidates with trigger conditions. |
| `proof-adversary` | Adversarial Verifier | opus / high | Tries to refute each candidate by reading actual code and tracing control flow. A finding confirms only when no refutation can be constructed. |
| `proof-exit-gate` | Exit Verifier | opus / high | Verifies the final finding report is complete and consistent before passing it downstream. |

---

## Pipeline

```
workspace → proof-recon → proof-scanner → proof-adversary → proof-exit-gate → finding-report@1
```

---

## Dead Code Exclusion

`proof-recon` traces imports from all declared entry points to build a verified live file set. Any file not reachable from any entry point is classified as dead and excluded from all scanning and adversarial phases. This eliminates false positives from unused code paths — proof only reports bugs that can actually be triggered.

---

## Language Detection

Recon inspects the workspace root automatically:

| File found | Language | Hazard reference loaded |
| :--- | :--- | :--- |
| `Cargo.toml` | Rust | `shared/references/rust.md` |
| `package.json` | TypeScript / JavaScript | `shared/references/typescript.md` |

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
| `verdict` | `confirmed` or `plausible` |

---

## References

Loaded at runtime by the scanner:

- `shared/references/rust.md` — Rust hazard taxonomies, NAPI boundary rules, non-negotiables
- `shared/references/typescript.md` — TypeScript hazard taxonomies, unhandled promise patterns

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
