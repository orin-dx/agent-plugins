# Rust Architecture Smells

## Outcome

Use confirmed findings to ask whether the codebase lacks one domain concept, state, operation, boundary, invariant, or enforcement mechanism. A smell is an architecture lead, not proof and not a predetermined trait design.

## Signals

- Structural equality is used where the domain exposes a broader predicate such as `matches`, `satisfies`, or `equivalent`.
- Related values and validity flags can represent contradictory states instead of one enum or result type.
- Several callers reconstruct the same command, mutation, transition, or error mapping.
- Multi-step filesystem or repository mutation has no owner for atomicity, rollback, or durability.
- Producer and consumer representations can lose formatting, aliases, variants, or fields across serialization.
- Traversal, retry, or fixpoint logic has no explicit bound or termination condition.
- User-provided metadata is replaced by defaults between capture and execution.
- User-visible or serialized collections have unstable order when the contract requires deterministic output.
- Tests hand-build serialized fixtures that can drift from the production representation.
- An architectural rule exists only in prose, with no type, test, lint, or CI enforcement.

## Refutation

Read the live callers, ownership boundaries, public contracts, and persisted architecture model. Dismiss or narrow the signal when behavior is intentionally local, the state cannot diverge, the boundary already has one owner, or the repository explicitly permits the variation.

Performance shapes such as allocation strategy are architecture concerns only with measurements or a documented hot-path constraint. Public documentation and collection choices follow the target repository's policy, not this reference.

## Disposition

- Repair a local instance when no shared responsibility exists.
- Unify behavior when several sites implement the same responsibility.
- Escalate to `scribe:architect` when recurrence requires a new model, boundary, invariant, or enforcement mechanism.
- Name the required responsibility first. Propose a concrete type or trait only after live architecture evidence supports it.
