# HackerNews Post Copy

**Title**: Hand-written harness migrations for 4 AI coding tools

**URL**: https://github.com/bringyour/ai-harness-migration-recipes

---

## Post Text (for HN comments if auto-submit doesn't work)

Every AI coding tool (Claude Code, Cursor, Codex, Aider) stores your agent configuration differently. Migrating your system prompt, custom rules, skills, and memory between them by hand means rewriting everything in a new format each time and hoping nothing silently breaks.

We've documented all 12 bidirectional migrations:
- Claude Code ↔ Cursor, Codex, Aider
- Cursor ↔ Claude Code, Codex, Aider  
- Codex ↔ Claude Code, Cursor, Aider
- Aider ↔ Claude Code, Cursor, Codex

Each recipe shows:
- Source and destination directory layouts
- Field-by-field mapping of config files
- Silent-breakage footguns (relative paths, template variables, model references)
- Manual migration checklist

All 12 recipes are hand-verified — we actually did each migration, not guesses.

If you're tired of copying-pasting your rules between tools, we also built BringYour (https://bringyour.ai) — a CLI + remote MCP that does the whole mapping in one command ($19–49 lifetime, first 10 slots available).

Regardless, the recipes are free and CC BY 4.0. Curious how these tools store your agent? This is the exhaustive guide.

---

## Metadata
- **Posted by**: (Shane's HN username)
- **Created**: 2026-04-18
- **Tags**: ai, tools, migration, claude-code, cursor, codex, aider
