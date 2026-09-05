---
name: scaffold-plugin
description: Create a complete plugin skeleton for a new workflow. Use when the user asks to build or scaffold a plugin; derive structure from the repository constitution and validate the result before handoff.
---

# Scaffold an ecosystem-conformant plugin

Start by turning the requested purpose into explicit skills, cognitive modes, artifact boundaries, and release surface. Do not create a folder full of placeholders that leaves the next author to rediscover the contract.

## Discovery

Read `shared/constitution.md` before choosing the structure. Inspect neighboring plugins for the closest domain pattern, but do not copy a workflow merely because its directory layout looks similar.

Establish:

- Plugin ID, description, user trigger phrases, and independent skill routes.
- Which cognitive modes need agents and the model/effort tier justified by their work.
- Every structured handoff and its existing or new `shared/schemas/<name>@<version>.json` contract.
- Which harness-specific adaptation trees are needed, rather than assuming Claude instructions are portable.

## Build order

1. Define a new shared schema before authoring a producer or consumer that needs it.
2. Read `shared/harness-authoring.md` when the plugin will ship to more than one harness. Create the source plugin manifest, skills, agent prompts, README, changelog, and shared linkage according to the constitution.
3. Register the plugin in the applicable marketplace source.
4. Create the Codex-native tree under `harnesses/codex/plugins/<id>/` with its own manifest and skill workflows when Codex is in scope.
5. Run the repository's structural validators and the Codex plugin validator against the resulting trees.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for comparable-plugin inventory and `author` only for a non-overlapping native-harness draft.

When teams are available, delegate independent bounded work: schema reconnaissance, comparable-plugin inventory, or non-overlapping harness authoring. One owner must reconcile the full plugin route, validate contracts, and reject conflicting assumptions. Without teams, perform those workstreams sequentially.

## Output

Report created paths, routing decisions, schema producers and consumers, validation results, and any user decision still required. Do not register, install, publish, or commit the plugin unless the user explicitly requests each action.
