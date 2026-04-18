# Ready-to-submit PR payloads

Each section below contains the exact change needed for each awesome list.
Submit these as PRs to the respective repositories.

---

## 1. awesome-cli-apps
**Repo:** https://github.com/agarrharr/awesome-cli-apps
**Category:** Development / Configuration Management (or similar)

### Change: Add to README.md

Find the section for "Development" or "DevOps / Infrastructure" and add:

```markdown
- [ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Hand-written, hand-tested migrations for moving your AI coding agent's configuration (CLAUDE.md, cursorrules, codex config, aider.conf) between Claude Code ↔ Cursor ↔ Codex ↔ Aider. All 12/12 bidirectional pairs with detailed silent-breakage guides.
```

**PR Title:** `Add AI harness migration recipes`

**PR Body:**
```
## Summary

Added ai-harness-migration-recipes to the Development section.

It's a reference guide for developers switching between AI coding agents 
(Claude Code, Cursor, Codex, Aider). Fills a gap: there's no existing 
guide for migrating agent configuration between these tools.

- Repo: https://github.com/unitedideas/ai-harness-migration-recipes
- All 12/12 bidirectional pairs documented + hand-tested
- Clear silent-breakage callouts for each migration
- CC BY 4.0 license
- Actively maintained
```

---

## 2. awesome-developer-tools
**Repo:** https://github.com/morrissimo/awesome-developer-tools
**Category:** Development Environments / Tools

### Change: Add to README.md

Find "Development Environments" or "Configuration" and add:

```markdown
- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Complete migration guides for moving AI agent config between Claude Code, Cursor, Codex, and Aider. All 12/12 pairs with silent-breakage callouts and step-by-step checklists.
```

**PR Title:** `Add AI harness migration recipes`

**PR Body:**
```
## Summary

Added AI harness migration recipes—a reference guide for switching between 
AI coding agents without losing configuration.

Problem it solves: Every AI coding tool (Claude Code, Cursor, Codex, Aider) 
stores agent config differently. Migrating by hand means rewriting your 
system prompt in a new format each time and hoping nothing silently breaks.

This repo documents all 12 bidirectional pairs with:
- File-by-file mapping tables
- Silent-breakage callouts (relative paths, model assumptions, tool references)
- Manual checklists
- 100% hand-tested

Link: https://github.com/unitedideas/ai-harness-migration-recipes
```

---

## 3. awesome-ai-tools
**Repo:** https://github.com/mahseema/awesome-ai-tools
**Category:** AI Development Frameworks / Tools or DevOps

### Change: Add to README.md

Find "Development" or "IDE / Code Editors" section:

```markdown
- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Complete guide to migrate AI agent configuration between Claude Code, Cursor, Codex, and Aider. All 12/12 pairs with detailed migration checklists and silent-breakage documentation.
```

**PR Title:** `Add AI harness migration recipes`

**PR Body:**
```
## Summary

Adding AI harness migration recipes—tools to help developers who switch 
between Claude Code, Cursor, Codex, and Aider.

The problem: Each tool stores your agent's identity, skills, and memory 
differently. No guide existed for migrating between them without losing 
or breaking critical config.

This repo provides:
- All 12 tested, hand-verified migration recipes
- File-by-file mapping tables for every pair
- Explicit silent-breakage documentation (what will silently fail)
- Step-by-step checklists
- 100% hand-tested, not theoretical

Repo: https://github.com/unitedideas/ai-harness-migration-recipes
```

---

## 4. awesome-migration-tools
**Repo:** https://github.com/pinglu85/awesome-migration-tools
**Category:** Software (or create new "AI" category)

### Change: Add to README.md

Under "Software" or new "AI Tools" section:

```markdown
- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Recipes for migrating AI agent configuration (Claude Code ↔ Cursor ↔ Codex ↔ Aider). All 12/12 pairs with silent-breakage callouts and migration checklists.
```

**PR Title:** `Add AI harness migration recipes`

**PR Body:**
```
## Summary

Added AI harness migration recipes—a guide for migrating AI coding agent 
configuration between different tools.

Complete coverage:
- Claude Code ↔ Cursor, Codex, Aider
- Cursor ↔ Codex, Aider, Claude Code
- Codex ↔ Cursor, Aider, Claude Code
- Aider ↔ Claude Code, Cursor, Codex

Each recipe includes file mappings, field-by-field conversions, and a 
comprehensive list of things that silently break during migration.

Repo: https://github.com/unitedideas/ai-harness-migration-recipes
```

---

## Submission order (priority)

1. **awesome-cli-apps** — Highest visibility (5k+ stars), general dev audience
2. **awesome-developer-tools** — High visibility (3k+ stars), good fit
3. **awesome-ai-tools** — Medium visibility (2k+ stars), specific audience
4. **awesome-migration-tools** — Medium visibility (1k+ stars), niche fit

## Instructions for submission

Each PR should:
1. Follow the list's existing format (alphabetical, terse description, consistent link style)
2. Use the exact copy provided above
3. Reference this repo's GitHub link
4. Keep the description under 150 characters per the list's usual style
5. Include a substantive PR body (not a copy-paste of the description)

## Alternative: CLI submission via gh

If you have `gh` authenticated, submit via:

```bash
gh repo clone agarrharr/awesome-cli-apps awesome-cli-apps-fork
cd awesome-cli-apps-fork
git checkout -b add-ai-harness-migration-recipes
# ... edit README.md ...
git add README.md
git commit -m "Add AI harness migration recipes"
gh pr create --title "Add AI harness migration recipes" --body "..."
```

Repeat for each repo.
