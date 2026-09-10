# Rust Hazard Reference

Patterns are leads, not findings. Confirm a reachable bad outcome in live code and record evidence that rules out the plausible exception. Use `rust-hazards-t7-t10.md` for boundary taxonomies T7 and T10.

## T8 · False-success mutation

- Signal: a write-like function returns `Ok(())` before the required mutation or acknowledgment occurs.
- Search: write/update/set/publish functions and early `Ok` returns.
- Confirm: the caller cannot distinguish required work from a no-op and proceeds with incorrect state.
- Refute: idempotent success is part of the contract or the caller verifies the resulting state.

## T1 · Discarded input

- Signal: a meaningful public or trait parameter is renamed with `_`, dropped, or never reaches the behavior it configures.
- Confirm: a caller supplies a value whose omission changes the outcome.
- Refute: the signature is imposed by a trait or compatibility boundary and the value is intentionally irrelevant.

## T2 · Silent fallback

- Signal: `unwrap_or*` substitutes a default after parsing, lookup, or I/O failure.
- Confirm: the default hides a state the caller must distinguish.
- Refute: the default is the documented domain value and preserves required behavior.

## T3 · Recoverable panic

- Signal: `unwrap`, `expect`, or `panic!` is reachable in reusable code.
- Confirm: valid external input or a recoverable dependency failure reaches it.
- Refute: the path is an established invariant, test-only code, or process entrypoint policy.

## T4 · Lost error

- Signal: a `Result` is assigned to `_`, dropped, or replaced by success.
- Confirm: failure changes subsequent correctness and no owner observes it.
- Refute: best-effort behavior is explicit and the discarded failure has no required consequence.

## T5 · Arithmetic overflow

- Signal: user- or data-controlled integers participate in unchecked arithmetic near a bound.
- Confirm: a reachable value overflows under the relevant build profile.
- Refute: types, validation, or domain limits prove the operation safe.

## T6 · Unsafe contract gap

- Signal: an `unsafe` block lacks a locally checkable safety contract or relies on an unverified caller invariant.
- Confirm: a reachable input violates the invariant and can cause undefined behavior.
- Refute: the contract is enforced at the boundary and covers every operation in the block.

## T9 · Incomplete or ambiguous variants

- Signal: enum conversion uses a catch-all that rejects a valid variant, or diagnostic identifiers collide where consumers require uniqueness.
- Confirm: a current variant is mishandled or a consumer cannot distinguish outcomes.
- Refute: the source is intentionally open, the fallback is contractual, or duplicate identifiers are documented aliases.

Search broadly enough to find candidates, then cite the exact caller, input, state transition, and failure for every confirmed result.
