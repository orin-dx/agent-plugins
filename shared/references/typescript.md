# TypeScript/JavaScript Language Reference for Agent Plugins

Runtime-pullable by agents when scanning or implementing TypeScript or JavaScript code.

## Workspace Discovery

```bash
# Find package roots
find . -name "package.json" -not -path "*/node_modules/*" -not -path "*/.pnpm/*"

# Check package manager
ls pnpm-lock.yaml yarn.lock package-lock.json bun.lockb 2>/dev/null

# List workspace packages (pnpm)
pnpm ls -r --depth 0

# Check what's actually compiled
# For TS: look at tsconfig.json include/exclude
# For bundled: look at entry points in package.json "main"/"exports"
```

## Hazard Taxonomies

### 1. Type Assertion Bypass
- **Signal:** `as unknown as T`, `as any`, `(<T>value)`
- **Search:** `as\s+unknown\s+as|as\s+any\b|<[A-Z]\w*>\w`
- **Risk:** Runtime type mismatch — TypeScript's safety is disabled
- **False positive check:** Is this in a test utility, a known-safe coercion, or a temporary migration shim?

### 2. Unhandled Promise Rejection
- **Signal:** Floating `async` calls without `await` or `.catch()`; `void` promises
- **Search:** `\.then\([^)]+\)(?!\s*\.catch)`, bare `someAsyncFn()` without `await`
- **Risk:** Rejection is silently swallowed; subsequent code runs in wrong state

### 3. `any` Propagation
- **Signal:** `any` in function signatures, especially in return types
- **Search:** `:\s*any\b`, `Promise<any>`, `Array<any>`
- **Risk:** Type errors escape to runtime

### 4. Non-Null Assertion Abuse
- **Signal:** `value!.property` — non-null assertion operator
- **Search:** `[a-zA-Z0-9_)\]]\!\.`
- **Risk:** Crashes at runtime when value is null or undefined
- **False positive check:** Is the value guaranteed non-null by surrounding logic?

### 5. Prototype Pollution
- **Signal:** Dynamic property assignment on objects from external input
- **Search:** `\[.*\]\s*=` where the key comes from user input
- **Risk:** Attacker can set `__proto__`, `constructor`, or `prototype` properties

### 6. Missing Async Error Boundary
- **Signal:** `async` route handlers or event handlers without try/catch
- **Search:** `async\s+function\s+\w+\s*\([^)]*\)\s*\{(?![\s\S]*try)`
- **Risk:** Uncaught promise rejection crashes the process or silently fails

## Architectural Smell Sweeps

### Implicit `undefined` Return
- Functions that return `T | undefined` but don't document the undefined case

### `console.log` in Production Code
- Search: `console\.log\(` in non-test, non-script files

### Magic Numbers and Strings
- Search: numeric literals > 1 not in constants, and string literals that appear 2+ times

### Missing `readonly` on Config Objects
- Mutable config objects are a common source of accidental mutation bugs

## Test Commands

```bash
# Detect test runner
ls vitest.config.* jest.config.* bun.test.* 2>/dev/null

# Vitest
npx vitest run
npx vitest run --reporter=verbose

# Jest
npx jest
npx jest --verbose

# Bun
bun test

# Type check only
npx tsc --noEmit
```

## NAPI/Node.js Boundary Rules (for michi-node)

- Return `Promise<T>` from async NAPI functions, never `T` directly from async
- Catch all errors at the boundary; never throw JS exceptions from sync NAPI exports
- Test with `cargo nextest run` for Rust side, then `node --test` or vitest for JS side

## Non-Negotiables

- No `any` in new code without a comment explaining why
- No unhandled promise rejections
- All exported functions have JSDoc or TSDoc
- No `console.log` in library code (use a logger or omit)
