# Workspace Conventions

_Loaded by any agent that needs to locate a persisted pipeline artifact on disk without being told its exact path — currently: scribe:auditor, scribe:arch-auditor, weaver:auditor, vanguard:recon._

---

## Where gated specs live

`scribe/gate-spec` writes every spec@1 that passes its exit gate to `<workspace_root>/docs/specs/<id>.json` and commits it (see `shared/constitution.md`'s Spec Persistence section — this file is the runtime-loadable restatement of that rule, for agents that need it as an operational fact, not just documented policy).

A spec still in draft — not yet gated — will not appear there. Treat an empty or sparse `docs/specs/` directory as "nothing gated yet," not as proof no related work exists; note the limitation in `reasoning` rather than treating the search as exhaustive.

## Where plans live

`navigator/plan` writes every plan@1 that passes challenger's review to `<workspace_root>/docs/projects/<linked_spec>.json` and commits it (see `shared/constitution.md`'s Plan Persistence section).

A plan still in draft — not yet through challenger — will not appear there. Treat an empty or sparse `docs/projects/` directory as "nothing persisted yet," not as proof no planning work exists.

## Where the architecture model lives

The system-wide `arch-model@1` is a single persisted document at `<workspace_root>/docs/architecture/model.json`, built and maintained by `scribe/arch-auditor` (build/refresh mode). Unlike specs and plans, it is not per-artifact — one workspace has one model, updated in place rather than versioned by id.

If the file is absent, treat it as "no model built yet," not as evidence the codebase lacks structure — `scribe/arch-auditor` bootstraps it on first use rather than failing.
