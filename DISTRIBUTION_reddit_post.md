# Reddit Post Copies

## Post 1: r/learnprogramming, r/coding

**Title**: We documented all 12 ways to migrate your AI coding agent between Claude Code, Cursor, Codex, and Aider

**Body**:

Every AI coding tool stores your agent (system prompt, rules, skills, memory) in a completely different format. Moving between them by hand means rewriting everything and hoping nothing silently breaks.

We just published hand-written recipes for all 12 bidirectional migrations:
- **Claude Code** ↔ Cursor, Codex, Aider
- **Cursor** ↔ Claude Code, Codex, Aider
- **Codex** ↔ Claude Code, Cursor, Aider
- **Aider** ↔ Claude Code, Cursor, Codex

Each recipe includes:
- Source and target directory layouts
- Field-by-field config mapping (what translates, what doesn't)
- Silent-breakage gotchas (relative paths, template syntax, model names)
- Step-by-step migration checklist

All 12 recipes are **hand-verified** — we actually did each migration instead of guessing.

**Free + CC BY 4.0**: https://github.com/bringyour/ai-harness-migration-recipes

If manual migration sounds tedious, we also built [BringYour](https://bringyour.ai) — a CLI + remote MCP server that does the whole mapping in one command ($19–49 lifetime, first 10 slots).

---

## Post 2: r/MachineLearning

**Title**: Open source: 12 hand-verified harness migration recipes between Claude Code, Cursor, Codex, and Aider

**Body**:

Migrating an AI agent's configuration ("harness") between different coding tools is a pain — each tool stores prompts, rules, and memory differently, so copy-pasting breaks things.

We've documented all 12 bidirectional migrations between the 4 major AI coding tools with explicit attention to silent-breakage gotchas:

- **Layout differences**: where files live in each tool
- **Format mapping**: what config syntax translates across tools
- **Gotchas**: relative paths that break, template variables with different syntax, model references, etc.
- **Checklists**: step-by-step verification for manual migrations

All recipes are hand-verified (not theoretical).

**Free** (CC BY 4.0): https://github.com/bringyour/ai-harness-migration-recipes

For automation, we built **BringYour** (https://bringyour.ai) — a CLI + remote MCP that runs migrations in one command. Lifetime access: $19 (first 10), $29 (next 10), $49 thereafter.

---

## Reddit Metadata
- Subreddits: r/learnprogramming, r/coding, r/MachineLearning, r/ArtificialIntelligence, r/PromptEngineering
- Posted by: (Shane's Reddit account)
- Created: 2026-04-18
