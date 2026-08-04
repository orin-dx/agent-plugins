# MCP Protocol Reference

Model Context Protocol (MCP) is the cross-platform protocol for exposing tools and resources to LLMs. Both Claude Code and Google ADK/AGY support MCP natively.

## Core Concepts

**Tool:** A function the LLM can call. Has a name, description, and JSON Schema input spec.
**Resource:** A readable artifact (file, URL, database record) the LLM can fetch.
**Prompt:** A template the LLM can use to pre-fill a message.

## Server Lifecycle

```
1. initialize    → server declares protocol version + capabilities
2. initialized   → client acknowledges
3. tools/list    → client fetches available tools
4. tools/call    → client invokes a tool by name with JSON arguments
5. (resources/list, prompts/list as needed)
```

## Tool Definition

```json
{
  "name": "axiom_verify",
  "description": "Verify an artifact against its criteria. Returns a verdict@1 schema.",
  "inputSchema": {
    "type": "object",
    "required": ["artifact_type", "artifact_path", "criteria"],
    "properties": {
      "artifact_type": { "type": "string" },
      "artifact_path": { "type": "string" },
      "criteria": { "type": "array", "items": { "type": "string" } }
    }
  }
}
```

## CallToolResult Shape

```json
{
  "content": [
    {
      "type": "text",
      "text": "Rendered output for the assistant",
      "annotations": { "audience": ["assistant"] }
    }
  ],
  "isError": false,
  "structuredContent": { "verdict": "pass", "confidence": "high", "..." }
}
```

`structuredContent` is the typed machine-readable result. `content[0].text` is the human-readable render. Never duplicate content between them — they serve different consumers.

## A2A AgentCard

For cross-service discovery, plugins publish an AgentCard at `/.well-known/agent.json`:

```json
{
  "name": "axiom",
  "description": "Cross-cutting verification gate for the Orin DX plugin ecosystem",
  "url": "https://plugins.orin.dev/axiom",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "verify-spec",
      "name": "Verify Spec",
      "description": "Verify a spec@1 artifact against its acceptance criteria"
    }
  ]
}
```

## Trust Boundaries

Plugin output always goes in `tool_result` blocks, JSON-encoded. Never elevate plugin output into the system prompt context without sanitization. If a tool's output could contain injected instructions, JSON-encode it before including in messages.

## Claude Code vs ADK

| Concern | Claude Code | ADK |
|---|---|---|
| MCP server config | `~/.claude/mcp.json` or `.mcp.json` | `McpToolset(server_params=...)` |
| Tool invocation | Native MCP client | `McpToolset.from_server()` |
| Subagent invocation | `--subagent` flag or Agent tool | `Agent(sub_agents=[...])` |
| Cross-platform | MCP tools work on both | MCP tools work on both |
