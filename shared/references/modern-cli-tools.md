# Modern CLI Tools Reference (`modern-cli-tools`)

**Status:** Mandatory Directive across all agents, skills, and subagents.
**Purpose:** Replace legacy POSIX/Unix shell builtins with high-performance, modern CLI tools in terminal executions and shell commands.

---

## Directives & Tool Substitutions

| Task / Operation | Preferred Modern Tool | Legacy Tool to Avoid | Command Example |
| :--- | :--- | :--- | :--- |
| **File Viewing & Syntax Highlighting** | `bat` | `cat`, `less`, `more` | `bat -n src/main.rs` |
| **Directory Navigation** | `zoxide` (`z`) | `cd` | `z callisto` or `zoxide query <dir>` |
| **Code & Pattern Search** | `ripgrep` (`rg`) | `grep`, `egrep` | `rg "fn handle_request" src/` |
| **File & Directory Discovery** | `fd` | `find` | `fd -e rs -e toml` |
| **Directory Formatting & Tree View** | `eza` (or `exa`) | `ls`, `tree` | `eza --tree --level=2` |
| **Git Diffs & Code Inspection** | `delta` | `diff`, raw `git diff` | `git diff | delta` |
| **JSON Querying & Transformations** | `jq` | `python -m json.tool`, `sed` | `jq '.dependencies' package.json` |
| **Interactive Choice Filtering** | `fzf` | Manual interactive selection | `fd | fzf` |
| **GitHub Workflow & Operations** | `gh` CLI | Manual curl GitHub API calls | `gh pr status` |

---

## Tool Usage Details

### 1. `bat` (File Viewing)
- Displays file contents with syntax highlighting and line numbers.
- For plain output without line decorations: `bat -p <file>`
- For specific line ranges: `bat -r 10:40 <file>`

### 2. `zoxide` (Smart Directory Navigation)
- Remembers frequently used directories and jumps via fuzzy matching.
- Query path without changing directory: `zoxide query <name>`

### 3. `ripgrep` (`rg`) (Code & Pattern Search)
- Respects `.gitignore` automatically, extremely fast multi-threaded search.
- Filter by file type: `rg -t rust "pattern"` or `rg -t ts "pattern"`
- Search literal string: `rg -F "string"`

### 4. `fd` (File & Directory Discovery)
- Fast, user-friendly alternative to `find`.
- Search hidden files: `fd -H "pattern"`
- Search extensions: `fd -e md`

### 5. `eza` (Directory Formatting)
- Modern replacement for `ls` with grid, tree, long format, git status integration.
- List with details and git state: `eza -la --git`
- Tree view: `eza --tree --level=3`

### 6. `delta` (Diff Inspection)
- Syntax-highlighting pager for git diff output.
- Side-by-side diff: `git diff | delta -s`

### 7. `jq` (JSON Processing)
- Query, format, filter JSON files and command output streams.
- Format file in-place: `jq . file.json > tmp.json && mv tmp.json file.json`

### 8. `gh` (GitHub Operations)
- Interact with GitHub repos, issues, pull requests, releases, and actions workflows directly.
