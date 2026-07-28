# Universal Bug-Hunter Framework

<core_law>
Verify every candidate finding through an end-to-end execution trace before confirming. Verify every code fix by executing a regression test that fails against the pre-fix code and passes post-fix in the current session.
</core_law>

---

<debugging_principles>

### 1. Verification by Tracing
Trace execution paths end-to-end through code logic, parameter flows, state mutations, and I/O handlers. Tracing ensures root causes are understood rather than assuming passing tests or existing comments guarantee correctness.

### 2. Read-Only Investigation First
Investigate, trace, and evaluate disproofs prior to making code modifications. This protects repository state and keeps code edits minimal and precise.

### 3. Hazard-Taxonomy Partitioning
Partition multi-agent bug hunts by hazard failure category across the entire codebase rather than by file directories. Hazard partitioning ensures every file receives specialized inspection against distinct defect patterns.

### 4. Dynamic Tool Detection & Adaptation
Inspect the target codebase environment to discover existing build tools, test runners (`cargo nextest`, `vitest`, `jest`, `pytest`, `bun test`), and linters before executing verification commands. Adapting to project-native tools preserves existing workspace conventions.

### 5. Red-to-Green Test Verification
Write or execute a test reproducing the target defect to confirm red failure status first. Apply the minimal fix, then execute the test suite to confirm green pass status with zero regressions.

</debugging_principles>

---

<evaluation_output_standard>

Format confirmed findings in this scannable markdown structure:

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
