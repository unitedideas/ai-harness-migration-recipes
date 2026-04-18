#!/usr/bin/env python3
"""
Automated awesome-list submission tool.
Submits AI Harness Migration Recipes to multiple awesome lists.
Usage: python tools/submit-awesome-lists.py [--list awesome-cli-apps]
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
        "section_search": ["Agents", "AI", "Tools", "Development"],
        "pr_title": "Add: AI Harness Migration Recipes",
        "pr_body": "Adds hand-written migrations for AI coding agent config between Claude Code, Cursor, Codex, Aider. All 12 pairs, tested, CC BY 4.0.",
    },
    "awesome-developer-tools": {
        "upstream_repo": "imteekay/awesome-developer-tools",
        "readme_file": "README.md",
        "section_search": ["AI & ML", "AI", "Development", "Tools"],
        "pr_title": "Add: AI Harness Migration Recipes (Agent Config Tool)",
        "pr_body": "Adds comprehensive migration guides for developers switching AI coding agents. Covers Claude Code, Cursor, Codex, Aider. All 12 pairs tested.",
    },
    "awesome": {
        "upstream_repo": "sindresorhus/awesome",
        "readme_file": "README.md",
        "section_search": ["Assistants", "AI", "Development", "Tools"],
        "pr_title": "Add: AI Harness Migration Recipes",
        "pr_body": "Adds resource for developers switching between AI coding tools. All major agents covered (Claude Code, Cursor, Codex, Aider). CC BY 4.0.",
    },
}


def run_cmd(cmd: list, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command, capturing output."""
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def find_section(readme_path: str, search_terms: list) -> Optional[int]:
    """Find section index using multiple search terms. Returns line number or None."""
    if not Path(readme_path).exists():
        return None

    content = Path(readme_path).read_text()
    lines = content.splitlines(keepends=True)

    # Try exact matches first
    for search_term in search_terms:
        for i, line in enumerate(lines):
            if f"## {search_term}" in line or f"### {search_term}" in line:
                return i

    # Try case-insensitive partial match
    for search_term in search_terms:
        term_lower = search_term.lower()
        for i, line in enumerate(lines):
            if term_lower in line.lower() and ("#" in line[:4]):
                return i

    return None


def submit_to_list(list_key: str, config: dict) -> bool:
    """Submit to a single awesome list (actual execution)."""
    print(f"\n{list_key}:")

    upstream = config["upstream_repo"]
    readme_file = config["readme_file"]

    # Fork & clone (gh handles "already forked" gracefully)
    print(f"  Forking {upstream}...")
    result = run_cmd(["gh", "repo", "fork", upstream, "--clone"], check=False)
    if result.returncode != 0 and "already exists" not in result.stderr:
        print(f"  ✗ Fork failed: {result.stderr[:100]}")
        return False

    # Get the fork directory name (last part of repo path)
    fork_dir = upstream.split("/")[1]

    if not Path(fork_dir).exists():
        print(f"  ✗ Fork directory not found: {fork_dir}")
        return False

    os.chdir(fork_dir)

    # Check if entry already exists
    readme_path = Path(readme_file)
    if not readme_path.exists():
        print(f"  ✗ README not found at {readme_file}")
        os.chdir("..")
        return False

    content = readme_path.read_text()
    if "AI Harness Migration Recipes" in content:
        print(f"  ⚠ Entry already exists in this fork")
        os.chdir("..")
        return False

    # Find section to add entry
    section_idx = find_section(readme_file, config["section_search"])
    if section_idx is None:
        print(f"  ⚠ Could not find appropriate section (tried: {', '.join(config['section_search'])})")
        print(f"    You may need to manually edit the README and select the right section.")
        os.chdir("..")
        return False

    # Find first list item after section
    lines = content.splitlines(keepends=True)
    insert_idx = section_idx + 1
    for i in range(section_idx + 1, len(lines)):
        if lines[i].strip().startswith("- "):
            insert_idx = i
            break

    lines.insert(insert_idx, ENTRY + "\n")
    readme_path.write_text("".join(lines))
    print(f"  ✓ Entry added to {readme_file}")

    # Commit & push
    print(f"  Committing...")
    run_cmd(["git", "add", readme_file])
    run_cmd(["git", "commit", "-m", "Add: AI Harness Migration Recipes"])

    print(f"  Pushing...")
    result = run_cmd(["git", "push", "origin", "main"], check=False)
    if result.returncode != 0:
        print(f"  ⚠ Push warning: {result.stderr[:100]}")

    # Create PR
    print(f"  Creating PR...")
    result = run_cmd([
        "gh", "pr", "create",
        "--title", config["pr_title"],
        "--body", config["pr_body"],
    ], check=False)

    if result.returncode == 0:
        pr_url = result.stdout.strip().split("\n")[0]
        print(f"  ✓ PR created: {pr_url}")
    else:
        print(f"  ⚠ PR creation note: {result.stderr[:100]}")

    os.chdir("..")
    return True


def main():
    parser = argparse.ArgumentParser(description="Submit AI Harness to awesome lists")
    parser.add_argument("--list", help="Submit to specific list only (default: all)")
    args = parser.parse_args()

    if args.list and args.list not in LISTS:
        print(f"Unknown list: {args.list}")
        print(f"Available: {', '.join(LISTS.keys())}")
        return 1

    lists_to_submit = {args.list: LISTS[args.list]} if args.list else LISTS

    print("Awesome-list submission automation")
    print(f"Submitting {len(lists_to_submit)} awesome list(s)...\n")
    print("⚠ This will fork repos and create PRs under your GitHub account")
    print("⚠ Make sure you're authenticated with: gh auth login\n")

    # Create temp work directory
    work_dir = Path("/tmp/awesome-submissions")
    work_dir.mkdir(exist_ok=True)
    original_dir = os.getcwd()
    os.chdir(work_dir)

    success_count = 0
    for list_key, config in lists_to_submit.items():
        try:
            if submit_to_list(list_key, config):
                success_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
        finally:
            if os.getcwd() != original_dir:
                try:
                    os.chdir(original_dir)
                except:
                    pass

    os.chdir(original_dir)

    print(f"\n{'='*60}")
    print(f"✓ Successfully submitted to {success_count}/{len(lists_to_submit)} lists")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("  1. Check your GitHub notifications for PR status")
    print("  2. Address any reviewer feedback")
    print("  3. Once merged, update README with 'Featured in' badges")

    return 0 if success_count == len(lists_to_submit) else 1


if __name__ == "__main__":
    sys.exit(main())
