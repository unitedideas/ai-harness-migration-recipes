# How to migrate your Claude Code agent to Cursor (or any other AI tool)

**TL;DR** — Every AI coding tool stores your agent differently. Claude Code uses `~/.claude/` with `CLAUDE.md` + `agents/` + `skills/`. Cursor uses `.cursor/rules/*.mdc`. Codex uses `~/.codex/`. Moving between them by hand means rewriting your system prompt in a new format and hoping you didn't miss anything.

Below is the manual recipe for the most common migration — Claude Code → Cursor — including every file that needs to move, the format differences to watch out for, and the subtle things that will silently break if you copy-paste. At the end I link to a one-command tool that does this automatically, because after doing it by hand twice I stopped doing it by hand.

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

Most important field is `CLAUDE.md` — that's your identity. Everything else is incremental.

### Cursor (destination)

```
<project-root>/
├── .cursorrules                  # project-level rules (distilled)
└── .cursor/rules/
    ├── <role>.mdc                # MDC-format rule with front-matter
    └── ...
```

Two structural differences matter:

1. **Cursor is project-local by default.** Your `.cursor/rules/` lives in a *project*, not your home directory. Claude Code is the opposite — `~/.claude/` is global. So a 1-to-1 copy means your rules only apply to one project. For global rules use Cursor's `Settings > Rules > User Rules`.

2. **Cursor uses `.mdc`, not `.md`.** MDC is Markdown plus a YAML-ish front-matter block Cursor reads for `description`, `globs`, and `alwaysApply`. A plain `.md` drop-in won't be read correctly.

---

## Mapping each piece

### `CLAUDE.md` → `.cursorrules` + user rules

The top-level `CLAUDE.md` lives in `~/.claude/` globally and also optionally in each project. Cursor splits this into two surfaces:

- **Project-level:** `.cursorrules` (plain text, at the project root). Gets loaded for every conversation in this project.
- **User-level:** Cursor Settings → Rules → User Rules (single textarea). Gets loaded for every project.

What I do: put truly-global preferences (my voice, what I hate in comments, error-handling conventions) in User Rules. Put project-specific stuff (test runner, deploy path, architecture) in `.cursorrules`. This gives the same separation as `~/.claude/CLAUDE.md` vs `<project>/CLAUDE.md`.

### `agents/<name>.md` → `.cursor/rules/<name>.mdc`

Claude Code subagents look like:

```markdown
---
name: code-reviewer
description: Reviews Go code for correctness
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review Go code. First, read...
```

Cursor rules look like:

```markdown
---
description: Use when reviewing Go code for correctness
globs: ["**/*.go"]
alwaysApply: false
---

You review Go code. First, read...
```

Field-by-field differences:

| Claude Code field | Cursor equivalent | Notes |
|---|---|---|
| `name` | (filename itself) | Cursor infers the name from the file |
| `description` | `description` | Same |
| `tools` | — | Cursor doesn't expose per-rule tool allowlists |
| `model` | — | Cursor picks the model globally |
| — | `globs` | Cursor needs this to auto-apply the rule to file types |
| — | `alwaysApply` | Default false; set true for rules you want in every message |

You lose the per-agent tool allowlist on the Cursor side. If your code-reviewer agent was carefully scoped to read-only, there's no equivalent in Cursor's model. This is a real loss, not something you can translate.

### `skills/<slug>/SKILL.md` → `.cursor/rules/skill-<slug>.mdc`

Skills are the cleanest 1-to-1 mapping because both are "procedural knowledge a coding agent can load on demand". The front-matter fields line up and the body ports over verbatim.

Watch out: skills in Claude Code live in a directory per skill (`skills/<slug>/SKILL.md`) because they can have asset files alongside. Cursor flattens this to a single file — if your skill includes `assets/template.tsx`, that asset has nowhere to go. You either inline the asset content as a code block or keep the template in your repo and reference it by path.

### `projects/-/memory/*.md` → `.cursor/rules/mem-*.mdc`

Claude Code's auto-memory lives as individual files indexed by `MEMORY.md`. There's no Cursor equivalent. Your options:

