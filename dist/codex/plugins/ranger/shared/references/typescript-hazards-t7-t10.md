# TypeScript and JavaScript Boundary Hazards · T7 and T10

Use this reference when tracing captured intent or failure information across module, process, serialization, or async boundaries.

## T7 · Intent lost before execution

- Signal: a request, options, config, or payload value contains a meaningful field, but a narrower structural type or downstream operation does not read or forward it.
- Outcome: user intent is silently replaced by default behavior.
- Evidence: identify construction, every call or transformation, the execution boundary, and the first hop where the field disappears.
- Refute: another owner consumes the field, omission is explicit for the active mode, or the field cannot affect the operation.

Candidate search:

- Derive fields from live inputs and domain responsibilities, not a fixed vocabulary.
- Compare wide input shapes with narrower parameters, destructuring, payload builders, command arguments, and storage writes.
- Confirm a candidate only when a reachable caller supplies a value that should change behavior.

## T10 · Failure suppressed or downgraded

- Signal: `catch`, rejection handling, or error mapping resolves successfully or removes structured information the caller needs.
- Outcome: a caller misses failure, retryability, cause, code, or actionable context.
- Evidence: trace the rejected or thrown value through the handler and show the incorrect success or lost capability at the consumer.
- Refute: the handler deliberately converts failure into a documented fallback, signals status through another channel, removes sensitive data, or crosses a boundary with a narrower required shape.

Distinguish T10 from T2: T2 has no failure owner; T10 has an owner that may hide or weaken the failure. Logging alone is evidence only when the contract defines logging as the terminal outcome.
