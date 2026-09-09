# Cross-Harness Behavioral Evaluation

This protocol measures whether a plugin workflow produces durable, evidence-led artifacts and detects known failure modes. It does not require Claude and Codex to produce identical prose, transcripts, plans, or delegation topology.

## When to run it

Run the affected case before release when changing a critical workflow, role card, model recommendation, lifecycle schema, or evidence rule. Use `mason:evaluate` when available.

## Core case

Use `tests/fixtures/cross-harness/lifecycle.json` as the fixed contract reference and evaluate this route:

```text
requirement@1 -> research-report@1 -> spec@1 -> plan@1
weaver/capture-need -> vanguard/research -> scribe/draft-spec -> navigator/plan
```

Extract only the first stage's `requirement@1` document as the run input. Do not expose the fixture's later example artifacts to the executing harness. Make a clean, disposable workspace with that input and any target code needed to ground the task. Do not use a self-authored toy answer as the expected result. The evaluator reviews artifacts and their evidence against the requirement's intent and the live workspace.

## Runs

Record one result per execution in `docs/evaluations/<id>.json` using `shared/schemas/harness-evaluation@2.json`.

| Run | Purpose |
| :--- | :--- |
| Claude source workflow | Baseline artifact and evidence quality. |
| Codex single-agent | Proves the Codex skill completes without an agent team. |
| Codex team | Measures optional role-card delegation when the host supports it. |

Record the actual host version, model, mode, roles, plugin versions, plugin source revisions, and workspace state. Do not infer them from current manifests or recommendations. If a host does not expose a requested mode or model, record the limitation and mark the comparison `unverifiable`.

## Evaluation procedure

1. Copy the same public input into a clean workspace for each run. Keep the fixture oracle outside that workspace.
2. Record execution and plugin provenance, then run the route without desired artifact content or seeded-defect labels.
3. Wait for every started command or delegated task to finish. Preserve each produced artifact unchanged and validate its schema.
4. Reveal the oracle. Inspect cited source, command, boundary, generator, and oracle evidence directly.
5. Feed each artifact to its declared consumer and record whether it can continue without prompt-local context.
6. Record detections, false passes, human corrections, duration, and available usage counts. Save one schema-valid result per run.

## Pass criteria

Mark a run `pass` only when every required artifact validates, is consumer-usable, and no seeded defect receives a false pass. Tool invocation alone is not evidence: semantic search needs plausible candidate sites, generative testing needs a relevant generator and oracle, and a boundary claim needs an observation across that boundary. Use `fail` for invalid artifacts, broken handoffs, unsupported claims, missed seeded defects, or leaked oracle data. Use `unverifiable` when access or host capability prevents a fair judgment.

Do not average scores, award credit for fluent prose, or declare behavioral equivalence from structural parity. A Codex team run may improve independent investigation, but it may not change the artifact schema, ownership rules, or exit criteria.

## Extension cases

After the core case passes, add a representative case for each changed critical route. Keep the input stable, name the exact producer and consumer, and include an adversarial condition such as incomplete evidence, a contradictory API, or a boundary-spanning change. A case belongs in version control when it becomes a recurring release gate; otherwise keep its evidence record with the change that introduced it.

## Implementation-verification suite

`tests/fixtures/behavioral/implementation-verification.json` covers four recurring risks across TypeScript, Rust, Python, and Go: semantic siblings written with different syntax, proof at a compiled process boundary, meaningful structured-input generation, and fresh external or asynchronous state. Copy only a case's `public_input` into the run workspace. The evaluator reads `oracle` only after the target workflow finishes.

Compare runs by fixture, route, and recorded provenance. A later date is not evidence of improvement; changed results should be correlated with the exact plugin versions and source revisions in each record.
