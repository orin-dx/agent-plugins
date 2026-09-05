# Cross-Harness Authoring

Use this guide when a change affects Claude/AGY source plugins, Codex-native plugins, shared artifact contracts, or generated Codex distribution.

## Design boundary

Shared sources preserve lifecycle identity and interoperable artifacts. Harness sources preserve execution quality. Never mechanically translate prompts, model tiers, named agents, or delegation topology across harnesses.

| Concern | Shared source | Claude/AGY source | Codex source |
| :--- | :--- | :--- | :--- |
| Identity | ID, version, author, `consumes`, `produces` | Uses `plugins/<id>/plugin.json` | Native manifest matches ID, version, and author |
| Artifact contract | Versioned JSON schema | Produces and consumes the schema | Produces and consumes the same schema bytes |
| Skill inventory | Lifecycle route name | `plugins/<id>/skills/<skill>/` | Same route name under `harnesses/codex/plugins/<id>/skills/` |
| Workflow | None | Specialist agents and Claude-native orchestration | Native skill plus optional Codex role cards |
| Delegation | None | Named source agents | `agent-roles/<role>.md` selected only for bounded independent work |

Codex role cards are portable plugin resources. They are not TOML configuration: host TOML controls local runtime defaults and is never a marketplace contract.

## Change procedure

1. Classify the change before editing: shared identity, shared artifact contract, Claude/AGY workflow, Codex workflow, or distribution only.
2. Read the counterpart source before deciding whether it needs a change. Preserve lifecycle intent and artifact validity; do not preserve wording or topology by default.
3. For an identity or schema change, update the shared source first. Version an incompatible schema, update every affected producer and consumer, then update both harness workflows.
4. For a new or renamed lifecycle skill, add the route to both harnesses. Match the directory name, not the prompt body. Author the Codex skill independently for its tools, context model, and delegation behavior.
5. For a Claude agent change, decide explicitly whether Codex needs a skill workflow or role-card change. A Claude prompt is not input to a Codex role card.
6. For a Codex role-card change, update every delegating skill whose task boundary or required evidence changes. Each delegation must carry the `agent-roles/README.md` packet. Keep the primary agent responsible for synthesis, judgment, and external writes.
7. For a Codex-only UI, model, category, or description change, do not alter the Claude prompt unless lifecycle intent changed.

## Required change record

Record this in the pull request description, implementation report, or task handoff whenever a cross-harness source changes:

```text
Classification: <shared contract | Claude/AGY workflow | Codex workflow | distribution>
Counterpart reviewed: <paths>
Intent preserved: <artifact, evidence, acceptance criteria, or lifecycle rule>
Intentional divergence: <why the harness differs, or none>
Codex role impact: <role cards and skills changed, or none>
Verification: <commands and behavioral checks>
```

## Review questions

- Does a consumer still receive a valid versioned artifact from either harness?
- Does the Codex skill have a complete single-agent path when multi-agent work is unavailable?
- If it delegates, are role, input boundary, write authority, and output evidence explicit?
- Does the delegation packet make owned paths, exclusions, evidence, and completion unambiguous?
- Did the change preserve an outcome or merely copy a source prompt's incidental wording?
- Does the generated bundle contain the exact native sources and only the runtime resources that skill needs?

## Deliberate non-goals

- No prompt generator transforms Claude agents into Codex roles.
- No TOML agent file is shipped as a plugin behavior contract.
- No behavioral equivalence claim is made from directory or schema parity alone; use a representative artifact and evidence review when changing a critical route.
