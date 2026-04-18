#!/usr/bin/env python3
"""Validate recipe structure and completeness."""

import os
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Source layout",
    "## Destination layout",
    "## Field mappings",
    "## Silent-breakage footguns",
    "## Manual migration checklist",
]

RECIPE_PAIRS = [
    ("claude-code", "cursor"),
    ("claude-code", "aider"),
    ("claude-code", "codex"),
    ("cursor", "claude-code"),
    ("cursor", "aider"),
    ("cursor", "codex"),
    ("codex", "claude-code"),
    ("codex", "cursor"),
    ("codex", "aider"),
    ("aider", "claude-code"),
    ("aider", "cursor"),
    ("aider", "codex"),
]

def validate_recipe(from_tool, to_tool):
    """Check if recipe file exists and has required sections."""
    filename = f"{from_tool}-to-{to_tool}.md"
    filepath = Path(filename)

    if not filepath.exists():
        return False, f"❌ {filename}: file not found"

    with open(filepath) as f:
        content = f.read()

    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing.append(section)

    if missing:
        return False, f"⚠️  {filename}: missing sections: {', '.join(missing)}"

    return True, f"✅ {filename}"

def main():
    os.chdir(Path(__file__).parent.parent)

    results = []
    for from_tool, to_tool in RECIPE_PAIRS:
        ok, msg = validate_recipe(from_tool, to_tool)
        results.append((ok, msg))

    for ok, msg in results:
        print(msg)

    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    print(f"\n{passed}/{total} recipes validated")

    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
