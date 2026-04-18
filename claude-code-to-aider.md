# How to migrate your Claude Code agent to Aider

**TL;DR** — Aider's configuration model is about as different from Claude
Code's as AI tools get. Claude Code lives in `~/.claude/` with a global
`CLAUDE.md` plus discrete `agents/`, `skills/`, and `hooks/` directories.
Aider lives in `~/.aider.conf.yml` (user-global) plus `.aider.conf.yml`
+ `.aiderignore` + `CONVENTIONS.md` (per project) — one config file, no
subagents, no skills, no hooks. Migration is mostly about **distilling**
Claude Code's scattered pieces into Aider's flat surfaces.

This is a one-way trip in the sense that a round-trip (Claude Code →
Aider → Claude Code) loses fidelity. Aider's model just can't hold
everything Claude Code can express. Below is what actually ports cleanly,
what needs manual consolidation, and what you'll lose outright.

---

## The file layouts

### Claude Code (source)

```
~/.claude/
├── CLAUDE.md                     # identity + top-level preferences
├── settings.json                 # permissions, hooks, MCP wiring
├── agents/<name>.md              # subagent definitions (frontmatter + body)
├── skills/<slug>/SKILL.md        # skills (frontmatter + body + assets)
├── hooks/*.py                    # lifecycle hook scripts
└── projects/-/memory/*.md        # persistent memory files
```

### Aider (destination)

```
~/.aider.conf.yml                 # user-global config + model + edit fmt
<project-root>/
├── .aider.conf.yml               # per-project overrides
├── .aiderignore                  # gitignore-style exclusion from context
├── CONVENTIONS.md                # project's coding conventions (auto-loaded)
└── .aider/                       # runtime cache — don't edit
    ├── history                   # chat transcripts
    └── repo.tags.cache.v4/       # symbol index
```

Key mental shift: **Aider loads CONVENTIONS.md into every prompt
automatically**, like a project-scoped prepend. There's no concept of
"subagent" you invoke on demand — either the instruction is in every
message (via CONVENTIONS.md) or it isn't there at all.

---

## Mapping each piece

### `CLAUDE.md` → `~/.aider.conf.yml` + `CONVENTIONS.md`

Claude Code's `CLAUDE.md` mixes three things:
- **Identity** ("I'm a senior Go engineer, I hate…")
- **Global preferences** (model choice, tool allowlists, always-on rules)
- **Project-specific** (architecture, test runner, deploy path)

Aider separates them:

| Claude Code content                          | Aider destination                 |
|----------------------------------------------|-----------------------------------|
| Identity / voice / style / comment rules     | `CONVENTIONS.md` (per project)    |
| Model choice (`"use Sonnet 4.6"`)            | `~/.aider.conf.yml` → `model:` key|
| Tool restrictions                            | **No direct equivalent** (see losses) |
| Project architecture / test runner / deploys | `CONVENTIONS.md` (per project)    |

Rule of thumb: if the content would apply to **every** repo you work in,
it's user-global — split it out into prose that you append to each
project's `CONVENTIONS.md`, or maintain one "base conventions" file and
`cat base-conventions.md project-specifics.md > CONVENTIONS.md` per
project.

### `agents/<name>.md` → prompts, not subagents

Aider has no subagent system. A Claude Code `code-reviewer` agent
doesn't become a file you can invoke. Closest equivalents:

