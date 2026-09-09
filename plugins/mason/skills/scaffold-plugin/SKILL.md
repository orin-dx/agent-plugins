---
name: scaffold-plugin
description: >-
  Create a complete plugin from an ID and purpose. Use for new plugin requests. Generate the manifest, skill, cognitive-mode agents, shared linkage, routing, and any required schema contracts; validate the result before handoff.
version: 2.2.0
---

# Mason — Scaffold Plugin

<overview>
Makes the correct plugin structure the easy one to produce. Delegates to `scaffolder`. The scaffold should pass `mason/audit-plugin` on the first run without manual fixes.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **scaffolder** | sonnet / medium | A new plugin needs a complete, installable directory generated from an ID and description. |
</dispatch>

<references>
`shared/constitution.md`, `shared/agent-best-practices.md`, `shared/harness-authoring.md` when the plugin will ship to more than one harness
</references>

<io>
**Consumes**: plugin ID, description of what it should do
**Produces**: `plugin.json`, `skills/<id>/SKILL.md`, one stub agent file per declared agent, `shared` symlink. Run `mason/audit-plugin` against the result to confirm conformance.
</io>
