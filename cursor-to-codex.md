# How to migrate your Cursor agent to Codex

**TL;DR** — Cursor stores rules as multi-file MDC files with glob-based
scoping; Codex uses a monolithic TOML config (`~/.codex/config.toml`) plus
global rules in `~/.codex/AGENTS.md`. Migrating means converting Cursor's
project-scoped `.cursor/rules/*.mdc` files into global agent rules, deciding
what to keep as project-level `AGENTS.md` overrides, and remapping Cursor's
Settings UI configuration into Codex's TOML structure. You'll also lose
Cursor's glob-based auto-scoping — Codex applies rules more coarsely.

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
    ├── mcp.json              # MCP server configuration
    └── settings.json         # project overrides (rarely used)

<cursor-user-settings>/       # Cursor's user-level config (Settings UI)
└── User Rules                # global rules (a big textarea)
```

### Codex (destination)

```
~/.codex/
├── config.toml              # user-level config (TOML, 200+ keys)
├── AGENTS.md                # global rules (Markdown)
├── rules/
│   ├── <name>.md            # optional rule files (referenced in AGENTS.md)
│   └── ...
├── skills/
│   ├── <name>/              # skill directories
│   │   ├── SKILL.md
│   │   └── ...
│   └── ...
└── .system/                 # OpenAI system skills (read-only)

<project-root>/
└── AGENTS.md                # project-level overrides (optional, trusted projects only)
```

**Structural challenge:** Cursor's project-scoped rules (`.cursor/rules/*.mdc`)
are not natively supported in Codex. You must either:
- Hoist them to `~/.codex/AGENTS.md` (making them global), or
- Create a project-level `<project-root>/AGENTS.md` override (Codex trusts only
  explicitly-approved projects to override)

Codex's TOML config is much larger and more structured than Cursor's
`settings.json` — it controls model selection, timeout, logging, auth, and
more. A direct port isn't possible; you'll cherry-pick values.

---

## Mapping each piece

### Cursor User Rules + `.cursorrules` → `~/.codex/AGENTS.md`

Cursor's UI-based User Rules become the global Codex rules file.

**In Cursor:**
```
User Rules (Settings UI):
You are a Go expert. Always use context.Background() for root contexts.
Error handling is mandatory. Check every return value.

.cursorrules (project file):
This is the authentication subsystem. Focus on session tokens and CSRF.
```

**In Codex:**
```markdown
# ~/.codex/AGENTS.md

You are a Go expert. Always use context.Background() for root contexts.
Error handling is mandatory. Check every return value.

## Project-specific (from .cursorrules)

This is the authentication subsystem. Focus on session tokens and CSRF.
```

If you have many separate `.mdc` files in `.cursor/rules/`, extract each one
and add it as a section in `AGENTS.md` with a comment describing its original
scope.

### `.cursor/rules/*.mdc` (multi-file rules) → `~/.codex/AGENTS.md` sections

Each `.cursor/rules/<name>.mdc` file has front-matter controlling scope:

```yaml
---
description: Use when reviewing Go code for correctness
globs: ["**/*.go"]
alwaysApply: false
---
Go-specific review guidance...
```

**Convert to:** A section in `~/.codex/AGENTS.md` or a separate file under
`~/.codex/rules/` and referenced in `AGENTS.md`:

```markdown
# Go code review (originally scoped to **/*.go, alwaysApply: false)

When reviewing Go code for correctness, remember:
- Check error handling patterns
- Verify context propagation
- Look for goroutine leaks
```

**If `alwaysApply: true`**, merge unconditionally. **If `alwaysApply: false`**,
add a comment explaining when to manually invoke it. Codex doesn't have
glob-based auto-scoping — you lose the ability to scope rules to file types.

### `.cursor/mcp.json` → `~/.codex/config.toml`

Codex supports MCP servers natively in TOML format:

```toml
# ~/.codex/config.toml
[[mcp_servers]]
name = "mcp-server"
command = "python"
args = ["-m", "mcp_server"]

