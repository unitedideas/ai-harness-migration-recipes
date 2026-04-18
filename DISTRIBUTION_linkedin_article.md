# LinkedIn Article Copy

**Title**: We Documented All 12 Ways to Migrate Your AI Coding Agent Between Tools

**Subtitle**: A free, hand-verified guide to moving your harness (prompts, rules, skills, memory) between Claude Code, Cursor, Codex, and Aider

---

## Article Body

AI coding agents are everywhere now. Claude Code. Cursor. Codex. Aider. We're all experimenting with these tools to boost our development speed. But here's the problem: **each tool stores your agent configuration completely differently.**

You build a killer system prompt, write custom rules, create reusable skills, build up project memory—and then you want to try a different tool. Do you have to rewrite everything from scratch? Almost.

### The Problem

- **Claude Code** uses `~/.claude/CLAUDE.md`, `agents/`, `skills/`, and project-local memory files
- **Cursor** uses `.cursorrules` and `.cursor/rules/` with a different syntax
- **Codex** uses `~/.codex/config.md` and `~/.codex/skills/`
- **Aider** uses `CONVENTIONS.md` and `~/.aider.conf.yml`

None of them have obvious equivalents for the others. Relative paths break. Template variables use different syntax. Model names don't translate. You lose features moving out (e.g., Claude Code's memory, Cursor's subagents).

### Our Solution

We spent weeks documenting **all 12 bidirectional migrations** between these four tools. Each recipe shows:

1. **Source layout** — where your config lives and what it controls
2. **Destination layout** — the target tool's structure
3. **Field-by-field mapping** — what translates, what doesn't
4. **Silent-breakage footguns** — gotchas that will bite you if you copy-paste blindly
5. **Step-by-step checklist** — verify nothing broke

Every recipe is **hand-verified** — we actually did each migration, not guesses.

**Free + open source** (CC BY 4.0): https://github.com/bringyour/ai-harness-migration-recipes

### For the Impatient

If manual migration sounds like a chore, we also built [BringYour](https://bringyour.ai) — a CLI tool that does the entire mapping in one command:

```bash
portable migrate --from claude-code --to cursor
portable migrate --from cursor --to aider
```

Lifetime access: $19 (first 10 slots), $29 (next 10), $49 thereafter. Every future tool in the toolkit is included.

### Why This Matters

AI coding tools are still evolving. You're going to want to experiment. Right now, switching costs you an hour of manual work per migration. We've cut that down to: read the recipe (5 min) + copy files (1 min) + verify (5 min) = 11 minutes instead of 60.

Or use BringYour and do it in 30 seconds.

Either way, you're not locked into one tool anymore.

---

## LinkedIn Metadata
- **Posted by**: Shane Cheek
- **Post type**: Article (long-form)
- **Hashtags**: #AI #ProductDevelopment #DeveloperTools #Automation #OpenSource #ToolMigration
- **Link**: https://github.com/bringyour/ai-harness-migration-recipes
- **Secondary link**: https://bringyour.ai
- **Created**: 2026-04-18
- **Tone**: Educational, practical, confident but not promotional
