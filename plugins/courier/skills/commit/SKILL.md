---
name: commit
description: >-
  Trigger when the user asks to commit code or write a commit message: "commit this", "write a commit message", "commit the staged changes". Reads the staged git diff and produces a conventional commit message explaining why the change was made, not what changed — the diff already shows what changed.
version: 2.0.0
---

# Courier — Commit

<overview>
Reads the staged git diff and produces a conventional commit message. Delegates entirely to `commit-analyzer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **commit-analyzer** | haiku / low | Staged changes are ready and need a conventional commit message. |
</dispatch>

<references>
`shared/references/conventional-commits.md` — type/scope conventions, commit message rules, and the voice standard for this artifact.
</references>

<io>
**Consumes**: staged git diff
**Produces**: conventional commit message. The skill runs `git commit` after the user confirms the message — committing is a local, reversible action per this repo's standing action-safety guidance, but still surface the message for confirmation before running it.
</io>
