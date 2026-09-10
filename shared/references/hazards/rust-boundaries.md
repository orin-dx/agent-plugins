# Rust Boundary Hazards · T7 and T10

Use this reference when tracing captured intent or error information across Rust boundaries. Record each hop; matching syntax alone cannot prove loss.

## T7 · Intent lost before execution

- Signal: a plan, config, request, or options value captures a meaningful field, but a narrower downstream signature or command omits it.
- Outcome: user intent is replaced by a default or never affects the side effect.
- Evidence: identify the construction site, field value, call chain, final execution boundary, and the first hop where the value disappears.
- Refute: the field is read by an equivalent owner, intentionally ignored under a documented mode, or cannot change the selected operation.

Candidate search:

- Start from user-controlled fields and domain state, not a fixed list of names.
- Compare constructed fields with downstream parameters, command arguments, serialized payloads, and storage writes.
- Treat an unused field as confirmable only when a reachable caller supplies a value that should change behavior.

## T10 · Error context lost across a boundary

- Signal: `map_err`, string conversion, or a replacement error discards the source, diagnostic identity, span, retryability, or structured fields.
- Outcome: the caller cannot make a required decision or diagnose the underlying failure.
- Evidence: compare the source error's useful capabilities with the destination error and show which required information no longer survives.
- Refute: the destination boundary accepts only a string or stable wire shape, sensitive detail must be removed, or the lost data has no consumer.

Distinguish T10 from T4: T4 leaves a failure unowned; T10 reports a failure through a representation that may be too weak. Preserve only the context the destination reader or machine consumer needs.
