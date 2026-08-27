---
name: audit-plugin
description: >-
  Trigger when the user asks to check an existing plugin for conformance: "audit this plugin", "check plugin conformance", "does this plugin follow the ecosystem rules?". Given a plugin directory path, checks plugin.json required fields, subagent file presence for every declared agent, YAML frontmatter completeness, SKILL.md description quality, and the shared symlink. Returns a structured pass/fail/warn report per check. Named audit-plugin rather than bare audit because that word is already ranger's plugin-level skill name (code/bug auditing) — a different domain entirely.
version: 2.0.0
---

# Mason — Audit Plugin

<overview>
Checks a plugin against the ecosystem's actual conformance rules — not vibes. Delegates to `auditor`. Run this after `mason/scaffold-plugin` or any manual plugin edit, before installing.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | An existing plugin directory needs checking against ecosystem conformance rules. |
</dispatch>

<references>
`shared/constitution.md`
</references>

<io>
**Consumes**: plugin directory path
**Produces**: structured pass/fail/warn report, one entry per conformance check.
</io>
