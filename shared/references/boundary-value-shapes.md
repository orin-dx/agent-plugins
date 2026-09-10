# Boundary Value Shapes

## Outcome

Represent absence, failure, freshness, and validity so callers cannot accidentally treat one state as another. Apply this when a changed value crosses a module, process, storage, serialization, or public API boundary.

## Signals

- A value sits beside `isValid`, `hasValue`, `isFresh`, `ok`, or another flag that can disagree with it.
- A sentinel such as an empty string, zero, or empty object carries a second undocumented meaning.
- A default erases whether a value was absent, invalid, stale, or explicitly supplied.
- Producer and consumer types encode the same states differently.
- Callers repeatedly perform the same validity check before use.

## Choose a shape

Name the real states and the operations each state permits. Prefer a representation that makes invalid combinations difficult to construct and requires meaningful branches at the point of use.

| Language | Useful shapes when they fit |
| :--- | :--- |
| Rust | `enum`, `Option<T>`, `Result<T, E>`, validated newtype |
| TypeScript | discriminated union, validated schema result, branded type |
| Python | enum plus dataclass/model variants, validated model, explicit result object |
| Go | separate concrete variants behind an interface, tagged struct with validated constructor, `(T, bool)` or `(T, error)` when consumed immediately and conventionally |

Use the language and repository's established model. Do not introduce a sum type merely because a boolean exists; prove that states can diverge or callers currently miss a required check.

## Refutation

Keep the existing shape when the state is local and immediately consumed, the language idiom is already handled consistently, serialization requires the representation, or compatibility cost exceeds the scoped risk. Record the constraint instead of forcing a redesign.

## Disposition

- Add local validation when one boundary owns the state and callers cannot bypass it.
- Unify producer and consumer models when parallel representations drift.
- Escalate to `scribe:architect` when the unsafe shape is public, widely constructed, or requires coordinated migration.
- Record a coverage gap when the external representation or callers cannot be inspected.
