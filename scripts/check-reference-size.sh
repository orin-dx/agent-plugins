#!/usr/bin/env bash
# Enforces constitution.md's Progressive Context Loading rule: a reference
# file covering mixed concerns must be split before publishing. The hard
# 120-line cap catches structural sprawl; the word-count warning catches
# dense one-line prose without turning length into an automatic failure.
# Checks canonical shared/references/ only; plugin shared paths link here.
#
# Usage: scripts/check-reference-size.sh

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/report.sh
source "$script_dir/lib/report.sh"
cd "$script_dir/.."

cap=120
word_review=800
fail=0
count=0
warnings=0

while IFS= read -r -d '' file; do
  count=$((count + 1))
  lines=$(wc -l < "$file" | tr -d ' ')
  if [[ "$lines" -gt "$cap" ]]; then
    fail=$((fail + 1))
    echo "FAIL: $file ($lines lines, cap is $cap) — split by concern"
  fi
  words=$(wc -w < "$file" | tr -d ' ')
  if [[ "$words" -gt "$word_review" ]]; then
    warnings=$((warnings + 1))
    echo "WARN: $file ($words words) — review for mixed concerns, repetition, and removable examples"
  fi
done < <(find shared/references -name '*.md' -print0)

if [[ "$warnings" -gt 0 ]]; then
  echo "WARN: $warnings reference file(s) crossed the review signal; this does not fail validation."
fi

report_check "$fail" "$count" \
  "reference file(s) in shared/references/, all at or under the ${cap}-line cap." \
  "reference file(s) exceed the ${cap}-line cap. Split by concern and re-run."
