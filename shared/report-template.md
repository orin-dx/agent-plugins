# Evaluation Report Standard

Report each confirmed finding in this standard format:

```markdown
### [Severity: Critical | High | Medium | Low] <Brief Vulnerability Title>

- **Status**: CONFIRMED (execution path fully traced, file:line cited) | PLAUSIBLE (strong signal, not fully traced)
- **Location**: `path/to/file.ext:L123-L135`
- **Classification**: [Discarded Parameter | Fixpoint Staleness | Spec Drift | Silent Fallback | Boundary Condition | I/O & Memory Safety]
- **Root Cause**: Concise explanation of the flaw in the current implementation logic.
- **Failing Scenario**: Concrete payload, CLI command, or input state that triggers the defect.
- **Verification Strategy**: A test that fails on current code and passes once fixed.
```

### Verification Checklist
Before marking a finding `CONFIRMED`:
- [ ] Traced exact execution path end-to-end.
- [ ] Created a concrete failing scenario.
- [ ] Verified finding is not a duplicate.

Before marking a fix `DONE`:
- [ ] Test failed pre-fix (red).
- [ ] Test passes post-fix (green).
