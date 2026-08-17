#!/usr/bin/env bash
# shared/hooks/subagent-start.sh
# Reference JIT hook: Injected on subagent initialization across Claude Code / AGY / Codex.
# Scans workspace root manifests and returns language-specific hazard context path.

set -euo pipefail

WORKSPACE_ROOT="${1:-.}"

if [[ -f "${WORKSPACE_ROOT}/Cargo.toml" ]]; then
  echo "shared/references/rust-hazards.md"
elif [[ -f "${WORKSPACE_ROOT}/package.json" ]]; then
  echo "shared/references/typescript-hazards.md"
elif [[ -f "${WORKSPACE_ROOT}/go.mod" ]]; then
  echo "shared/references/go-hazards.md"
elif [[ -f "${WORKSPACE_ROOT}/pyproject.toml" ]] || [[ -f "${WORKSPACE_ROOT}/requirements.txt" ]]; then
  echo "shared/references/python-hazards.md"
else
  echo ""
fi
