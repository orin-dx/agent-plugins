# basis — Plugin Authoring

**Stage:** Meta · **Output:** conformant plugin directory

Scaffolds new plugins and audits existing ones for ecosystem conformance. The tool for building tools.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `basis-scaffolder` | Scaffolder | sonnet/medium | Generates a complete, installable plugin directory: `plugin.json`, `SKILL.md`, stub subagents, `shared` symlink. |
| `basis-auditor` | Conformance Auditor | sonnet/medium | Audits an existing plugin directory for ecosystem conformance: manifest fields, subagent structure, Section 9 authoring rules. |
| `basis-schema-designer` | Schema Designer | sonnet/medium | Designs a new JSON Schema for a proposed inter-agent artifact, checking for conflicts with existing schemas. |

## Usage

**Create a new plugin:**
```
"Create a plugin called <id> that does <goal>"
```
`basis-scaffolder` generates the full structure. Run `basis-auditor` on the output to verify.

**Audit an existing plugin:**
```
"Audit the <id> plugin for conformance"
```

**Design a new schema:**
```
"Design a schema for an artifact that carries <description>"
```

## Conformance Checks (basis-auditor)

- `plugin.json` has all required fields
- `SKILL.md` exists with a valid frontmatter description
- All subagents listed in `plugin.json` have corresponding `.md` files
- Subagent descriptions are 80–200 words and start with "Delegate to this subagent when…"
- Body word count <200 for each subagent
- Model/effort tiers match the mechanical/analysis/judgment pattern
- `shared` symlink points to `../../shared`
- No references to `shared/agent-best-practices.md` in subagent bodies (authoring-time only)

## References

- `shared/agent-best-practices.md` Section 9 — full authoring checklist (basis authors use this; subagent bodies do not reference it at runtime)
- `shared/schemas/` — existing schemas to check against when designing a new one
