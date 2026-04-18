# How to migrate your Codex agent to Claude Code

**TL;DR** — Codex uses `~/.codex/` with `AGENTS.md` + `config.toml`. Claude Code uses `~/.claude/` with `CLAUDE.md` + `settings.json`. Skills are identical (same format, different path), but Codex's TOML config and missing hooks make the reverse migration slightly different from Claude Code → Codex.

Below is the manual recipe for migrating Codex → Claude Code, including file layouts, field-by-field mappings, and gotchas.

---

## The file layouts

### Codex (source)

```
~/.codex/
├── AGENTS.md                     # identity + top-level preferences
├── config.toml                   # structured config (MCP, model, features)
├── agents/
│   └── <agent-name>.md           # subagent rules (optional)
├── skills/
│   └── <skill-name>/SKILL.md     # skill definitions
└── hooks.json                    # optional experimental hooks

$REPO_ROOT/
├── AGENTS.md                     # project-level rules (optional)
└── .agents/skills/               # project-level skills (optional)
```

### Claude Code (destination)

```
~/.claude/
├── CLAUDE.md                     # identity + top-level preferences (renamed from AGENTS.md)
├── settings.json                 # structured config (MCP, permissions, hooks)
├── agents/
│   └── <agent-name>.md           # subagent rules with Claude-specific frontmatter
├── skills/
│   └── <skill-name>/SKILL.md     # identical to Codex (same format)
├── hooks/*.py                    # lifecycle hook scripts (Codex has no equivalent)
└── projects/-/memory/*.md        # persistent memory files (optional)
```

Key differences:

1. **Rules file renamed.** Codex uses `AGENTS.md`, Claude Code uses `CLAUDE.md`.
2. **Config format.** Codex: `config.toml` (TOML). Claude Code: `settings.json` (JSON).
3. **Agents need extra metadata.** Codex agents are minimal; Claude Code agents require additional frontmatter (`tools`, `model` scoping).
4. **Skills path.** Codex: `~/.agents/skills/`. Claude Code: `~/.claude/skills/`.
5. **Hooks.** Codex has no real hook system; Claude Code has 17 lifecycle hooks. You gain this capability on the Claude Code side.

---

## Mapping each piece

### `AGENTS.md` → `CLAUDE.md`

The rules file is a straight rename — both are Markdown with identical semantics.

**Action:** Copy `~/.codex/AGENTS.md` to `~/.claude/CLAUDE.md`. Replace any Codex-specific references with Claude Code equivalents:

| Codex section | Claude Code equivalent | Notes |
|---|---|---|
| `## Operating principles` | `## How I Operate` | Rephrase if needed |
| `## Working agreements` | `## Golden Rules` | Same intent, different structure |
| `## Core model` config note | `## Model Tier Usage` (table or section) | Claude Code uses structured sections |
| References to `~/.codex/` | Change to `~/.claude/` | Update paths |
| References to `~/.agents/skills/` | Change to `~/.claude/skills/` | Skills path differs |

Also add Claude Code-specific sections that don't exist in Codex:

- `## Autonomy & Escalation` — decision rules for when to ask vs. execute
- `## Agents` — specialist registry with dispatching criteria
- `## Work in Progress` — optional but useful for tracking blockers

For project-level overrides, also create `$REPO_ROOT/CLAUDE.md` with the same content if you're working in a single project.

### Codex `agents/<name>.md` → Claude Code `agents/<name>.md`

Both tools support subagents, but Claude Code's frontmatter is richer.

Codex agent:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
model: claude-opus-4-7
---

You review Go code. First, read...
```

Claude Code agent:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review Go code. First, read...
```

| Codex field | Claude Code equivalent | Notes |
|---|---|---|
| `name` | `name` | Same |
| `description` | `description` | Same |
| `model` | `model` | Same; update to Claude Code model names (opus, sonnet, haiku) |
| — | `tools` | NEW field; Claude Code scopes tools per agent. List the tools this agent can use. |

**Action:** For each agent in `~/.codex/agents/`, create `~/.claude/agents/<same-name>.md` with:
1. Copy the frontmatter
2. Add a `tools:` field with the tools this agent needs (e.g., `Read, Grep, Bash`)
3. Update `model:` to Claude Code names (if `gpt-5.4` → `opus`, if `gpt-4` → `sonnet`)
4. Keep the body text as-is

Example conversion:

**Codex source:**
```markdown
---
name: discovery
description: Pre-implementation code scoping
model: claude-opus-4-7
---

You explore unfamiliar codebases...
```

**Claude Code target:**
```markdown
---
name: discovery
description: Pre-implementation code scoping
tools: Read, Grep, Glob, Bash
model: opus
---

You explore unfamiliar codebases...
```

### `skills/<slug>/SKILL.md` → `~/.claude/skills/<slug>/SKILL.md`

**This is the cleanest migration — no format change needed.**

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

Just copy the files:

```bash
mkdir -p ~/.claude/skills
cp -r ~/.agents/skills/* ~/.claude/skills/
```

The SKILL.md format is identical in both tools.

### `config.toml` → `settings.json`

Codex config (config.toml):

```toml
[core]
model = "claude-opus-4-7"

[mcpServers.firecrawl]
type = "stdio"
command = "node"
args = ["/path/to/firecrawl-mcp.js"]
```

Claude Code config (settings.json):

```json
{
  "defaultModel": "opus-4-7",
  "mcpServers": {
    "firecrawl": {
      "command": "node",
      "args": ["/path/to/firecrawl-mcp.js"]
    }
  },
  "permissions": {
    "read": true,
    "bash": true,
    "bash-dangerous-commands": false
  }
}
```

