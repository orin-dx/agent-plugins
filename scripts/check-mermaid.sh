#!/usr/bin/env bash
# Validates every Mermaid fence in repository Markdown through Mermaid's parser.
# Rendering is intentionally separate: syntax validation does not need Chromium.
#
# Usage: scripts/check-mermaid.sh

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$script_dir/.."

exec node "$script_dir/check-mermaid.mjs"
