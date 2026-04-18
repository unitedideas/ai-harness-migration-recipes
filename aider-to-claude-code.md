# How to migrate your Aider agent to Claude Code

**TL;DR** — Aider's flat configuration model is simpler than Claude Code's
structured harness, so the reverse migration (Aider → Claude Code) is mostly
about **expanding** Aider's single `CONVENTIONS.md` prompt into Claude Code's
discrete layers: `CLAUDE.md`, agents, skills, and memory. You gain
subagents, on-demand skills, hooks, and persistent memory — but you'll need
to manually decompose Aider's monolithic prompt into these pieces.

This is a one-way trip in the sense that a round-trip (Aider → Claude Code
→ Aider) loses fidelity the other way. Claude Code's subagent system,
hooks, and persistent memory have no Aider equivalent. Below is what ports
cleanly, what needs manual decomposition, and what you'll gain.

---

## The file layouts

### Aider (source)

```
~/.aider.conf.yml                 # user-global: model, edit format, API keys
<project-root>/
├── .aider.conf.yml               # per-project config overrides
├── CONVENTIONS.md                # project-scoped instructions (always-loaded)
├── .aiderignore                  # gitignore-style exclusions
└── .aider/                        # runtime cache — don't edit
    ├── history
    └── repo.tags.cache.v4/
```

### Claude Code (destination)

```
~/.claude/
├── CLAUDE.md                      # identity + global preferences
├── settings.json                  # tool permissions, hooks, MCP wiring
├── agents/<name>.md               # subagent definitions
├── skills/<slug>/SKILL.md         # reusable knowledge + assets
├── hooks/*.py                     # lifecycle automation
└── projects/-/memory/*.md         # persistent per-project memories
<project-root>/
├── CLAUDE.md                       # project-level overrides (optional)
└── .claude/settings.json          # project-level permissions (optional)
```

Key mental shift: **Claude Code separates global identity from project
context** — your `~/.claude/CLAUDE.md` is persistent across repos, while
project `CLAUDE.md` files layer on top. Aider merges everything into
`CONVENTIONS.md`. Migration means **extracting and distributing** Aider's
flat instructions into the right layer.

---

## Mapping each piece

### `~/.aider.conf.yml` → `~/.claude/CLAUDE.md` (+ per-project `CLAUDE.md`)

Aider's config file has two sections: user-global + per-project.

| Aider setting                    | Claude Code destination          |
|----------------------------------|----------------------------------|
| `model: anthropic/claude-sonnet` | `~/.claude/CLAUDE.md` → `Model Tier Usage` table |
| `api-key:` (Anthropic/OpenAI)    | Environment: `ANTHROPIC_API_KEY` or `~/.anthropic-key` |
| `edit-format: diff`              | `~/.claude/CLAUDE.md` → `## Autonomy & Escalation` |
| Aider per-project overrides      | `<project-root>/CLAUDE.md` or `.claude/settings.json` |

Your `~/.claude/CLAUDE.md` should document:
- Which Claude model you prefer by default (Opus for complex, Sonnet for
  standard, Haiku for simple)
- API key location
- Global tool restrictions (e.g., "no direct Bash to production")

Per-project `CLAUDE.md` can override for specific repos.

### `CONVENTIONS.md` → `~/.claude/CLAUDE.md` + agents + skills + memory

This is where the real work is. Aider's `CONVENTIONS.md` is a **single
prompt** that gets loaded into every chat. Claude Code distributes the
same instructions across multiple layers:

1. **Global voice + identity** → `~/.claude/CLAUDE.md` section
   (e.g., "I'm a senior Go engineer…")

2. **Always-relevant patterns** → `~/.claude/agents/enforcement.md`
   - Example: error-handling rules, naming conventions, test structure
   - Reason: subagents can be explicitly invoked or always-on via hooks

3. **Occasional / on-demand patterns** → `~/.claude/skills/<slug>/SKILL.md`
   - Example: "how to debug the async race condition", "database migration
     checklist"
   - Reason: skills are indexed by the harness; you invoke them by name
     rather than always loading them

4. **Project-specific gotchas** → `~/.claude/projects/-/memory/<name>.md`
   - Example: "this codebase has a 15-year legacy code path that uses X"
   - Reason: memories persist across sessions; future-you will read them

**Practical strategy:**
- Split `CONVENTIONS.md` into sections
- Identity + voice → global `CLAUDE.md`
- Architecture rules → per-project `CLAUDE.md` or new agent file
- Checklists (test checklist, deploy checklist) → agents
- Reusable tricks / how-tos → skills
- "Remember that…" → memory files

### `.aiderignore` → `.claude/settings.json` + project `CLAUDE.md`

Aider's `.aiderignore` excludes files from the symbol index (so they don't
bloat context). Claude Code has similar exclusions:

| Aider                            | Claude Code                          |
|----------------------------------|--------------------------------------|
| `.aiderignore` patterns          | `.claude/settings.json` → `exclude` array |
|                                  | Or: document in project `CLAUDE.md` |

Create `.claude/settings.json` in the project root:

```json
{
  "exclude": [
    "node_modules/**",
    "*.min.js",
    "build/",
    "dist/"
  ]
}
```

Alternatively, document the exclusion reasoning in project `CLAUDE.md` and
rely on `.gitignore` (Claude Code respects `.gitignore` by default).

### MCP servers

Both tools support MCP servers (Aider ≥0.75).

