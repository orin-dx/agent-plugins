---
name: evaluate
description: >-
  Evaluate a plugin workflow against a fixed behavioral fixture. Use for release
  gates, Claude/Codex comparisons, regression checks, and longitudinal plugin
  quality analysis. Preserve exact execution provenance and hidden-oracle isolation.
version: 1.0.0
---

# Mason — Evaluate

## Outcome

Produce one `harness-evaluation@2` per run. Compare runs only when the fixture and route are identical and each record names the exact host, model, mode, roles, plugin versions, source revisions, and workspace state.

## Dispatch

| Agent | Mode | Tier | Responsibility |
| :--- | :--- | :--- | :--- |
| `evaluation-runner` | Execution | haiku / low | Run the public fixture input in isolation and return `evaluation-run@1`. |
| `evaluation-adjudicator` | Judgment | opus / high | Reveal the oracle after completion and issue the evaluation. |

## Method

Keep fixture input and oracle separate. The target workflow must not receive seeded-defect labels, expected artifact content, or scoring criteria that disclose the answer. Preserve its outputs unchanged.

The adjudicator validates schemas, follows evidence to source, checks downstream usability, and counts false passes and human corrections. Tool invocation earns no credit without a relevant generator and oracle, mutation discrimination, sibling search, or boundary observation.

Run single-agent and team modes only when supported. Record unavailable modes as unverifiable. Do not infer improvement from time alone; compare results with the plugin versions and source revisions that actually ran.

## Contracts

- Protocol: `shared/references/evaluation/behavioral.md`
- Run evidence: `shared/schemas/evaluation-run@1.json`
- Output: `shared/schemas/harness-evaluation@2.json`
- Fixtures: `tests/fixtures/behavioral/`
