#!/usr/bin/env bash
# Shared OK/FAILED summary for scripts/check-*.sh — keeps their output in
# one consistent shape instead of each script reimplementing it.
#
# Usage: report_check <fail_count> <total_count> <ok_suffix> <fail_suffix>
#   report_check "$fail" "$count" \
#     "plugin(s), all versions agree." \
#     "plugin(s) have version drift. Fix and re-run."
# Prints "OK: $count $ok_suffix" and returns 0, or prints
# "FAILED: $fail of $count $fail_suffix" and exits 1.

report_check() {
  local fail="$1" count="$2" ok_suffix="$3" fail_suffix="$4"
  echo ""
  if [[ "$fail" -eq 0 ]]; then
    echo "OK: $count $ok_suffix"
  else
    echo "FAILED: $fail of $count $fail_suffix"
    exit 1
  fi
}