- **If the agent is always-relevant** (e.g., "always enforce error
  handling patterns"): inline its body into `CONVENTIONS.md`.
- **If the agent is occasional** (e.g., "review security when I say
  /security"): create a short shell alias or keyboard macro that pipes
  the agent's prompt into Aider as a user message. Aider doesn't have a
  registered-command concept.
- **If the agent was scoped to read-only** (via Claude Code's
  `tools: Read, Grep, Glob, Bash`): that scoping has NO equivalent —
  document it in a comment and rely on reviewing Aider's diff before
  accepting changes (`/accept` flow).

This is real capability loss. Don't migrate security-critical
read-only subagents to Aider expecting the tool guardrails to carry
over.

### `skills/<slug>/SKILL.md` → `CONVENTIONS.md` section OR prompt snippet

Skills are procedural knowledge. Aider doesn't load on-demand docs the
way Claude Code does, but:

- **Short, always-relevant skills** (e.g., "how we format migrations"):
  inline into `CONVENTIONS.md` as a named section.
- **Long, occasional skills** (e.g., "how to debug the websocket race"):
  keep as a standalone markdown file and `/read <path>` it into Aider's
  chat context when needed — that's Aider's ergonomic for pulling in a
  doc ad-hoc.
- **Skills with assets** (templates, schemas): Aider can `/read` those
  too, but there's no auto-bundling. Document the asset paths in the
  `CONVENTIONS.md` section and rely on the user to `/read` them
  explicitly.

### `projects/-/memory/*.md` → prose on `CONVENTIONS.md`, aggressively pruned

Claude Code's auto-memory is a long tail of small notes indexed by
`MEMORY.md`. Aider has no equivalent. Your options:

- **Skip the migration.** Most memories go stale. If nothing has
  referenced a memory in weeks, delete it.
- **Promote the load-bearing ones** (invariants, hard-won lessons,
  project-specific gotchas) into a `## Lessons learned` section in
  `CONVENTIONS.md`.
- **Keep historical memories in a separate file** that Aider doesn't
  auto-load — e.g., `docs/agent-memories.md` in the repo. When a
  relevant one comes up, `/read` it into Aider's context.

### Hooks (`~/.claude/hooks/*.py`)

**These don't port.** Aider has no hook system. If you rely on hooks
(stop-hook enforcement, autonomy gates, git-commit validators), you
lose that capability moving to Aider. Options:

- **Re-implement at the shell layer** — e.g., a git pre-commit hook
  that runs the same check Claude Code's stop-hook ran.
- **Rely on Aider's built-in /commit flow** — Aider shows the diff
  before committing; the human gates instead of the hook.

### MCP servers

Aider added MCP support in v0.75 (check your Aider version with
`aider --version`). Config lives in `~/.aider.conf.yml` under the
`mcp-servers:` key — YAML equivalent of Claude Code's
`settings.json > mcpServers`. Same JSON-RPC spec under the hood.

If your Aider is older than v0.75, you lose MCP — note the gap and
either upgrade or plan around it.

### Model selection

Aider picks the model globally via `~/.aider.conf.yml`:

```yaml
model: anthropic/claude-sonnet-4-5
```

Or via environment:

```bash
ANTHROPIC_API_KEY=sk-ant-... aider --model sonnet
```

Claude Code picks via CLI session / per-agent `model:` frontmatter.
For Aider, you pick one model and it's used for every turn — no per-
subagent override.

---

## Things that will silently break

1. **Slash commands that reference `$ARGUMENTS`.** If your Claude Code
   setup had slash commands like `/test $ARGUMENTS`, Aider won't
   expand those. Replace with shell aliases.

2. **Agent-scoped file-read restrictions.** A Claude Code subagent
   declared `tools: Read, Grep, Glob` could only read — Aider has no
   equivalent, all context is the same context.

3. **Branded tool names in prompts.** "Use the `WebFetch` tool" in
   CLAUDE.md is meaningless to Aider (which has `/web`). Strip or
   rewrite.

4. **Auto-loaded memory.** Anything that relied on `projects/-/memory/`
   being auto-prepended to every turn now needs to be either inlined
   in `CONVENTIONS.md` or explicitly `/read` each session.

5. **PII scrub.** Claude Code's hooks may have had a PII-scrub hook.
   Aider doesn't — you manually ensure the codebase you're editing is
   free of the previous company's secrets before editing.

---

## Doing this by hand

1. `~/.aider.conf.yml`: pick a model, set `edit-format: diff`,
   configure your Anthropic/OpenAI key.
2. `cd <project>`; `touch CONVENTIONS.md`.
3. Read your `~/.claude/CLAUDE.md`. Copy identity + project-applicable
   rules into `CONVENTIONS.md`. Leave model references behind (those
   go in `~/.aider.conf.yml`).
4. For each `~/.claude/agents/<name>.md`:
   - Always-relevant? → inline into `CONVENTIONS.md` as a `## <Name>
     checklist` section.
   - Occasional? → save the body as `docs/prompts/<name>.md` in the
     repo; `/read docs/prompts/<name>.md` when needed.
5. For each `~/.claude/skills/<slug>/SKILL.md`: same split as agents.
6. Promote 2-3 load-bearing memory files into `CONVENTIONS.md`; archive
   the rest or delete.
7. Port MCP servers via the `mcp-servers:` key if your Aider is ≥0.75.
8. Add a `.aiderignore` that mirrors your repo's `.gitignore` plus any
   heavy files you don't want in Aider's symbol index.
9. Run `aider` from the repo root; sanity-check a prompt to verify the
   conventions carry through.

Figure 60-90 minutes for a non-trivial setup, more if you have many
custom agents/skills to inline.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the mapping in one command:

```
npx portable migrate --from claude-code --to aider
```

It reads `~/.claude/`, inlines agents + skills into a generated
`CONVENTIONS.md` (flagging what it couldn't map), writes
`~/.aider.conf.yml` with reasonable defaults, and emits an
`.aiderignore` stub. You review everything before it's applied —
nothing touches your disk without confirmation.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at
**$29**, then **$49**. One-time payment, every future tool in the
Foundry Practitioner Toolkit included free.

- [Buy a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
