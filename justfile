# Wisp Plugins validation and formatting.
# `just` and `pnpm` must be installed; `just install` fetches pinned tooling.

# Run every check (same set CI runs)
# fmt-check is deliberately excluded: the repo isn't formatted yet. Run
# `just fmt` once, review the diff, commit it, then add fmt-check here.
check: manifests test versions skills-doc reference-size marketplace-check mermaid

# Install pinned tooling dependencies
install:
    pnpm install --frozen-lockfile

# Validate every JSON manifest and schema parses
manifests:
    jq . marketplace.json > /dev/null
    jq . .claude-plugin/marketplace.json > /dev/null
    jq . plugins/*/plugin.json > /dev/null
    jq . shared/schemas/*.json > /dev/null
    jq . harnesses/codex/catalog.json > /dev/null
    jq . .agents/plugins/marketplace.json > /dev/null

# Run the Python test suite
test:
    python3 -m unittest discover -s tests

# Check plugin.json/README/CHANGELOG/marketplace.json versions agree
versions:
    ./scripts/check-versions.sh

# Check every documented skill has a skills/ directory
skills-doc:
    ./scripts/check-skills-doc.sh

# Enforce the reference file line cap
reference-size:
    ./scripts/check-reference-size.sh

# Confirm the generated Codex marketplace matches its authored sources
marketplace-check:
    python3 tools/build-codex-marketplace.py --check

# Rebuild the generated Codex marketplace from authored sources
marketplace-sync:
    python3 tools/build-codex-marketplace.py

# Parse every Mermaid diagram in the repo
mermaid:
    node scripts/check-mermaid.mjs

# Check formatting without writing
fmt-check:
    pnpm exec oxfmt --check .

# Format the repo in place
fmt:
    pnpm exec oxfmt --write .
