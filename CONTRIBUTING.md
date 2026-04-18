# Contributing to AI Harness Migration Recipes

Thank you for contributing! This guide explains how to add new recipes or improve existing ones.

## Recipe Requirements

Every recipe **must be hand-verified** by actually performing the migration. We don't accept theoretical or untested recipes.

Each recipe file should follow this structure:

1. **Source layout** — Directory tree and file purposes for the source tool
2. **Destination layout** — Same for the target tool
3. **Field mappings** — Table showing how configuration translates between tools
4. **Silent-breakage footguns** — Gotchas that silently break if you miss them
5. **Manual migration checklist** — Step-by-step walkthrough

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

### Source layout

```markdown
## Source layout

Claude Code stores configuration in `~/.claude/`:

```
~/.claude/
├── CLAUDE.md          # Main identity/settings
├── agents/            # Subagents (optional)
│   ├── code-reviewer.md
│   └── discovery.md
├── skills/            # Custom skills (optional)
│   └── my-skill/
│       ├── SKILL.md
│       └── index.ts
├── hooks/             # Event hooks (optional)
│   └── custom-hook.py
├── projects/          # Per-project memory
│   └── myproject/
│       └── memory/
│           └── context.md
└── settings.json      # Tool config + MCP servers
```
```

### Field mappings

Use a table to show how fields from source format map to destination:

```markdown
## Field mappings

| Claude Code | Cursor | Notes |
|---|---|---|
| `CLAUDE.md` (main prompt) | `.cursorrules` (text) | Cursor rules are plain text, not YAML |
| `agents/*.md` | `.cursor/rules/*.mdc` | Similar structure, different file extension |
| `skills/*/SKILL.md` | `.cursor/rules/skill-*.mdc` | Skills are rules in Cursor |
| `hooks/*.py` | (no equivalent) | Cursor doesn't support event hooks |
| `settings.json.mcpServers` | `.cursor/mcp.json` | Different JSON structure |
```
```

### Silent-breakage footguns

List things that will silently break:

```markdown
## Silent-breakage footguns

1. **Relative paths in prompts** — If your CLAUDE.md references `./path/to/file`, Cursor rules won't find it the same way
2. **Model names** — Claude Code uses `claude-opus-4-7`, Cursor uses `claude-opus-4` (different format)
3. **MCP socket location** — Claude Code reads from `settings.json`, but Cursor won't if it's in wrong directory
```
```

### Manual checklist

End with a numbered checklist:

```markdown
## Manual migration checklist

1. [ ] Create or locate `.cursorrules` file in project root
2. [ ] Copy the identity prompt from CLAUDE.md into `.cursorrules`
3. [ ] Create `.cursor/` directory if it doesn't exist
4. [ ] For each skill in `~/.claude/skills/`, create a matching `.cursor/rules/skill-*.mdc` file
5. [ ] If using MCP servers, create `.cursor/mcp.json` with mapping from `settings.json.mcpServers`
6. [ ] Test in Cursor: open a file and verify custom rules are applied
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
