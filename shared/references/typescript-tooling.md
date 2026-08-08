# TypeScript Tooling Reference

_Loaded by: mutator, remediator. Contains test runner detection, test commands, and the non-negotiables every fix must satisfy. Do not load for scanning or smell analysis._

---

## Test Runner Detection

```bash
# Identify what's available
ls vitest.config.* jest.config.* bun.test.* 2>/dev/null
cat package.json | jq '.scripts'
```

---

## Test Commands

```bash
# Vitest
npx vitest run
npx vitest run --reporter=verbose

# Jest
npx jest
npx jest --verbose

# Bun
bun test

# Type-check only (no test execution)
npx tsc --noEmit

# Mutation testing (mutator agent)
npx stryker run
```

---

## Non-Negotiables

Every fix must satisfy these before the green pass is claimed:

- No `any` in new code without an inline comment explaining why.
- No unhandled promise rejections — every `async` call is either `await`ed, `.catch()`ed, or explicitly `void`-ed with a comment.
- All exported functions have JSDoc or TSDoc.
- No `console.log` in library code — use a structured logger or remove.
- Config and options interfaces must be `readonly`.
- No `JSON.parse(JSON.stringify(x))` — use `structuredClone`.
- Discriminated union switches must have an `assertNever` default.