[[mcp_servers]]
name = "github"
command = "python"
args = ["-m", "mcp_github"]
```

MCP tool interfaces transfer cleanly — both use JSON-RPC. Just convert from
Cursor's JSON object to Codex's TOML array-of-tables format.

### Cursor `settings.json` → `~/.codex/config.toml`

Cursor's `settings.json` is sparse (model, theme, a few toggles). Codex's
`config.toml` is comprehensive. Map the most important values:

| Cursor | Codex | Notes |
|---|---|---|
| `model` (e.g., `gpt-4o`) | `[chat]\nmodel = "gpt-4o"` | Codex adds a `[chat]` section for LLM settings |
| `temperature` | `[chat]\ntemperature = 0.7` | Same semantics |
| `theme` | `[ui]\ntheme = "dark"` | Codex supports themes |
| N/A | `[logging]\nlevel = "info"` | Codex has no equivalent; defaults to `info` |
| N/A | `[timeout]\nrequest_ms = 30000` | Codex is more explicit about request timeouts |

See `~/.codex/config.toml` (if Codex is already installed) or
[official Codex config reference](https://codex.openai.com/docs/config) for
the full key list.

### Project-scoped rules → `<project-root>/AGENTS.md`

If you want project-specific rules *without* making them global, create
`./<project-root>/AGENTS.md`:

```markdown
# Project-specific rules for this repo

## Auth subsystem context
This is the authentication subsystem. Focus on session tokens and CSRF.

