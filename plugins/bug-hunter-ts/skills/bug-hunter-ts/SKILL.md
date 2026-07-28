---
name: bug-hunter-ts
description: >-
  TypeScript/JavaScript bug hunting framework. Finds type assertion traps, unhandled floating promises, SSR hydration mismatches, truthiness traps, and memory leaks across any TS/JS codebase.
---

# Universal TypeScript Bug-Hunter Skill

## Core Laws & Verification Framework
Before auditing, review the shared debugging laws and evaluation standards:
- [General Debugging Laws](../../../shared/debugging-laws.md)
- [Evaluation Report Template](../../../shared/report-template.md)

---

## The 6 Universal TypeScript Hazard Taxonomies & Regex Heuristics

When auditing any TS/JS repository, scan all code paths using ripgrep against these 6 hazard categories:

### 1. Type Assertion & Any-Casting Traps
- **Search Pattern**: `\bas\s+any\b|\bas\s+unknown\b|!\.|\bassertNever\b`
- Overriding TypeScript's type checker using `val as any` or non-null assertions (`val!`), masking runtime `undefined` / `null` crashes. Missing exhaustive `switch` checks on discriminated unions.

### 2. Async / Promise Concurrency & Floating Promises
- **Search Pattern**: `async\s+function|const\s+\w+\s*=\s*async|\.then\(`
- Calling `async` functions without `await`, `.catch()`, or `void` (floating promises), causing silent unhandled rejections. Using `Promise.all` instead of `Promise.allSettled` when partial failures should be recovered. Missing `AbortController` timeouts on fetch requests.

### 3. React / Framework Hydration & State Mutation Hazards
- **Search Pattern**: `state\.\w+\.push\(|setState\(|useEffect\(`
- Mutating state objects directly (e.g. `state.items.push(x)`) instead of immutably updating state. SSR/hydration mismatches caused by `Date.now()`, `Math.random()`, or `window` access during initial render. Stale closures in `useEffect` / `useCallback` missing reactive dependencies.

### 4. Truthiness & Loose Equality Traps
- **Search Pattern**: `if\s*\([^!=]+?\)|==\s*null|Object\.assign\(`
- Loose falsy checks (`if (val)` instead of `if (val !== undefined && val !== null)`), misinterpreting `0`, `""`, or `false` as missing values. Prototype pollution when merging untrusted objects with `Object.assign`.

### 5. Monorepo Dependency Resolution Hazards
- **Search Pattern**: `import\s+.*?from\s+['"]([^'"]+)['"]`
- "Phantom dependencies"—importing packages available in root `node_modules` that are missing from the sub-package's `package.json`. Mismatched peer dependencies across workspace packages.

### 6. Memory Leaks & Event Listener Cleanups
- **Search Pattern**: `addEventListener|setInterval|EventEmitter`
- Registering global listeners or intervals inside components/effects without returning a cleanup function (`removeEventListener` / `clearInterval`), leading to memory leaks.

---

## Subagent Dispatch Matrix

| Agent Role | Target Taxonomies | Objective |
| :--- | :--- | :--- |
| **`bug-hunter-scanner-ts`** | Taxonomies 1 & 4 | Audit for `as any`, non-null assertions, and falsy truthiness traps. |
| **`bug-hunter-adversary-ts`** | Taxonomies 2 & 3 | Audit floating promises, state mutations, and SSR hydration mismatches. |
| **`bug-hunter-remediator-ts`** | Taxonomies 5 & 6 | Audit phantom monorepo deps, event listener memory leaks, and run test suite (`npm test` / `vitest`). |