- **Accept the loss.** Memories are often stale anyway.
- **Manually promote the load-bearing ones to `.cursorrules` or a user-level rule.**
- **Squash them all into one `mem-summary.mdc` rule.** Works but loses the per-memory context.

### Hooks (`~/.claude/hooks/*.py`)

**These don't port.** Cursor doesn't have a hook system. If you rely on hooks (stop-hook enforcement, autonomy gates, etc.) you lose that capability by moving to Cursor. Document what each hook did, note the gap, plan to re-implement anything critical at the application layer.

### MCP servers

Both tools support MCP, but the wiring is different:

- **Claude Code:** `claude mcp add` CLI or `~/.claude/settings.json` under `mcpServers`.
- **Cursor:** `.cursor/mcp.json` (project) or user settings.

A remote streamable-http MCP server works identically — just paste the URL into whichever config format the tool expects. Stdio MCPs (running a local binary) work in both but with slightly different config shapes.

---

## Things that will silently break

1. **Relative paths in your CLAUDE.md.** If you wrote `read /Users/you/.claude/scripts/foo.sh`, that path is baked in. Cursor won't have `~/.claude/scripts/` so the agent will get a file-not-found.

2. **Tool name assumptions.** If your CLAUDE.md says "use the `Bash` tool", Cursor's tool is just `run_terminal_cmd`. The model is smart enough to translate but the prompt reads awkwardly.

3. **`$ARGUMENTS` and other Claude Code template variables.** If your slash commands reference `$ARGUMENTS`, Cursor won't expand them.

4. **Models mentioned by name.** "Use Sonnet 4.6" in a Claude Code prompt is meaningless on Cursor's side — they pick the model, you don't.

5. **PII baked into memories.** Moving to a new company's tooling? Your old memories likely contain traces of the old company. Scrub before migration — `grep -r "<old-company>" ~/.claude/` is a quick first pass.

---

## Doing this by hand

1. `cp ~/.claude/CLAUDE.md /tmp/claude.md`, strip anything global vs project-specific, paste global bits into Cursor User Rules.
2. `mkdir -p <project>/.cursor/rules`
3. For each file in `~/.claude/agents/`: rewrite front-matter to Cursor's MDC shape, rename to `.mdc`, drop into `.cursor/rules/agent-<name>.mdc`.
4. Same for `~/.claude/skills/<slug>/SKILL.md` → `.cursor/rules/skill-<slug>.mdc`.
5. Skim your memory files, promote 2-3 load-bearing ones, delete the rest.
6. Set up MCP servers in Cursor's format (if any).
7. Restart Cursor. Sanity-check a few prompts to make sure your voice is preserved.

Figure 30-60 minutes if you have a non-trivial setup, less if you're starting fresh.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does this whole thing in a single command:

```
npx portable migrate --from claude-code --to cursor
```

It reads `~/.claude/` (or the project copy), maps everything to Cursor's layout, scrubs PII, signs the bundle with ed25519 so the receiving side can verify provenance, and emits the file tree. You get to review everything before it's applied — nothing auto-writes to your disk without your OK.

It supports the same thing in reverse (Cursor → Claude Code), and across 10+ other tools (Codex, Aider, Continue, Cline, Goose, Zed, Roo Code, plus ChatGPT / Claude.ai paste interfaces and a Copilot write path). 

Launch pricing: first 10 buyers at $19 lifetime, next 10 at $29, then $49 forever. One payment, every current feature + every future tool in the Foundry Practitioner Toolkit.

[Grab a $19 slot →](https://bringyour.ai/buy) · [See how it works →](https://bringyour.ai/how-it-works)

---

## Footnote — why this exists

I wrote BringYour after migrating my own harness Claude Code → Cursor → Codex → back to Claude Code in a 3-month span as I was testing which tool fit different projects. Every time I did it by hand, I'd lose something — a memory I'd forgotten to bring, a hook I'd relied on, a skill I hadn't promoted to a rule. The tool is the accumulation of all the small things I kept missing.
