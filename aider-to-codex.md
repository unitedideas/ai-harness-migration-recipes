# How to migrate your Aider agent to Codex

**TL;DR** — Aider uses a flat `.aider.conf.yml` with `system_prompt` as a
single string; Codex uses `~/.codex/AGENTS.md` (Markdown rules file) + `config.toml`
(structured config). Migrating means extracting your Aider prompt into `AGENTS.md`,
converting YAML config into TOML, and moving MCP servers into `config.toml`.
Skills transfer 1:1. You gain Codex's TOML-based clarity and optional project-level
overrides; you lose Aider's simplicity (one config file becomes two, one in TOML).

---

## The file layouts

### Aider (source)

```
<project-root>/
├── .aider.conf.yml           # per-project config (YAML)
├── CONVENTIONS.md            # optional: broader project context
└── .aiderignore              # exclusions (gitignore syntax)

~/.aider/
├── .aider.conf.yml           # user-level fallback config
├── prompts/                   # optional: reusable prompt files
└── <model-name>.yaml         # optional: per-model settings
```

### Codex (destination)

```
~/.codex/
├── AGENTS.md                 # identity + top-level preferences (replaces CONVENTIONS.md)
├── config.toml               # structured config (MCP, model, approvals)
├── agents/
│   └── <agent-name>.md       # optional: project-specific agents
└── skills/
    └── <skill-name>/
        └── SKILL.md          # identical to Aider format

<project-root>/
└── AGENTS.md                 # project-level rules (optional override)
```

**Structural difference:** Aider keeps everything in one YAML file per directory
(global + project). Codex separates rules (`AGENTS.md`) from config (`config.toml`),
allowing per-project rule overrides without duplicating config.

---

## Mapping each piece

### `.aider.conf.yml` system_prompt → `~/.codex/AGENTS.md`

Aider's monolithic prompt becomes Codex's Markdown rules file.

**In Aider (`~/.aider.conf.yml`):**
```yaml
system_prompt: |
  You are a senior backend engineer with 15 years of experience in distributed systems.
  
  ## Core principles
  - Always validate input at system boundaries
  - Write tests before implementation
  - Prefer explicit error handling over silent failures
  
  ## Python best practices
  When writing Python:
  - Use type hints
  - Follow PEP 8
  - Prefer dataclasses over NamedTuple
  
  ## Project context
  This is a microservices architecture. Remember:
  - All services communicate via gRPC
  - Use structured logging (JSON format)
  - Monitor distributed traces via Jaeger
```

**In Codex (`~/.codex/AGENTS.md`):**
```markdown
# Senior Backend Engineer

You are a senior backend engineer with 15 years of experience in distributed systems.

## Core Principles
- Always validate input at system boundaries
- Write tests before implementation
- Prefer explicit error handling over silent failures

## Python Best Practices

When writing Python:
- Use type hints
- Follow PEP 8
- Prefer dataclasses over NamedTuple

## Project Context

This is a microservices architecture. Remember:
- All services communicate via gRPC
- Use structured logging (JSON format)
- Monitor distributed traces via Jaeger
```

**Key differences:**
- Aider uses a YAML `system_prompt:` field with escaped newlines
- Codex uses a plain Markdown file (no escaping needed)
- Codex treats the H1 title (`# Senior Backend Engineer`) as the identity
- Codex files are easier to read and version-control (plain text, natural formatting)

**Migration steps:**
1. Create `~/.codex/AGENTS.md`
2. Extract the `system_prompt:` value from `.aider.conf.yml`
3. Remove the YAML escaping (`\n` → newlines)
4. Add an H1 title at the top (e.g., `# Your Role`)
5. Keep all H2+ sections as-is

---

### `.aider.conf.yml` config settings → `config.toml`

Aider's config becomes Codex's structured TOML file.

| Aider setting | Codex config.toml | Notes |
|---|---|---|
| `model: claude-3-5-sonnet` | `[model]`<br>`default = "claude-3-5-sonnet"` | Format differs; value identical |
| `api_key: <key>` | Environment: `ANTHROPIC_API_KEY` | Don't hardcode in config |
| `auto_commit: true` | (no equivalent) | Use Git hooks instead |
| `auto_commits_message: "..."` | (no equivalent) | Document in project AGENTS.md |

**Create `~/.codex/config.toml`:**
```toml
[model]
default = "claude-3-5-sonnet-20241022"

[mcp]
# MCP servers defined here (see MCP section below)

[approvals]
# Any approval workflows or feature flags
```

**If per-project config is needed**, create `<project-root>/AGENTS.md` with
overrides (e.g., project-specific rules). Codex will layer project-level
`AGENTS.md` on top of `~/.codex/AGENTS.md`.

---

### `.aider.conf.yml` MCP servers → `config.toml`

Aider (≥v0.75) supports MCP servers in `.aider.conf.yml`:
```yaml
mcp_servers:
  - name: filesystem
    command: npx
    args:
      - "@modelcontextprotocol/server-filesystem"
      - /home/user
```

Codex's equivalent in `config.toml`:
```toml
[mcp.filesystem]
command = "npx"
args = [
  "@modelcontextprotocol/server-filesystem",
  "/home/user"
]
```

**Migration:**
- Convert YAML list format to TOML table format
- Each server becomes `[mcp.<server-name>]`
- String values stay strings; arrays stay arrays

---

### `.aider.conf.yml` → Per-project overrides

Aider allows per-project `.aider.conf.yml` in `<project-root>/`:
```yaml
# .aider.conf.yml (project-level)
# This overrides ~/.aider.conf.yml
system_prompt: |
  ...project-specific rules...
```

