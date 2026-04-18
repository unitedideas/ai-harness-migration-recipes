#!/bin/bash
set -euo pipefail

# One-click awesome-list submission helper
# Run: bash DISTRIBUTION_EXEC_AWESOME_LISTS.sh
# This script forks, edits, commits, and creates PRs for 3 awesome lists.

REPO_OWNER="unitedideas"
REPO_NAME="ai-harness-migration-recipes"
GH_URL="https://github.com/$REPO_OWNER/$REPO_NAME"

ENTRY="- [AI Harness Migration Recipes]($GH_URL) - Hand-written, tested migrations between Claude Code ↔ Cursor ↔ Codex ↔ Aider. All 12 bidirectional pairs with format diffs, breakage warnings, and step-by-step checklists. CC BY 4.0."

echo "🎯 Awesome List Submission Script"
echo "=================================="
echo ""
echo "This will submit BringYour recipes to 3 awesome lists:"
echo "1. awesome-cli-apps (3.2k★)"
echo "2. awesome-developer-tools (3.1k★)"
echo "3. awesome-ai-tools (2.2k★)"
echo ""
echo "Prerequisites:"
echo "  ✓ GitHub CLI (gh) installed & authenticated"
echo "  ✓ Git configured (git config user.name/email)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Work in a temp directory
WORKDIR=$(mktemp -d)
trap "rm -rf $WORKDIR" EXIT

echo ""
echo "📦 Submission 1: awesome-cli-apps"
echo "=================================="
cd "$WORKDIR"
gh repo fork sindresorhus/awesome-cli-apps --clone --remote=false
cd awesome-cli-apps

# Find where to insert the entry (usually in Tools or Development section)
# For now, add at the end of the file before any final sections
if grep -q "## Related\|## Tools\|## Development"; then
    echo "✓ Found relevant section, adding entry..."
    # Insert after first matching section header
    sed -i '' "/## Related\|## Tools\|## Development/{n;/^$/!{N;};s/$/\n\n$ENTRY/;}" README.md
else
    echo "⚠ Could not auto-detect section. Please manually edit and add to appropriate location."
    echo "Entry to add:"
    echo "$ENTRY"
fi

git add README.md
git commit -m "Add: AI Harness Migration Recipes"
git push origin main

gh pr create \
    --title "Add: AI Harness Migration Recipes" \
    --body "Adds hand-written migrations for AI coding agent config between Claude Code, Cursor, Codex, Aider. All 12 pairs, tested, CC BY 4.0. $GH_URL"
echo "✓ PR created for awesome-cli-apps"

echo ""
echo "📦 Submission 2: awesome-developer-tools"
echo "========================================"
cd "$WORKDIR"
gh repo fork imteekay/awesome-developer-tools --clone --remote=false
cd awesome-developer-tools

# Add entry before final sections
if grep -q "## Related\|## Tools\|## Development"; then
    sed -i '' "/## Related\|## Tools\|## Development/{n;/^$/!{N;};s/$/\n\n$ENTRY/;}" README.md
fi

git add README.md
git commit -m "Add: AI Harness Migration Recipes"
git push origin main

gh pr create \
    --title "Add: AI Harness Migration Recipes (Agent Config Tool)" \
    --body "Adds comprehensive migration guides for developers switching AI coding agents. Covers Claude Code, Cursor, Codex, Aider. All 12 pairs tested. $GH_URL"
echo "✓ PR created for awesome-developer-tools"

echo ""
echo "📦 Submission 3: awesome-ai-tools"
echo "=================================="
cd "$WORKDIR"
# This one is tricky — might be awesome-ai or just awesome
if gh repo view sindresorhus/awesome-ai &>/dev/null; then
    TARGET="sindresorhus/awesome-ai"
else
    TARGET="sindresorhus/awesome"
fi
echo "Targeting: $TARGET"

gh repo fork "$TARGET" --clone --remote=false
cd $(basename "$TARGET")

# Add entry
if grep -q "## AI\|## Development\|## Tools"; then
    sed -i '' "/## AI\|## Development\|## Tools/{n;/^$/!{N;};s/$/\n\n$ENTRY/;}" README.md
fi

git add README.md
git commit -m "Add: AI Harness Migration Recipes"
git push origin main

gh pr create \
    --title "Add: AI Harness Migration Recipes" \
    --body "Adds resource for developers switching between AI coding tools. All major agents covered (Claude Code, Cursor, Codex, Aider). CC BY 4.0. $GH_URL"
echo "✓ PR created for awesome-ai-tools"

echo ""
echo "✅ All 3 PRs created!"
echo ""
echo "Next steps:"
echo "  1. Monitor PR status (typically 3-7 days for maintainer review)"
echo "  2. Once 1-2 merge, update main README with 'Featured in' badges"
echo "  3. Post on HN/Twitter about the mentions for social proof"
echo ""
