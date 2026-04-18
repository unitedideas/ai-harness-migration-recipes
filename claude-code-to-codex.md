# How to migrate your Claude Code agent to Codex

**TL;DR** — Claude Code uses `~/.claude/` with `CLAUDE.md` + `agents/` + `skills/`. Codex (the OpenAI CLI tool) uses `~/.codex/` with `AGENTS.md` + `config.toml`. The good news: skills are identical, MCP support is native. The bad news: Codex has no hook system and config format is TOML, not JSON.

Below is the manual recipe for migrating Claude Code → Codex, including file layouts, field-by-field mappings, and the things that break if you copy-paste. At the end I link to a one-command tool that does this automatically.

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

Most important: `CLAUDE.md` is your identity. Everything else is incremental.

### Codex (destination)

```
~/.codex/
├── AGENTS.md                     # identity + top-level preferences (replaces CLAUDE.md)
├── config.toml                   # structured config (MCP, model, features, approvals)
├── skills/
│   └── <skill-name>/SKILL.md     # identical format to Claude Code
└── hooks.json                    # optional hook config (limited, experimental)

$REPO_ROOT/
├── AGENTS.md                     # project-level rules (optional override)
└── .agents/skills/               # project-level skills (optional)
```

Three structural differences:

1. **Rules files are named differently.** Claude Code uses `CLAUDE.md`, Codex uses `AGENTS.md`. They're semantically identical (both Markdown, both global/project-layered), just named differently per the Linux Foundation Agentic AI standard.

2. **Config format changed.** Claude Code's `settings.json` (JSON) becomes `config.toml` (TOML). This includes all MCP server configs, model selection, and feature flags.

3. **Skills paths changed.** Claude Code: `~/.claude/skills/`. Codex: `~/.agents/skills/`. The `SKILL.md` format itself is identical.

4. **No hooks system.** Codex has an experimental `hooks.json` but it's coarse and doesn't map to Claude Code's 17 lifecycle events. You lose hook-based automation.

---

## Mapping each piece

### `CLAUDE.md` → `AGENTS.md`

The rules file is a straight rename with no format changes — both are Markdown. But watch for Claude Code-specific fields that Codex won't recognize:

| Claude Code section | Codex equivalent | Notes |
|---|---|---|
| `## How I Operate` | `## Operating principles` | Same idea, may need reword |
| `## Golden Rules` | `## Working agreements` | Same intent, different section name |
| Tool names (e.g., `Bash` tool) | Same tool names | Codex tool names are identical |
| `### Rule X: No assumptions` | Keep as-is | Codex respects structured rule sections |
| References to `.claude/` paths | Change to `~/.codex/` or `~/.agents/` | Update any hardcoded paths |
| References to Claude Code-specific features (hooks, settings.json) | Replace with Codex equivalents | Hooks don't exist; config goes in config.toml |

**Action:** Copy `~/.claude/CLAUDE.md` to `~/.codex/AGENTS.md`, do a find-and-replace for `.claude/` → `.codex/`, and strip any Claude Code-specific guidance (e.g., "/hookify" commands, "settings.json adjustment" steps). The rest ports 1:1.

