# How to migrate your Codex agent to Aider

**TL;DR** — Codex stores rules in `~/.codex/AGENTS.md` (Markdown) + `~/.codex/config.toml`
(TOML config); Aider uses a single `.aider.conf.yml` (YAML per project or user). Migrating
means collapsing Codex's two-file structure into Aider's one-file model, converting TOML
to YAML, and flattening Codex's optional project-level `AGENTS.md` overrides into a single
config file. You lose Codex's structural clarity but gain Aider's simplicity (one file per
directory).

---

## The file layouts

### Codex (source)

```
~/.codex/
├── AGENTS.md                # identity + rules (Markdown)
├── config.toml              # structured config (TOML)
├── agents/
│   └── <agent-name>.md      # optional: project-specific agent definitions
└── skills/
    └── <skill-name>/
        └── SKILL.md         # reusable skills

<project-root>/
└── AGENTS.md                # project-level rule overrides (optional)
```

### Aider (destination)

```
<project-root>/
└── .aider.conf.yml          # per-project config (YAML)

~/.aider/
├── .aider.conf.yml          # user-level fallback config
├── prompts/                  # optional: reusable prompt files
└── <model-name>.yaml        # optional: per-model settings
```

**Structural challenge:** Codex's two-tier system (global `config.toml` + rules in `AGENTS.md`,
plus optional project overrides) becomes Aider's flat per-directory model. If you have
project-level `AGENTS.md` overrides in Codex, they must be merged into a project-level
`.aider.conf.yml` in Aider (losing the separate user/project split).

---

## Mapping each piece

### `~/.codex/AGENTS.md` (+ project-level overrides) → `.aider.conf.yml` system_prompt

Codex's Markdown rules file (with optional project-level override) becomes Aider's YAML
system_prompt string.

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

## MCP Tools

You have access to:
- `git` for version control
- `bash` for shell commands
```

**In project-level `<project-root>/AGENTS.md` (Codex override, if it exists):**
```markdown
## Project Context

This is a microservices architecture.
- All services communicate via gRPC
- Use structured logging (JSON format)
```

**In Aider (`.aider.conf.yml` or `~/.aider/.aider.conf.yml`):**
```yaml
system_prompt: |
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
  
  ## MCP Tools
  
  You have access to:
  - `git` for version control
  - `bash` for shell commands
  
  ## Project Context
  
  This is a microservices architecture.
  - All services communicate via gRPC
  - Use structured logging (JSON format)
```

**Key differences:**
- Codex uses plain Markdown files (easy to read, version-control friendly)
- Aider uses YAML with a `system_prompt:` field (single string, requires manual escaping of newlines)
- Codex's H1 title is metadata; Aider's is just documentation (include it in system_prompt as a comment/header)
- If you have a project-level `AGENTS.md` override in Codex, **merge it into the system_prompt** (there's no separate override layer in Aider)

**Migration steps:**
1. Read both `~/.codex/AGENTS.md` and any project-level `<project-root>/AGENTS.md`
2. Create `.aider.conf.yml` (in project root or `~/.aider/`)
3. Copy the Markdown content into the `system_prompt:` field
4. Preserve all section headers and content
5. If you have MCP tool references in Codex (like "You have access to: `git`, `bash`"), keep them in system_prompt

---

### `~/.codex/config.toml` → `.aider.conf.yml` root level

Codex's TOML config becomes Aider's YAML settings at the top level.

| Codex config.toml | Aider .aider.conf.yml | Notes |
|---|---|---|
| `[model]`<br>`default = "claude-3-5-sonnet"` | `model: claude-3-5-sonnet-20241022` | String value instead of table |
| `[mcp]` section (servers) | `mcp_servers:` (if Aider has this) | Usually handled via system_prompt reference |
| No direct equivalent | `auto_commit: true` | Aider supports auto-commit; use if needed |
| (auth env var) | (auth env var) | Both use `ANTHROPIC_API_KEY` environment variable |

**Example `~/.codex/config.toml`:**
```toml
[model]
default = "claude-3-5-sonnet-20241022"

