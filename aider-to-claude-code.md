# How to migrate your Aider agent to Claude Code

**TL;DR** — Aider's flat, project-local configuration model is the opposite
of Claude Code's structured global-plus-local hierarchy. Aider stores
everything in one per-project `CONVENTIONS.md` plus a global `~/.aider.conf.yml`.
Claude Code splits identity, agents, skills, memory, and hooks into discrete
`~/.claude/` directories + a per-project `CLAUDE.md` override. Migration
is mostly about **deconstructing** Aider's flat `CONVENTIONS.md` into Claude
Code's modular pieces and gaining back subagent scoping and hook automation.

This is a **net gain** in the reverse direction: you're going from flat
config to structured, gaining back tool-scoping, subagent dispatch, skill
modularity, and automated hooks. The main loss is Aider's simplicity — you're
moving from "one config file" to "a directory structure," but gaining
expressiveness.

---

## The file layouts

### Aider (source)

```
~/.aider.conf.yml                 # user-global: model, edit-format, MCP
<project-root>/
├── .aider.conf.yml               # per-project overrides (rarely used)
├── CONVENTIONS.md                # all project instructions + agent rules
├── .aiderignore                  # context exclusions (gitignore syntax)
└── .aider/                       # runtime cache (don't migrate)
    ├── history                   # chat transcripts
    └── repo.tags.cache.v4/       # symbol index
```

### Claude Code (destination)

```
~/.claude/
├── CLAUDE.md                     # user-global identity + preferences
├── settings.json                 # permissions, hooks, MCP config
├── agents/<name>.md              # modular subagent definitions
├── skills/<slug>/SKILL.md        # modular skill definitions
├── hooks/*.py                    # lifecycle hook scripts (new capability)
├── projects/-/memory/<project>/*.md  # per-project memory
└── keybindings.json              # optional: keybinding customization
```

Key mental shift: **Claude Code loads `CONVENTIONS.md` equivalent as discrete
pieces** — agents are invocable, skills are registered by slug, memory is
auto-indexed and auto-loaded. You regain the ability to invoke a specific
agent (`/agent code-reviewer`) instead of having it always-on.

---

## Mapping each piece

### `~/.aider.conf.yml` + `.aider.conf.yml` → `~/.claude/CLAUDE.md`

Aider's config is purely **runtime settings** (model, edit format) plus
**per-project conventions embedded in CONVENTIONS.md**. Claude Code separates
them:

| Aider config                     | Claude Code destination          |
|----------------------------------|----------------------------------|
| `model:` (e.g., `claude-sonnet`) | `~/.claude/CLAUDE.md` (or per-session CLI) |
| `edit-format:` (e.g., `diff`)    | **Not applicable** (Claude Code uses built-in diffs) |
| `mcp-servers:` (if Aider ≥0.75)  | `~/.claude/settings.json` → `mcpServers` |
| Project overrides (`.aider.conf.yml`) | Skip — use per-project CLAUDE.md overrides in Claude Code instead |

Put identity preferences and global voice/style directly in `~/.claude/CLAUDE.md`.

### `CONVENTIONS.md` → `agents/` + `skills/` + `CLAUDE.md` sections

Aider's `CONVENTIONS.md` is a catch-all. Claude Code lets you split it:

**Always-on instructions** (identity, voice, patterns) → inline into `~/.claude/CLAUDE.md` as "Global rules" section.

**Agent-like rules** (e.g., "always use error handling X", "code reviewer checklist") → create `agents/<name>.md` with frontmatter:

```yaml
---
description: Code review agent for this project
tools: Read, Grep, Glob, Bash  # scoped tools if read-only agent
model: claude-opus-4-7  # optional override
---
## Code Review Checklist
- Check error handling on all IO operations
- Verify test coverage on new functions
- Flag any type assertions without guards
```

Then invoke with `/agent code-reviewer` or spawn as subagent with `Agent()` tool.

**Skill-like procedures** (e.g., "our test-running pattern", "migration procedure") → create `skills/<slug>/SKILL.md`:

```yaml
---
slug: test-migration-pattern
description: The four-step pattern for database migrations
---
## Four-Step Migration Pattern
1. Write reversible migration ...
2. Test both directions ...
```

Then reference in prompts with `/skill test-migration-pattern` or load inline where needed.

**Project-specific overrides** → create `.claude/CLAUDE.md` in the project root (if you use per-project overrides). Claude Code reads `CLAUDE.md` at the repo root as overrides to `~/.claude/CLAUDE.md`.

### `.aiderignore` → `~/.claude/settings.json` exclusions

Aider's `.aiderignore` controls what files Aider indexes for its symbol cache.
Claude Code doesn't have an equivalent exclusion file, but:

- **For general glob patterns** (node_modules, dist, .git): rely on Claude Code's
  default `.gitignore` integration — Claude Code already excludes these.
- **For tool-level restrictions**: document exclusions in `~/.claude/settings.json`
  under `allowedPaths` or tool-specific rules if you use the permissions system.

