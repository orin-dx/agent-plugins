---
name: scaffold-subagent
description: >-
  Trigger when the user wants one new agent added to an existing plugin: "write an agent for X", "add a subagent to this plugin", "create a subagent for this task". Given an existing plugin's directory, a task description, and a model/effort tier, generates a single conformant agent file at plugins/<id>/agents/<role>.md using the 5-part structure (constitution copied verbatim from an existing agent, plus backstory/goal/judgment/output) — skipping plugin.json, SKILL.md, and the symlink, which already exist for the target plugin. Distinct from basis/scaffold-plugin, which builds a whole new plugin from nothing.
version: 2.0.0
---

# Basis — Scaffold Subagent

<overview>
The narrower sibling of `basis/scaffold-plugin`: one agent file for a plugin that already exists, not a full plugin directory. Delegates to `scaffolder` in its single-subagent mode.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **scaffolder** (single-subagent mode) | sonnet / medium | An existing plugin needs exactly one new conformant agent file for a given task and tier. |
</dispatch>

<references>
`shared/agent-best-practices.md`
</references>

<io>
**Consumes**: target plugin ID, task description, model/effort tier
**Produces**: one agent file at `plugins/<id>/agents/<role>.md`. Does not touch `plugin.json` or `SKILL.md` — if the new agent should be dispatched from a skill, that wiring is a separate manual step.
</io>
