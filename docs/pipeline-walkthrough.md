# Pipeline Walkthrough

A concrete example tracing one feature request through the full lifecycle pipeline. The scenario: *"requests to our upstream API sometimes hang forever — we need configurable timeouts."*

This walkthrough shows the actual schema shapes at each handoff, why typed contracts matter, and how the ranger audit loop feeds back into the design stage.

---

## The Scenario

A backend team files an issue: requests to an upstream service occasionally stall with no response. The fix is adding a configurable timeout to the HTTP client. Simple enough — but the most common implementation mistake is capturing the timeout in a config struct and never passing it to the actual HTTP call. The hazard has a name: **T7 (Write-Only Fields / Intent-Capture-to-Execution Discard)**.

This walkthrough shows how the pipeline catches that bug before it ships, and how ranger's finding feeds back into a structural spec rather than a one-off patch.

---

## Stage 1 — weaver: Need

The user invokes the `weaver` skill. `intake` (sonnet/medium) converts free text into a structured requirement. `clarifier` asks one targeted question if the success condition is ambiguous. `auditor` (sonnet/medium) checks for testability.

**Output: `requirement@1`**

```json
{
  "id": "req-timeout-001",
  "title": "Configurable HTTP request timeout",
  "stakeholders": ["backend-team"],
  "problem": "Requests to the upstream catalog API hang indefinitely when the service is slow or unreachable, blocking the caller thread with no way to recover.",
  "success_conditions": [
    "Caller can specify a timeout in milliseconds at client construction time",
    "A request that exceeds the timeout returns a structured error, not a hung future",
    "Default behaviour (no timeout set) is unchanged"
  ],
  "out_of_scope": ["Per-request timeout overrides", "Retry logic"],
  "reasoning": "The stakeholder mentioned 'sometimes hang' which implies the service is reachable but slow, not unreachable — making timeout more appropriate than circuit-breaking."
}
```

`reasoning` is the agent's chain-of-thought. It is never forwarded to the next stage.

---

## Stage 2 — vanguard: Research

`vanguard` receives `requirement@1`. `recon` (haiku/low) builds a workspace manifest. `reader` (sonnet/medium) reads relevant source files. `risk-assessor` (sonnet/medium) identifies what could go wrong. `synthesizer` (sonnet/medium) produces the research report.

**Output: `research-report@1`**

```json
{
  "id": "rr-timeout-001",
  "requirement_id": "req-timeout-001",
  "findings": [
    {
      "type": "prior-art",
      "summary": "The HTTP client is built with reqwest::ClientBuilder. Connection timeout and read timeout are configured separately via .connection_verbose() and .timeout(). Both accept std::time::Duration.",
      "evidence_files": ["src/client/builder.rs:42-58"]
    },
    {
      "type": "risk",
      "summary": "The existing ClientConfig struct has 11 fields. New timeout fields added here have historically been read at construction time but not forwarded to the builder — see the proxy_url field added in commit a3f91d2 that was silently ignored for 6 weeks.",
      "evidence_files": ["src/client/config.rs", "src/client/builder.rs:61"]
    },
    {
      "type": "constraint",
      "summary": "Integration tests use a mock server (wiremock). Timeout behaviour can be tested by configuring the mock to delay responses."
    }
  ],
  "recommended_approach": "Add connect_timeout_ms and read_timeout_ms to ClientConfig. Enforce that both reach the ClientBuilder call site — the existing proxy_url precedent is a strong signal to verify field survival explicitly.",
  "reasoning": "The proxy_url finding is the most important signal here. It predicts exactly how timeout fields will fail."
}
```

---

## Stage 3 — scribe: Spec

`drafter` (sonnet/medium) turns the requirement and research report into a testable spec. `verifier` (sonnet/medium) checks every acceptance criterion against the source artifacts — not the codebase. `auditor` (sonnet/medium) hunts vague language. `exit-gate` (opus/high) issues a binding pass or fail.

**Output: `spec@1`**

```json
{
  "id": "spec-timeout-001",
  "requirement_id": "req-timeout-001",
  "title": "Configurable HTTP timeout via ClientConfig",
  "acceptance_criteria": [
    {
      "id": "ac-1",
      "statement": "WHEN ClientConfig is constructed with connect_timeout_ms set, THE SYSTEM SHALL pass a Duration of that value to ClientBuilder.connection_verbose() before the client is built.",
      "test_type": "integration",
      "verifiable": true
    },
    {
      "id": "ac-2",
      "statement": "WHEN a request exceeds connect_timeout_ms, THE SYSTEM SHALL return Err(ClientError::Timeout { kind: TimeoutKind::Connect }).",
      "test_type": "integration",
      "verifiable": true
    },
    {
      "id": "ac-3",
      "statement": "WHEN ClientConfig is constructed without timeout fields, THE SYSTEM SHALL build the client identically to the current behaviour.",
      "test_type": "unit",
      "verifiable": true
    }
  ],
  "non_goals": ["Per-request timeout override", "Automatic retry on timeout"],
  "reasoning": "ac-1 is the structural invariant the research flagged as the most likely failure mode. Making it explicit and testable is the main value this spec adds over the raw requirement."
}
```

