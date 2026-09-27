# Decision Records

Decide whether an architectural choice needs a durable record, and write the record so a later reader with no memory of the discussion does not silently reverse it. A record preserves the reason behind a decision, so nobody accepts it blindly or reverses it blindly.

## Write one only when both gates pass

- **Architectural:** the choice sets a boundary, a model, a direction, or a rule that several changes must respect.
- **Expensive to reverse or not obvious from the code:** a reader who sees only the code would plausibly undo it, or undoing it would be costly.

One decision per record. A choice that fails a gate belongs elsewhere.

| Fact | Home |
| :--- | :--- |
| Architecture, model, direction, decision, rejected alternative | Decision record in `docs/adr/` |
| Rule for every session: command, invariant, style, routing | `AGENTS.md` |
| Required behavior | Spec |
| How the system works today | Docs |
| Why one change was made | Commit message |
| Personal preference or correction for one repository | Agent memory, uncommitted |

Agent memory is unshared and goes stale, so a decision never lives only there.

## Form

Title, status, context, decision, options considered, consequences. Each rejected option carries its "because". Keep a record to one or two pages. Records written before this form may state the alternatives inside the context; leave them as written.

Add an `Enforced by` line only when a test, lint, type, or hook enforces the decision. A decision that a check can enforce should have the check; the record explains why it exists.

Add one line to the `docs/adr/README.md` index in the form `Do not <X> without a new ADR`, for a decision an agent could undo without noticing.

## Prose

Keep the causal "because" and the rejected alternative. Cut narration of the discussion, restated code, and hedging. Write one paragraph per line; do not hard-wrap.

## Status and change

Do not rewrite an accepted record's context, decision, or options; the reasoning at the time is what the record preserves. Update its status and links, and fix errors that do not change its meaning. To change a decision, write a new record that supersedes it and mark the old one superseded; the old record stays. Keep the active set small by writing records only for decisions that pass both gates.

## Refutation and disposition

Evidence for a record is the code, spec, or constraint it governs. Before proposing a boundary, read the accepted records for that area. Treat a superseded record as history, not a constraint.

- **Write:** both gates pass and no accepted record covers the choice.
- **Supersede:** the new decision reverses an accepted record; cite it and state what changed.
- **Skip:** the choice is a preference, a routine change, or already obvious from the code; put the reason in the commit message.
- **Coverage gap:** if `docs/adr/` is absent, say so. Absence does not prove that no decision governs the area.
