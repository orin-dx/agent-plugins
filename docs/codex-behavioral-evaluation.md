# Codex Behavioral Evaluation

This protocol measures whether a native Codex workflow produces durable, evidence-led artifacts that downstream stages can use. It is not a claim that Claude and Codex should produce identical prose, transcripts, plans, or delegation topology.

## When to run it

Run the affected case before release when changing a critical native workflow, a role card, a Codex model recommendation, a shared lifecycle schema, or a skill's evidence or acceptance rules. Run the core case before the first public Codex marketplace release.

## Core case

Use `tests/fixtures/cross-harness/lifecycle.json` as the fixed contract reference and evaluate this route:

```text
requirement@1 -> research-report@1 -> spec@1 -> plan@1
weaver/capture-need -> vanguard/research -> scribe/draft-spec -> navigator/plan
```

Extract only the first stage's `requirement@1` document as the run input. Do not expose the fixture's later example artifacts to the executing harness. Make a clean, disposable workspace with that input and any target code needed to ground the task. Do not use a self-authored toy answer as the expected result. The evaluator reviews artifacts and their evidence against the requirement's intent and the live workspace.

## Runs

Record one result per execution in `docs/evaluations/<id>.json` using `shared/schemas/harness-evaluation@1.json`.

| Run | Purpose |
| :--- | :--- |
| Claude source workflow | Baseline artifact and evidence quality. |
| Codex single-agent | Proves the Codex skill completes without an agent team. |
| Codex team | Measures optional role-card delegation when the host supports it. |

Record the actual host version, model, mode, and roles. Do not infer a model choice from a recommendation. If a host does not expose a requested mode or model, record that limitation and mark the comparison `unverifiable` rather than treating it as a failure.

## Evaluation procedure

1. Copy the same input package into a clean workspace for each run.
2. Run the stated lifecycle route without supplying the desired artifact content.
3. Save every produced artifact at its durable path and validate it against its versioned schema.
4. Inspect the cited source locations, commands, and research evidence directly; mark unsupported claims rather than accepting summaries.
5. Feed each artifact to its declared next consumer and record whether that consumer can continue without prompt-local context.
6. Save one schema-valid record per run, then compare outcomes and material findings in the pull request or release handoff.

## Pass criteria

Mark a run `pass` only when every required artifact validates, contains traceable evidence, is usable by its declared consumer, and satisfies the fixture's acceptance intent without invented facts. Mark it `fail` for an invalid artifact, broken handoff, unsupported material claim, missing required evidence, or a delegation boundary violation. Mark it `unverifiable` when environment, host capability, or evidence access prevents a fair judgment.

Do not average scores, award credit for fluent prose, or declare behavioral equivalence from structural parity. A Codex team run may improve independent investigation, but it may not change the artifact schema, ownership rules, or exit criteria.

## Extension cases

After the core case passes, add a representative case for each changed critical route. Keep the input stable, name the exact producer and consumer, and include an adversarial condition such as incomplete evidence, a contradictory API, or a boundary-spanning change. A case belongs in version control when it becomes a recurring release gate; otherwise keep its evidence record with the change that introduced it.