Notice `ac-1` directly addresses the T7 risk `vanguard` found: the spec requires the field to *reach the builder call site*, not just exist in the struct. This is the enforcement the research recommended.

---

## Stage 4 — navigator: Plan

`planner` (sonnet/medium) decomposes the spec into sequenced tasks, each with an implementation approach, exact code, and the tests proving its criteria. `estimator` (sonnet/medium) adds sizing. `challenger` (opus/high) pressure-tests the sequence for hidden dependencies.

**Output: `plan@1`** (abridged)

```json
{
  "id": "plan-timeout-001",
  "spec_id": "spec-timeout-001",
  "tasks": [
    {
      "id": "t1",
      "title": "Add timeout fields to ClientConfig",
      "steps": [
        "Add connect_timeout_ms: Option<u64> and read_timeout_ms: Option<u64> to ClientConfig",
        "Update ClientBuilder to map both fields to the reqwest builder before build()",
        "Write test: ClientConfig with connect_timeout_ms=500 builds a client whose underlying reqwest client has connection_timeout == Duration::from_millis(500)"
      ],
      "acceptance_criteria": ["ac-1", "ac-3"],
      "depends_on": []
    },
    {
      "id": "t2",
      "title": "Integration test: timeout returns structured error",
      "steps": [
        "Configure wiremock to delay response by 2000ms",
        "Build client with connect_timeout_ms=100",
        "Assert request returns Err(ClientError::Timeout { kind: TimeoutKind::Connect })"
      ],
      "acceptance_criteria": ["ac-2"],
      "depends_on": ["t1"]
    }
  ],
  "reasoning": "t1 before t2 because the integration test requires the field wiring to exist. challenger flagged that the wiremock delay must exceed connect_timeout_ms by a margin — added 2000ms vs 100ms to avoid flake."
}
```

---

## Stage 5 — smith: Code

`recon` (haiku/low) reads the manifest from `plan@1`. `implementer` (sonnet/medium) executes each task — design the approach, write the implementation, write comprehensive tests proving the task's criteria, confirm the suite passes. `mutator` (sonnet/medium) runs cargo-mutants after each task to verify the tests would actually catch a wrong implementation.

**Mutation gate: mutator catches the T7 bug**

**The mutation gate catches a slot-swap bug the unit test missed.**

- `implementer` inverts the condition — mapping `read_timeout_ms` to the connection slot instead of `connect_timeout_ms`
- The unit test passes because it checks the Duration value, not which builder slot it went into
- The surviving mutant is the specific code path that was never killed — `mutator` returns a precision test targeting exactly that slot assignment

**Output: `mutation-report@1`**

```json
{
  "tool_used": "cargo-mutants",
  "mutants_tested": 14,
  "survived_mutants": [
    {
      "id": "mut-01",
      "file": "src/client/builder.rs",
      "line": 47,
      "mutation_description": "Swap connect_timeout_ms binding with read_timeout_ms binding in builder mapping",
      "why_it_survived": "The test asserts that Duration::from_millis(500) reaches the builder, but does not assert which slot (connection vs read) receives it."
    }
  ],
  "precision_tests": [
    {
      "for_mutant_id": "mut-01",
      "test_name": "WHEN connect_timeout_ms is set THEN connection_timeout slot receives the value AND read_timeout slot is None",
      "test_description": "Assert that the reqwest ClientBuilder receives the timeout in the connection_timeout field, not the read_timeout field, when only connect_timeout_ms is configured.",
      "assertion": "assert_eq!(builder.get_connection_timeout(), Some(Duration::from_millis(500))); assert_eq!(builder.get_timeout(), None);"
    }
  ],
  "verdict": "fail",
  "reasoning": "The surviving mutant reveals that the test cannot distinguish which builder slot receives the timeout. The precision test forces that distinction."
}
```

`mutator` re-invokes `implementer` with the precision test to write and make pass. The implementer fixes the slot assignment and both tests go green. `exit-gate` (opus/high) confirms the mutation gate passed on the second cycle and issues the changeset.

