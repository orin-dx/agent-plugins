# Modern CLI Tools

## Outcome

Use fast, structured tools when they are installed and fit the repository. Repository-native commands, task runners, and required wrappers take priority. A missing preferred tool is a reason to use a safe fallback, not to install software or stop the task.

| Need | Prefer when available | Practical fallback |
| :--- | :--- | :--- |
| Search text | `rg` | platform search tool |
| Discover files | `fd` | platform file discovery |
| Read source | `bat` | plain file reader |
| Inspect directories | `eza` | directory listing tool |
| Query JSON | `jq` | repository script or structured reader |
| Inspect Git changes | `git` with `delta` as pager | plain `git diff` |
| Filter an interactive choice | `fzf` | explicit non-interactive selection |
| Work with GitHub | `gh` | purpose-built connector or API |
| Navigate interactively | `zoxide` | explicit working directory |

## Selection

- Prefer structured output when another command or agent will consume the result.
- Use non-interactive commands for automation.
- Preserve the repository's wrapper, task runner, working-directory, and environment conventions.
- Avoid a pipeline when one tool can perform the filter or transformation directly.
- Confirm visible GitHub mutations immediately before running them.

Examples are illustrative, not mandatory:

```bash
rg -n "pattern" src
fd -e md . docs
jq '.scripts' package.json
git diff --stat
gh pr status
```
