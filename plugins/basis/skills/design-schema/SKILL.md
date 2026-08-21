---
name: design-schema
description: >-
  Trigger when the user wants to design a new inter-agent artifact schema: "design a schema for X", "add a new schema to shared/schemas", "what should this handoff look like?". Given a description of what the artifact represents, who produces it, and who consumes it, produces a JSON Schema (draft 2020-12) following ecosystem conventions — $id as name@version, additionalProperties false, a reasoning scratchpad field, all fields documented — and checks for conflicts with existing schemas.
version: 2.0.0
---

# Basis — Design Schema

<overview>
The schema that ships first sets the pattern every consumer inherits — required vs. optional has to be a deliberate choice. Delegates to `schema-designer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **schema-designer** | sonnet / medium | A new inter-agent artifact needs a JSON Schema designed and checked against existing schemas for conflicts. |
</dispatch>

<references>
`shared/schemas/` (existing schemas, checked for conflicts before proposing a new one)
</references>

<io>
**Consumes**: artifact description, producer, consumer(s)
**Produces**: JSON Schema object plus a recommended filename (`shared/schemas/<name>@<version>.json`).
</io>
