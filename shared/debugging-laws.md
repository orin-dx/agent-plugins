# Universal Bug-Hunter Framework

<core_goal>
Verify candidate findings through the boundary implicated by the defect. Verify fixes with safe evidence that distinguishes the faulty behavior from the correction, such as a controlled mutation, deliberate fault, isolated prior revision, or equivalent check.
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
Inspect project configuration and CI to discover applicable build, test, analysis, mutation, property, and fuzz capabilities. Prefer project-native commands and record relevant environment gaps.

### 5. Discriminating Verification
Prove that the verification detects the relevant wrong behavior and accepts the correction. Do not require a fixed test-writing order or mutate shared workspace state merely to manufacture a red run.

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
- **Verification Strategy**: Evidence that distinguishes the faulty behavior from the correction without risking shared workspace state.
```

</evaluation_output_standard>
