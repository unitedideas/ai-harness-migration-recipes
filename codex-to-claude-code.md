# How to migrate your Codex agent to Claude Code

**TL;DR** — Codex uses `~/.codex/` with `AGENTS.md` + `config.toml`. Claude Code uses `~/.claude/` with `CLAUDE.md` + `settings.json` + hooks + memory. The good news: skills port directly, MCP config is simpler. The bad news: Codex doesn't have hooks or persistent memory, so you're gaining infrastructure you need to populate.

Below is the manual recipe for migrating Codex → Claude Code, including file layouts, field-by-field mappings, and the things that break if you copy-paste. At the end I link to a one-command tool that does this automatically.

---

## The file layouts

### Codex (source)

```
~/.codex/
├── AGENTS.md                     # identity + top-level preferences
├── config.toml                   # structured config (MCP, model, features)
├── agents/
│   └── <agent-name>.md           # frontmatter + agent prompt
├── skills/
│   └── <skill-name>/SKILL.md     # identical format to Claude Code
└── hooks.json                    # optional hook config (limited, experimental)

$REPO_ROOT/
├── AGENTS.md                     # project-level rules (optional override)
└── .agents/skills/               # project-level skills (optional)
```

### Claude Code (destination)

```
~/.claude/
├── CLAUDE.md                     # identity + top-level preferences
├── settings.json                 # permissions, hooks, MCP config
├── agents/
│   └── <agent-name>.md           # frontmatter + subagent prompt
├── skills/
│   └── <skill-name>/SKILL.md     # identical format to Codex
├── hooks/*.py                    # lifecycle hook scripts
└── projects/-/memory/*.md        # persistent memory files
```

Four structural differences:

1. **Rules files are named differently.** Codex uses `AGENTS.md`, Claude Code uses `CLAUDE.md`. They're semantically identical (both Markdown, both global/project-layered), just named differently per the Linux Foundation Agentic AI standard vs. Claude Code's established convention.

2. **Config format changed.** Codex's `config.toml` (TOML) becomes Claude Code's `settings.json` (JSON). This includes all MCP server configs, model selection, and permission scopes.

3. **Skills paths unchanged.** Both use `<tool>/skills/`. The `SKILL.md` format itself is identical.

4. **Gaining hooks system.** Claude Code has 17 lifecycle events (SessionStart, PreToolUse, StopHook, etc.). Codex's experimental `hooks.json` doesn't map to these. You're migrating TO hooks, so plan what you want to automate.

5. **Gaining memory system.** Claude Code has per-project persistent memory. Codex has none. You'll need to populate `~/.claude/projects/-/memory/` files with learnings from your Codex work.

---

## Mapping each piece

### `AGENTS.md` → `CLAUDE.md`

The rules file is a straight rename with no format changes — both are Markdown. But watch for Codex-specific fields that Claude Code doesn't recognize:

| Codex section | Claude Code equivalent | Notes |
|---|---|---|
| `## Operating principles` | `## How I Operate` | Same idea, may need reword |
| `## Working agreements` | `## Golden Rules` | Same intent, different section name |
| Tool names (e.g., `Bash` tool) | Same tool names | Claude Code tool names are identical |
| References to `~/.codex/` or `~/.agents/` paths | Change to `~/.claude/` | Update any hardcoded paths |
| References to Codex-specific features (experimental hooks) | Replace with Claude Code equivalents | Hooks are native; add new ones for Codex workflows |
| Model references to GPT | Update to Claude models | Claude Code supports `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5` |

**Action:** Copy `~/.codex/AGENTS.md` to `~/.claude/CLAUDE.md`, do a find-and-replace for `~/.codex/` → `~/.claude/`, and update any OpenAI model references to Claude models. Add a new `## Session Persistence` or `## Memory` section documenting what you want to remember between sessions.

For project-level overrides, also create `$REPO_ROOT/.claude/CLAUDE.md` if your Codex setup had `$REPO_ROOT/AGENTS.md`.

### `agents/<name>.md` → Claude Code agents

