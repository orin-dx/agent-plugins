# Universal Bug-Hunter Framework

<core_goal>
Verify candidate findings through end-to-end execution traces before confirming. Verify code fixes by demonstrating that a regression test fails on pre-fix code and passes post-fix in the current session.
</core_goal>

---

<debugging_heuristics>

### 1. End-to-End Execution Tracing
Trace execution paths through code logic, parameter flows, state mutations, and I/O handlers. Tracing ensures root causes are understood rather than assuming comments or passing unit tests guarantee correctness.

### 2. Read-Only Investigation First
Investigate, trace, and evaluate disproofs prior to making code modifications. This keeps code changes minimal, precise, and well-justified.

### 3. Flexible Workspace Partitioning
Choose the optimal auditing partition (by hazard taxonomy, by package boundary, or by architectural layer) that fits the repository scale. Adapt the audit depth to the project structure.

### 4. Dynamic Tool Detection & Adaptation
Inspect the target codebase environment to discover existing build tools, test runners (`cargo nextest`, `vitest`, `jest`, `pytest`, `bun test`), and linters before executing verification commands. Adapt to project-native conventions.

### 5. Red-to-Green Test Verification
Write or execute a test reproducing the target defect to confirm failure status first. Apply the minimal fix, then execute the test suite to confirm green pass status with zero regressions.

</debugging_heuristics>

---

<evaluation_output_standard>

Format confirmed findings in a scannable structure:

```markdown
### [Severity: Critical | High | Medium | Low] <Brief Vulnerability Title>

- **Status**: CONFIRMED (execution path fully traced, file:line cited) | PLAUSIBLE (strong signal, not fully traced)
- **Location**: `path/to/file.ext:L123-L135`
- **Classification**: [Discarded Parameter | Fixpoint Staleness | Spec Drift | Silent Fallback | Boundary Condition | I/O Safety]
- **Root Cause**: Concise explanation of the flaw in current implementation logic.
- **Failing Scenario**: Concrete payload, CLI command, or input state that triggers the defect.
- **Verification Strategy**: Test that fails on current code and passes once fixed.
```

</evaluation_output_standard>