| Codex (config.toml) | Claude Code (settings.json) | Notes |
|---|---|---|
| `[core]` model | `defaultModel` | Same purpose; different location |
| `[mcpServers.<name>]` | `mcpServers.<name>` | Same structure, JSON format instead of TOML |
| `[mcpServers.*.type]` | (Not needed) | Claude Code infers from config structure |
| `[approvals].*` | `permissions.*` | Similar concept, different structure |
| — | `hooks` | NEW; list hook event paths for Claude Code lifecycle events |

**Action:**

1. Convert `config.toml` to JSON:
   ```bash
   cat ~/.codex/config.toml | toml-to-json > /tmp/config.json
   ```
   (If you don't have `toml-to-json`, manually convert key-value pairs.)

2. Restructure for Claude Code:
   - Copy MCP server definitions as-is (drop the `type` field)
   - Copy or set `defaultModel`
   - Add `permissions` object with `read`, `bash`, etc. as needed
   - Remove Codex-specific fields (e.g., `[features]`, `[core]` except model)

3. Example `settings.json`:
   ```json
   {
     "defaultModel": "opus-4-7",
     "mcpServers": {
       "firecrawl": {
         "command": "node",
         "args": ["/path/to/firecrawl-mcp.js"]
       }
     },
     "permissions": {
       "read": true,
       "bash": true
     }
   }
   ```

### `hooks.json` → `hooks/*.py`

Codex has an experimental `hooks.json` with limited functionality. Claude Code's hook system is mature with 17 events (SessionStart, PreToolUse, StopHook, PostToolUse, etc.).

**Action:**

1. Document what Codex's `hooks.json` did (if anything).
2. For critical hook logic, implement equivalent Claude Code hooks:
   - **SessionStart:** Initialize state, load secrets, set up logging
   - **PreToolUse:** Validate tool invocation (e.g., prevent destructive operations)
   - **StopHook:** Cleanup, summarize, enforce completion criteria
   - **PostToolUse:** Validate tool results, trigger side effects

3. Place hook scripts in `~/.claude/hooks/` with naming like `session_start.py`, `pre_tool_use.py`, etc.

Codex doesn't have a hook system, so you're not losing anything — you're gaining the capability.

---

## Things that will silently break

1. **`~/.agents/` vs `~/.claude/`.** Make sure all hardcoded paths in `AGENTS.md` are updated to `~/.claude/`.

2. **TOML vs JSON config.** If your `config.toml` has complex TOML syntax (arrays, nested tables), manual conversion to JSON is error-prone. Use a TOML-to-JSON converter or `codex config export` if available.

3. **Model name mismatch.** Codex uses full model names (e.g., `claude-opus-4-7`); Claude Code uses shorthand (e.g., `opus`). Update your AGENTS.md → CLAUDE.md during migration.

4. **Agent tool scoping.** Claude Code agents can be restricted to specific tools (e.g., a code-reviewer with only read-only tools). If your Codex agents relied on full tool access, add the `tools:` field to Claude Code agents.

5. **Missing memory system.** Codex doesn't have persistent memory. If you stored important config in Codex as `AGENTS.md` notes, manually promote those to `~/.claude/projects/-/memory/` files when you move to Claude Code.

6. **`AGENTS.override.md` precedence.** Codex supports override files for project-specific rules. Claude Code uses `$REPO_ROOT/CLAUDE.md` for the same purpose — name it `CLAUDE.md`, not `CLAUDE.override.md`.

---

## Doing this by hand

1. `cp ~/.codex/AGENTS.md ~/.claude/CLAUDE.md`. Update paths and section names per the mapping table above.
2. `mkdir -p ~/.claude/agents/`; for each file in `~/.codex/agents/`, create `~/.claude/agents/<name>.md` with added `tools:` field.
3. `mkdir -p ~/.claude/skills/`; `cp -r ~/.agents/skills/* ~/.claude/skills/`.
4. Convert `~/.codex/config.toml` to JSON → `~/.claude/settings.json`. Test with `cat ~/.claude/settings.json | jq .` to verify JSON syntax.
5. Add MCP servers to `settings.json` under `mcpServers`. Remove the `type` field from each.
6. Create hook scripts in `~/.claude/hooks/` if you have critical automation. Start with a simple `session_start.py` to verify the hook system works.
7. Create a `~/.claude/projects/-/memory/MEMORY.md` index (optional but recommended).
8. Test: run `claude --version`. Try `claude prompt` with a simple task. Verify agents show up via `ls ~/.claude/agents/`.

Figure 20-40 minutes if you have a non-trivial setup.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does this whole thing in a single command:

```
npx portable migrate --from codex --to claude-code
```

It reads `~/.codex/`, maps everything to Claude Code's layout, converts TOML → JSON, adds tool scoping to agents, scrubs PII, and emits the file tree. You review everything before it's applied — nothing auto-writes without your OK.

Launch pricing: first 10 buyers at $19 lifetime, next 10 at $29, then $49 (rising as traction grows). One payment, every current feature + every future tool in the Foundry Practitioner Toolkit.

[Grab a $19 slot →](https://bringyour.ai/buy) · [See how it works →](https://bringyour.ai/how-it-works)

---

## Footnote — why this exists

Codex pioneered the AGENTS.md standard, which is now the Linux Foundation baseline for agentic AI. Migration *to* Codex is straightforward because it's simpler than Claude Code. Migration *from* Codex gains Claude Code's richness (hooks, memory, tool scoping) — this is where you get more capability, not less.