Codex agents:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
model: claude-opus-4-7
---

You review Go code. First, read...
```

Claude Code subagents:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
tools: Read, Grep, Glob, Bash
model: claude-opus-4-7
---

You review Go code. First, read...
```

The main addition: Claude Code lets you scope tool access per agent. If your code-reviewer should only have read-only access, you can restrict it.

**Migration path:** Copy each file from `~/.codex/agents/` to `~/.claude/agents/`. Add a `tools:` field to the frontmatter with the tools that agent needs:

| Codex field | Claude Code equivalent | Notes |
|---|---|---|
| `name` | `name` | Same |
| `description` | `description` | Same |
| `model` | `model` | Same; if using GPT, switch to Claude |
| — | `tools` | NEW: specify which tools this agent can access |

**Best practice:** For each agent, think about what it actually needs:
- Read-only research agent? `tools: Read, Glob, WebFetch`
- Code reviewer? `tools: Read, Grep, Glob, Bash`
- Full access orchestrator? `tools: *` (implicit)

This is a security and focus win you get by moving to Claude Code.

### `skills/<slug>/SKILL.md` → `~/.claude/skills/<slug>/SKILL.md`

This is the cleanest migration — skills are format-identical.

Codex:
```
~/.agents/skills/
└── simplify/SKILL.md
```

Claude Code:
```
~/.claude/skills/
└── simplify/SKILL.md
```

The file format is identical — YAML frontmatter + Markdown body. Just move the files:

```bash
cp -r ~/.agents/skills/* ~/.claude/skills/
```

The only gotcha: if your skills have asset files (templates, scripts, etc.), verify they moved with the directory. Claude Code treats the skill directory the same way Codex does.

### `config.toml` → `settings.json`

Codex config (config.toml):

```toml
[mcpServers.firecrawl]
type = "stdio"
command = "node"
args = ["/path/to/firecrawl-mcp.js"]

[core]
model = "claude-opus-4-7"
```

