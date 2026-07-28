---
name: agent-plugin-builder
description: >-
  Trigger this skill when the user asks to create, scaffold, generate, or add a new plugin, skill, or subagent to the Orin DX marketplace or an agentic workspace. Use when adding new domain plugins (e.g., bug-hunter-python, github-actions-auditor, docker-security-audit, terraform-gcp-architect), scaffolding plugin.json manifests, generating SKILL.md files with CSO user intent frontmatter, creating subagent prompts using the Superpowers 5-section framework, or updating marketplace.json. Also activate when enforcing context engineering and progressive disclosure standards on newly created skills.
---

# Agent Plugin Builder Meta-Skill

<overview>
This meta-skill provides adaptable guidance for scaffolding new AI agent plugins, skills, and subagent prompts. It enforces Orin DX context engineering principles—CSO trigger descriptions (100–200 words), 3-layer progressive disclosure, and tool-agnostic discovery—while allowing the agent to adapt directory layouts, subagent counts, and domain rules to the specific plugin being created.
</overview>

---

<framework_references>
Review core guidelines before scaffolding:
- [Agent Authoring Specification](../../../AGENTS.md)
- [Universal Agent Best Practices](../../../shared/agent-best-practices.md)
- [Plugin Architecture Specification](../../../ARCHITECTURE.md)
</framework_references>

---

<authoring_guidelines>

### 1. Adaptable Plugin Structure
Determine the optimal layout for the target domain:
- **Simple / Tool Plugins**: May contain only a `plugin.json` and a single `SKILL.md`.
- **Complex / Multi-Agent Plugins**: May contain `plugin.json`, `SKILL.md`, and 1 to 3 specialized subagents (`subagents/*.md`).

### 2. Generate `plugin.json` Manifest
Ensure `plugin.json` contains valid JSON with `"id"`, `"name"`, `"version"`, `"description"`, `"author": "Gabriel Castro (Orin DX)"`, `"skills": [...]`, and optional `"agents": [...]`.

### 3. Generate `SKILL.md` (CSO User Intent Focus)
- **CSO Frontmatter (100–200 Words)**: Describe user intent triggers, request phrasing, target file types, adjacent domains, and boundary edge cases.
- **Progressive Disclosure**: Link to relevant shared framework guides (`shared/debugging-laws.md` or `shared/agent-best-practices.md`) via relative Markdown links.
- **Positive Framing**: Structure behavioral directives inside logical `<xml_tags>`.

### 4. Generate Subagent Prompts (Superpowers Framework, If Applicable)
If the plugin requires subagents, tailor subagent roles to the domain and format prompt files using the Superpowers 5-Section Framework:
```markdown
# <Subagent Name>
<context>Workspace environment and stack boundaries.</context>
<role>Specialized expert persona.</role>
<goal>Singular, outcome-driven objective.</goal>
<execution_strategy>Tool-agnostic dynamic detection heuristics and rules.</execution_strategy>
<success_criteria>Explicit, verifiable completion checklist.</success_criteria>
```

### 5. Register in `marketplace.json`
Append the new plugin entry under `"plugins"` in root `marketplace.json` and validate JSON syntax (`jq . marketplace.json`).

</authoring_guidelines>

---

<success_criteria>
- [ ] Plugin files created under `plugins/<plugin-id>/`.
- [ ] Validated `plugin.json` schema.
- [ ] `SKILL.md` generated with 100–200 word CSO user intent description.
- [ ] Subagents (if created) follow Superpowers 5-section framework and CSO delegation descriptions.
- [ ] Root `marketplace.json` updated and validated.
</success_criteria>
