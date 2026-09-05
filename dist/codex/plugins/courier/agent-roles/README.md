# Codex Agent Roles

These are portable role instructions for Codex multi-agent work. They are resources, not a Codex TOML configuration surface: a skill reads the applicable card before it asks the host to delegate a bounded task.

The primary agent owns task decomposition, shared interfaces, final artifact assembly, verification, and all external writes. A role card defines a cognitive boundary, not a substitute owner.

| Role | Use for | Recommended tier |
| :--- | :--- | :--- |
| `recon` | File, API, and evidence inventory | `gpt-5.6-luna` / low |
| `tracer` | Control-flow, data-flow, and boundary tracing | `gpt-5.6-terra` / medium |
| `research` | Bounded internal or external evidence collection | `gpt-5.6-terra` / medium |
| `author` | A defined draft with fixed inputs and output schema | `gpt-5.6-terra` / high |
| `implementer` | An isolated implementation batch with fixed interfaces | `gpt-5.6-terra` / high |
| `adversary` | Independent refutation or counterexample search | `gpt-5.6-terra` / high |
| `reviewer` | Evidence-led code or artifact review | `gpt-5.6-terra` / high |
| `judge` | Binding synthesis or exit decision | `gpt-5.6-sol` / high |

Use the recommended tier only when the host lets the primary agent choose it. If it does not, preserve the role boundary and run with the host default. If multi-agent work is unavailable, perform the same bounded passes sequentially in the primary agent.

## Delegation packet

Before requesting a teammate, provide this packet after reading the selected role card. The packet is the task boundary; the role card supplies the cognitive mode.

| Field | Required content |
| :--- | :--- |
| Role | One card from this directory and why that cognitive mode fits. |
| Objective | One bounded question or implementation batch, not a pipeline stage. |
| Inputs | Exact artifact IDs, criteria, paths, and relevant evidence. |
| Owned paths | Files the teammate may edit, or `read-only`. |
| Exclusions | Decisions, paths, interfaces, and external actions outside its authority. |
| Output | Required artifact or report shape, including schema when one exists. |
| Evidence | Commands, source locations, test results, or citations required to support the result. |
| Completion | The condition that returns control to the primary agent. |

Keep synthesis, cross-batch interface decisions, final verification, commits, publication, and other external writes with the primary agent. Do not delegate coupled work merely because agent teams are available. If the packet cannot make ownership and completion unambiguous, complete the work sequentially instead.