Claude Code config (settings.json):

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "node",
      "args": ["/path/to/firecrawl-mcp.js"]
    }
  },
  "model": "claude-opus-4-7"
}
```

Key differences:

| Codex (config.toml) | Claude Code (settings.json) | Notes |
|---|---|---|
| `[mcpServers.<name>]` TOML sections | `"mcpServers": { "<name>": {...} }` JSON | Codex adds `type` field; Claude Code doesn't need it |
| (No equivalent) | `"tools": {...}` | Claude Code can scope tool permissions globally |
| (No equivalent) | `"permissions": {...}` | Claude Code has permission scoping per environment |
| `[core]` model field | `"model"` at root | Different structure, same meaning |

**Action:** Convert `config.toml` to JSON. For MCP servers, extract each `[mcpServers.<name>]` section and convert to the JSON object format. Strip the `type` field (Claude Code doesn't need it).

Example conversion:

**Codex input:**
```toml
[mcpServers.firecrawl]
type = "stdio"
command = "node"
args = ["/path/to/firecrawl-mcp.js"]
```

**Claude Code output:**
```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "node",
      "args": ["/path/to/firecrawl-mcp.js"]
    }
  }
}
```

### `hooks.json` (Codex) → `hooks/*.py` (Claude Code)

Codex's experimental `hooks.json` is coarse and doesn't map to Claude Code's 17 lifecycle events. You're migrating TO hooks, so document what you want to automate:

| Lifecycle event | Use case | Example |
|---|---|---|
| `SessionStart` | Load memory, verify environment | Read user context files, check tool paths |
| `PreToolUse` | Validate before running tools | Enforce no `rm -rf`, check spend limits |
| `StopHook` | Run on session end | Save memory, run tests, commit changes |
| `UserPromptSubmit` | Process user input before responding | Inject context, validate requests |

**Action:** Don't port Codex's `hooks.json`. Instead:

1. Document what automation you relied on (if any).
2. Write new Python hook scripts in `~/.claude/hooks/` for the critical automations.
3. Check the [Claude Code hooks reference](https://claude.com/docs/claude-code/hooks) for exact lifecycle events and signatures.

Example: If you had a workflow that always ran tests on session end, write:

```python
# ~/.claude/hooks/stop_hook.py
def run(context):
    # Run tests on session end
    os.system("cd $PROJECT_ROOT && npm test")
    return True
```

---

## Things that will silently break

1. **Codex-specific tool names.** While Claude Code and Codex share most tool names, some differ. Check your agent prompts for references to tools that might have different names in Claude Code.

2. **Model name differences.** Codex defaults to GPT-5.4. If you wrote "use GPT-5," Claude Code won't know what that is. Update all model references to Claude models: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`.

3. **Missing memory files.** Codex doesn't have persistent memory, so you're starting with an empty `~/.claude/projects/-/memory/` directory. If you had learnings or project context in Codex, write them out to memory files.

4. **Hooks are now powerful.** Claude Code hooks can block or modify execution. If you write a hook incorrectly, it might prevent tools from running. Test new hooks in a sandbox first.

5. **Per-agent tool scoping is now possible.** Claude Code lets you restrict tools per agent. If you don't specify `tools:`, agents default to full access. Think about what each agent actually needs.

6. **Project-level rules are optional.** Claude Code supports `.claude/CLAUDE.md` at the project root, but it's optional. Codex's `$REPO_ROOT/AGENTS.md` is the same — migrate it if you have one, but it's not required.

---

## Doing this by hand

1. `cp ~/.codex/AGENTS.md ~/.claude/CLAUDE.md`. Do a find-and-replace for `~/.codex/` → `~/.claude/` and `~/.agents/` → `~/.claude/`. Update all GPT model references to Claude models.

2. Add a new `## Session Persistence` section to `CLAUDE.md` with notes on what you want to remember between sessions.

3. `mkdir -p ~/.claude/skills && cp -r ~/.agents/skills/* ~/.claude/skills/`.

4. For each file in `~/.codex/agents/`: create `~/.claude/agents/<name>.md` with the same content. Add a `tools:` field to each agent's frontmatter (e.g., `tools: Read, Grep, Glob, Bash`).

5. Convert `~/.codex/config.toml` → `~/.claude/settings.json`. Parse the TOML file, extract MCP server configs, and write as JSON. Strip `type` fields.

6. Create memory files for load-bearing learnings. Examples:
   - `~/.claude/projects/-memory/project_codex_migration.md` — notes on what you're bringing over
   - `~/.claude/projects/-memory/tool_patterns.md` — common tool usage patterns you discovered in Codex

7. Create hook scripts for critical automations:
   - `~/.claude/hooks/session_start.py` — initialize environment
   - `~/.claude/hooks/stop_hook.py` — save memory, run tests, etc.

   Check [Claude Code hooks reference](https://claude.com/docs/claude-code/hooks) for function signatures.

8. Run `claude code` to verify setup. Test a simple task to confirm tools and agents work.

Figure 30-45 minutes if you have a non-trivial Codex setup with multiple agents and MCP servers.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does this whole thing in a single command:

```
npx portable migrate --from codex --to claude-code
```

It reads `~/.codex/`, maps everything to Claude Code's layout, converts TOML config to JSON, validates MCP servers, generates stub memory files, and signs the bundle with ed25519. You review everything before it's applied — nothing auto-writes without your OK.

Launch pricing: first 10 buyers at $19 lifetime, next 10 at $29, then $49 (rising as traction grows). One payment, every current feature + every future tool in the Foundry Practitioner Toolkit.

[Grab a $19 slot →](https://bringyour.ai/buy) · [See how it works →](https://bringyour.ai/how-it-works)

---

## Footnote — why this exists

Claude Code is a mature AI agent harness with hooks, memory, and per-agent tool scoping. Codex is a solid open-source CLI with native MCP support. Both use the AGENTS.md standard (now backed by the Linux Foundation). Migrating between them is straightforward — the real gains on moving to Claude Code are hooks (automation) and memory (learning), which Codex doesn't have.
