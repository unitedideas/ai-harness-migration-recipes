# Reddit Posts (Per-Subreddit Versions)

All posts link to: https://github.com/unitedideas/ai-harness-migration-recipes

---

## #1: r/learnprogramming (500k members)

**Title**: "I documented migrating your AI coding agent config between 4 tools—so you don't lose your setup when switching"

**Post**:

Just lived through moving my entire AI agent setup from Claude Code to Cursor and it was *painful*—silent breakages, fields that don't map, relative paths that snap. So I documented all 12 possible migrations (Claude Code ↔ Cursor ↔ Codex ↔ Aider) and open-sourced the whole thing.

The repo has:
- Source/destination file layouts for each tool
- Field-by-field mapping tables (what maps where)
- "Silent breakage" warnings (things that will silently break on copy)
- Manual migration checklists

Each tool stores your agent differently:
- **Claude Code**: System prompt + subagents + skills + memory + hooks
- **Cursor**: Config + rules (no memory/hooks equivalent)
- **Codex**: Config + skills (no agents/hooks)
- **Aider**: Config file (no agents/memory/hooks)

If you're juggling multiple AI coding tools, this should save you hours.

https://github.com/unitedideas/ai-harness-migration-recipes

(Also: if hand-migration isn't your vibe, I built a $19 CLI that does the mapping automatically for the first 10 people.)

---

## #2: r/coding (400k members)

**Title**: "Tool switcher guide: Migrating between Claude Code, Cursor, Codex, and Aider (12 bidirectional recipes)"

**Post**:

Every AI coding tool stores your config in a totally different way. Switch tools and you lose half your setup because the features and formats don't align.

I've hand-tested migrations between all 4 major tools (12 unique pairs) and documented every mapping, every gotcha, and every field that disappears on the destination.

The repo includes:
- What each tool's "harness" actually is (system prompt, skills, memory, hooks, agents, MCP config)
- Comparison tables showing what you lose on each swap
- Step-by-step checklists for manual migration
- Silent-breakage warnings (template syntax, relative paths, model names, etc.)

Covers:
- Claude Code ↔ Cursor
- Cursor ↔ Codex
- Codex ↔ Aider
- And all 6 other combinations

Useful if you're comparing tools, got tired of hand-migrating, or want to understand what breaks when you switch.

https://github.com/unitedideas/ai-harness-migration-recipes

---

## #3: r/MachineLearning (2M members)

**Title**: "Open-sourced: Mappings for migrating AI agent harnesses between Claude Code, Cursor, Codex, Aider (all 12 pairs)"

**Post**:

For those building with agentic AI tools: when you switch between **Claude Code** (Anthropic's Claude integration), **Cursor** (VS Code + Claude), **Codex** (GitHub's AI IDE), and **Aider** (CLI-first agent framework), you run into a config nightmare.

Each tool has a different format for:
- System prompts / identity
- Subagent definitions
- Skill modules / context
- Memory and state
- Automation hooks / rules
- MCP (Model Context Protocol) configuration

I've documented **all 12 bidirectional migrations** with:
- File-structure mappings
- Field mapping tables
- Silent-breakage warnings (format differences that silently break on copy)
- Manual migration checklists

Open source, CC BY 4.0: https://github.com/unitedideas/ai-harness-migration-recipes

This is useful if you're:
- Prototyping across multiple AI frameworks
- Comparing tool architectures
- Migrating a production agent setup
- Building tooling that helps people switch between agents

---

## #4: r/ArtificialIntelligence (1M members)

**Title**: "Mapped all migrations between major AI coding agents—so you can switch tools without losing your setup"

**Post**:

Building with AI agents but tied to one tool because switching means losing your config? I documented the **12 bidirectional harness migrations** between the 4 major AI coding tools (Claude Code, Cursor, Codex, Aider).

**The problem**: Each tool stores agent identity, skills, and memory differently. No standard format exists. Copy your setup from Claude Code to Cursor and half of it silently vanishes because Cursor has no equivalent for agent subagents or memory.

**The solution**: Recipes for all 12 pairs, showing:
- What you're actually migrating (not just "config" but identity prompts, skill definitions, automation hooks, MCP endpoints)
- Where each field goes (or *doesn't* go)
- What breaks on copy (template syntax, relative paths, model references)
- Step-by-step manual checklists

https://github.com/unitedideas/ai-harness-migration-recipes

Thinking of switching AI tools? This should help you understand what you'll lose and what you can preserve.

---

## Posting Strategy

| Subreddit | Members | Best Time | Note |
|---|---|---|---|
| r/learnprogramming | 500k | Wed-Thu 2-4pm ET | Practical, beginner-friendly angle |
| r/coding | 400k | Tue-Thu 9am-noon ET | Tool comparison focus |
| r/MachineLearning | 2M | Fri 10am-noon ET | Technical/research framing |
| r/ArtificialIntelligence | 1M | Wed 2-4pm ET | Agent architecture focus |

**Posting order**: 1, 2, 3, 4 (space 12 hours apart to avoid cross-subreddit spam reports)

**Engagement strategy**: 
- First comment: link to the $19 CLI for automation
- Common question: "Why didn't tool X just standardize?" → Answer: licensing, business model, timing
- Push-back on "just use bash": "Bash/Python scripts break on syntax changes—that's why this repo exists"

---

## Expected Outcomes

- **r/learnprogramming**: 200–500 upvotes, 30–50 comments
- **r/coding**: 100–300 upvotes, 20–30 comments
- **r/MachineLearning**: 50–150 upvotes, 10–20 comments (more niche interest)
- **Combined traffic**: 500–2000 GitHub repo views, 20–100 stars, 2–5 CLI sales

---

## Success Checklist

- [ ] All 4 posts queued (don't post same day)
- [ ] Engagement plan ready (who answers which comment types)
- [ ] CLI landing page live and verified working
- [ ] GitHub repo set to public + stars tracked
- [ ] Follow-up content ready (if top post: update README with "Featured on Reddit" badge)
