# TypeScript Tooling Reference

_Loaded by: mutator, remediator. Contains test runner detection, test commands, and the non-negotiables every fix must satisfy. Do not load for scanning or smell analysis._

---

## Workspace Test Discovery & Execution

Before running tests, check `package.json` scripts and workspace task runners:

```bash
# Check package scripts and task runner configs
jq '.scripts' package.json 2>/dev/null
ls vitest.config.* jest.config.* bun.test.* moonrepo.yml turbo.json 2>/dev/null
```

1. **Package Script / Task Runner First**: Prefer running project-defined scripts (e.g. `pnpm test`, `npm test`, `bun test`, `moon run :test`) or targeted file runs supported by the project runner.
2. **Framework Commands**: If invoking native test frameworks directly, target the specific test file:
   - Vitest: `npx vitest run <file>`
   - Jest: `npx jest <file>`
   - Bun: `bun test <file>`
   - Type check: `npx tsc --noEmit`
   - Mutation testing: `npx stryker run`
3. **Context Efficiency**: Scope test runs to the affected module or file during inner development cycles to keep context windows clean.

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
