---
name: scaffold-subagent
description: Add one conformant Claude-style agent prompt to an existing source plugin. Use when the user asks to add an agent without changing the plugin's unrelated routes.
---

# Add one agent without breaking the static contract

Inspect the target plugin's manifest, skill dispatch, and existing agent prompts first. This skill changes the source-plugin agent surface; it does not assume that the same prompt belongs in the Codex adaptation.

## Workflow

1. Confirm the requested cognitive mode, actual responsibility, input artifact, output artifact, and chosen model/effort tier.
2. Read an existing source agent and copy its `<constitution>` section byte-for-byte.
3. Author `<backstory>`, `<goal>`, `<judgment>`, and `<output>` in the required order.
4. Add a single `<load_first>` block only when the agent needs one phase-specific reference.
5. Cite `shared/schemas/<name>@<version>.json` for every structured output or create that schema first.
6. Update the source manifest and a skill dispatch only when the new agent must be reachable through that route.
7. Validate the shared prefix, manifest wiring, and resulting path.

## Boundaries

- Do not alter unrelated agents, skills, or the Codex-native tree to make the source prompt fit.
- Do not create a generic role prompt. Define the agent's actual evidence and judgment boundary.
- If the requested role overlaps an existing agent, report the overlap and propose reuse before adding duplication.

## Team use

This is a tightly coupled edit. Complete it yourself; do not request an agent team.
