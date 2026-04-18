#!/usr/bin/env bash
set -euo pipefail

# Automated awesome-list submission script
# Submits AI Harness Migration Recipes to multiple awesome lists in one go
# Usage: ./tools/submit-awesome-lists.sh [--dry-run]

DRY_RUN=${1:-}
ENTRY='- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Hand-written, tested migrations between Claude Code ↔ Cursor ↔ Codex ↔ Aider. All 12 bidirectional pairs with format diffs, breakage warnings, and step-by-step checklists. CC BY 4.0. [Automation via BringYour](https://bringyour.ai).'

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [[ "$DRY_RUN" == "--dry-run" ]]; then
  log_info "DRY RUN MODE — no actual changes will be made"
fi

submit_to_list() {
  local list_key=$1
  local repo_path=$2
  local readme_file=$3
  local section=$4

  log_info "Processing $list_key..."

  # Check if fork already exists
  if gh repo view "$repo_path" &>/dev/null 2>&1; then
    log_warn "Fork already exists at $repo_path"
  else
    log_info "Forking and cloning $repo_path..."
    if [[ "$DRY_RUN" != "--dry-run" ]]; then
      gh repo fork "$repo_path" --clone
    else
      log_info "[DRY RUN] Would fork: gh repo fork $repo_path --clone"
      return 0
    fi
  fi

  cd "$list_key"

  # Check if entry already exists
  if grep -q "AI Harness Migration Recipes" "$readme_file" 2>/dev/null; then
    log_warn "Entry already exists in $list_key"
    cd ..
    return 0
  fi

  log_info "Editing $readme_file to add entry under [$section] section..."

  if [[ "$DRY_RUN" != "--dry-run" ]]; then
    # Find the section and add entry before first list item in that section
    if [[ "$OSTYPE" == "darwin"* ]]; then
      # macOS sed
      sed -i '' "/^### $section$/,/^###/{ /^- /i\\
$ENTRY
}" "$readme_file"
    else
      # Linux sed
      sed -i "/^### $section$/,/^###/{ /^- /i\\
$ENTRY
}" "$readme_file"
    fi

    log_info "Committing changes..."
    git add "$readme_file"
    git commit -m "Add: AI Harness Migration Recipes"

    log_info "Pushing branch..."
    git push origin main

    log_info "Creating PR..."
    gh pr create \
      --title "Add: AI Harness Migration Recipes" \
      --body "Adds hand-written, tested migrations for AI coding agents. All 12 pairs between Claude Code, Cursor, Codex, Aider. CC BY 4.0. https://github.com/unitedideas/ai-harness-migration-recipes"

    log_info "✓ PR created for $list_key"
  else
    log_info "[DRY RUN] Would edit $readme_file, commit, push, and create PR"
  fi

  cd ..
}

# Main execution
log_info "Awesome-list submission automation"
log_info "Starting submission process..."

# Process each list (name, repo, readme, section)
submit_to_list "awesome-cli-apps" "sindresorhus/awesome-cli-apps" "README.md" "Tools"
submit_to_list "awesome-developer-tools" "imteekay/awesome-developer-tools" "README.md" "Development"
submit_to_list "awesome-ai" "sindresorhus/awesome" "README.md" "Development"

log_info "Submission process complete!"
log_info "Next steps:"
log_info "  1. Check PR status: gh pr list"
log_info "  2. Once merged, update README.md with 'Featured in' badges"
log_info "  3. Post announcement to HN/Twitter"
