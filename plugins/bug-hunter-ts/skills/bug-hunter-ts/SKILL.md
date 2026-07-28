---
name: bug-hunter-ts
description: >-
  Trigger this skill when the user requests a code audit, bug hunt, type soundness review, or async verification in a TypeScript or JavaScript codebase. Use when inspecting for as any type assertion bypasses, non-null assertions, unhandled floating promises, missing AbortController fetch timeouts, direct React or global state mutations, SSR hydration mismatches caused by window or Date.now access, loose falsy truthiness traps, phantom monorepo dependencies missing from package.json, or unhandled addEventListener and setInterval memory leaks. Also activate when auditing Node.js, Bun, Deno, React, Next.js, Vite, or pnpm/yarn workspace codebases.
---

# Universal TypeScript Bug-Hunter Skill

<overview>
This skill provides an outcome-driven framework for auditing TypeScript and JavaScript codebases across 6 universal hazard taxonomies. It dynamically adapts to any TS/JS workspace structure (Node.js, Bun, Deno, Next.js, Vite, npm/pnpm/yarn monorepos) and automatically detects available workspace test runners (`vitest`, `jest`, `bun test`, `npm test`).
</overview>

---

<framework_references>
Review shared framework standards prior to executing an audit:
- [General Debugging Laws](../../../shared/debugging-laws.md)
- [Evaluation Report Template](../../../shared/report-template.md)
</framework_references>

---

<hazard_taxonomies>

### 1. Type Assertion & Any-Casting Traps
- **Search Pattern**: `\bas\s+any\b|\bas\s+unknown\b|!\.|\bassertNever\b`
- **Pattern**: Overriding TypeScript's type checker using `val as any` or non-null assertions (`val!`), masking runtime `undefined` / `null` crashes. Missing exhaustive `switch` checks on discriminated unions.

### 2. Async / Promise Concurrency & Floating Promises
- **Search Pattern**: `async\s+function|const\s+\w+\s*=\s*async|\.then\(`
- **Pattern**: Calling `async` functions without `await`, `.catch()`, or `void` (floating promises), causing silent unhandled rejections. Using `Promise.all` instead of `Promise.allSettled` when partial failures should be recovered. Missing `AbortController` timeouts on fetch requests.

### 3. React / Framework Hydration & State Mutation Hazards
- **Search Pattern**: `state\.\w+\.push\(|setState\(|useEffect\(`
- **Pattern**: Mutating state objects directly (e.g. `state.items.push(x)`) instead of immutably updating state. SSR/hydration mismatches caused by `Date.now()`, `Math.random()`, or `window` access during initial render. Stale closures in `useEffect` / `useCallback` missing reactive dependencies.

### 4. Truthiness & Loose Equality Traps
- **Search Pattern**: `if\s*\([^!=]+?\)|==\s*null|Object\.assign\(`
- **Pattern**: Loose falsy checks (`if (val)` instead of `if (val !== undefined && val !== null)`), misinterpreting `0`, `""`, or `false` as missing values. Prototype pollution when merging untrusted objects with `Object.assign`.

### 5. Monorepo Dependency Resolution Hazards
- **Search Pattern**: `import\s+.*?from\s+['"]([^'"]+)['"]`
- **Pattern**: "Phantom dependencies"—importing packages available in root `node_modules` that are missing from the sub-package's `package.json`. Mismatched peer dependencies across workspace packages.

### 6. Memory Leaks & Event Listener Cleanups
- **Search Pattern**: `addEventListener|setInterval|EventEmitter`
- **Pattern**: Registering global listeners or intervals inside components/effects without returning a cleanup function (`removeEventListener` / `clearInterval`), leading to memory leaks.

</hazard_taxonomies>

---

<execution_guidance>
Adapt execution to workspace scale:
- **Direct Execution**: For quick checks or targeted file audits, inspect and verify findings directly.
- **Parallel Subagent Delegation**: For large monorepo sweeps, optionally delegate work to specialized subagents (`bug-hunter-scanner-ts`, `bug-hunter-adversary-ts`, `bug-hunter-remediator-ts`).
</execution_guidance>
