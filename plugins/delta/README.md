# delta — Ship Tooling

**Stage:** Ship · **Output:** `release-artifact@2` · **Version:** 2.1.2

Handles everything after implementation: commit messages, PR descriptions, changeset extraction, review triage, posting a review, and release notes. Delta is not a linear pipeline — six independently-triggered skills, each dispatching to the subagent that matches the task. It reads the staged diff, linked spec, and linked requirement at runtime to produce meaningful, context-aware output, not mechanical templates.

Delta does not critique code quality or spec conformance — that's the built-in `code-review` skill and `axiom`'s job respectively. Delta consumes their findings when relevant (e.g. `delta/post-review` can post an already-drafted `code-review` finding) rather than re-implementing them.

---

## When to Use

- You need a commit message that explains *why*, not just *what*
- You're opening a PR and want a description a reviewer with zero context can act on
- You need to categorize incoming PR review comments and respond to them
- You have an already-drafted review or reply and want it posted to GitHub
- You're cutting a release and need user-facing release notes
- You want to extract a `changeset@2` from a git diff for semantic versioning, classified from a consumer's perspective

**Invoke with:** `"Commit this"`, `"Write a commit message"`, `"Open a PR"`, `"Write the PR description"`, `"Address the feedback"`, `"Respond to review comments"`, `"Post this review"`, `"Cut a release"`, `"What's in this release"`, `"Add a changeset"`

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `delta/commit` | Reads staged diff, produces a conventional commit message explaining the *why* | `commit-analyzer` |
| `delta/pr` | Produces a PR title and body a reviewer with zero prior context can understand, opens the PR after confirmation | `pr-narrator` |
| `delta/changeset` | Splits a diff into independent topics if it has more than one, classifies consumer_impact and semver_impact per topic, and writes a changeset whose detail scales with that classification | `changeset-analyzer` |
| `delta/receive-feedback` | Triages incoming review comments (must-fix / suggestion / question) and assembles the review package | `review-preprocessor` |
| `delta/post-review` | Posts an already-drafted review or reply via `gh pr review`/`gh pr comment`, gated by explicit confirmation | none — mechanical orchestration only |
| `delta/release` | Aggregates changesets since the last release; version is `max(semver_impact)` across included changesets | `release-summarizer` |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `commit-analyzer` | Commit Author | haiku / low | Reads staged diff and produces a conventional commit message explaining why, not what. |
| `changeset-analyzer` | Changeset Extractor | sonnet / medium | Classifies `consumer_impact` and `semver_impact` from a git diff per the decision table in `changesets.md`, then produces a `changeset@2` whose summary detail scales with that classification. |
| `pr-narrator` | PR Author | sonnet / medium | Writes a PR title and body from the reviewer's perspective — zero prior context assumed. |
| `review-preprocessor` | Review Package Assembler | haiku / low | Bundles the diff, linked spec, test results, and open questions into a structured review package; categorizes incoming comments by priority. |
| `release-summarizer` | Release Author | sonnet / medium | Aggregates `changeset@2` entries into a `release-artifact@2`, computing the version as `max(semver_impact)` and filtering `internal-only` entries. |

`delta/post-review` has no subagent — posting is mechanical execution of already-drafted content, gated by user confirmation, not a judgment task.

---

## Pipeline

```mermaid
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:2px,color:#1e1b4b,rx:8px,ry:8px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95,rx:8px,ry:8px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#78350f,rx:8px,ry:8px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b,rx:8px,ry:8px;

    diff[git diff] --> chg["delta/changeset"]
    chg -->|"changeset@2"| pr["delta/pr"]
    chg -->|"changeset@2"| rel["delta/release"]
    pr --> prOut(["PR opened"])
    rel --> relOut(["release-artifact@2"])

    comments[PR comments] --> recv["delta/receive-feedback"]
    recv -->|"response plan"| fix[fix code]
    fix --> post["delta/post-review"]
    post --> reply(["posted reply"])

    class diff,comments source
    class chg,pr,rel engine
    class recv,post router
    class prOut,relOut,reply output
```

`fix code` is the one step delta doesn't do — a human or `lambda` closes that gap before `delta/post-review` picks back up.

---

## Output Schemas

- `changeset@2` — see `shared/schemas/changeset@2.json` (supersedes `changeset@1`, still valid but legacy — adds required `consumer_impact`/`semver_impact`)
- `release-artifact@2` — see `shared/schemas/release-artifact@2.json` (supersedes `release-artifact@1`)

---

## References

Agents read these at runtime — they are not injected at startup:

- `shared/references/conventional-commits.md` — type/scope conventions, commit message rules, voice
- `shared/references/github.md` — PR template, label conventions, review-comment vocabulary, voice
- `shared/references/changesets.md` — changeset format, consumer/semver classification tables, voice
- `shared/references/docs-voice.md` — the full voice standard these three embed a subset of

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

Consumes lambda's per-task `criteria_evidence` from **[lambda](../lambda/)** (aggregated across the implementation run) as the precise input to `delta/changeset`, or produces `changeset@2` directly from a staged git diff when no lambda run backs the change.
