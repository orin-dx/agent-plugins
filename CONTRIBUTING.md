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

## 2. Authoring a New Language Plugin

To add a new language plugin (e.g. `bug-hunter-python` or `bug-hunter-go`):

### Step 1: Create Plugin Directory Structure

```bash
mkdir -p plugins/bug-hunter-python/skills/bug-hunter-python plugins/bug-hunter-python/subagents
```

### Step 2: Define `plugin.json` Manifest

Create `plugins/bug-hunter-python/plugin.json`:

```json
{
  "id": "bug-hunter-python",
  "name": "bug-hunter-python",
  "version": "1.0.0",
  "description": "Python Bug Hunter plugin with 6 Python Hazard Taxonomies & Multi-Agent Orchestration.",
  "author": "Orin DX",
  "skills": ["bug-hunter-python"],
  "agents": [
    "bug-hunter-scanner-python",
    "bug-hunter-adversary-python",
    "bug-hunter-remediator-python"
  ]
}
```

### Step 3: Define Language Skill (`SKILL.md`)

Create `plugins/bug-hunter-python/skills/bug-hunter-python/SKILL.md`:
- Include relative Markdown links to shared debugging laws: `[General Debugging Laws](../../../shared/debugging-laws.md)` and `[Evaluation Report Template](../../../shared/report-template.md)`.
- Define 6 language-specific hazard taxonomies with exact ripgrep regex search patterns.

### Step 4: Define Subagents (`subagents/*.md`)

Create 3 subagent prompt files under `plugins/bug-hunter-python/subagents/`:
- `bug-hunter-scanner-python.md`: Static ripgrep regex scanner (Taxonomies 1 & 4).
- `bug-hunter-adversary-python.md`: Execution path tracer & adversary (Taxonomies 2 & 3).
- `bug-hunter-remediator-python.md`: Red-to-Green test engineer (Taxonomies 5 & 6).

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

1. **Self-Contained Plugin Scoping**: Keep language rules isolated within `plugins/<plugin-id>/`. Do not mix rules for multiple languages in a single plugin.
2. **On-Demand Context**: Reference `shared/debugging-laws.md` via relative Markdown links instead of duplicating general debugging text.
3. **No Hardcoded Absolute Paths**: All paths in `SKILL.md` and prompt files must be relative.
4. **Clean Technical Writing**: Avoid emojis, marketing fluff, or AI filler phrases in documentation, skill descriptions, and commit messages.
5. **Conventional Commits**: Commit messages follow `feat:`, `fix:`, `docs:`, or `refactor:`.
