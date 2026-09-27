# Decision Records

Index of accepted architectural decisions. Read the record before changing what its guardrail names. Do not rewrite an accepted record's context, decision, or options. Change its status and links, or supersede it with a new record and leave the old one marked. Status is Accepted, Partially superseded, or Superseded, and a test checks each row against its record. Guidance for writing a record is in `shared/references/architecture/decision-records.md`.

| ADR | Status | Decision | Relation | Guardrail |
| :--- | :--- | :--- | :--- | :--- |
| [001](./001-four-part-agent-structure.md) | Accepted | Agent bodies use fixed sections | Extended by 006 | Do not add a `<role>` body section or a `success_criteria` checklist without a new ADR |
| [002](./002-ears-output-only.md) | Accepted | EARS notation only in output contracts | None | Do not use EARS in `<backstory>`, `<goal>`, or `<judgment>` without a new ADR |
| [003](./003-cognitive-mode-separation.md) | Accepted | Agents are split by cognitive mode | None | Do not combine enumeration and judgment in one agent without a new ADR |
| [004](./004-schema-driven-handoffs.md) | Accepted | Handoffs use immutable versioned JSON schemas | None | Do not edit a published schema in place; add `<name>@<n+1>.json` |
| [005](./005-axiom-artifact-agnostic-gate.md) | Accepted | Verification gates are artifact-agnostic | None | Do not make the gate depend on one artifact type without a new ADR |
| [006](./006-constitution-section-five-part-structure.md) | Accepted | Every agent has a byte-identical `<constitution>` section | Extends 001 | Do not put agent-specific rules in `<constitution>` without a new ADR |
| [007](./007-wisp-persona-naming.md) | Partially superseded | Plugin ids use persona names; its umbrella-brand clause is superseded by 010 | Umbrella-brand clause superseded by 010 | Do not rename a plugin id or skill without a new ADR |
| [008](./008-drop-test-first-ordering.md) | Accepted | Feature implementation does not require a failing test first | None | Do not restore mandatory test-first ordering for feature work without a new ADR |
| [009](./009-implementer-shape-latitude.md) | Accepted | Plan code is a baseline; tasks use compilation boundaries | None | Do not size tasks by clock time without a new ADR |
| [010](./010-wisp-plugins-brand.md) | Accepted | The ecosystem brand is Wisp Plugins | Supersedes the umbrella-brand clause of 007 | Do not use "Wisp" alone for the ecosystem without a new ADR |
