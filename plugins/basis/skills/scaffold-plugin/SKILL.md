---
name: scaffold-plugin
description: >-
  Trigger when the user asks to build a new plugin from scratch: "build a new plugin", "create a plugin for X", "scaffold a plugin directory". Given a plugin ID and a description of what it should do, generates a complete, installable plugin directory — plugin.json, skills/<id>/SKILL.md, one stub agent file per declared agent using the 4-part structure, and the shared symlink.
version: 2.0.0
---

# Basis — Scaffold Plugin

<overview>
Makes the correct plugin structure the easy one to produce. Delegates to `scaffolder`. The scaffold should pass `basis/audit-plugin` on the first run without manual fixes.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **scaffolder** | sonnet / medium | A new plugin needs a complete, installable directory generated from an ID and description. |
</dispatch>

<references>
`shared/constitution.md`, `shared/agent-best-practices.md`
</references>

<io>
**Consumes**: plugin ID, description of what it should do
**Produces**: `plugin.json`, `skills/<id>/SKILL.md`, one stub agent file per declared agent, `shared` symlink. Run `basis/audit-plugin` against the result to confirm conformance.
</io>
