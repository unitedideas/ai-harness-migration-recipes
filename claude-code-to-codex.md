# How to migrate your Claude Code agent to Codex

**TL;DR** — Claude Code uses `~/.claude/` with `CLAUDE.md` + `agents/` + `skills/`. Codex uses `~/.codex/config.toml` (TOML format). Both support subagents and MCP, but Codex's personality/preferences live in config, not a single identity file. This recipe maps every piece you'll need to move, the format differences to watch out for, and what you'll lose in the translation.

---

## The file layouts

### Claude Code (source)

```
~/.claude/
├── CLAUDE.md                     # identity + top-level preferences
├── settings.json                 # permissions, hooks, MCP config
├── agents/
│   └── <agent-name>.md           # frontmatter + subagent prompt
├── skills/
│   └── <skill-name>/SKILL.md     # frontmatter + skill body
├── hooks/*.py                    # lifecycle hook scripts
└── projects/-/memory/*.md        # persistent memory files
```

### Codex (destination)

```
~/.codex/
├── config.toml                   # identity + preferences (TOML format)
├── auth.json                     # optional credentials file
├── hooks.json                    # lifecycle hooks (experimental)
└── [optional project overrides]
  .codex/
  └── config.toml                 # project-level config override
```

**Key difference:** Codex is much simpler at the filesystem level. There's no `agents/` or `skills/` directory — everything is in the config file or project conventions. Project-level config lives in `.codex/config.toml` (at the project root), not in the global `~/.codex/`.

---

## Mapping each piece

### `CLAUDE.md` → `~/.codex/config.toml`

Your `CLAUDE.md` is a Markdown document with prose + inline key-value pairs. Codex's config is pure TOML. Here's what maps:

| Claude Code (`CLAUDE.md`) | Codex (`config.toml`) | Notes |
|---|---|---|
| Your "Mission" / voice section | `personality = "pragmatic"` (or `"friendly"`, `"none"`) | Codex offers preset personalities; you can't embed free-form prose |
| Model tier decisions (Haiku/Sonnet/Opus for different tasks) | `model = "gpt-5.4"` + `[profiles.deep-review]` with `model = "gpt-5-pro"` | Codex doesn't support per-agent model routing; use profiles instead |
| Rules / constraints (no assumptions, always verify, etc.) | None — Codex has no direct equivalent | You lose this. Document in a project `CONVENTIONS.md` and set `read: [CONVENTIONS.md]` in project config |
| Infrastructure / secrets management | `[shell_environment_policy]` + `approval_policy` | Codex handles secrets differently; see "Silent breakages" |
| Platform knowledge / external API docs | Not in config; use read-only files via project config | Create a `docs/` folder with your notes, add to `read` in project config |

### `agents/<name>.md` → Codex profiles

Claude Code agents are subagents with their own model tier + tools. Codex doesn't have explicit subagents, but it has **profiles** for task-specific model configs:

**Claude Code agent example:**
```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review Go code...
```

**Codex profile equivalent** (`config.toml`):
```toml
[profiles.code-reviewer]
model = "gpt-4o"  # no Sonnet/Opus tiers in Codex; map Sonnet→gpt-4o, Opus→gpt-5-pro
approval_policy = "never"  # equivalent to "read-only tools" via trust model
```

Then invoke via CLI: `codex --profile code-reviewer <task>`

**Limitations:**
- Codex profiles don't have explicit tool allowlists. You lose the per-agent scoping.
- No way to say "this profile uses Read/Grep/Bash only" — the model decides which tools to use.
- Profiles are CLI-selected, not auto-invoked like Claude Code agents.

### `skills/<slug>/SKILL.md` → Not directly supported

Codex has no native skills system. Your options:

1. **Inline into config:** If the skill is small, convert it to a `[profiles.<skillname>]` with the procedure in the profile description.
2. **Conventions file:** Add it to a project `CONVENTIONS.md` and reference via `read: [CONVENTIONS.md, skills/my-skill.md]`.
3. **Accept the loss:** Codex's model selection and profiles serve the same purpose (task-specific behavior), so skills may not be needed.

### `projects/-/memory/*.md` → Not directly supported

Codex has no built-in memory system like Claude Code. You have two options:

1. **Promote to CONVENTIONS:** Merge load-bearing memories into a project `CONVENTIONS.md` file. Add `read: [CONVENTIONS.md]` to your project config.
2. **Accept the loss:** Codex doesn't have session memory, so re-provide context each conversation.

### Hooks (`~/.claude/hooks/*.py`) → `~/.codex/hooks.json` (experimental)

Codex has an **experimental** hooks system in `~/.codex/hooks.json`. Structure:

```json
{
  "pre_chat": [
    {
      "name": "my-pre-chat-hook",
      "script": "/path/to/script.py",
      "trigger": "always"
    }
  ],
  "post_chat": [
    {
      "name": "my-post-chat-hook",
      "script": "/path/to/script.py",
      "trigger": "always"
    }
  ]
}
```

