# Boundary Value Shapes

_Loaded by: smith:implementer, whenever a task's acceptance criterion involves a value that can be absent, wrong, or stale — especially where it crosses a process, crate, or serialization boundary. Not a bug-hunting taxonomy — ranger and reviewer do not load this file._

---

## Default posture

A value that is sometimes absent, sometimes wrong, or sometimes stale is a **state**, not an annotation on a value. Represent the state as a sum type — a Rust `enum`, a TypeScript discriminated union, a `Result` — so the compiler forces every caller to handle every state. A raw value sitting next to a separate `bool`/sentinel lets a caller read the value and forget to check the flag; nothing in the type system ties the two together.

This applies hardest at a boundary — a value that crossed a process, crate, or serialization edge is exactly the value most likely to be stale, absent, or wrong on the far side, and exactly the value a caller is most likely to trust without re-checking.

### Rust

```rust
// ✗ raw value + bool — nothing stops a caller from reading `price` without checking `is_priced`
struct ModelInfo {
    price: f64,
    is_priced: bool,   // true only if `price` reflects real pricing data
}

fn cost(info: &ModelInfo) -> f64 {
    info.price // compiles even when is_priced is false
}

// ✓ the unpriced state is a variant, not a flag — cost() has nothing to read if there's no price
enum Pricing {
    Priced(f64),
    Unpriced,
}

fn cost(pricing: &Pricing) -> Option<f64> {
    match pricing {
        Pricing::Priced(p) => Some(*p),
        Pricing::Unpriced => None,
    }
}
```

- **Grep for the anti-pattern:** a struct field paired with a separate `bool` describing that field's validity (`is_valid`, `is_priced`, `is_fresh`, `_ok`, `_stale`) — including when the paired field is already `Option<T>`, since the bool is then redundant with (and can drift from) the `None` case.
- **Prefer:** `enum` with one variant per real state, or `Result<T, E>` when the alternative is failure rather than a distinct valid state.

### TypeScript

```typescript
// ✗ raw value + boolean — nothing ties toolCounts to whether it was actually populated
interface SessionSummary {
  toolCounts: Record<string, number>
  hasToolCounts: boolean   // caller must remember to check this
}

// ✓ discriminated union — the populated/unavailable states are distinguishable by their shape
type ToolCounts =
  | { status: 'populated'; counts: Record<string, number> }
  | { status: 'unavailable' }

function render(summary: { toolCounts: ToolCounts }) {
  switch (summary.toolCounts.status) {
    case 'populated': return summary.toolCounts.counts
    case 'unavailable': return null
  }
}
```

- **Grep for the anti-pattern:** an interface or type with a data field paired with a separate `has*`/`is*`/`*Valid` boolean sibling.
- **Prefer:** a discriminated union keyed on a `status`/`kind`/`tag` field (see `typescript-hazards.md`'s T9 for the matching exhaustiveness check once the union exists), or the built-in rejection path when the alternative is failure rather than a distinct valid state.

## When the task's own scope can't get there

Sometimes the unsafe shape is already load-bearing beyond this one task — the struct is a public type other crates construct directly, or the interface is exported and consumed by code outside this task's `covers_criteria`. Changing it here would silently break call sites this task was never scoped to touch. That is the signal to stop and report `needs_architecture` rather than either writing the narrower unsafe shape to make this task's own test pass, or changing the shared type anyway and hoping nothing else depended on the old one.