---

## Stage 6 — ranger: Audit (cross-cutting)

**`ranger` runs independently of the main pipeline — typically before a release.**

- `recon` (haiku/low) — builds the workspace manifest: live files, dead files, language detection
- `scanner` (sonnet/medium) — runs hazard taxonomy T1–T10 grep patterns against all live files

For this codebase, the scanner surfaces a T7 candidate: an `AccessConfig` struct whose `private_registry` field is captured from user config but never reaches the publish command.

`boundary-tracer` (sonnet/medium) is dispatched because T7 was found. It traces every field in `AccessConfig` to determine which reach the execution boundary.

**Output: `field-survival-map@1`**

```json
{
  "candidate_id": "cand-access-001",
  "struct_or_type": "AccessConfig",
  "fields": [
    {
      "name": "private_registry",
      "reaches_boundary": false,
      "boundary_type": "none",
      "evidence": "Field read at AccessConfig construction (config.rs:88) but not present in any argument passed to publish() at publisher.rs:134.",
      "last_observed_site": "src/publish/config.rs:88"
    },
    {
      "name": "access_level",
      "reaches_boundary": true,
      "boundary_type": "subprocess",
      "evidence": "Passed as --access flag to npm publish subprocess at publisher.rs:142.",
      "last_observed_site": "src/publish/publisher.rs:142"
    }
  ],
  "reasoning": "private_registry disappears at the function call boundary at publisher.rs:134. The publish() signature accepts access_level but not registry."
}
```

`adversary` (opus/high) confirms the finding is real — user-specified registry is silently overridden by the hardcoded default. `exit-gate` (opus/high) issues the finding report.

**Output: `finding-report@1`** (abridged)

```json
{
  "id": "fr-access-001",
  "verdict": "confirmed",
  "findings": [
    {
      "taxonomy": "T7",
      "file": "src/publish/publisher.rs",
      "line": 134,
      "title": "private_registry field captured but never reaches publish subprocess",
      "severity": "high",
      "failing_scenario": "User sets private_registry: 'https://registry.internal'. publish() receives the AccessConfig but its signature only reads access_level. The subprocess is always invoked against the public registry."
    }
  ]
}
```

---

## The Ranger → Scribe Loop

**`architect` designs a structural fix — not a patch.**

- A patch would add `private_registry` to the existing `publish()` parameter list — it would fix this one field but leave the narrow type intact, ready to silently drop the next field that gets added
- The structural fix widens the parameter type to accept the full `AccessConfig` directly, eliminating the class of bug rather than the instance

`architect` (opus/high) receives `finding-report@1` and applies this fix.

**Output: `spec@1` (structural)**

```json
{
  "id": "spec-access-structural-001",
  "title": "Replace narrow publish() parameter type with full AccessConfig",
  "acceptance_criteria": [
    {
      "id": "ac-1",
      "statement": "WHEN publish() is called, THE SYSTEM SHALL accept AccessConfig directly and read all fields that have corresponding subprocess flags.",
      "test_type": "unit",
      "verifiable": true
    },
    {
      "id": "ac-2",
      "statement": "WHEN AccessConfig gains a new field with a corresponding npm publish flag, THE SYSTEM SHALL require no change to the publish() call site to forward it.",
      "test_type": "compile-time",
      "verifiable": true,
      "invariant_check": "#[deny(unused_variables)] on the AccessConfig destructure in publish()"
    }
  ],
  "reasoning": "ac-2 is the structural invariant: the compiler enforces field survival, so the T7 class of bug cannot recur without a compile error."
}
```

This spec re-enters the pipeline at `navigator` for planning, then `smith` for implementation. The fix is structural — the next field added to `AccessConfig` reaches the subprocess automatically.

---

## What This Demonstrates

| Principle | Where it appeared |
| :--- | :--- |
| **Schema-driven handoffs** | Each stage received a typed document. `synthesizer` couldn't omit the risk finding without schema validation failing. |
| **EARS output contracts** | `spec@1` ac-1 is an EARS statement — it makes the T7 risk machine-checkable, not advisory. |
| **Cognitive mode separation** | `scanner` found T7 candidates without filtering. `boundary-tracer` traced field survival. `adversary` verdicted. Three agents, three modes, none contaminating the others. |
| **Mutation gate** | `mutator` caught the slot-swap bug that unit tests missed. The precision test it generated became part of the permanent test suite. |
| **Ranger → scribe loop** | The finding didn't produce a patch. `architect` designed a structural fix that makes the whole class of bug a compile error. |
