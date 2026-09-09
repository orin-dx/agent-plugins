# Claude Code Guidelines (`CLAUDE.md`)

Claude Code follows [`AGENTS.md`](./AGENTS.md), the shared repository guide for every harness. Read [`shared/constitution.md`](./shared/constitution.md) first and last. Use [`shared/agent-best-practices.md`](./shared/agent-best-practices.md) only while authoring prompts; runtime agents must not load it.

## Claude Marketplace

```text
/plugin marketplace add orin-dx/agent-plugins
/plugin install <plugin-id>
```

See the root [`README.md`](./README.md#claude-code) for migration and complete install guidance.

## Cross-Harness Changes

Read [`shared/harness-authoring.md`](./shared/harness-authoring.md) before changing plugin identity, lifecycle intent, shared schemas, or either harness workflow. Claude/AGY and Codex must preserve route names, artifact contracts, evidence, and acceptance intent; prompt wording, model routing, and delegation topology remain native.

## Validation

```bash
jq . marketplace.json plugins/*/plugin.json harnesses/codex/catalog.json
python3 -m unittest discover -s tests
./scripts/check-versions.sh
./scripts/check-skills-doc.sh
./scripts/check-reference-size.sh
python3 tools/build-codex-marketplace.py --check
./scripts/check-mermaid.sh
```

Run the relevant subset while editing and the full set before release. Generated Codex files in `.agents/plugins/` and `dist/codex/` must match their authored sources; never edit them directly.