For project-level overrides, also create `$REPO_ROOT/AGENTS.md` (same content as the user-level file if you're still developing).

### `agents/<name>.md` → Codex agents

Claude Code subagents:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review Go code. First, read...
```

Codex doesn't have a separate "subagent" concept. Instead, agents are invoked via `codex agent <name>` and read their rules from `~/.codex/agents/<name>.md`.

**Best practice:** Keep subagents as separate files in `~/.codex/agents/`, following the same naming:

```
~/.codex/
├── AGENTS.md                   # global identity
└── agents/
    ├── code-reviewer.md        # migrated from Claude Code
    ├── discovery.md
    └── ...
```

Each agent file has the same frontmatter (minus the `tools` field):

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
model: claude-opus-4-7
---

You review Go code. First, read...
```

| Claude Code field | Codex equivalent | Notes |
|---|---|---|
| `name` | `name` | Same |
| `description` | `description` | Same |
| `tools` | — | Codex doesn't scope tools per agent; agents have full access |
| `model` | `model` | Same; Codex defaults to GPT-5.4 if omitted |

You lose the per-agent tool allowlist. If you had a read-only code-reviewer, Codex agents can't be restricted that way — all agents have the same tool access.

### `skills/<slug>/SKILL.md` → `~/.agents/skills/<slug>/SKILL.md`

This is the cleanest migration — skills are format-identical.

Claude Code:
```
~/.claude/skills/
└── simplify/SKILL.md
```

Codex:
```
~/.agents/skills/
└── simplify/SKILL.md
```

The file format is identical — YAML frontmatter + Markdown body. Just move the files:

```bash
cp -r ~/.claude/skills/* ~/.agents/skills/
```

The only gotcha: if your skills have asset files (templates, scripts, etc.), verify they moved with the directory. Codex treats the skill directory the same way Claude Code does.

### `projects/-/memory/*.md` → `AGENTS.md` (memory)

Claude Code has a persistent memory system with per-memory files. Codex doesn't have an equivalent built-in memory system.

Options:

1. **Accept the loss.** Memories often go stale anyway. Starting fresh on Codex might be cleaner.
2. **Manually promote load-bearing memories to `~/.codex/AGENTS.md`.** For instance, if you have a memory about "always run tests in this project," just add that as a bullet point in the `AGENTS.md` under a `## Project memory` section.
3. **Store them as comments in `.agents/skills/` or `~/.agents/memory/` directory.** Not auto-loaded, but discoverable.

### `settings.json` → `config.toml`

Claude Code config (settings.json):

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

Codex config (config.toml):

```toml
[mcpServers.firecrawl]
type = "stdio"
command = "node"
args = ["/path/to/firecrawl-mcp.js"]

[core]
model = "claude-opus-4-7"
```

Key differences:

| Claude Code (settings.json) | Codex (config.toml) | Notes |
|---|---|---|
| `mcpServers` → `[mcpServers.<name>]` | Same structure, TOML syntax | Codex adds a `type` field (`stdio`, `sse`) |
| `permissions.*` | (No direct equivalent) | Codex doesn't have permission scoping |
| `model` (global) | `[core]` or `[approvals]` model | May be in different section |
| `tools.*` | (No equivalent) | Codex doesn't have per-tool permissions |

**Action:** Convert `settings.json` to TOML format. Use `codex config` CLI for guided setup, or manually write `~/.codex/config.toml`. For MCP servers, convert JSON to TOML and ensure each server has `type = "stdio"` or `type = "sse"`.

### Hooks (`~/.claude/hooks/*.py`)

**These don't port.** Codex has an experimental `hooks.json` but it doesn't map to Claude Code's lifecycle events (SessionStart, PreToolUse, StopHook, etc.). 

Options:

1. **Accept the loss.** If your hooks enforced policy (e.g., "never run rm -rf"), document that requirement and rely on Codex's audit features instead.
2. **Rebuild in your project.** For critical hooks, implement them as a CI/CD pipeline step or wrapper script.
3. **Use Codex's audit trail.** Codex logs all agent actions; integrate with external monitoring instead.

For each hook, document what it did and manually re-implement the critical ones at the application layer.

---

## Things that will silently break

1. **Path references to `.claude/`.** If your `AGENTS.md` mentions `~/.claude/scripts/foo.sh`, Codex won't have that directory. Update paths to `~/.codex/` or `~/.agents/`.

2. **Tool availability assumptions.** Claude Code and Codex share most tool names, but some differ slightly. Check the tool names in your AGENTS.md against Codex's tool list.

3. **Hook-based automation.** If you relied on a StopHook to run tests or a PreToolUse hook to validate permissions, those don't exist in Codex. Document the requirement and implement elsewhere.

4. **Model references.** If you wrote "use Opus 4.6," Codex defaults to GPT-5.4. Update model names in `AGENTS.md` to match what Codex supports (check `codex config list-models`).

5. **`$ARGUMENTS` and other Claude Code variables.** Codex doesn't expand these. Remove or rephrase.

6. **Memory files in conversation context.** Codex doesn't auto-inject memory files. If your flow relied on memories being present, manually promote them to `AGENTS.md` or store them differently.

---

## Doing this by hand

1. `cp ~/.claude/CLAUDE.md ~/.codex/AGENTS.md`. Do a find-and-replace for `.claude/` → `.codex/` and strip Claude Code-specific sections.
2. `mkdir -p ~/.agents/skills`; `cp -r ~/.claude/skills/* ~/.agents/skills/`.
3. For each file in `~/.claude/agents/`: create `~/.codex/agents/<name>.md` with the same content (keep frontmatter, strip `tools` field).
4. Convert `~/.claude/settings.json` → `~/.codex/config.toml`. Use `codex config` CLI for help, or manually write TOML format.
5. For MCP servers: list each under `[mcpServers.<name>]`, add `type = "stdio"` or `type = "sse"`, paste the command and args.
6. Skim your memory files (`~/.claude/projects/-/memory/`); promote 2-3 load-bearing memories to `AGENTS.md` under a `## Project memory` section.
7. Document what your hooks did; plan re-implementation if critical.
8. Run `codex --version` to verify setup. Try `codex agent list` to see your agents.

Figure 15-30 minutes if you have a non-trivial setup.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does this whole thing in a single command:

```
npx portable migrate --from claude-code --to codex
```

It reads `~/.claude/`, maps everything to Codex's layout, converts JSON config to TOML, validates MCP servers, scrubs PII, signs the bundle with ed25519, and emits the file tree. You review everything before it's applied — nothing auto-writes without your OK.

Launch pricing: first 10 buyers at $19 lifetime, next 10 at $29, then $49 (rising as traction grows). One payment, every current feature + every future tool in the Foundry Practitioner Toolkit.

[Grab a $19 slot →](https://bringyour.ai/buy) · [See how it works →](https://bringyour.ai/how-it-works)

---

## Footnote — why this exists

Codex is a solid open-source CLI with native MCP support. The AGENTS.md standard (now backed by the Linux Foundation) is becoming the default across multiple tools. Migrating to it is straightforward — the only real loss is hooks, and for most use cases those are nice-to-have, not critical.
