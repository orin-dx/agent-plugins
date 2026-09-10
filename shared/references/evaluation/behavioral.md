# Behavioral evaluation

Evaluate observable workflow behavior, not prose similarity or tool invocation.

## Isolation

- Use a committed fixture with separate public input and oracle.
- Copy only public input into a disposable workspace.
- Keep the oracle hidden until the target workflow reaches a terminal result.
- Preserve produced artifacts unchanged.

## Provenance

Record the actual host version, model, mode, roles, plugin versions, plugin source revisions, workspace revision, and dirty state. Do not infer historical versions from current manifests.

Compare runs only when fixture and route match. Correlate changed outcomes with recorded plugin provenance, not dates alone.

## Evidence

- Validate each artifact against its declared schema.
- Inspect cited source, command, boundary, generator, and oracle evidence.
- Confirm the declared consumer can continue without prompt-local context.
- Wait for every started command or delegated task to finish.
- Count seeded detections, false passes, human corrections, and duration.

A tool call earns no credit by itself. Semantic search needs plausible candidate sites. Generative testing needs a relevant generator and oracle. Boundary claims need observations across the boundary.

## Outcomes

- `pass`: artifacts are valid and usable, evidence supports their claims, and no seeded defect receives a false pass.
- `fail`: a required artifact or handoff fails, a material claim is unsupported, a seeded defect is missed, or oracle data leaked.
- `unverifiable`: missing access or host capability prevents a fair judgment.

Return `shared/schemas/harness-evaluation@2.json`. Do not average independent failures into a passing score.