Codex equivalent: Create `<project-root>/AGENTS.md`:
```markdown
# Project-Specific Rules

This document overrides ~/.codex/AGENTS.md for this project.

## Project Context
This is the auth subsystem. Focus on:
- Session token lifecycle
- CSRF protection
```

Codex will **layer** the project `AGENTS.md` on top of the global one
(unlike Aider, which replaces wholesale). If you want a complete override,
include all sections in your project `AGENTS.md`.

---

### `.aiderignore` → `.codexignore` or project `AGENTS.md`

Aider's `.aiderignore` (gitignore syntax) excludes files from context:
```
*.log
__pycache__/
.env
node_modules/
```

Codex doesn't have a built-in ignore file. Instead:
- **Respect `.gitignore` by default** (Codex does this)
- **For project-specific exclusions**, document them in `<project-root>/AGENTS.md`:
  ```markdown
  ## File Exclusions
  - Exclude `__pycache__/`, `*.log`, `.env`, `node_modules/` from context
  - Always ignore build artifacts and vendored dependencies
  ```

**Best practice:** Delete `.aiderignore` and rely on `.gitignore`. If you need
Codex-specific exclusions, add them to your project's `AGENTS.md` as a
reminder (Codex doesn't enforce this, but you'll remember to exclude them
during conversations).

---

## What you gain moving to Codex

- **Separation of concerns.** Rules (`AGENTS.md`) and config (`config.toml`)
  are now in separate files. Easier to version-control and share rules without
  sharing API keys or model preferences.

- **Clearer config format.** TOML is more readable than YAML with escaped
  newlines. MCP servers are explicit `[mcp.name]` tables, not a confusing
  nested YAML list.

- **Project-level rule layers.** Codex combines global + project `AGENTS.md`
  files. Aider requires per-project `.aider.conf.yml` that completely overrides
  the global one.

- **Markdown rules file.** `AGENTS.md` is plain Markdown, easier to read than
  YAML with embedded multi-line strings. Diff'ing rules is clearer.

- **Skills are identical.** Skills transfer 1:1 from Aider to Codex (both use
  `~/.codex/skills/<name>/SKILL.md` format).

---

## What you lose moving to Codex

- **Single-file config.** You now need both `AGENTS.md` and `config.toml`.
  Remembering where each setting goes takes practice.

- **Auto-commit hooks.** Aider's `auto_commit: true` has no equivalent. You
  need to manually commit or use Git hooks.

- **Monolithic prompt.** Codex's `AGENTS.md` still expects a single prompt
  (unlike Claude Code's subagent system). You can't split identity across
  multiple agents unless you create separate files in `~/.codex/agents/`.

- **Feature parity.** Codex has fewer features than Aider (no API version
  pinning, no model fallback on rate-limit, etc.).

---

## Migration checklist

- [ ] Extract `system_prompt` from `~/.aider.conf.yml` (or global + project
      level) → Create `~/.codex/AGENTS.md` with Markdown formatting
- [ ] Add H1 title at the top of `AGENTS.md` (e.g., `# Your Role`)
- [ ] Unescape YAML newlines (`\n` → actual newlines)
- [ ] Create `~/.codex/config.toml` with model and any global config
- [ ] Convert `mcp_servers` from YAML list → TOML tables in `config.toml`
- [ ] If you have per-project `.aider.conf.yml`, create `<project-root>/AGENTS.md`
      (optional, only if project-specific rules differ)
- [ ] Delete `.aider.conf.yml` and `.aiderignore` (no longer needed)
- [ ] Delete or archive `CONVENTIONS.md` if it exists (rules now in `AGENTS.md`)
- [ ] Test: Run `codex chat` or open a new session in Codex; verify your rules
      load and match your intent
- [ ] Commit `.codex/` directory and project `AGENTS.md` to version control

---

## Pitfalls

**Silent breakage 1: Forgetting to unescape YAML newlines**
If you copy the `system_prompt` string from YAML directly, it will still have
`\n` escape sequences. Markdown doesn't interpret these; your rules will appear
as a single wrapped line. **Always unescape:**
```yaml
system_prompt: |
  Line 1\nLine 2\nLine 3
```
becomes:
```markdown
Line 1
Line 2
Line 3
```

**Silent breakage 2: Missing H1 title**
Codex uses the H1 (`# Title`) in `AGENTS.md` as the agent name. Without one,
Codex may not recognize the file or may use a generic fallback. **Always start
with `# Your Role` or similar.**

**Silent breakage 3: Per-project rules overriding too much**
Unlike Aider (which replaces wholesale), Codex **layers** project `AGENTS.md`
on top of global. If you want a completely different ruleset for a project,
you'll need to duplicate the core identity in the project file (Codex doesn't
have a "fully override" mode). **Recommendation:** keep project files minimal,
only adding project-specific context.

**Silent breakage 4: TOML syntax errors**
If you hand-edit `config.toml` and make a syntax error, Codex may silently
fail to load it. **Always validate TOML** with a tool like:
```bash
python3 -c "import tomllib; tomllib.load(open('config.toml'))"
```

**Silent breakage 5: MCP servers with complex args**
If your MCP server command has spaces or special characters, TOML arrays
require careful escaping:
```toml
# ❌ Wrong — space in arg will break
args = ["server-filesystem /home/user data"]

# ✅ Correct — separate args
args = ["server-filesystem", "/home/user", "data"]
```

**Silent breakage 6: Model names changing**
Codex might use a different model name format than Aider. Verify your model
name in Codex's docs before setting `config.toml`. For example:
- Aider: `claude-3-5-sonnet-20241022`
- Codex: May need a different format depending on Codex version

Check Codex's model list:
```bash
codex models list
```
