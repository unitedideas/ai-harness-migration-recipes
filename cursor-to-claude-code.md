# How to migrate your Cursor agent to Claude Code

**TL;DR** — Cursor and Claude Code look superficially similar (both "the
AI pair programming tool") but their configuration models are different
in ways that matter. Claude Code is global-by-default (`~/.claude/`);
Cursor is project-local-by-default (`.cursor/rules/`). Moving from Cursor
to Claude Code means deciding which of your Cursor rules belong in the
global `~/.claude/CLAUDE.md` vs a per-project `<project>/CLAUDE.md`, and
which of your MDC front-matter fields have nowhere to go.

This is the reverse direction of
[claude-code-to-cursor.md](claude-code-to-cursor.md). Same tools, different
direction, slightly different gotchas.

---

## The file layouts

### Cursor (source)

```
<project-root>/
├── .cursorrules              # project-level rules (plain text)
└── .cursor/
    ├── rules/
    │   ├── <name>.mdc        # MDC-format rule + front-matter
    │   └── ...
    └── mcp.json              # MCP server configuration

<user-settings>/              # Cursor's user-level config (Settings UI)
└── User Rules                # global rules (a big textarea in Settings)
```

### Claude Code (destination)

```
~/.claude/                    # global
├── CLAUDE.md                 # identity + global preferences
├── settings.json             # permissions, hooks, MCP wiring
├── agents/
│   └── <name>.md             # frontmatter + subagent
├── skills/
│   └── <slug>/SKILL.md
└── projects/-/memory/*.md    # auto-memory

<project-root>/               # per-project (optional)
└── CLAUDE.md                 # project-specific overrides + context
```

First structural decision: **what goes global vs project?** Cursor's
User Rules map cleanly to `~/.claude/CLAUDE.md`. Cursor's per-project
`.cursorrules` maps to `<project>/CLAUDE.md`. Individual `.mdc` rules
split based on whether they're role-scoped (`agents/`) or procedural
(`skills/`).

---

## Mapping each piece

### Cursor User Rules → `~/.claude/CLAUDE.md`

Cursor's User Rules is one big textarea. Your global preferences (voice,
comment rules, error-handling conventions, "I use `~/scripts/...`") go
there. Claude Code's equivalent is `~/.claude/CLAUDE.md`.

Paste the content through. Claude Code doesn't require any specific
structure but markdown headers help you navigate later. Typical sections:

```markdown
# My profile
- Background, role, preferences.

# How I work
- Pacing, communication style, when to ask vs when to act.

# Code I write
- Comment style, error handling, test patterns.
```

### `.cursorrules` (project file) → `<project>/CLAUDE.md`

Same idea, project-scoped. Cursor's `.cursorrules` is plain text; Claude
Code's per-project `CLAUDE.md` is markdown and gets loaded automatically
when the CLI is started in that directory.

This is the one mapping that's actually 1-to-1. Just rename the file.

### `.cursor/rules/<name>.mdc` (role rules) → `~/.claude/agents/<name>.md`

MDC rules with `alwaysApply: false` and a scoped `description` are
Cursor's closest equivalent to a Claude Code subagent. Convert the
front-matter:

Cursor MDC:
```yaml
---
description: Use when reviewing Go code for correctness
globs: ["**/*.go"]
alwaysApply: false
---
```

