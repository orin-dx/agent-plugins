#!/usr/bin/env bash
# shared/hooks/pre-command.sh
# Reference JIT hook: Injected on first shell execution across Claude Code / AGY / Codex.
# Emits lightweight modern CLI guidance (~20 tokens).

cat << 'EOF'
[Workspace Tooling Context]: For code/pattern search prefer `rg`, for file discovery prefer `fd`, for line inspection prefer `bat`, for JSON processing prefer `jq`.
EOF
