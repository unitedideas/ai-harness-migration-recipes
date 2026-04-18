#!/usr/bin/env python3
"""
Automated awesome-list submission tool.
Submits AI Harness Migration Recipes to multiple awesome lists with one command.
Usage: python tools/submit-awesome-lists.py [--dry-run] [--list awesome-cli-apps]
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path
from typing import Optional

ENTRY = (
    "- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - "
    "Hand-written, tested migrations between Claude Code ↔ Cursor ↔ Codex ↔ Aider. "
    "All 12 bidirectional pairs with format diffs, breakage warnings, and step-by-step checklists. "
    "CC BY 4.0. [Automation via BringYour](https://bringyour.ai)."
)

LISTS = {
    "awesome-cli-apps": {
        "upstream_repo": "sindresorhus/awesome-cli-apps",
        "readme_file": "readme.md",
        "section_name": "Agents",
        "pr_title": "Add: AI Harness Migration Recipes",
        "pr_body": "Adds hand-written migrations for AI coding agent config between Claude Code, Cursor, Codex, Aider. All 12 pairs, tested, CC BY 4.0.",
    },
    "awesome-developer-tools": {
        "upstream_repo": "imteekay/awesome-developer-tools",
        "readme_file": "README.md",
        "section_name": "AI & ML",
        "pr_title": "Add: AI Harness Migration Recipes (Agent Config Tool)",
        "pr_body": "Adds comprehensive migration guides for developers switching AI coding agents. Covers Claude Code, Cursor, Codex, Aider. All 12 pairs tested.",
    },
    "awesome": {
        "upstream_repo": "sindresorhus/awesome",
        "readme_file": "README.md",
        "section_name": "Assistants",
        "pr_title": "Add: AI Harness Migration Recipes",
        "pr_body": "Adds resource for developers switching between AI coding tools. All major agents covered (Claude Code, Cursor, Codex, Aider). CC BY 4.0.",
    },
}


def run_cmd(cmd: list, dry_run: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command."""
    if dry_run:
        print(f"  [DRY RUN] Would run: {' '.join(cmd)}")
        result = subprocess.CompletedProcess(cmd, 0)
        result.stdout = b""
        result.stderr = b""
        return result

    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def fork_repo(upstream_repo: str, list_key: str, dry_run: bool = False) -> bool:
    """Fork and clone repo. Returns True if cloned, False if already exists."""
    if os.path.isdir(list_key):
        print(f"  ⚠ Fork already exists locally at {list_key}")
        return True  # Use existing

    print(f"  Forking {upstream_repo}...")
    run_cmd(["gh", "repo", "fork", upstream_repo, "--clone"], dry_run=dry_run)
    return True


def add_entry_to_readme(readme_path: str, section_name: str, entry: str, dry_run: bool = False) -> bool:
    """Add entry to README under specified section. Returns True if successful."""
    if not Path(readme_path).exists():
        print(f"  ✗ README not found at {readme_path}")
        return False

    content = Path(readme_path).read_text()

    if "AI Harness Migration Recipes" in content:
        print(f"  ⚠ Entry already exists in {readme_path}")
        return False

    # Find section header
    lines = content.splitlines(keepends=True)
    section_index = None

    for i, line in enumerate(lines):
        if f"### {section_name}" in line:
            section_index = i
            break

    if section_index is None:
        # Try without "###" (might be "##" or different format)
        for i, line in enumerate(lines):
            if section_name in line and "#" in line:
                section_index = i
                break

    if section_index is None:
        print(f"  ✗ Section [{section_name}] not found in {readme_path}")
        return False

    # Find first list item after section
    list_item_index = None
    for i in range(section_index + 1, len(lines)):
        if lines[i].strip().startswith("- "):
            list_item_index = i
            break

    if list_item_index is None:
        # No list items yet; add after section header
        list_item_index = section_index + 1

    # Insert entry
    lines.insert(list_item_index, entry + "\n")

    if not dry_run:
        Path(readme_path).write_text("".join(lines))
        print(f"  ✓ Added entry to {readme_path}")
    else:
        print(f"  [DRY RUN] Would add entry to {readme_path}")

    return True


def submit_to_list(list_key: str, config: dict, dry_run: bool = False) -> bool:
    """Submit to a single awesome list."""
    print(f"\n{list_key}:")

    # Fork & clone
    if not fork_repo(config["upstream_repo"], list_key, dry_run):
        return False

    if not dry_run:
        os.chdir(list_key)

    # Add entry
    if not add_entry_to_readme(config["readme_file"], config["section_name"], ENTRY, dry_run):
        if not dry_run:
            os.chdir("..")
        return False

    if not dry_run:
        # Commit & push
        print(f"  Committing...")
        run_cmd(["git", "add", config["readme_file"]], dry_run=False)
        run_cmd(["git", "commit", "-m", "Add: AI Harness Migration Recipes"], dry_run=False)

        print(f"  Pushing branch...")
        run_cmd(["git", "push", "origin", "main"], dry_run=False, check=False)

        # Create PR
        print(f"  Creating PR...")
        run_cmd(
            [
                "gh",
                "pr",
                "create",
                "--title",
                config["pr_title"],
                "--body",
                config["pr_body"],
            ],
            dry_run=False,
        )

        print(f"  ✓ PR created for {list_key}")
    else:
        print(f"  [DRY RUN] Would commit, push, and create PR")

    if not dry_run:
        os.chdir("..")
    return True


def main():
    parser = argparse.ArgumentParser(description="Submit AI Harness to awesome lists")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--list", help="Submit to specific list only (default: all)")
    args = parser.parse_args()

    if args.list and args.list not in LISTS:
        print(f"Unknown list: {args.list}")
        print(f"Available: {', '.join(LISTS.keys())}")
        return 1

    lists_to_submit = {args.list: LISTS[args.list]} if args.list else LISTS

    if args.dry_run:
        print("DRY RUN MODE — no actual changes will be made\n")

    print("Awesome-list submission automation")
    print(f"Submitting {len(lists_to_submit)} awesome list(s)...\n")

    # Create temp directory for work
    work_dir = Path("/tmp/awesome-submissions")
    if not args.dry_run:
        work_dir.mkdir(exist_ok=True)
        os.chdir(work_dir)

    success_count = 0
    for list_key, config in lists_to_submit.items():
        try:
            if submit_to_list(list_key, config, args.dry_run):
                success_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\n✓ Successfully submitted to {success_count}/{len(lists_to_submit)} lists")
    print("\nNext steps:")
    print("  1. Check PR status: gh pr list")
    print("  2. Once merged, update README.md with 'Featured in' badges")
    print("  3. Post announcement to HN/Twitter with social proof")

    return 0 if success_count == len(lists_to_submit) else 1


if __name__ == "__main__":
    sys.exit(main())