Claude Code agent:
```yaml
---
name: code-reviewer
description: Use when reviewing Go code for correctness
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

Field translation:

| Cursor MDC field | Claude Code agent field | Notes |
|---|---|---|
| `description` | `description` | Direct |
| (filename) | `name` | Add explicitly in Claude Code |
| `globs` | — | Claude Code agents don't auto-apply based on file globs |
| `alwaysApply: true` | (put in CLAUDE.md, not a subagent) | Subagents are on-demand, not always-on |
| — | `tools` | Optional — restricts which tools this subagent can use |
| — | `model` | Optional — pin a model per agent |

You *gain* two knobs in Claude Code (`tools` and `model`) that Cursor
didn't expose. Both are optional — skipping them means the agent uses
defaults.

**Watch out:** if your Cursor MDC had `alwaysApply: true`, don't convert
it to a Claude Code subagent. Put that content directly into `CLAUDE.md`
or a `skills/*/SKILL.md` — subagents in Claude Code are only loaded when
explicitly invoked, not at every turn.

### `.cursor/rules/<name>.mdc` (procedural rules) → `~/.claude/skills/<slug>/SKILL.md`

If your Cursor rule is more "procedural knowledge" ("how to deploy this
service", "how we format migrations") than "role" ("you are the security
reviewer"), it's a Claude Code skill, not an agent. Skills live in their
own directory because they can have asset files alongside (templates,
schemas, reference docs the skill might need to read).

Convert:

```yaml
# Cursor .cursor/rules/deploy-steps.mdc
---
description: How to deploy the gateway
---
Here's the deploy procedure...
```

→ 

```yaml
# ~/.claude/skills/deploy-steps/SKILL.md
---
name: deploy-steps
description: How to deploy the gateway
---
Here's the deploy procedure...
```

Plus you can add `templates/`, `scripts/`, or other assets under the skill
directory, which the skill body can reference by relative path.

### `.cursor/mcp.json` → Claude Code MCP config

Cursor's MCP config is a JSON object; Claude Code's lives in
`~/.claude/settings.json` under `mcpServers`, or can be added via the CLI:

```bash
claude mcp add <name> --transport http <url>
# or for stdio:
claude mcp add <name> -- <binary> <args>
```

The MCP specs themselves transfer cleanly — same JSON-RPC, same tool
interfaces. It's the wrapping config that differs in shape.

---

## What you gain moving to Claude Code

- **Global memory system.** `~/.claude/projects/-/memory/*.md` + `MEMORY.md`
  index gives you persistent, categorized notes across every session,
  auto-loaded. Cursor has no equivalent.

- **Hooks.** `~/.claude/hooks/*.py` run on lifecycle events (stop, session
  start, tool pre/post). Lets you enforce rules at the runtime layer, not
  just via prompt. Cursor has no hooks.

- **Per-agent tool restrictions.** A Claude Code `code-reviewer` can be
  declared read-only via `tools: Read, Grep, Glob, Bash`. Cursor has no
  equivalent — every rule runs with the tool's global permissions.

- **Slash commands.** Skills get auto-discovered as `/skill-name` slash
  commands when appropriate. Cursor has Composer's `@` but not the same
  ergonomic.

## What you lose

- **Project-local rule scoping is less automatic.** Claude Code does load
  a project's `CLAUDE.md`, but Cursor's `.cursor/rules/*.mdc` with
  `globs: ["**/*.go"]` can auto-apply to Go files and stay dormant for
  others. Claude Code's subagents are invoked explicitly — the auto-scope
  has no direct equivalent.

- **UI-driven rule editing.** Cursor's Settings UI for User Rules is nice.
  Claude Code is text editor + CLI; no rule-editing GUI.

---

## Things that will silently break

1. **`globs:` auto-scoping.** Any rule that relied on Cursor auto-applying
   based on file glob needs re-thinking in Claude Code — either bake the
   context into CLAUDE.md globally, or have a subagent the user invokes
   explicitly.

2. **`alwaysApply: true` rules.** If they were always-on, don't become a
   subagent (which is on-demand). They become part of `CLAUDE.md`.

3. **`@` references in Cursor rules.** `@Codebase`, `@Web`, `@Docs` mean
   something specific to Cursor. Remove them — Claude Code has its own
   set (`Read`, `Grep`, `WebFetch`, etc.).

4. **Model assumptions.** If your Cursor rule said "use Claude Opus", that
   was a hint to Cursor's model router. Claude Code picks based on the
   user's current CLI session — don't put model-name strings in agent
   prompts.

5. **PII.** Same as migrating anywhere — grep for the previous company's
   name, domain, project slugs. Scrub before the move.

---

## Doing this by hand

1. Create `~/.claude/` directory tree: `mkdir -p ~/.claude/{agents,skills,hooks,projects/-/memory}`
2. Copy Cursor User Rules content → `~/.claude/CLAUDE.md` (open Cursor Settings → Rules → User Rules, copy, paste).
3. `<project>/.cursorrules` → `<project>/CLAUDE.md` (rename).
4. For each `.cursor/rules/*.mdc`:
   - Decide: role-scoped (→ agent) vs procedural (→ skill) vs always-on (→ merge into CLAUDE.md)
   - Convert front-matter to Claude Code's shape
   - Drop into the right directory
5. MCP config: re-add each server via `claude mcp add` CLI.
6. Close Cursor, open a terminal in the project, run `claude` — verify your voice carries across, memory lookups work, and any subagents invoke correctly.

30-60 minutes for a non-trivial setup.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the whole thing in a single command:

```
npx portable migrate --from cursor --to claude-code
```

Reads your Cursor project + User Rules, maps each MDC rule to the right
Claude Code destination (agent vs skill vs inline), scrubs PII, and emits
the file tree for your review before writing.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at **$29**,
then $49 forever. One-time payment, every future tool in the Foundry
Practitioner Toolkit included free.

- [Grab a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