Most `.aiderignore` patterns won't need to migrate — Claude Code's context
management is different.

### Runtime cache (`.aider/history`, `.aider/repo.tags.cache.v4/`)

**Don't migrate.** These are Aider runtime artifacts. Claude Code doesn't use
them and they're tool-specific. Delete them.

---

## Things that will silently break

1. **Always-on conventions.** In Aider, anything in `CONVENTIONS.md` is
   prepended to every message. In Claude Code, you have to be explicit: either
   inline into `CLAUDE.md` or dispatch to an agent. If you relied on a 100-line
   convention being present in every turn, you now have to choose: keep it in
   `CLAUDE.md` (always-on but verbose) or make it an `agents/<name>` that you
   invoke when needed.

2. **Model selection.** Aider's `model:` in `~/.aider.conf.yml` is global —
   every session uses the same model. Claude Code lets you override per-agent
   (`model:` frontmatter in `agents/<name>.md`) or per-session (CLI flag).
   You're gaining flexibility but need to decide per-agent instead of globally.

3. **MCP servers in old Aider versions.** If your Aider is <0.75, you had no
   MCP support. After migration to Claude Code, you can use MCP — this is a
   gain, not a loss.

4. **Tool scoping.** Aider doesn't have tool scoping — the LLM sees the full
   set of tools. Claude Code lets you declare `tools: Read, Grep, Glob` on
   specific agents for read-only review flows. This is a **gain** on reverse
   migration — you're not losing it, you're gaining the ability to scope tools
   again if you want to.

5. **Git hook automation.** Aider has no hook system — you manually gate changes
   via `/accept` before they're committed. Claude Code lets you define
   `~/.claude/hooks/*.py` to run pre-commit, stop-on-failure, etc. This is a
   **gain** — you regain automation, but only if you explicitly add hooks.

6. **Per-project config overrides.** Aider's `.aider.conf.yml` per-project is
   rarely used. Claude Code's per-project `CLAUDE.md` is more standard and
   works better — this is a sideways move, mostly a gain.

---

## Doing this by hand

1. **Extract identity and voice from `CONVENTIONS.md`.**
   - Copy the opening paragraphs, any "How I operate" sections, personality
     notes into `~/.claude/CLAUDE.md`.
   - Everything else in `CONVENTIONS.md` will be split next.

2. **Create `~/.claude/CLAUDE.md` if it doesn't exist.**
   - Paste identity, voice, and project-agnostic rules.
   - Add a `## AI tools and environment` section with model preference (if you
     had one in `~/.aider.conf.yml`).
   - Add your coding standards and patterns.

3. **Extract agents from `CONVENTIONS.md`.**
   - Look for named sections or checklists (e.g., "Code Review", "Security
     Audit", "Testing Checklist").
   - Each becomes `~/.claude/agents/<lowercase-name>.md` with frontmatter:
     ```yaml
     ---
     description: One-liner description
     tools: Read, Grep, Glob, Bash  # optional: constrain if read-only agent
     ---
     ```
   - Paste the checklist body into the file.

4. **Extract skills from `CONVENTIONS.md`.**
   - Look for procedure sections ("How we migrate databases", "Pattern for
     writing tests").
   - Each becomes `~/.claude/skills/<slug>/SKILL.md`:
     ```yaml
     ---
     slug: db-migration-pattern
     description: Reversible four-step pattern
     ---
     ```

5. **Create `.claude/CLAUDE.md` in your project root (optional).**
   - If your Aider setup had project-specific rules, copy them here as
     overrides. Claude Code reads this after `~/.claude/CLAUDE.md`.

6. **Port MCP servers from `~/.aider.conf.yml` to `~/.claude/settings.json`.**
   - If you had `mcp-servers:` in Aider, convert to Claude Code's format:
     ```json
     {
       "mcpServers": {
         "server-name": {
           "command": "...",
           "args": [...]
         }
       }
     }
     ```

7. **Delete `.aider/` cache directory** — Claude Code doesn't use it.

8. **Optionally create hooks** for automation you previously relied on `/accept`
   for. For example, a `pre-commit.py` hook to validate migrations before commit.

9. **Test:** start a session with Claude Code, invoke an agent with `/agent
   <name>`, verify the tool scoping and conventions carry through.

Typical migration time: 30-60 minutes for a straightforward setup, more if
you have many interwoven conventions to split into agents/skills.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the mapping in one command:

```bash
npx portable migrate --from aider --to claude-code
```

It reads `CONVENTIONS.md` + `~/.aider.conf.yml`, auto-extracts agents
and skills into modular files, generates `~/.claude/CLAUDE.md` with
reasonable defaults, and bundles everything into the `~/.claude/`
directory structure. You review the extractions before they're applied
— nothing touches your disk without confirmation.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at
**$29**, then **$49**. One-time payment, every future tool in the
Foundry Practitioner Toolkit included free.

- [Buy a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
