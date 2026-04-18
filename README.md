# AI harness migration recipes

Hand-written, file-by-file mappings for moving an AI coding agent's
configuration ("harness") between tools.

Every AI coding tool stores your agent differently. **Claude Code** uses
`~/.claude/` with `CLAUDE.md` + `agents/` + `skills/`. **Cursor** uses
`.cursor/rules/*.mdc` at the project root. **Codex** uses `~/.codex/`.
**Aider** uses `.aider.conf.yml`. Moving your identity, skills, and memory
between them by hand means rewriting your system prompt in a new format
each time and hoping nothing silently breaks.

This repo is the manual recipes. One file per migration pair, each showing
the source and target layouts, the format differences, and the subtle
things that will bite you if you copy-paste.

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
| Aider | Claude Code | [aider-to-claude-code.md](aider-to-claude-code.md) |

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
