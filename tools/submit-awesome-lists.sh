#!/usr/bin/env bash
set -euo pipefail

# Automated awesome-list submission script
# Usage: ./tools/submit-awesome-lists.sh [--dry-run]

DRY_RUN=${1:-}
ENTRY='- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Hand-written, tested migrations between Claude Code ↔ Cursor ↔ Codex ↔ Aider. All 12 bidirectional pairs with format diffs, breakage warnings, and step-by-step checklists. CC BY 4.0. [Automation via BringYour](https://bringyour.ai).'

log_info() { echo -e "\033[0;32m[INFO]\033[0m $1"; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }

[[ "$DRY_RUN" == "--dry-run" ]] && log_info "DRY RUN MODE — no actual changes will be made"

submit_to_list() {
  local list_name=$1
  local repo_path=$2
  local repo_dir=$3
  local readme_file=$4
  local section=$5

  log_info "Processing $list_name..."

  if [[ "$DRY_RUN" != "--dry-run" ]]; then
    if ! gh repo view "$repo_path" &>/dev/null 2>&1; then
      log_info "Forking and cloning..."
      gh repo fork "$repo_path" --clone
    fi

    cd "$repo_dir"

    if ! grep -q "AI Harness Migration Recipes" "$readme_file" 2>/dev/null; then
      log_info "Adding entry to $readme_file..."
      if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "/^### $section$/,/^###/{ /^- /i\\
$ENTRY
}" "$readme_file"
      else
        sed -i "/^### $section$/,/^###/{ /^- /i\\
$ENTRY
}" "$readme_file"
      fi

      git add "$readme_file"
      git commit -m "Add: AI Harness Migration Recipes"
      git push origin main

      gh pr create --title "Add: AI Harness Migration Recipes" \
        --body "Adds hand-written, tested migrations for AI coding agents. All 12 pairs between Claude Code, Cursor, Codex, Aider. CC BY 4.0. https://github.com/unitedideas/ai-harness-migration-recipes"

      log_info "✓ PR created"
    else
      log_warn "Entry already exists"
    fi

    cd ..
  else
    log_info "[DRY RUN] Would fork $repo_path, edit $readme_file, and create PR"
  fi
}

log_info "Awesome-list submission automation"
submit_to_list "awesome-cli-apps" "sindresorhus/awesome-cli-apps" "awesome-cli-apps" "README.md" "Tools"
submit_to_list "awesome-developer-tools" "imteekay/awesome-developer-tools" "awesome-developer-tools" "README.md" "Development"
submit_to_list "awesome-ai" "sindresorhus/awesome" "awesome" "README.md" "Development"
log_info "Done!"
