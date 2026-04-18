# Quick Start: Migrate Your AI Agent Harness

New to migrating between AI tools? Start here.

## What is a "harness"?

Your AI agent's **harness** is everything that makes it *you*:

- **System prompt** (CLAUDE.md, .cursorrules, etc.) — your identity and instructions
- **Custom skills/tools** — the abilities you've taught it
- **Memory/context** — notes, decisions, patterns from past work
- **MCP servers** — external integrations (GitHub, databases, APIs)
- **Settings** — model choice, temperature, plugins, hooks

When you switch tools, you lose your harness unless you migrate it manually.

## The Problem

Each tool stores these differently:

- **Claude Code**: `~/.claude/CLAUDE.md` + `agents/` + `skills/` + `settings.json`
- **Cursor**: `.cursorrules` + `.cursor/rules/*.mdc` + `.cursor/mcp.json`
- **Codex**: `~/.codex/config.md` + `~/.codex/skills/`
- **Aider**: `.aider.conf.yml` + `CONVENTIONS.md`

Migrating by hand means rewriting your prompt in a new format, reorganizing skills, reconfiguring MCP servers — and hoping you didn't break anything silently.

## Solution: Use These Recipes

Pick your migration pair:

| Source | Targets |
|---|---|
| Claude Code | → [Cursor](claude-code-to-cursor.md), [Aider](claude-code-to-aider.md), [Codex](claude-code-to-codex.md) |
| Cursor | → [Claude Code](cursor-to-claude-code.md), [Aider](cursor-to-aider.md), [Codex](cursor-to-codex.md) |
| Codex | → [Claude Code](codex-to-claude-code.md), [Cursor](codex-to-cursor.md), [Aider](codex-to-aider.md) |
| Aider | → [Claude Code](aider-to-claude-code.md), [Cursor](aider-to-cursor.md), [Codex](aider-to-codex.md) |

Each recipe shows:
1. **Where files go** — directory layout for source and target
2. **How fields map** — which settings translate to which
3. **What breaks silently** — common gotchas
4. **Step-by-step checklist** — follow to complete migration

## Example: Claude Code → Cursor

Open [claude-code-to-cursor.md](claude-code-to-cursor.md):

1. Look at "Source layout" — understand your current `~/.claude/` structure
2. Look at "Destination layout" — see where Cursor stores things
3. Use "Field mappings" to find where each setting goes
4. Read "Silent-breakage footguns" for surprises (relative paths, model names, etc.)
5. Follow "Manual migration checklist" step-by-step

Takes ~15–30 minutes for a complete harness.

## Doing This Automatically

If manual migration is tedious, use [BringYour](https://bringyour.ai):

```bash
npx portable migrate --from claude-code --to cursor
npx portable migrate --from cursor --to codex
npx portable migrate --from codex --to aider
```

Supports 10 bidirectional targets + paste targets.  Launch pricing: **$19** (first 10), **$29** (next 10), then **$49** (rising as traction grows).

- [Buy →](https://bringyour.ai/buy)
- [FAQ →](https://bringyour.ai/faq)
- [Remote MCP server →](https://bringyour.ai/mcp)

## Still Have Questions?

- **How do I know if I did it right?** Test in your target tool. Create a new project file, invoke your agent, and check: Does it remember your instructions? Are skills available? Do MCP servers connect?
- **What if something breaks?** Check the "Silent-breakage footguns" section of your recipe first — most issues are listed there.
- **Can I migrate only part of my harness?** Yes. You don't have to move skills or MCP servers if you don't use them. The recipe shows all options.
- **What if my tool isn't listed?** File a GitHub issue or submit a PR with a new recipe. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Next Steps

1. Pick your migration from the table above
2. Open the recipe file
3. Follow the manual checklist
4. Test in your new tool
5. Enjoy your familiar harness in a new environment

---

All recipes are hand-tested and CC BY 4.0 licensed. Attribute to [bringyour.ai](https://bringyour.ai) if you repost.
