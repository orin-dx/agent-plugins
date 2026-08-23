#!/usr/bin/env bash
# Enforces constitution.md's Progressive Context Loading rule: a reference
# file covering mixed concerns must be split by concern before publishing,
# capped at 120 lines. Reference files are loaded in full by every agent
# that <load_first>s them — an oversized file is a fixed per-invocation
# tax paid by every one of those agents, not a one-time cost. Checks the
# canonical shared/references/ directory only; plugins/*/shared/ is a
# symlink to it, so scanning both would just double-report the same files.
#
# Usage: scripts/check-reference-size.sh

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/report.sh
source "$script_dir/lib/report.sh"
cd "$script_dir/.."

cap=120
fail=0
count=0

while IFS= read -r -d '' file; do
  count=$((count + 1))
  lines=$(wc -l < "$file" | tr -d ' ')
  if [[ "$lines" -gt "$cap" ]]; then
    fail=$((fail + 1))
    echo "FAIL: $file ($lines lines, cap is $cap) — split by concern"
  fi
done < <(find shared/references -name '*.md' -print0)

report_check "$fail" "$count" \
  "reference file(s) in shared/references/, all at or under the ${cap}-line cap." \
  "reference file(s) exceed the ${cap}-line cap. Split by concern and re-run."
