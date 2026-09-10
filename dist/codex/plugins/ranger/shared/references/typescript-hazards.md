# TypeScript and JavaScript Hazard Reference

Patterns are leads, not findings. Confirm a reachable bad outcome in the target runtime and account for framework behavior. Use `typescript-hazards-t7-t10.md` for boundary taxonomies T7 and T10.

## T8 · False-success mutation

- Signal: a write-like async function resolves before required work or acknowledgment occurs.
- Confirm: the caller proceeds as though state changed when it did not.
- Refute: idempotent no-op is contractual or the caller verifies resulting state.

## T1 · Type assertion bypass

- Signal: `as any`, `as unknown as T`, or an unchecked assertion appears at a dynamic boundary.
- Confirm: a reachable value violates the asserted shape before validation.
- Refute: a local adapter validates the same invariant or the assertion bridges a proven library limitation.

## T2 · Unowned promise failure

- Signal: async work starts without awaiting, returning, retaining, or observing rejection.
- Confirm: no framework or caller owns completion and failure.
- Refute: the runtime explicitly owns the handler or a deliberate fire-and-forget path reports failure elsewhere.

## T3 · Dynamic type propagation

- Signal: `any` or unchecked parsed data escapes a boundary into domain code.
- Confirm: downstream operations trust a property or variant that runtime data may not contain.
- Refute: validation, generated types, or a narrow adapter establishes the shape first.

## T4 · Unchecked nullish state

- Signal: non-null assertions or a partially guarded property chain dereference a value that can still be nullish.
- Confirm: construct a reachable state where the asserted segment is absent.
- Refute: control flow, schema validation, or framework lifecycle guarantees presence.

## T5 · Prototype-key mutation

- Signal: an external key controls assignment into an ordinary object.
- Confirm: `__proto__`, `constructor`, or `prototype` can reach a mutation with security or correctness impact.
- Refute: keys are allow-listed or storage uses a safe representation.

## T6 · Missing async error owner

- Signal: an async route, event, or callback can reject with no local or framework error boundary.
- Confirm: trace a failure to an unhandled rejection or false-success response.
- Refute: the host contract captures and reports returned rejections.

## T9 · Incomplete closed variants

- Signal: a closed union gains a variant while a switch or branch silently falls back.
- Confirm: the new or existing variant reaches an incorrect default behavior.
- Refute: the input set is intentionally open and the fallback is the documented behavior.

## Additional leads

- Shallow copies of nested mutable state when later mutation is reachable.
- JSON-based cloning when required values include types or properties it cannot preserve.
- Shared state read before `await` and trusted afterward despite concurrent mutation.

For each, prove the required value shape, runtime support, ownership model, and failing outcome before reporting a defect.
