# Persisted Workspace Artifacts

Use this reference only when an artifact path was not supplied.

| Artifact | Canonical path | Owner | Persistence event |
| :--- | :--- | :--- | :--- |
| Gated specification | `docs/specs/<id>.json` | `scribe/gate-spec` | Pass verdict; file committed |
| Approved plan | `docs/projects/<linked_spec>.json` | `navigator/plan` | Challenger pass; file committed |
| Architecture model | `docs/architecture/model.json` | `scribe/audit-architecture` | Build or refresh; same file updated and committed |

Read a supplied `spec_file_path` or `plan_file_path` instead of reconstructing the path. An uncommitted artifact is not durable pipeline state.

## Absence

- Missing spec: no matching gated spec was found. Draft or external requirements may still exist.
- Missing plan: no matching approved plan was found. In-context or draft planning may still exist.
- Missing architecture model: no model has been persisted. Live code still has structure; let `scribe/audit-architecture` bootstrap the model when needed.

Record the missing artifact and search scope as a coverage gap. Do not treat an empty directory as proof that no related work or constraint exists.
