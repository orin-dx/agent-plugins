# Codex Marketplace Release Policy

`dist/codex` is the installable, generated Codex marketplace. The authored sources are `plugins/*/plugin.json`, `harnesses/codex/plugins/*/`, `shared/schemas/`, and `harnesses/codex/catalog.json`. Never edit `dist/codex` by hand.

## What is portable

Versioned JSON artifacts in `shared/schemas/` are the compatibility boundary between Claude and Codex. A requirement, research report, specification, or plan can move between harnesses by its schema ID and JSON content. Named Claude agents, prompt wording, tool availability, and team delegation are not portable contracts. Codex skills must complete their workflow without an agent team; teams may improve independent investigation but cannot change the artifact shape.

The focused compatibility fixture at `tests/fixtures/cross-harness/lifecycle.json` covers the core handoff:

```text
weaver/capture-need  requirement@1  vanguard/research
vanguard/research    research-report@1  scribe/draft-spec
scribe/draft-spec    spec@1  navigator/plan
navigator/plan       plan@1  smith/implement
```

Its test validates fixture documents against the source schemas, confirms the same schema bytes are materialized into the relevant Codex plugins, and checks that both harnesses declare each producer/consumer relationship. It is a contract compatibility evaluation, not proof that two models reach identical judgment or prose.

## Change and release procedure

1. Change Claude source manifests, native Codex source files, shared schemas, or the Codex catalog as needed. If a schema changes incompatibly, add a new version; do not modify an existing version.
2. Regenerate the release payload:

   ```bash
   python3 tools/build-codex-marketplace.py
   ```

3. Run the release gates:

   ```bash
   python3 -m unittest tests/test_build_codex_marketplace.py -v
   python3 -m unittest tests/test_cross_harness_artifacts.py -v
   python3 -m unittest tests/test_codex_native_sources.py -v
   python3 tools/build-codex-marketplace.py --check
   ```

4. Review native Codex source and generated changes in the same pull request. A generated change without a native-source, catalog, or schema explanation is a release blocker.
5. Tag and publish only a commit for which the check command succeeds. The tag includes the generated marketplace so users install a deterministic payload.
6. Register the published bundle with Codex using its marketplace root:

   ```bash
   codex plugin marketplace add orin-dx/agent-plugins --sparse dist/codex
   ```

   Codex registers this source as `wisp-plugins`; install a plugin with `codex plugin add <plugin>@wisp-plugins`. A source previously registered at the repository root or as `orin-dx-agent-plugins` must be removed and re-added with this sparse path after the first release.

CI runs the generator and compatibility tests. A stale generated bundle, a symlink in the bundle, a missing contract, or a mismatch between source and materialized schema must fail before release.

## Behavioral evaluations

The fixture is intentionally narrow. Before declaring a workflow change behaviorally equivalent across harnesses, run a representative task through each harness and compare durable JSON artifacts against the same schema and acceptance criteria. Follow [Codex Behavioral Evaluation](./codex-behavioral-evaluation.md) for the core case, record format, and pass criteria. Do not require identical transcripts, plans, or language; require valid artifacts, traceable evidence, and the intended lifecycle links.