| Aider                            | Claude Code                      |
|----------------------------------|----------------------------------|
| `~/.aider.conf.yml` → `mcp-servers:` | `~/.claude/settings.json` → `mcpServers` |

Copy your MCP server config directly; the JSON schema is equivalent.

### Model selection

**Aider:** One global model per user (`~/.aider.conf.yml`).
```yaml
model: anthropic/claude-sonnet-4-6
```

**Claude Code:** Per-session or per-agent choice.
```
/fast              # uses Claude Opus 4.7 for this session
/model sonnet      # switch to Sonnet for remaining turns
```

Your `~/.claude/CLAUDE.md` should document your default model choice and
when to override (e.g., "Opus for architecture, Sonnet for standard work").

---

## Things that will silently break

1. **Always-loaded prompt discipline.** Aider auto-loads `CONVENTIONS.md`
   into every turn. Claude Code does NOT auto-load `CLAUDE.md` into every
   turn — it's a reference document. If you need instructions to be always
   applied, wire them into a hook (`~/.claude/hooks/prompt_prepend.py`)
   or keep them short and pin them in your mental model, not expecting
   the tool to enforce them.

2. **No built-in `/commit` gating.** Aider shows diffs before `git commit`;
   you approve manually. Claude Code has no equivalent (the human is always
   the gate). Make sure you review diffs explicitly before committing.

3. **Chat history expectations.** Aider stores full chat transcripts in
   `.aider/history/` and loads them on context misses. Claude Code has no
   automatic chat history loading — use project memory files to store
   decisions that should persist across sessions.

4. **Filesystem context assumptions.** Aider scans the whole repo and
   builds a symbol index (`.aider/repo.tags.cache/`). Claude Code requires
   explicit reads or globs. If your prompt assumed Aider could see the
   whole codebase implicitly, rewrite it to explicitly specify which files
   to read or check.

5. **API key fallback.** Aider can use OpenAI's API without any Claude
   Code setup — if you relied on `OPENAI_API_KEY`, you'll need to switch
   to `ANTHROPIC_API_KEY` (Claude Code focuses on Anthropic models). If
   you need multi-model support, use environment variables and inline
   them.

6. **Slash command vocabulary.** Aider's `/web`, `/commit`, `/add`, `/drop`
   don't have exact Claude Code equivalents. Document any custom workflows
   you used in Aider and adapt them to Claude Code's slash commands
   (`/plan`, `/help`, `/clear`, etc.) or shell aliases.

---

## Doing this by hand

1. **Read your `CONVENTIONS.md`.** Extract three groups:
   - Identity + voice (who you are, how you speak)
   - Always-relevant rules (style, architecture, testing)
   - Occasional patterns (checklists, debugging techniques)

2. **Copy identity + voice to `~/.claude/CLAUDE.md`.**
   Keep it terse. Aider's prose doesn't need to be repeated verbatim —
   distill the essence.

3. **Create a project `CLAUDE.md`** (in the repo root).
   This is where you put project-specific context (architecture, test
   runner, deploy path, team conventions). Keep it short; future-you will
   read this every time you work in the repo.

4. **Create agents for always-on rules.**
   If `CONVENTIONS.md` had a "error handling checklist", make it
   `~/.claude/agents/error-handling.md`. You can wire it into a hook to
   always be applied, or invoke it manually as `/agent error-handling`.

5. **Create skills for reusable techniques.**
   If `CONVENTIONS.md` had a section "how to debug async deadlocks",
   make `~/.claude/skills/async-debugging/SKILL.md` with the full
   technique + code examples.

6. **Promote load-bearing notes to memory.**
   If you wrote down "this codebase has a legacy path in X.go that uses
   outdated library Y", make `~/.claude/projects/-/memory/codebase-gotchas.md`.

7. **Create `.claude/settings.json`** (project root).
   Add any file exclusions from `.aiderignore`:
   ```json
   {
     "exclude": ["node_modules/**", "*.min.js"]
   }
   ```

8. **Port MCP servers** via `~/.claude/settings.json`.
   Copy the `mcpServers` key from `~/.aider.conf.yml` → `mcp-servers`.

9. **Test a simple prompt** in Claude Code.
   Open the project, run `/help` to verify the harness is loaded, then
   ask Claude Code to do a trivial task. Verify the agent has the right
   context.

Expect 45-75 minutes for a non-trivial migration. More if `CONVENTIONS.md`
was large and you're decomposing it into many agents + skills.

---

## What you're gaining

Moving to Claude Code unlocks:

- **Subagents:** Invoke specialists by name (e.g., `/agent code-reviewer`).
  Useful for security reviews, architecture audits, on-demand expertise.
- **Skills:** Index reusable knowledge. Reference by name, auto-discovered.
- **Hooks:** Automate gates, validations, formatting. Fire at specific
  lifecycle points (before commit, before push, on tool failure).
- **Persistent memory:** `projects/-/memory/` auto-indexes across sessions.
  Future-you reads these without asking.
- **Multi-session context:** Claude Code's memory system bridges gaps Aider's
  history can't fill — especially for decision rationales and lessons
  learned.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the reverse mapping in one command:

```
npx portable migrate --from aider --to claude-code
```

It reads `CONVENTIONS.md` + project config, decomposes your Aider prompt
into separate agents, skills, and memory files, and generates a `~/.claude/`
structure with reasonable defaults. You review everything before it's
applied — nothing touches your disk without confirmation.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at **$29**,
then **$49**. One-time payment, every future tool in the Foundry
Practitioner Toolkit included free.

- [Buy a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
