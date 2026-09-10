#!/usr/bin/env bash
# shared/hooks/subagent-start.sh
# Reference JIT hook: Injected on subagent initialization across Claude Code / AGY / Codex.
# Scans workspace root manifests and returns language-specific hazard context path.

set -euo pipefail

WORKSPACE_ROOT="${1:-.}"

if [[ -f "${WORKSPACE_ROOT}/Cargo.toml" ]]; then
  echo "shared/references/hazards/rust.md"
elif [[ -f "${WORKSPACE_ROOT}/package.json" ]]; then
  echo "shared/references/hazards/typescript.md"
elif [[ -f "${WORKSPACE_ROOT}/go.mod" ]]; then
  echo "shared/references/hazards/go.md"
elif [[ -f "${WORKSPACE_ROOT}/pyproject.toml" ]] || [[ -f "${WORKSPACE_ROOT}/requirements.txt" ]]; then
  echo "shared/references/hazards/python.md"
else
  echo ""
fi
