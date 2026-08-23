# Workspace Conventions

_Loaded by any agent that needs to locate a persisted pipeline artifact on disk without being told its exact path — currently: canon:auditor, graph:auditor, trace:recon._

---

## Where gated specs live

`canon/gate-spec` writes every spec@1 that passes its exit gate to `<workspace_root>/.claude/specs/<id>.json` and commits it (see `shared/constitution.md`'s Spec Persistence section — this file is the runtime-loadable restatement of that rule, for agents that need it as an operational fact, not just documented policy).

A spec still in draft — not yet gated — will not appear there. Treat an empty or sparse `.claude/specs/` directory as "nothing gated yet," not as proof no related work exists; note the limitation in `reasoning` rather than treating the search as exhaustive.

## Where plans live

`plan@1` is never persisted to disk anywhere in this pipeline — it exists only in conversation context between `vector` producing it and `lambda` consuming it. Do not search the workspace for a plan file; none exists to find.
