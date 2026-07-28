<h1 align="center">Contributing to Orin DX Agent Plugins</h1>

<p align="center">
  <b>Guidelines, manifest standards, skill authoring, and contribution workflows.</b>
</p>

---

## 1. Development Prerequisites & Setup

### Prerequisites

- **Git**: VCS for managing plugin versions and submodules.
- **`jq`**: JSON validator for checking `marketplace.json` and `plugin.json` schema validity.
- **Antigravity CLI (`agy`) or Claude Code**: For local plugin testing.

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/orin-dx/agent-plugins.git
cd agent-plugins

# Validate marketplace and plugin manifests
jq . marketplace.json > /dev/null
jq . plugins/*/plugin.json > /dev/null
```

---

## 2. Plugin Authoring Specification

To add a new plugin (e.g. `bug-hunter-python`, `github-actions-auditor`, `docker-security-audit`):

### Step 1: Create Directory Structure

```bash
mkdir -p plugins/<plugin-id>/skills/<plugin-id> plugins/<plugin-id>/subagents
```

### Step 2: Define `plugin.json` Manifest

Create `plugins/<plugin-id>/plugin.json`:

```json
{
  "id": "bug-hunter-python",
  "name": "bug-hunter-python",
  "version": "1.0.0",
  "description": "Python Bug Hunter plugin with 6 Python Hazard Taxonomies & Multi-Agent Orchestration.",
  "author": "Gabriel Castro (Orin DX)",
  "skills": ["bug-hunter-python"],
  "agents": [
    "bug-hunter-scanner-python",
    "bug-hunter-adversary-python",
    "bug-hunter-remediator-python"
  ]
}
```

### Step 3: Define Skill (`SKILL.md`) with CSO Intent Trigger

Create `plugins/<plugin-id>/skills/<plugin-id>/SKILL.md`:
- **CSO Frontmatter Description (100–200 Words)**: Write description focused on **User Intent** (what user requests or goals trigger this skill), including adjacent domains and boundary edge cases.
- **Progressive Disclosure**: Include relative Markdown links to shared framework guides (`[General Debugging Laws](../../../shared/debugging-laws.md)` and `[Agent Best Practices](../../../shared/agent-best-practices.md)`).
- **XML Directives**: Use positive framing inside `<overview>`, `<hazard_taxonomies>`, and `<subagent_dispatch_matrix>` tags.

### Step 4: Define Subagents (`subagents/*.md`) with Superpowers Framework

Create subagent prompt files under `plugins/<plugin-id>/subagents/`:
- **CSO Frontmatter Description (100–200 Words)**: Write description focused on **Delegation Scenarios** (when orchestrator should delegate to this subagent and what structured payload it returns).
- **Superpowers 5-Section Structure**:
  ```markdown
  # <Subagent Name>
  <context>Workspace environment and stack boundaries.</context>
  <role>Specialized expert persona.</role>
  <goal>Singular, outcome-driven objective.</goal>
  <execution_strategy>Dynamic detection heuristics and search rules.</execution_strategy>
  <success_criteria>Explicit, verifiable completion checklist.</success_criteria>
  ```

### Step 5: Register in `marketplace.json`

Add an entry under the `"plugins"` array in `marketplace.json`:

```json
{
  "id": "bug-hunter-python",
  "name": "Python Bug Hunter",
  "version": "1.0.0",
  "path": "./plugins/bug-hunter-python",
  "description": "Python Bug Hunter plugin with 6 Python Hazard Taxonomies & Multi-Agent Orchestration."
}
```

---

## 3. Engineering Invariants & PR Rules

1. **Tool-Agnostic Dynamic Discovery**: Prompts must instruct agents to discover project tools (`cargo nextest` vs `test`, `vitest` vs `jest`, `pnpm` vs `npm`) before executing verification commands.
2. **Self-Contained Plugin Scoping**: Keep domain rules isolated within `plugins/<plugin-id>/`.
3. **On-Demand Context**: Reference shared files in `shared/` via relative Markdown links instead of duplicating context.
4. **No Hardcoded Absolute Paths**: All paths in `SKILL.md` and prompt files must be relative.
5. **Reserved ALL CAPS**: Reserve ALL CAPS (`ALWAYS`/`NEVER`) strictly for genuinely dangerous mistakes (data loss, security holes).
6. **Clean Technical Writing**: Avoid emojis, marketing fluff, or AI filler phrases.
7. **Conventional Commits**: Commit messages follow `feat:`, `fix:`, `docs:`, `legal:`, or `refactor:`.
