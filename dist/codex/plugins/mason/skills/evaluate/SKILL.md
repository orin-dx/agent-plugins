---
name: evaluate
description: Evaluate a plugin workflow against a fixed hidden-oracle fixture. Use for release gates, regression checks, Claude/Codex comparisons, or longitudinal plugin analysis.
---

# Evaluate plugin behavior

Use `shared/references/behavioral-evaluation.md` and return `shared/schemas/harness-evaluation@2.json`.

## Method

1. Select a committed fixture and route. Copy only its public input into a disposable workspace.
2. Record the exact host version, model, mode, roles, plugin versions, plugin source revisions, and workspace revision before execution.
3. Run the target workflow to completion. Preserve its artifacts and command results unchanged as `shared/schemas/evaluation-run@1.json`. Do not read the fixture oracle during this run.
4. After completion, reveal the oracle. Validate each artifact, inspect cited evidence, test downstream usability, and count seeded detections, false passes, human corrections, and duration.
5. Write one `harness-evaluation@2` record. Use `unverifiable` when missing access or host capability prevents a fair judgment.

Tool use is not evidence by itself. A generative test needs a relevant generator and oracle; a semantic search needs plausible candidate sites; a boundary claim needs an observation across that boundary.

When delegation is available, use `recon` for the isolated run and keep hidden-oracle adjudication with the primary `judge`. The same sequential method is required when delegation is unavailable.
