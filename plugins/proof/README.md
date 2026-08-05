# proof — Adversarial Bug Hunting

**Stage:** Cross-cutting · **Output:** `finding-report@1`

Adversarial bug hunting on live code. Builds a reachability manifest to exclude dead code, scans live files for hazard patterns, adversarially refutes each candidate, and gates the output through an exit verifier.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `proof-recon` | Module Manifest Builder | haiku/low | Traces imports from entry points to build a live/dead file manifest. Scanners only operate on live files. |
| `proof-scanner` | Hazard Scanner | sonnet/medium | Scans live files for bug patterns across 6 hazard taxonomies. Returns candidates with trigger conditions. |
| `proof-adversary` | Adversarial Verifier | opus/high | Tries to refute each candidate by reading actual code and tracing control flow. A finding confirms only when no refutation can be constructed. |
| `proof-exit-gate` | Exit Verifier | opus/high | Verifies the final finding report is complete and consistent before passing it downstream. |

## Pipeline

```
workspace → proof-recon → proof-scanner → proof-adversary → proof-exit-gate → finding-report@1
```

## Dead Code Exclusion

`proof-recon` traces imports from all entry points to build a live file set. Any file not reachable from any entry point is classified as dead and excluded from scanning. This prevents false positives from unused code paths.

## Output Schema

`finding-report@1` — see `shared/schemas/finding-report@1.json`

Each finding requires: `id`, `description`, `file`, `line`, `severity`, `trigger_condition`, `root_cause`, `verdict` (`confirmed` | `plausible`)

## References

- `shared/references/rust.md` — Rust hazard taxonomies and search patterns
- `shared/references/typescript.md` — TypeScript hazard taxonomies
