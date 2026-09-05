---
name: commit
description: Prepare or create a conventional commit from staged work. Use when the user asks to commit changes or write a commit message; never create a commit without confirmation.
---

# Commit verified work

Inspect the staged diff, staged file list, and recent commit history before drafting anything. Do not infer scope from unstaged work or a task description when the index says otherwise.

## Workflow

1. Confirm that the index contains the intended files and identify the smallest coherent change represented by it.
2. Read `shared/references/conventional-commits.md` for type, scope, and voice rules.
3. Draft a conventional commit subject and body that explains why the change exists. Let the diff carry mechanical detail.
4. Show the exact message and staged file scope.
5. Create the commit only after the user explicitly confirms that exact message and scope.

## Safety

- Do not stage, amend, reset, rebase, or commit unrelated changes unless the user explicitly asks.
- If staged work contains unrelated topics, explain the split and ask which subset to commit rather than producing a misleading umbrella message.
- If no changes are staged, report that fact and do not substitute the working-tree diff.

## Team use

This is a bounded single-artifact task. Complete it yourself; do not request an agent team.