[mcp]
[[mcp.servers]]
name = "github"
```

**Convert to `~/.aider/.aider.conf.yml`:**
```yaml
model: claude-3-5-sonnet-20241022
auto_commit: false  # set based on your preference
```

**Important:** Aider doesn't have a structured MCP server table like Codex. If you reference
MCP tools in Codex's config, document them in the system_prompt instead (e.g., "You have
access to the `github` MCP server for...").

---

### `~/.codex/skills/*` → `.aider/prompts/` (optional)

Codex's `skills/` directory (reusable skill definitions) maps to Aider's `prompts/` directory.

**In Codex (`~/.codex/skills/code-review/SKILL.md`):**
```markdown
# Code Review Skill

When reviewing code:
- Check for race conditions
- Verify error handling
- Ensure logging is structured
```

**In Aider (`~/.aider/prompts/code-review.md`):**
```markdown
# Code Review

When reviewing code:
- Check for race conditions
- Verify error handling
- Ensure logging is structured
```

**To use in Aider:**
```yaml
# In .aider.conf.yml:
system_prompt: |
  <your base prompt>
  
  # Code Review (see ~/.aider/prompts/code-review.md)
  [Include content from code-review.md when reviewing code]
```

Or reference them explicitly when needed in Aider (no auto-loading like Codex).

---

### `~/.codex/agents/*` → no direct equivalent

Codex's `agents/` directory (project-specific agent definitions) has **no equivalent in
Aider**. Each Aider config is itself an "agent" (one system_prompt per project or user).

**Options:**
1. **Merge all agents into one system_prompt** (recommended if you have few agents)
2. **Create separate `<project>/.aider.conf.yml` files** for each agent's project
3. **Use comments in system_prompt** to document which sections apply to which agent

**Example:** If Codex has:
```
~/.codex/agents/
├── senior-backend.md
├── junior-frontend.md
└── devops.md
```

In Aider, create:
```
~/.aider/.aider.conf.yml        # senior-backend (your primary/user-level)
<project1>/.aider.conf.yml       # junior-frontend (project-specific)
<project2>/.aider.conf.yml       # devops (project-specific)
```

Or keep one `.aider.conf.yml` and use comments to switch identities:
```yaml
system_prompt: |
  # Senior Backend Engineer
  You are...
  
  # (If you're a Junior Frontend Dev instead, replace the above with:)
  # # Junior Frontend Developer
  # You are...
```

---

## Silent breakages: Codex → Aider

### 1. Project-level rule overrides don't exist in Aider

**Problem:** Codex lets you have `~/.codex/AGENTS.md` (global) and `<project>/AGENTS.md`
(per-project override). Aider has no override layer; each `.aider.conf.yml` stands alone.

**Impact:** If you rely on project-level `AGENTS.md` in Codex, you must:
- Create a separate `.aider.conf.yml` in each project (duplicates your base system_prompt)
- Or merge project-specific context into the `~/.aider/.aider.conf.yml` (loses flexibility)

**Mitigation:** Use project-level `.aider.conf.yml` files for projects that need different
rules; use `~/.aider/.aider.conf.yml` as a fallback for projects with no local config.

### 2. No multi-file rule system

**Problem:** Codex supports `~/.codex/agents/` (named agent definitions). Aider treats
each `.aider.conf.yml` as a single agent.

**Impact:** You can't have multiple named agents sharing one directory in Aider. Each agent
needs its own project or config file.

**Mitigation:** Create separate project directories (one per agent) or store multiple
`.aider.conf.yml` files with different names and manually switch between them.

### 3. Config structure differences

**Problem:** Codex's `[mcp]` table and structured config don't map 1:1 to Aider's flat
settings.

**Impact:** MCP server definitions, approvals workflows, and other structured Codex
settings don't have direct equivalents in Aider.

**Mitigation:** Document MCP servers and approvals in the system_prompt as comments.

### 4. Skills transfer but need manual invocation

**Problem:** Codex's `skills/` directory is optional and referenced; Aider has no built-in
skill loader.

**Impact:** You must manually reference skill content in `.aider/prompts/` or inline it
into system_prompt.

**Mitigation:** Create `~/.aider/prompts/` files and refer to them in comments within
system_prompt (e.g., "See `~/.aider/prompts/code-review.md` when reviewing").

---

## Checklist

- [ ] Read `~/.codex/AGENTS.md` entirely
- [ ] Read `~/.codex/config.toml` for model, MCP servers, and any custom settings
- [ ] Check if project has a `<project-root>/AGENTS.md` override
- [ ] Create `.aider.conf.yml` (in project root or `~/.aider/`)
- [ ] Paste Codex's Markdown rules into `system_prompt:` field
- [ ] Merge any project-level Codex rules into the system_prompt
- [ ] Convert Codex's model setting to Aider's `model:` field
- [ ] Document MCP servers as comments in system_prompt
- [ ] If you have Codex `skills/`, copy them to `~/.aider/prompts/`
- [ ] Test in Aider: spawn an agent and verify it has the right identity
- [ ] Delete old `~/.codex/` config if not needed elsewhere

---

## Need help?

For more on Aider's config, see [aider.chat docs](https://aider.chat/docs/config.html).
For more on Codex's config, see [codex.sh docs](https://codex.sh).

---

**Licensed:** CC BY 4.0. Attribute to [bringyour.ai](https://bringyour.ai) if you repost.
