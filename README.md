# AI harness migration recipes

[![GitHub release](https://img.shields.io/github/v/release/unitedideas/ai-harness-migration-recipes?label=version)](https://github.com/unitedideas/ai-harness-migration-recipes/releases)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-blue)](LICENSE.md)
![Recipes](https://img.shields.io/badge/recipes-12%2F12-brightgreen)
![Verified](https://img.shields.io/badge/verified-hand--tested-success)

Hand-written, file-by-file mappings for moving an AI coding agent's
configuration ("harness") between tools. **Migrate between Claude Code ↔ Cursor ↔ Codex ↔ Aider** without losing your system prompts, skills, or memory.

Every AI coding tool stores your agent differently. **Claude Code** uses
`~/.claude/` with `CLAUDE.md` + `agents/` + `skills/`. **Cursor** uses
`.cursor/rules/*.mdc` at the project root. **Codex** uses `~/.codex/`.
**Aider** uses `.aider.conf.yml`. Moving your identity, skills, and memory
between them by hand means rewriting your system prompt in a new format
each time and hoping nothing silently breaks.

This repo is the manual recipes for all **12 bidirectional migrations** 
(4 tools, 4 × 3 ÷ 2 unique pairs = 6 directions per tool). One file per 
migration pair, each showing the source and target layouts, the format 
differences, and the subtle things that will bite you if you copy-paste.

## Quick Start

**Want to automate this?** Use [BringYour](https://bringyour.ai):

```bash
npx portable migrate --from claude-code --to cursor
npx portable migrate --from cursor --to codex
```

One command handles everything. Early-bird pricing: **$19 lifetime** (first 10 buyers), then $29, then $49. All future tool upgrades included.

- [Try BringYour →](https://bringyour.ai)
- [See how it works →](https://bringyour.ai/how-it-works)

**Prefer manual control?** See the recipes below.

## Recipes

| From | To | Recipe |
|---|---|---|
| Claude Code | Cursor | [claude-code-to-cursor.md](claude-code-to-cursor.md) |
| Claude Code | Aider | [claude-code-to-aider.md](claude-code-to-aider.md) |
| Claude Code | Codex | [claude-code-to-codex.md](claude-code-to-codex.md) |
| Cursor | Claude Code | [cursor-to-claude-code.md](cursor-to-claude-code.md) |
| Cursor | Aider | [cursor-to-aider.md](cursor-to-aider.md) |
| Cursor | Codex | [cursor-to-codex.md](cursor-to-codex.md) |
| Codex | Claude Code | [codex-to-claude-code.md](codex-to-claude-code.md) |
| Codex | Cursor | [codex-to-cursor.md](codex-to-cursor.md) |
| Codex | Aider | [codex-to-aider.md](codex-to-aider.md) |
| Aider | Claude Code | [aider-to-claude-code.md](aider-to-claude-code.md) |
| Aider | Cursor | [aider-to-cursor.md](aider-to-cursor.md) |
| Aider | Codex | [aider-to-codex.md](aider-to-codex.md) |

Each recipe documents:

- Source and destination directory layouts
- Field-by-field mapping of front-matter (e.g., `tools:` in Claude Code
  has no Cursor equivalent)
- Silent-breakage footguns (relative paths, template variables, model
  name references)
- Manual-migration checklist

## What each tool's "harness" includes

| Component | Claude Code | Cursor | Codex | Aider |
|---|---|---|---|---|
| Identity prompt | `~/.claude/CLAUDE.md` | `.cursorrules` + user rules | `~/.codex/config.md` | `CONVENTIONS.md` + `~/.aider.conf.yml` |
| Subagents | `agents/*.md` | `.cursor/rules/*.mdc` | (no equivalent) | (no equivalent — always-on in CONVENTIONS.md) |
| Skills | `skills/<slug>/SKILL.md` | `.cursor/rules/skill-*.mdc` | `~/.codex/skills/` | (sections in CONVENTIONS.md) |
| Memory | `projects/-/memory/*.md` | (no equivalent) | (no equivalent) | (no equivalent) |
| Hooks | `hooks/*.py` | (no equivalent) | (no equivalent) | (no equivalent) |
| MCP config | `settings.json > mcpServers` | `.cursor/mcp.json` | `~/.codex/mcp.toml` | `~/.aider.conf.yml` (≥v0.75) |

The "no equivalent" cells are where you lose something on the way out.
The recipes call those out explicitly so you can plan around them.

## Doing this with one command

Hand-migrating every time gets old fast. [BringYour](https://bringyour.ai)
is a CLI + remote MCP server that does the whole mapping in one command:

```bash
npx portable migrate --from claude-code --to cursor
npx portable migrate --from cursor --to codex
npx portable migrate --from codex --to aider
```

It supports 10 bidirectional targets plus a few write-only / paste targets.
Launch pricing: first 10 at **$19** lifetime, next 10 at **$29**, then
$49 (rising as traction grows) — one-time payment, every future tool in the toolkit included.

- [Buy a slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
- [Remote MCP →](https://bringyour.ai/mcp) (streamable-http, 4 tools)

## Share This

Found this useful? Help others discover it:

- **HackerNews**: [Submit to HN](https://news.ycombinator.com/submit?url=https%3A%2F%2Fgithub.com%2Funitedideas%2Fai-harness-migration-recipes)
- **Twitter/X**: Thread at [@bringyour](https://twitter.com/bringyour)
- **Reddit**: r/learnprogramming, r/coding, r/MachineLearning
- **dev.to**: [Full article](https://dev.to/bringyour/migrating-your-ai-agent-harness) (publish via Shane's account)
- **Awesome Lists**: Submit via [SUBMISSION_PLAYBOOK.md](SUBMISSION_PLAYBOOK.md) (awesome-cli-apps, awesome-developer-tools, awesome-ai-tools)

For detailed submission strategy, see [DISTRIBUTION_TRACKER.md](DISTRIBUTION_TRACKER.md) and [SUBMISSION_PLAYBOOK.md](SUBMISSION_PLAYBOOK.md).

## Contributing

PRs welcome for any pair not yet covered. Each recipe should follow the
same structure as [claude-code-to-cursor.md](claude-code-to-cursor.md):

1. Source layout (directory tree, file purposes)
2. Destination layout (same)
3. Field-by-field mapping tables
4. Silent-breakage list
5. Manual checklist

Content must be hand-verified — no "I think this works" sections. If you
haven't actually done the migration, don't submit the recipe.

## License

CC BY 4.0. Attribute to bringyour.ai if you repost.
