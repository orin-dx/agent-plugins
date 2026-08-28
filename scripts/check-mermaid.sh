#!/usr/bin/env bash
# Extracts every ```mermaid fenced block from every .md file in the repo and
# renders each through @mermaid-js/mermaid-cli. Reports which files/blocks
# fail to parse — a diagram with a syntax error still displays as valid
# markdown, so `git status`/`jq`-style checks never catch this; only an
# actual render does. Needs Node (npx); no repo dependency required, resolved
# on demand.
#
# Usage: scripts/check-mermaid.sh

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/report.sh
source "$script_dir/lib/report.sh"
cd "$script_dir/.."

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

# CI runners run jobs as root, where Chrome refuses to start its sandbox
# without this flag — passed via a puppeteer config file since mmdc has no
# CLI flag for it directly. Scoped to CI only (GitHub Actions always sets
# CI=true): a custom puppeteer config on a local machine can interfere with
# how mermaid-cli resolves an already-cached Chrome binary, so local runs
# keep using mmdc's own default resolution, which needs no such override.
mmdc_args=()
if [[ "${CI:-}" == "true" ]]; then
  puppeteer_config="$workdir/puppeteer-config.json"
  cat > "$puppeteer_config" <<'JSON'
{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}
JSON
  mmdc_args=(-p "$puppeteer_config")
fi

fail=0
count=0

while IFS= read -r -d '' file; do
  block_index=0
  in_block=0
  block_content=""
  while IFS= read -r line; do
    if [[ "$line" == '```mermaid' ]]; then
      in_block=1
      block_content=""
      continue
    fi
    if [[ $in_block -eq 1 && "$line" == '```' ]]; then
      in_block=0
      count=$((count + 1))
      mmd="$workdir/block_${count}.mmd"
      printf '%s\n' "$block_content" > "$mmd"
      if ! npx --yes @mermaid-js/mermaid-cli -i "$mmd" -o "$workdir/block_${count}.svg" "${mmdc_args[@]+"${mmdc_args[@]}"}" > "$workdir/log_${count}.txt" 2>&1; then
        fail=$((fail + 1))
        echo "FAIL: $file (block $((block_index + 1)))"
        grep -A2 '^Error' "$workdir/log_${count}.txt" | head -3 | sed 's/^/    /'
      fi
      block_index=$((block_index + 1))
      continue
    fi
    if [[ $in_block -eq 1 ]]; then
      block_content="${block_content}${line}"$'\n'
    fi
  done < "$file"
done < <(find . -name '*.md' -not -path './.git/*' -not -path '*/node_modules/*' -not -path '*/target/*' -print0)

report_check "$fail" "$count" \
  "mermaid block(s) across the repo, all render cleanly." \
  "mermaid block(s) did not render. Fix and re-run."
