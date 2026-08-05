# delta — Ship Tooling

**Stage:** Ship · **Output:** `release-artifact@1`

Handles everything after implementation: commit messages, PR descriptions, changeset extraction, review triage, and release notes. Consumes `changeset@1` entries and produces `release-artifact@1`.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `delta-commit-analyzer` | Commit Author | haiku/low | Reads staged diff and produces a conventional commit message explaining why, not what. |
| `delta-changeset-analyzer` | Changeset Extractor | sonnet/medium | Produces a `changeset@1` from a git diff, mapping files changed and acceptance criteria met. |
| `delta-pr-narrator` | PR Author | sonnet/medium | Writes a PR title and body from the reviewer's perspective — zero prior context assumed. |
| `delta-review-preprocessor` | Review Triager | sonnet/medium | Categorizes PR review comments as must-fix, suggestion, or question; produces an action plan. |
| `delta-release-summarizer` | Release Author | sonnet/medium | Aggregates `changeset@1` entries into a `release-artifact@1` with user-facing summaries. |

## Subagent Selection

Run subagents individually based on the task at hand — delta is not a linear pipeline:

- **Making a commit:** `delta-commit-analyzer`
- **Opening a PR:** `delta-changeset-analyzer` → `delta-pr-narrator`
- **Responding to review:** `delta-review-preprocessor`
- **Cutting a release:** `delta-release-summarizer`

## Output Schemas

- `changeset@1` — see `shared/schemas/changeset@1.json`
- `release-artifact@1` — see `shared/schemas/release-artifact@1.json`

## References

- `shared/references/conventional-commits.md` — type/scope conventions
- `shared/references/github.md` — PR template, `gh` CLI commands
- `shared/references/changesets.md` — semver bump decision guide
