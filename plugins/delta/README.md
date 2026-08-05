# delta — Ship Tooling

**Stage:** Ship · **Output:** `release-artifact@1` · **Version:** 1.0.1

Handles everything after implementation: commit messages, PR descriptions, changeset extraction, review triage, and release notes. Delta is not a linear pipeline — each subagent is invoked individually based on the task at hand. It reads the staged diff, linked spec, and linked requirement at runtime to produce meaningful, context-aware output, not mechanical templates.

---

## When to Use

- You need a commit message that explains *why*, not just *what*
- You're opening a PR and want a description a reviewer with zero context can act on
- You need to categorize and respond to PR review comments
- You're cutting a release and need user-facing release notes
- You want to extract a `changeset@1` from a git diff for semantic versioning

**Invoke with:** `"Commit this"`, `"Write a commit message"`, `"Open a PR"`, `"Write the PR description"`, `"Address the feedback"`, `"Respond to review comments"`, `"Cut a release"`, `"What's in this release"`, `"Add a changeset"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `delta/commit` | Reads staged diff, produces a conventional commit message explaining the *why* |
| `delta/pr` | Produces a PR title and body a reviewer with zero prior context can understand |
| `delta/changeset` | Extracts semantic change meaning, distinguishes user-facing from internal, determines semver impact |
| `delta/review` | Categorizes incoming review comments as must-fix, suggestion, or question; produces a response plan |
| `delta/receive` | Alias for `delta/review` — use when framing work as receiving feedback rather than reviewing |
| `delta/release` | Aggregates changesets since last release into grouped user-facing notes and determines the semver bump |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `delta-commit-analyzer` | Commit Author | haiku / low | Reads staged diff and produces a conventional commit message explaining why, not what. |
| `delta-changeset-analyzer` | Changeset Extractor | sonnet / medium | Produces a `changeset@1` from a git diff, mapping files changed and acceptance criteria met. |
| `delta-pr-narrator` | PR Author | sonnet / medium | Writes a PR title and body from the reviewer's perspective — zero prior context assumed. |
| `delta-review-preprocessor` | Review Triager | sonnet / medium | Categorizes PR review comments as must-fix, suggestion, or question; produces an action plan. |
| `delta-release-summarizer` | Release Author | sonnet / medium | Aggregates `changeset@1` entries into a `release-artifact@1` with user-facing summaries. |

---

## Subagent Selection

Delta is a toolbox, not a pipeline. Pick the subagent that matches the task:

| Task | Subagents to run |
| :--- | :--- |
| Making a commit | `delta-commit-analyzer` |
| Opening a PR | `delta-changeset-analyzer` → `delta-pr-narrator` |
| Responding to review | `delta-review-preprocessor` |
| Cutting a release | `delta-release-summarizer` |

---

## Output Schemas

- `changeset@1` — see `shared/schemas/changeset@1.json`
- `release-artifact@1` — see `shared/schemas/release-artifact@1.json`

---

## References

Agents read these at runtime — they are not injected at startup:

- `shared/references/conventional-commits.md` — type/scope conventions and commit message rules
- `shared/references/github.md` — PR template and label conventions
- `shared/references/changesets.md` — changeset format and semver bump decision rules

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install delta
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Previous Stage

Consumes `changeset@1` from **[lambda](../lambda/)** or produced directly from a staged git diff.
