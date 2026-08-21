# Security Policy

## Reporting a Vulnerability

Email **gabe@techworx.dev** — don't open a public issue for anything that could be exploited before a fix ships.

Include:
- What plugin, agent, or schema is affected
- The concrete failure scenario — what an attacker could do, and how
- Steps to reproduce, if you have them

Expect an acknowledgment within 5 business days. We'll keep you posted as a fix moves through triage, and credit you in the release notes unless you'd rather stay anonymous.

## Scope

This repo ships agent prompts, JSON schemas, and orchestration logic — not a running service. The relevant threat model is different from a typical web app:

- **Prompt injection via scanned workspace content** — an agent reading a target codebase's `CLAUDE.md`, comments, or docstrings treating that content as instructions instead of data. `shared/constitution.md`'s Trust Boundaries section is the governing rule here; a bypass of it is a real finding.
- **Unsafe tool invocation** — an agent prompt that could be steered into running a destructive shell command, exfiltrating data, or writing outside its intended scope.
- **Schema validation bypass** — a way to get invalid or malicious data through a `shared/schemas/*.json` contract and into a downstream agent that trusts it.
- **Supply chain** — anything in `marketplace.json`, `.claude-plugin/marketplace.json`, or a `plugin.json`'s `source`/install path that could resolve to unintended code.

Out of scope: issues in Claude Code, AGY, or Cursor themselves — report those to the respective platform, not here.

## Supported Versions

Security fixes land on `main` and the current major version of the marketplace (see `marketplace.json`'s top-level `version` and the root `CHANGELOG.md`). Older tagged releases are not backported.