## Test guidelines
- 100% coverage for security-sensitive paths
- Use table-driven tests for parser functions
```

Codex will merge this with global `~/.codex/AGENTS.md` when running in this
project directory. But Codex only trusts explicitly approved projects — you'll
see a prompt the first time it encounters a new `AGENTS.md`.

---

## What you gain moving to Codex

- **Integrated config management.** Codex's `config.toml` is a single source of
  truth for all user-level settings (model, timeout, MCP servers, logging). No
  scattered Settings UI.

- **Consistent rule format.** `~/.codex/AGENTS.md` is Markdown, a human-readable
  open standard. Same format works in Cursor, Copilot, and other tools.

- **Open-source alternative.** Codex is Apache-2.0 licensed. Cursor is
  proprietary.

- **CLI-first design.** Codex runs in the terminal; no IDE integration overhead.

## What you lose

- **Project-local vs user-global split.** Cursor distinguishes User Rules
  (global) from project `.cursorrules` (per-project). Codex has `~/.codex/AGENTS.md`
  (global) vs `<project>/AGENTS.md` (project), but requires explicit trust
  approval for the latter — less seamless.

- **Glob-based auto-scoping.** Cursor's `globs: ["**/*.go"]` auto-applies a rule
  to Go files. Codex has no equivalent. You lose automatic context routing; all
  rules apply to all files.

- **Multi-file rule organization.** Cursor's `.cursor/rules/` lets you break rules
  into separate files (one per concern). Codex consolidates into `AGENTS.md`, which
  gets long fast.

- **Rule metadata.** Cursor's `description`, `globs`, `alwaysApply` are front-matter
  fields. Codex has no equivalent — everything is free-form Markdown.

---

## Things that will silently break

1. **`globs:` auto-scoping is gone.** If you had a rule that only applied to
   `**/*.go` files, Codex will include that text in *every* response, even for
   Python files. Comment it clearly in `AGENTS.md`.

2. **Separate rule descriptions become Markdown sections.** Cursor's `description:
   Use when reviewing Go code` is lost. Add Markdown headers (`## Go code review`)
   so you remember what each section is for.

3. **`alwaysApply: false` rules need manual invocation.** If a Cursor rule was only
   sometimes relevant, you'll need to re-mention it in conversation. Codex doesn't
   have conditional rule inclusion.

4. **Project rules require trust approval.** Codex won't load `<project>/AGENTS.md`
   without explicit user approval the first time. You'll see a security prompt.

5. **Model assumptions.** If your Cursor rule mentioned "GPT-4o", Codex may default
   to a different model depending on user config. Remove model-specific hints or
   centralize them in `[chat]\nmodel =` in `config.toml`.

6. **Tool references.** Cursor rules might reference `@Codebase`, `@Web`, `@Docs`.
   Codex's tool set is different — `git`, `bash`, `python`, `web`. Rewrite.

7. **PII.** Grep for company names, domain, project slugs. Scrub before the move.

8. **TOML syntax gotchas.** Keys are case-sensitive, strings must be quoted,
   arrays use `[[table]]` syntax. Invalid TOML will fail silently on startup.

---

## Doing this by hand

1. **Create `~/.codex/` if it doesn't exist:**
   ```bash
   mkdir -p ~/.codex
   ```

2. **Extract Cursor's User Rules → `~/.codex/AGENTS.md`:**
   - Open Cursor Settings → Rules → User Rules
   - Copy the entire text
   - Create `~/.codex/AGENTS.md` and paste it in
   ```bash
   cat > ~/.codex/AGENTS.md << 'EOF'
   You are a Go expert. Always use context.Background() for root contexts.
   Error handling is mandatory. Check every return value.
   EOF
   ```

3. **Add project-specific rules from `.cursorrules`:**
   - Append to `AGENTS.md` with a section header:
   ```bash
   cat >> ~/.codex/AGENTS.md << 'EOF'
   
   ## Project-specific context
   
   This is the authentication subsystem. Focus on session tokens and CSRF.
   EOF
   ```

4. **Extract each `.cursor/rules/*.mdc` file:**
   - For each file, read the front-matter (`description`, `globs`, `alwaysApply`)
   - Add a Markdown section to `AGENTS.md`:
   ```markdown
   ## Go code review (originally scoped to **/*.go, alwaysApply: false)
   
   When reviewing Go code:
   - Check error handling patterns
   - Verify context propagation
   - Look for goroutine leaks
   ```

5. **Port MCP config to `~/.codex/config.toml`:**
   ```toml
   [[mcp_servers]]
   name = "mcp-github"
   command = "python"
   args = ["-m", "mcp_github"]
   ```

6. **Add any critical Cursor settings:**
   ```toml
   [chat]
   model = "gpt-4o"
   temperature = 0.7
   
   [ui]
   theme = "dark"
   ```

7. **Clean up:**
   - Delete or rename `.cursor/` directory (keep backup if paranoid)
   - Grep `AGENTS.md` for PII, company names, project slugs → scrub
   - Test: run `codex` in the directory and verify AGENTS.md is loaded

**Typical `~/.codex/AGENTS.md` structure:**

```markdown
# Global Agent Rules

You are a Go backend engineer with 10 years of experience.

## Core principles

- Always check error returns
- Use structured logging
- Context propagation is non-negotiable

## Go code review (originally scoped to **/*.go)

When reviewing Go code:
- Verify goroutine cleanup
- Check for race conditions
- Ensure proper error wrapping

## Project context (from .cursorrules)

This is the auth subsystem. Focus on:
- Session token lifecycle
- CSRF protection
- Login/logout flows

## Test guidelines (originally alwaysApply: false)

Invoke this when writing tests:
- 100% coverage for security-sensitive paths
- Use table-driven tests for parser functions
```

**Time:** 30-60 minutes depending on rule count and TOML complexity.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the whole thing in a single command:

```bash
npx portable migrate --from cursor --to codex
```

Reads your Cursor project + User Rules, extracts all `.mdc` rules, merges them
into `~/.codex/AGENTS.md`, converts MCP config and settings to TOML, and outputs
a ready-to-paste `config.toml` block for review.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at **$29**, then
$49 (rising as traction grows). One-time payment, every future tool in the
Foundry Practitioner Toolkit included free.

- [Grab a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
