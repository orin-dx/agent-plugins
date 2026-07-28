# Universal Bug-Hunter Core Laws & Debugging Framework

## The Fundamental Law

> NO FINDING MARKED `CONFIRMED` WITHOUT AN END-TO-END TRACE. NO FIX MARKED DONE WITHOUT A TEST THAT FAILED BEFORE THE FIX AND PASSES AFTER, RUN IN THIS SESSION.

## Core Debugging Principles

1. **Verify by Tracing**: Don't trust comments, docstrings, or passing unit tests. Trace code execution paths end-to-end yourself.
2. **Read-Only Investigation First**: Investigate, construct traces, and attempt to disprove findings before mutating code.
3. **Hazard-Taxonomy Partitioning**: Always partition multi-agent sweeps by **Hazard Category** across the entire workspace, never by folder paths.
4. **Red-to-Green Test Verification**: Write a unit/integration test reproducing the failure first (red pass), apply the minimal robust fix, and verify clean test execution (green pass).
