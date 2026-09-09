# TypeScript Smell Reference

_Loaded by: architect. Contains architectural smell sweeps for TypeScript codebases. Do not load for scanning or fix work._

---

## Code-Level Smell Sweeps

Quick checks any agent can run during a pass.

### `console.log` in Production Code
- **Search:** `console\.log\(` in non-test, non-script files.
- Use a structured logger or omit; `console.log` in library code produces noise and masks real signal.

### Magic Numbers and Strings
- Numeric literals greater than 1 not extracted to named constants.
- String literals appearing two or more times without a shared constant.

### Implicit `undefined` Return
- Functions typed as `T | undefined` that don't document the `undefined` case in JSDoc/TSDoc.

### Missing `readonly` on Config Objects
- Config objects passed across module boundaries without `readonly` are a common source of accidental mutation.
- **Search:** exported `interface` or `type` definitions for options/config shapes — check for absent `readonly` modifiers.

---

## Architectural Pattern Smells

Higher-level patterns indicating systemic design problems. The architect clusters these across confirmed findings.

### 1. Structural Subtyping Leak
- An options object is constructed with user-provided fields (`dryRun`, `registry`, `tag`) but the execution function's parameter type is narrower — TypeScript's structural compatibility silently accepts the narrower type, and the extra fields are dropped.
- This is the TS analogue of Rust's Write-Only Fields (Taxonomy 7).
- **Resolution:** Define a single authoritative `ExecutionOptions` type that is both the construction type and the parameter type. Derive the narrower display/logging type from it with `Omit<>`, not the other way around.

### 2. `any` Propagation Chain
- One `any` at a utility function's return type infects all downstream inferred types through function composition — callers lose type safety without a single explicit assertion.
- **Resolution:** Centralize boundary coercions (API payloads, JSON parse results, third-party SDK returns) in typed adapter functions. No `any` escapes the adapter layer.

### 3. Discriminated Union Without Exhaustiveness Enforcement
- A union type grows (new variant added) and existing switch statements silently hit the `default` branch instead of failing at compile time. No `assertNever` guard means new variants are silently mishandled.
- **Resolution:** Add a shared `assertNever` utility and enforce its use in every discriminated union switch. ESLint rule: `@typescript-eslint/switch-exhaustiveness-check`.

### 4. Inconsistent `readonly` Enforcement
- Config and options types are `readonly` in some paths and mutable in others. The mutable path allows accidental mutation that propagates silently.
- **Resolution:** Define all config/options interfaces as fully `readonly` at declaration. Use `Readonly<T>` at function boundaries that should not mutate.

### 5. Multi-Writer File Race
- Multiple async paths write to the same file or config entry without coordination — a module's `writeFile`/`fs.promises.writeFile` in one async chain and another in a concurrent handler targeting the same path.
- **Sub-pattern — shared-state writer**: An in-memory store (module singleton, React context, Zustand slice) is mutated by two concurrent async operations without atomic swap or lock. Both read the current state before either write lands, then both overwrite it with stale base state.
- **Search:**
  1. `grep -rn 'writeFile\|appendFile\|createWriteStream'` — identify write targets.
  2. For each target path that appears in more than one function, trace whether any callers can run concurrently (event listeners, parallel `Promise.all`, concurrent request handlers).
  3. `grep -rn '\bset\b.*=\b' ` for singleton mutation — check if the same assignment can be reached from two concurrent paths.
- **Resolution:** Serialize writes through a queue or mutex (e.g. `async-mutex`); use `fs.rename` for atomic file replacement; replace shared mutable singleton with a proper state machine or immutable update.

### 6. Async State Race (TOCTOU Pattern)
- Shared mutable state (module singleton, React ref, cache entry) is read before an `await`, then used after the `await` without re-reading. Concurrent calls can mutate the shared state during the suspension.
- **Resolution:** Snapshot shared state into a local `const` before the first `await`. Never rely on a shared reference's value being stable across an async boundary.

### 6. Test Fixture Drift
- Hardcoded JSON/object literals in test files whose property names no longer match the production type's fields. After any schema change (new field, rename, type change), test fixtures silently pass because TypeScript only checks structural compatibility of the literal against the type at assignment — removed required fields are caught, but extra fields and renamed fields may not be.
- **Search:** Object literals in test files — cross-reference against current type/interface definition, particularly for `zod` schemas where the runtime shape is the authority.

### 7. Invisible Invariants
- Architectural constraints stated in project constitution files (`CLAUDE.md`, `AGENTS.md`, design docs) — module boundary rules, package dependency restrictions, naming conventions, type constraint requirements — that have no corresponding test, ESLint rule, `dependency-cruiser` config, or CI assertion.
- The constraint is known and documented. It is simply not machine-enforced, so it breaks silently as the codebase evolves.
- **Sweep:** Read the project's constitution file if present. For each stated architectural invariant, check for an enforcing mechanism: a test whose name is the invariant statement, an ESLint/TypeScript strict config rule, a `dependency-cruiser` constraint, or a CI step. Report any invariant with no enforcer.
- **Resolution:** Write the enforcement first — a test that fails when the invariant is violated — then verify it currently passes. The `it()` description should be the invariant statement verbatim.
