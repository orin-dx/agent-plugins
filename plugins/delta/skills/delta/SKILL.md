---
name: ship
description: >-
  Trigger this skill when the user asks to commit code, write a commit message, open a PR, create a pull request, write the PR description, review a PR, address feedback, respond to review comments, add a changeset, cut a release, summarize what's in a release, or document a change. Activate when the user says "commit this", "write a commit message", "open a PR", "create a pull request", "write the PR description", "review this PR", "address the feedback", "add a changeset", "cut a release", "what's in this release", or "document this change". This skill reads the staged diff, linked spec, and linked requirement to produce meaningful, context-aware output — not mechanical templates. It coordinates five subagents that each handle one phase of the shipping lifecycle: commit authoring, PR narration, changeset extraction, review preprocessing, and release summarization.
version: "1.0.0"
---

# Delta — Shipping Skill

<overview>
Delta shepherds completed, verified code through the full shipping lifecycle. It reads the diff, the spec, and any linked requirement at runtime to produce output that means something — commit messages that explain why, PR descriptions a reviewer can act on, changesets that distinguish user-facing changes from internal refactors, and release notes written for the person using the product.
</overview>

---

<sub_skills>

## Sub-skills

### `delta/commit`
Reads the staged git diff and produces a conventional commit message that explains why the change was made. Delegates to `delta-commit-analyzer`.

### `delta/pr`
Given a diff, a linked spec, and a linked requirement, produces a PR title and body a reviewer with zero context can understand. Delegates to `delta-pr-narrator`.

### `delta/changeset`
Extracts the semantic meaning of a change for a changeset entry, distinguishes user-facing from internal changes, and determines semver impact. Delegates to `delta-changeset-analyzer`. Produces `changeset@1`.

### `delta/review`
Categorizes incoming review comments as must-fix, suggestion, or question. Produces a prioritized response plan. Delegates to `delta-review-preprocessor`.

### `delta/receive`
Alias for `delta/review` — used when framing the work as receiving and processing feedback rather than reviewing.

### `delta/release`
Aggregates changesets since the last release into grouped, user-facing release notes and determines the semver bump. Delegates to `delta-release-summarizer`. Produces `release-artifact@1`.

</sub_skills>

---

<subagent_dispatch_matrix>

| Agent | Role | Model / Effort | Delegate When |
| :--- | :--- | :--- | :--- |
| **delta-commit-analyzer** | Commit author | haiku / low | Staged changes are ready and need a conventional commit message explaining why. |
| **delta-changeset-analyzer** | Changeset extractor | sonnet / medium | A git diff needs a structured changeset@1 with semver impact and acceptance criteria mapping. |
| **delta-pr-narrator** | PR description author | sonnet / medium | A PR needs a title and body a reviewer with zero context can act on. |
| **delta-review-preprocessor** | Review package assembler | haiku / low | Before opening a PR, bundle diff, linked spec, test results, and open questions for the reviewer. |
| **delta-release-summarizer** | Release notes author | sonnet / medium | Aggregate changeset@1 entries into a user-facing release-artifact@1. |

</subagent_dispatch_matrix>

---

<references>
At runtime, agents read the following shared reference files:
- `shared/references/conventional-commits.md` — type/scope conventions and commit message rules
- `shared/references/github.md` — PR template and label conventions
- `shared/references/changesets.md` — changeset format and semver bump decision rules
</references>

---

<io>

**Consumes**: `changeset@1`, staged git changes, PR diff, review comments

**Produces**: merged PR, `release-artifact@1`

</io>
