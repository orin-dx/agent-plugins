# TypeScript and JavaScript Architecture Smells

## Outcome

Use confirmed findings to detect missing domain ownership or enforcement. A repeated syntax pattern is not enough; trace the responsibility and failure state across modules and runtime boundaries.

## Signals

- Construction and execution use different option shapes, allowing user intent to disappear through structural compatibility.
- Unvalidated dynamic data escapes an adapter and weakens downstream types.
- Closed variants are handled in several places without one exhaustiveness mechanism.
- Related data and boolean flags can represent contradictory states instead of one explicit state model.
- Multiple async paths write the same file, cache entry, store, or UI state without one owner for ordering and failure.
- Shared state is read before `await` and trusted afterward even though another operation can change it.
- Producer and consumer schemas disagree on aliases, defaults, validation, or optionality.
- The same domain transition is implemented in several handlers, services, or reducers.
- Tests hand-build objects that can drift from the production parser or serializer.
- Architectural rules exist only in prose, with no type, test, lint, or CI enforcement.

## Refutation

Read the actual call graph, concurrency model, framework error boundary, schema authority, and architecture model. Dismiss or narrow the signal when a framework owns ordering or failure, a type is intentionally open, a boundary validates before use, or variation is part of the public contract.

Repeated literals, mutable types, console output, or missing documentation are style signals only when the target repository establishes that policy or observed behavior makes them harmful.

## Disposition

- Repair isolated behavior locally.
- Centralize one domain operation or state model when several sites own the same responsibility.
- Add enforcement when a documented invariant can drift silently.
- Escalate to `scribe:architect` when recurrence cannot be prevented within the current boundary.
- Derive names and abstractions from live code; do not import a design from the reference.
