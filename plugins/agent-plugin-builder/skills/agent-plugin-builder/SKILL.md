---
name: agent-plugin-builder
description: >-
  Trigger this skill when the user asks to create, scaffold, generate, or add a new plugin, skill, or subagent to the Orin DX marketplace or an agentic workspace. Use when adding new domain plugins (e.g., bug-hunter-python, github-actions-auditor, docker-security-audit, terraform-gcp-architect), scaffolding plugin.json manifests, generating SKILL.md files with CSO user intent frontmatter, creating subagent prompts using the Superpowers 5-section framework, or updating marketplace.json. Also activate when enforcing context engineering and progressive disclosure standards on newly created skills.
---

# Agent Plugin Builder Meta-Skill

<overview>
This meta-skill automates the scaffolding and generation of self-contained AI agent plugins, skills, and subagent prompts adhering to the Orin DX prompt authoring specification. It ensures all generated plugins follow CSO trigger descriptions (100–200 words), 3-layer progressive disclosure, tool-agnostic dynamic tool discovery, and the Superpowers 5-section subagent framework.
</overview>

---

<framework_references>
Review authoritative authoring standards before scaffolding a new plugin:
- [Agent Authoring Specification](../../../AGENTS.md)
- [Universal Agent Best Practices](../../../shared/agent-best-practices.md)
- [Plugin Architecture Specification](../../../ARCHITECTURE.md)
</framework_references>

---

<scaffolding_pipeline>

### Step 1: Create Plugin Directory Hierarchy
Create target plugin directories under `plugins/<plugin-id>/`:
```bash
mkdir -p plugins/<plugin-id>/skills/<plugin-id> plugins/<plugin-id>/subagents
```

### Step 2: Generate `plugin.json` Manifest
Create `plugins/<plugin-id>/plugin.json`:
```json
{
  "id": "<plugin-id>",
  "name": "<plugin-id>",
  "version": "1.0.0",
  "description": "<Concise 1-sentence description>",
  "author": "Gabriel Castro (Orin DX)",
  "skills": ["<plugin-id>"],
  "agents": [
    "<plugin-id>-scanner",
    "<plugin-id>-adversary",
    "<plugin-id>-remediator"
  ]
}
```

### Step 3: Generate `SKILL.md` (CSO User Intent Focus)
Create `plugins/<plugin-id>/skills/<plugin-id>/SKILL.md`:
- **CSO Frontmatter**: 100–200 words focusing on **User Intent** (request triggers, user phrasing, target file types, adjacent domains, boundary edge cases).
- **Progressive Disclosure**: Include relative links to `shared/debugging-laws.md` and `shared/agent-best-practices.md`.
- **XML Directives**: Enclose overview, taxonomies/directives, and subagent dispatch matrices inside positive `<xml_tags>`.

### Step 4: Generate 3 Subagent Prompts (Superpowers Framework)
Create subagent prompt files under `plugins/<plugin-id>/subagents/`:
1. `<plugin-id>-scanner.md`: CSO Delegation description (100–200 words) for static analysis.
2. `<plugin-id>-adversary.md`: CSO Delegation description (100–200 words) for end-to-end tracing.
3. `<plugin-id>-remediator.md`: CSO Delegation description (100–200 words) for Red-to-Green fixes.

Structure each subagent using the Superpowers 5-Section Framework:
```markdown
# <Subagent Name>
<context>Workspace environment and stack boundaries.</context>
<role>Specialized expert persona.</role>
<goal>Singular, outcome-driven objective.</goal>
<execution_strategy>Tool-agnostic dynamic detection heuristics and rules.</execution_strategy>
<success_criteria>Explicit, verifiable completion checklist.</success_criteria>
```

### Step 5: Register Entry in `marketplace.json`
Append the new plugin entry under `"plugins"` in root `marketplace.json`:
```json
{
  "id": "<plugin-id>",
  "name": "<Human Readable Name>",
  "version": "1.0.0",
  "path": "./plugins/<plugin-id>",
  "description": "<Concise description>"
}
```

</scaffolding_pipeline>

---

<success_criteria>
- [ ] Directory hierarchy created under `plugins/<plugin-id>/`.
- [ ] `plugin.json` generated with valid JSON syntax (`jq . plugins/<plugin-id>/plugin.json`).
- [ ] `SKILL.md` generated with 100–200 word CSO user intent description and relative `shared/` links.
- [ ] 3 subagents generated using the Superpowers 5-section framework and CSO delegation descriptions.
- [ ] Root `marketplace.json` updated and validated with `jq . marketplace.json`.
</success_criteria>
