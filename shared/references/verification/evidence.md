# Verification Evidence

Choose evidence from the changed risk and the workspace's available capabilities. Do not run every method by default.

## Method selection

- Examples: bounded behavior with clear representative cases.
- Property or fuzz testing: parsers, combinatorial inputs, state transitions, graph logic, or round trips. Name the generated domain and a meaningful oracle or invariant; a no-panic check alone rarely proves behavior.
- Mutation or deliberate fault: show that tests distinguish an important wrong implementation from the intended one.
- Boundary testing: exercise the contract implicated by the change. Name any mocked segment and why the remaining boundary is sufficient.
- Environment testing: exercise only environment assumptions that can change the outcome, such as runtime version, PATH, working directory, build tags, packaging, or CI configuration.

Prefer project-configured commands and installed tools. A missing optional tool is a coverage gap, not permission to install it or fabricate a result.

## Evidence quality

Record the claim, actual command or inspection, observed result, and remaining gap. Generated tests also record the generator and oracle. External state records an immutable identity and observation time when it affects the decision.

A test discriminates behavior when a controlled mutation, deliberate fault, isolated prior revision, or equivalent evidence makes it fail for the relevant wrong behavior and pass for the corrected behavior. Do not modify shared worktrees or user state merely to manufacture a red run.

Before completion, every started verification task has a terminal result that was read, or is explicitly excluded from the verified scope.
