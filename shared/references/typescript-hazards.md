# TypeScript Hazard Reference

_Loaded by: scanner, adversary, boundary-tracer. Contains workspace discovery and all hazard taxonomies. Do not load for smell analysis or fix work — use `typescript-smells.md` and `typescript-tooling.md` instead._

---

## Workspace Discovery

```bash
# Find package roots
find . -name "package.json" -not -path "*/node_modules/*" -not -path "*/.pnpm/*"

# Identify package manager
ls pnpm-lock.yaml yarn.lock package-lock.json bun.lockb 2>/dev/null

# List workspace packages (pnpm)
pnpm ls -r --depth 0

# Find compiled entry points
# For TS: check tsconfig.json include/exclude
# For bundled: check package.json "main"/"exports"
```

**Dead code rule:** files not reachable from a `main`/`exports` entry point or imported by another live file are dead. Do not report findings in dead code.

---

## Hazard Taxonomies

Ordered by impact — start here when triaging.

### T7. Intent-Capture-to-Execution Discard ← highest impact
- **Signal:** A wide options object or validated config is constructed with user-specified fields (`dryRun`, `registry`, `tag`, `access`), but the function that performs the side effect accepts a narrower interface — those fields are never read at the execution boundary.

```typescript
// ✗ BEFORE — tag and registry captured, silently dropped at the call site
interface PublishOptions {
  packageId: string
  version: string
  registry?: string  // user-specified
  tag?: string       // user-specified
}

// Narrow parameter type — extra fields structurally compatible but never read
function publish(opts: { packageId: string; version: string }) {
  execSync(`npm publish`) // registry, tag never reach the command
}

function run(opts: PublishOptions) {
  publish(opts) // TypeScript allows this; registry and tag are silently gone
}

// ✓ AFTER — execution function accepts the full options type
function publish(opts: PublishOptions) {
  const args = ['npm', 'publish']
  if (opts.registry) args.push('--registry', opts.registry)
  if (opts.tag)      args.push('--tag', opts.tag)
  execSync(args.join(' '))
}
```
- **Search:**
  1. Find options/config types — interfaces or types matching `*Options`, `*Config`, `*Params`, `*Payload`, `*Args`.
  2. Find construction sites where the wide type is built with user-provided values.
  3. Find the execution function — check its parameter type and what it actually reads.
  4. Flag any field present in the constructed object but absent from the execution function's parameter type or body.
- **Risk:** User intent (dry-run, private registry, access level) is silently overridden by a hardcoded default.
- **False positive check:** Is the field explicitly documented as unused at the call site?
- **Verdict signal:** Confirmable when the field is absent from the execution function's parameter type, or present in the type but not read in the body. Dismissible only when the field is explicitly read and forwarded to the subprocess or external call.

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

### T10. Error Suppression & Downgrade ← distinct from T2
- **Signal:** A catch block or rejection handler that swallows the error without signaling failure to the caller. The outer call resolves or returns successfully even though the operation failed.
  - `.catch(() => {})` or `.catch((_) => undefined)` — empty or null-returning handler
  - `try { ... } catch { }` — catch with no body (TS 4.0+ allows omitting the binding entirely)
  - `try { ... } catch (e) { console.log(e) }` — only logging, not re-throwing or returning a failure signal
- **Grep patterns:**
  - `\.catch\(\s*[(_)]\s*=>\s*\{?\s*\}?\s*\)` — empty or trivially-returning catch handler
  - `catch\s*\([^)]*\)\s*\{\s*\}` — empty catch body
  - `catch\s*\([^)]*\)\s*\{\s*console\.\w+` — logging-only catch
- **Risk:** Callers receive a resolved promise or a non-throwing return believing the operation succeeded. The failure is invisible to monitoring, retry logic, and the caller's control flow.
- **False positive check:** Is the no-op explicitly documented as intentional? Is the error logged AND the caller notified via a return value or status field? If neither, it is suppression.
- **Distinguisher from T2 (Unhandled Promise Rejection):** T2 has no catch at all — the rejection propagates unhandled. T10 has a catch that actively hides the error from the caller.
- **Verdict signal:** Confirmable when the catch handler resolves or returns without signaling failure and the caller has no recovery path. Dismissible when the handler logs the error AND signals failure via a return value, status field, or re-throw.
