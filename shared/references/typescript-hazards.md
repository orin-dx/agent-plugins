# TypeScript Hazard Reference

_Loaded by: scanner (all taxonomies), adversary (when the candidate's taxonomy is not T7 or T10). T7 and T10 live in `typescript-hazards-t7-t10.md` — boundary-tracer's exact scope, loaded directly instead of this file. Do not load for smell analysis or fix work — use `typescript-smells.md` and `typescript-tooling.md` instead._

---

## Hazard Taxonomies

Ordered by impact — start here when triaging. T7 and T10 are documented in `typescript-hazards-t7-t10.md`.

### T8. False-Success Async ← highest impact
- **Signal:** An async function named `update*`, `write*`, `save*`, `sync*`, or `set*` returns `Promise<void>` and has a bare `return` (no value) reached before any `await` of a write or mutation.

```typescript
// ✗ BEFORE — caller receives a resolved promise with no way to know nothing was written
async function updateConfig(path: string, next: Config): Promise<void> {
  const current = await readConfig(path)
  if (deepEqual(current, next)) {
    return // silent no-op; caller assumes disk was updated
  }
  await writeConfig(path, next)
}

// ✓ AFTER — outcome is explicit; caller can log, retry, or branch
async function updateConfig(path: string, next: Config): Promise<boolean> {
  const current = await readConfig(path)
  if (deepEqual(current, next)) {
    return false // no-op, signaled
  }
  await writeConfig(path, next)
  return true // write confirmed
}
```
- **Grep pattern:** `async.*function.*(update|write|save|sync|set)` — then check the body for `return;` before any `await` of a side-effecting call.
- **Risk:** Caller believes the write succeeded; state is silently wrong.
- **False positive check:** Is the early return an explicitly documented "already-correct" guard with a caller-side check after?

### T9. Discriminated Union Incomplete Coverage ← highest impact
- **Signal:** A `switch` or if-chain on a `.kind`, `.type`, or `.tag` field that handles some variants explicitly and falls through to a `default` that returns a wrong value or throws a generic error — without `assertNever`.
- **Grep pattern:** `switch.*\.kind|switch.*\.type|switch.*\.tag` — check `default` branch for `assertNever`.
- **Risk:** A new variant added to the union silently hits the wrong code path at runtime with no compile-time warning.
- **False positive check:** Is the `default` branch an intentional catch-all with a documented contract?

### T1. Type Assertion Bypass
- **Signal:** `as unknown as T`, `as any`, `(<T>value)`.
- **Grep pattern:** `as\s+unknown\s+as|as\s+any\b|<[A-Z]\w*>\w`
- **Risk:** Runtime type mismatch — TypeScript's safety is bypassed.
- **False positive check:** Is this in a test utility, a known-safe coercion, or a migration shim with a comment?

### T4. Non-Null Assertion Abuse
- **Signal:** `value!.property`.
- **Grep pattern:** `[a-zA-Z0-9_)\]]\!\.`
- **Risk:** Crashes at runtime when value is null or undefined.
- **False positive check:** Is the value guaranteed non-null by surrounding logic?

### T2. Unhandled Promise Rejection
- **Signal:** Floating `async` calls without `await` or `.catch()`.
- **Grep pattern:** `\.then\([^)]+\)(?!\s*\.catch)`, async calls without `await` assignment.
- **Risk:** Rejection is silently swallowed; subsequent code runs in wrong state.

### T3. `any` Propagation
- **Signal:** `any` in function signatures, especially return types.
- **Grep pattern:** `:\s*any\b`, `Promise<any>`, `Array<any>`
- **Risk:** Type errors escape to runtime; one `any` infects downstream inferred types through function composition.

### T5. Prototype Pollution
- **Signal:** Dynamic property assignment on objects from external input.
- **Grep pattern:** `\[.*\]\s*=` where the key originates from user input.
- **Risk:** Attacker sets `__proto__`, `constructor`, or `prototype` properties.

### T6. Missing Async Error Boundary
- **Signal:** `async` route or event handlers without try/catch.
- **Grep pattern:** `async\s+function\s+\w+\s*\([^)]*\)\s*\{(?![\s\S]*try)`
- **Risk:** Uncaught promise rejection crashes the process or silently fails.

### Optional Chain False Safety
- **Signal:** `a?.b.c` — the `?.` stops protecting after `b`. If `b` resolves but `c` is undefined on it, this throws.
- **Grep pattern:** `\?\.[a-zA-Z_]+\.[a-zA-Z_]+` (a `.` after the first property following `?.` without a second `?.`).
- **Risk:** Developers read `?.` as "whole chain is safe" — it isn't past the first dereference.

### Shallow Spread on Nested State
- **Signal:** `{ ...state, items: state.items }` — the inner `items` array is still the same reference. Mutations to it after the spread affect both objects.
- **Risk:** Particularly dangerous in reducers and immutable state patterns.
- **Search:** Spread assignments where the RHS of any field is a reference-typed property of the spread source.

### JSON Clone Footgun
- **Signal:** `JSON.parse(JSON.stringify(x))` as a deep-clone.
- **Grep pattern:** `JSON\.parse\(JSON\.stringify\(`
- **Risk:** Drops `Date` objects (serialized to strings), `undefined` values (dropped), `Map`/`Set`/`BigInt` (thrown or dropped). Use `structuredClone` instead.

### Async TOCTOU
- **Signal:** A value is read, then an `await` occurs, then the original pre-await value is used — but the value may have changed during the await (mutable module singleton, React ref, cache entry).
- **Risk:** Stale reads after async suspension produce subtle race conditions invisible to the type system.
- **Search:** Variables read before an `await` and used again after it, where the variable is a shared reference (not a local copy).