**Caveat:** Codex hooks are experimental and less mature than Claude Code's. Test thoroughly.

### MCP servers

Both tools support MCP. The wiring is different:

- **Claude Code:** `~/.claude/settings.json` under `mcpServers` (JSON).
- **Codex:** `~/.codex/config.toml` under `[mcp_servers.<server_id>]` (TOML).

If you have a remote MCP server (e.g., `https://example.com/mcp`), convert your JSON config to TOML:

**Claude Code:**
```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "npx",
      "args": ["@my-org/mcp-server"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

**Codex:**
```toml
[mcp_servers.my-mcp]
command = "npx"
args = ["@my-org/mcp-server"]
[mcp_servers.my-mcp.env]
API_KEY = "${API_KEY}"
```

---

## Things that will silently break

1. **Per-agent model selection doesn't exist.** If you wrote "use Opus for this subagent", you'll need to manually select a profile or accept Codex's default model. Codex doesn't auto-route agents to different models.

2. **Tool allowlists are gone.** Your careful scoping ("this code-reviewer agent can only use Read/Grep") becomes unenforced. Codex's model decides which tools to use globally.

3. **Hooks are experimental.** If you rely on stop-hook enforcement (e.g., `golden_rules_stop.py`), test thoroughly. Codex's hook system may not be stable.

4. **No memory persistence.** Codex doesn't carry memories between conversations. You'll need to re-provide context or keep a `CONVENTIONS.md` file.

5. **Relative paths and `~` expansion.** If your `CLAUDE.md` references `~/.claude/scripts/foo.sh` or `/Users/you/projects/`, those paths are hardcoded. Codex won't have `~/.claude/` so you'll need to update paths.

6. **Environment variable references like `${SOME_VAR}` in config.** Codex supports this in `[shell_environment_policy]` and MCP config, but not in prose comments. Don't embed secrets in config file comments.

7. **Personality is preset, not free-form.** You lose the ability to write a multi-paragraph "voice" section. Codex offers `"friendly"`, `"pragmatic"`, or `"none"`. That's it.

---

## Manual checklist

1. **Create `~/.codex/config.toml`:**
   ```toml
   model = "gpt-4o"  # or "gpt-5-pro" if you were using Opus
   personality = "pragmatic"
   
   [features]
   memories = false  # or true if you want history persistence
   shell_snapshot = true
   
   [mcp_servers.my-mcp]
   # (copy your MCP configs, converting from JSON to TOML)
   ```

2. **For each agent in `~/.claude/agents/`, create a profile:**
   - `code-reviewer.md` → `[profiles.code-reviewer]` in config.toml with the agent description + recommended approval_policy

3. **For each skill in `~/.claude/skills/`, decide:**
   - Small/critical? → Add to project `CONVENTIONS.md` with `read: [CONVENTIONS.md]`
   - Large/optional? → Archive it in a project folder and reference via `read: [skills/my-skill.md]`

4. **Copy load-bearing memories to `CONVENTIONS.md`:**
   - Read through `~/.claude/projects/-/memory/*.md`
   - Promote 2-3 files that contain rules/patterns you actually use
   - Delete or archive the rest

5. **Update MCP server configs:**
   - Convert from `~/.claude/settings.json` format to Codex TOML format
   - Test each MCP server with a simple query

6. **Update any CLI scripts or automation:**
   - If you had `~/.claude/scripts/` referenced anywhere, update paths to point to new locations
   - Update any Codex invocations to use `--profile <name>` instead of agent names

7. **Disable hooks if not needed:**
   - If you weren't using hooks, leave `~/.codex/hooks.json` unwritten
   - If you were, port them to JSON and test thoroughly (experimental feature)

8. **Create a project `.codex/config.toml` if project-specific:**
   - For any config that's project-specific (not global), create `.codex/config.toml` at the project root
   - Project config cascades over user config

9. **Test a few conversations:**
   - Run `codex "prompt"` and verify your voice / model selection is preserved
   - Run `codex --profile code-reviewer "review this Go file"` and verify profile works
   - Test MCP servers with a tool call

10. **Clean up old files:**
    - `rm -rf ~/.claude/` once you're confident the migration worked
    - Or keep it as a backup until you're sure Codex works for you

---

## Notes

- **Model names differ.** Claude Code uses `haiku`, `sonnet`, `opus`. Codex uses `gpt-4o`, `gpt-5-pro`, `gpt-5.4`. Map your tier choice to Codex's model list.
- **Profiles are manual, not auto-invoked.** You can't set up a trigger like "when the file is `*.go`, use code-reviewer profile". You select the profile on the command line.
- **Codex is newer and less feature-complete than Claude Code.** Hooks, memory, subagents are less mature. If you rely heavily on automation, consider waiting or staying on Claude Code.
