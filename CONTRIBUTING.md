# Contributing to AI Harness Migration Recipes

Thank you for contributing! This guide explains how to add new recipes or improve existing ones.

## Recipe Requirements

Every recipe **must be hand-verified** by actually performing the migration. We don't accept theoretical or untested recipes.

Each recipe file should follow this structure:

1. **The file layouts** — Directory tree and file purposes for both source and target tools
2. **Mapping each piece** — Table showing how configuration translates between tools
3. **Pitfalls** — Gotchas that silently break if you miss them
4. **Checklist** — Step-by-step walkthrough

## Validation

Before submitting a PR, verify your recipe passes structure validation:

```bash
python3 tests/validate_recipes.py
```

This checks that your recipe contains all required sections.

## File Naming

Use the pattern `{from-tool}-to-{to-tool}.md`, e.g., `claude-code-to-cursor.md`.

## Structure Example

See [claude-code-to-cursor.md](claude-code-to-cursor.md) for a full example.

### The file layouts

Show both source and target directory structures:

```markdown
## The file layouts

### Claude Code (source)

Claude Code stores configuration in `~/.claude/`:

```
~/.claude/
├── CLAUDE.md          # Main identity/settings
├── agents/            # Subagents (optional)
├── skills/            # Custom skills (optional)
├── hooks/             # Event hooks (optional)
├── projects/          # Per-project memory
└── settings.json      # Tool config + MCP servers
```

### Cursor (destination)

Cursor stores configuration in the project root and `~/.cursor/`:

```
.cursorrules                  # Main identity prompt
.cursor/
├── mcp.json                  # MCP server config
└── rules/                    # Skills as rules
```
```

### Mapping each piece

Use a table to show how fields translate:

```markdown
## Mapping each piece

| Claude Code | Cursor | Notes |
|---|---|---|
| `CLAUDE.md` | `.cursorrules` | Cursor rules are plain text |
| `agents/*.md` | `.cursor/rules/*.mdc` | Similar structure, different extension |
| `skills/*/SKILL.md` | `.cursor/rules/skill-*.mdc` | Skills become rules |
| `hooks/*.py` | (no equivalent) | Cursor has no event hooks |
| `settings.json.mcpServers` | `.cursor/mcp.json` | Different JSON structure |
```
```

### Pitfalls

List gotchas that silently break:

```markdown
## Pitfalls

1. **Relative paths** — If your CLAUDE.md references `./path/to/file`, Cursor may not find it the same way
2. **Model name format** — Claude Code uses `claude-opus-4-7`, Cursor expects `claude-opus-4`
3. **MCP socket location** — Cursor looks for MCP config in project root, not `~/.cursor/`
```
```

### Checklist

End with a numbered checklist:

```markdown
## Checklist

1. [ ] Create or locate `.cursorrules` file in project root
2. [ ] Copy your identity prompt from CLAUDE.md into `.cursorrules`
3. [ ] Create `.cursor/` directory and `mcp.json` if using MCP servers
4. [ ] For each skill in `~/.claude/skills/`, create `.cursor/rules/skill-*.mdc`
5. [ ] Test in Cursor: open a file and verify rules are applied
```
```

## Testing Your Migration

1. Actually perform the migration using your recipe
2. Verify the target tool works correctly (agent loads, skills available, MCP servers connect)
3. Document any surprises in the "Silent-breakage footguns" section
4. Add any tool-specific gotchas you discover

## Pull Request Process

1. Create a new file `{from}-to-{to}.md` following the structure above
2. Run `python3 tests/validate_recipes.py` to ensure all sections exist
3. Push and open a PR
4. Include a note that you've hand-tested the migration and it works end-to-end

## License

All contributions are licensed CC BY 4.0. By submitting a PR, you agree to license your contribution under CC BY 4.0.
