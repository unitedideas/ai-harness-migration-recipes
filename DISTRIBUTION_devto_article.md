# Migrating Your AI Coding Agent Config: The Complete Guide

You just decided to switch from Claude Code to Cursor. Or maybe from Aider to Codex. Excitement turns to dread when you realize: **your config, keybindings, hooks, and custom prompts don't transfer.**

You're staring at the blank setup screen. Again.

This guide covers all 12 possible migrations between Claude Code, Cursor, Codex, and Aider—with hand-written recipes that document the silent breakages, format differences, and exact checklist for each move.

## Why this matters

AI coding agents are still young enough that switching tools feels like starting over:
- **Hooks**: Each tool has a different lifecycle model (Claude Code uses pre-tool/post-tool phases; Cursor uses keystroke-level intercepts)
- **Keybindings**: Claude Code uses `~/.claude/keybindings.json`; Cursor uses `keybindings.json` in the app folder
- **Prompts**: System prompts live in CLAUDE.md for Claude Code, but `.cursorfiles`/`cursor.md` elsewhere
- **Secrets**: One tool reads from 1Password, another from Keychain, another from environment files

Copy-paste your config from the old tool into the new one and you'll hit permission errors, syntax failures, or silent no-ops.

## The recipes

All 12 bidirectional migrations are documented and tested:

### Claude Code ↔ Cursor
- **Claude Code → Cursor**: Transfer keybindings, hooks (rewrite in Cursor's event model), CLAUDE.md content (becomes cursor.md)
- **Cursor → Claude Code**: Reverse; handle Cursor's sandboxed permission model

### Claude Code ↔ Codex
- **Claude Code → Codex**: Codex reads only `.env` and code comments for context. Keybindings must be rewritten in C#/CLI syntax.
- **Codex → Claude Code**: Import Codex profiles; translate context injection patterns

### Claude Code ↔ Aider
- **Claude Code → Aider**: Aider is terminal-first. Config lives in `~/.aider/conf.yml`. Keybindings become shell aliases.
- **Aider → Claude Code**: Export Aider's history; import as CLAUDE.md system prompts

### Cursor ↔ Codex, Cursor ↔ Aider, Codex ↔ Aider
- All documented, tested. Full recipes at the repo.

## Each recipe includes

1. **Silent breakages** — what LOOKS like it copied but doesn't work
2. **Format translation** — exact syntax for each config type
3. **Permission models** — which tool requires explicit allow-list setup (vs auto-grant)
4. **Step-by-step checklist** — what to do, in order, with no guessing
5. **Tested on real machines** — not theoretical; each recipe has been walked through in practice

## From manual to automatic

The recipes are for **understanding**: why migrations break, what each tool expects, what's portable vs tool-specific.

For **automation**, use [BringYour](https://bringyour.ai)—a $49 one-time tool that:
- Reads your current agent config
- Translates it to the target tool
- Handles permission rewrites
- Outputs a ready-to-import bundle

Same intelligence, zero manual steps.

## Get the recipes

Full repo with all 12 migrations: **https://github.com/unitedideas/ai-harness-migration-recipes**

CC BY 4.0 — attribute to BringYour on repost.

---

*Switched agents recently? Share your migration story in the comments—what broke, what surprised you, what you wish you'd known.*
