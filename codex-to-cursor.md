# How to migrate your Codex agent to Cursor

**TL;DR** — Codex uses a monolithic TOML config (`~/.codex/config.toml`) plus
global rules in `~/.codex/AGENTS.md` (Markdown); Cursor stores rules as
multi-file MDC files with glob-based scoping in `.cursor/rules/*.mdc`. Migrating
means splitting Codex's single `AGENTS.md` into separate topic-focused `.mdc`
files, deciding which rules should be `alwaysApply: true` vs `false`, and
remapping Codex's TOML config into Cursor's JSON `settings.json`. You'll gain
Cursor's glob-based file-type scoping but lose the simplicity of a single rules
file.

---

## The file layouts

### Codex (source)

```
~/.codex/
├── config.toml              # user-level config (TOML)
├── AGENTS.md                # global rules (Markdown)
├── rules/
│   ├── <name>.md            # optional rule files
│   └── ...
└── skills/
    └── <name>/
        └── SKILL.md

<project-root>/
└── AGENTS.md                # project-level overrides (optional)
```

### Cursor (destination)

```
<project-root>/
├── .cursorrules             # plain-text project rules
└── .cursor/
    ├── rules/
    │   ├── <name>.mdc       # MDC-format rules (each with front-matter)
    │   └── ...
    └── mcp.json             # MCP config (JSON)

<cursor-user-settings>/      # Cursor Settings UI
└── User Rules               # global rules textarea
```

**Structural challenge:** Codex's single `AGENTS.md` must be split into
multiple Cursor `.mdc` files, each with front-matter controlling whether it
auto-applies and which file globs it targets. You'll need to manually decide:
- Which rules are always-on (core identity) vs conditional (domain-specific)
- Which rules apply to Go vs Python vs all files

---

## Mapping each piece

### `~/.codex/AGENTS.md` → Cursor User Rules + `.cursor/rules/*.mdc`

Codex's monolithic rules file must be split into Cursor's multi-file structure.

**In Codex (`~/.codex/AGENTS.md`):**
```markdown
You are a Go backend engineer with 10 years of experience.

## Core principles
- Always check error returns
- Use structured logging
- Context propagation is non-negotiable

## Go code review
When reviewing Go code:
- Verify goroutine cleanup
- Check for race conditions

## Project context
This is the auth subsystem. Focus on session tokens and CSRF.
```

**In Cursor:**
- Core principles + identity → Cursor Settings → User Rules (a textarea)
- Each section → separate `.cursor/rules/<topic>.mdc` file with front-matter

**User Rules in Cursor Settings:**
```
You are a Go backend engineer with 10 years of experience.

Core principles:
- Always check error returns
- Use structured logging
- Context propagation is non-negotiable
```

**`.cursor/rules/go-code-review.mdc`:**
```yaml
---
description: Go code review and best practices
globs: ["**/*.go"]
alwaysApply: true
---

When reviewing Go code:
- Verify goroutine cleanup
- Check for race conditions
- Ensure proper error wrapping
```

**`.cursor/rules/auth-subsystem.mdc`:**
```yaml
---
description: Authentication subsystem context
globs: ["**/auth/**", "**/*auth*.go"]
alwaysApply: false
---

This is the auth subsystem. Focus on:
- Session token lifecycle
- CSRF protection
- Login/logout flows
```

**Decision points:**
- Is this a core principle? → User Rules (Cursor Settings)
- Is this always relevant? → `alwaysApply: true` in `.mdc`
- Is this domain-specific? → `alwaysApply: false` + appropriate globs

### Project-level `AGENTS.md` → `.cursorrules`

If Codex had a project-level override:

```markdown
# project-specific context
This is the authentication subsystem...
```

**Convert to:** Plain text in `<project-root>/.cursorrules`:

```
This is the authentication subsystem. Focus on:
- Session token lifecycle
- CSRF protection
- Login/logout flows
```

Cursor loads `.cursorrules` automatically without requiring trust approval.

### `~/.codex/config.toml` → `<cursor-settings>/settings.json`

Codex's TOML config is much larger than Cursor's settings. Cherry-pick the
important values:

| Codex | Cursor | Notes |
|---|---|---|
| `[chat]\nmodel = "gpt-4o"` | `"model": "gpt-4o"` | Cursor settings are at the top level |
| `[chat]\ntemperature = 0.7` | `"temperature": 0.7` | Same semantics |
| `[ui]\ntheme = "dark"` | `"theme": "dark"` | Cursor has a Settings UI for this |
| `[logging]\nlevel = "info"` | N/A | Cursor doesn't expose logging config |
| `[timeout]\nrequest_ms = 30000` | N/A | Cursor doesn't expose timeout config |

Cursor's `settings.json` is optional — most settings live in the UI. If you had
no special Codex config, you can skip this step.

### MCP servers: `~/.codex/config.toml` → `.cursor/mcp.json`

Codex's TOML format converts to Cursor's JSON:

**Codex (`~/.codex/config.toml`):**
```toml
[[mcp_servers]]
name = "mcp-github"
command = "python"
args = ["-m", "mcp_github"]
timeout_ms = 10000

[[mcp_servers]]
name = "mcp-web"
command = "node"
args = ["server.js"]
```

**Cursor (`.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "mcp-github": {
      "command": "python",
      "args": ["-m", "mcp_github"],
      "timeout": 10000
    },
    "mcp-web": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
```

MCP tool interfaces transfer cleanly — both use JSON-RPC. Just convert from
Codex's TOML array-of-tables to Cursor's JSON object format.

---

## What you gain moving to Cursor

- **Glob-based file-type scoping.** `globs: ["**/*.go"]` auto-applies a rule to
  Go files only. Codex applies all rules to all files.

- **Multi-file rule organization.** Separate `.mdc` files (one per concern) are
  easier to navigate and version-control than a single long `AGENTS.md`.

- **Rule metadata.** Front-matter fields (`description`, `globs`, `alwaysApply`)
  give structure to rules. Codex has no equivalent metadata.

- **IDE integration.** Cursor is a VS Code fork with native support for rules and
  codebase context. Codex is CLI-only.

- **Project-local rules without trust prompts.** Cursor's `.cursorrules` loads
  automatically. Codex requires explicit trust approval.

## What you lose

- **Monolithic rules file.** Codex's `AGENTS.md` is a single file; Cursor's rules
  are scattered across multiple `.mdc` files. Harder to see the full agent identity
  at a glance.

- **Cross-tool portability.** `AGENTS.md` is an open standard (works in Codex,
  Cursor, Copilot, others). Cursor's `.mdc` files are proprietary. Moving back to
  another tool later will require re-conversion.

- **Open-source accessibility.** Codex is Apache-2.0. Cursor is proprietary.

- **CLI simplicity.** Codex is terminal-first. Cursor is IDE-first with more UI
  complexity.

---

## Things that will silently break

1. **File-scoping decisions are now your responsibility.** Codex applied all rules
   globally; you must now decide which rules apply to Go vs Python vs all files.
   Wrong `globs:` patterns will either miss relevant files or waste context on
   irrelevant rules.

2. **`alwaysApply: false` rules won't auto-fire.** Cursor's checkbox controls
   whether a rule applies automatically or requires manual invocation. Codex had no
   equivalent — if a rule was important but not always, you must decide now.

3. **Markdown → MDC syntax.** Codex used free-form Markdown (easy). Cursor's MDC
   format requires proper YAML front-matter (syntax-sensitive). Invalid YAML will
   silently fail to load.

4. **Section headers become file names.** Each `##` header in Codex's `AGENTS.md`
   becomes a separate `.mdc` file. Choosing good filenames is up to you.

5. **Model assumptions.** If your Codex rules mentioned "GPT-5.4 (1M context)",
   update them to Cursor's model names (Claude, GPT-4, etc.). Cursor's default
   model may differ.

6. **Tool references.** Codex uses `git`, `bash`, `python`, `web` as tools. Cursor
   uses `@Codebase`, `@Web`, `@Docs` references. Rewrite tool assumptions.

7. **PII.** Grep for company names, domain, project slugs. Scrub before the move.

8. **Project-level rules lose privacy.** Codex's project `AGENTS.md` required
   trust approval. Cursor's `.cursorrules` loads automatically — anyone who clones
   the repo sees it. Don't commit sensitive project context.

---

## Doing this by hand

1. **Create `.cursor/rules/` directory:**
   ```bash
   mkdir -p .cursor/rules
   ```

2. **Extract core identity → Cursor Settings User Rules:**
   - Open Cursor Settings → Rules → User Rules
   - Copy the first paragraph/section from `~/.codex/AGENTS.md` (the core identity)
   - Paste it into the User Rules textarea
   - Save (Cursor auto-syncs)

3. **Split remaining sections into `.mdc` files:**
   - For each `## Section` in `AGENTS.md`, create a separate file:
   ```bash
   cat > .cursor/rules/go-code-review.mdc << 'EOF'
   ---
   description: Go code review and best practices
   globs: ["**/*.go"]
   alwaysApply: true
   ---
   
   When reviewing Go code:
   - Verify goroutine cleanup
   - Check for race conditions
   EOF
   ```

4. **Decide on `alwaysApply` and `globs` for each rule:**
   - Is this always relevant? → `alwaysApply: true`
   - Is this sometimes useful? → `alwaysApply: false`
   - Does this apply only to Go files? → `globs: ["**/*.go"]`
   - Does this apply to auth-related paths? → `globs: ["**/auth/**"]`

   Examples:
   ```yaml
   # Always-on rules
   alwaysApply: true
   globs: ["**/*"]  # or omit if applicable to all
   
   # Sometimes-useful rules
   alwaysApply: false
   globs: ["**/test/**", "**/*_test.go"]
   ```

5. **Add project context → `.cursorrules`:**
   - If `<project>/AGENTS.md` exists in Codex, create `.cursorrules`:
   ```bash
   cat > .cursorrules << 'EOF'
   This is the auth subsystem. Focus on:
   - Session token lifecycle
   - CSRF protection
   - Login/logout flows
   EOF
   ```

6. **Port MCP config:**
   - Extract `[[mcp_servers]]` entries from `~/.codex/config.toml`
   - Convert to JSON and save as `.cursor/mcp.json`:
   ```bash
   cat > .cursor/mcp.json << 'EOF'
   {
     "mcpServers": {
       "mcp-github": {
         "command": "python",
         "args": ["-m", "mcp_github"]
       }
     }
   }
   EOF
   ```

7. **Optional: Cursor Settings → `settings.json`:**
   - If you had important Codex settings, add `settings.json`:
   ```bash
   mkdir -p .cursor
   cat > .cursor/settings.json << 'EOF'
   {
     "model": "gpt-4o",
     "temperature": 0.7,
     "theme": "dark"
   }
   EOF
   ```

8. **Clean up:**
   - Test: open the project in Cursor, verify `.mdc` files are loaded
   - Grep all `.mdc` files for PII, company names → scrub
   - Check `.cursorrules` for sensitive project context → consider moving to private project config
   - Optional: delete `~/.codex/` if fully migrated

**Typical `.cursor/rules/` structure:**

```
.cursor/
├── rules/
│   ├── core-identity.mdc        # alwaysApply: true, globs: ["**/*"]
│   ├── go-code-review.mdc       # alwaysApply: true, globs: ["**/*.go"]
│   ├── auth-subsystem.mdc       # alwaysApply: false, globs: ["**/auth/**"]
│   ├── test-guidelines.mdc      # alwaysApply: false, globs: ["**/*_test.go"]
│   └── performance-notes.mdc    # alwaysApply: false, globs: ["**/*"]
├── mcp.json
└── settings.json (optional)

.cursorrules                      # project-level plain-text rules
```

**Time:** 30-60 minutes depending on rule count and glob-pattern decisions.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the whole thing in a single command:

```bash
npx portable migrate --from codex --to cursor
```

Reads `~/.codex/AGENTS.md` and `config.toml`, splits `AGENTS.md` into
topic-focused `.mdc` files with intelligent glob patterns and `alwaysApply`
decisions, converts MCP and settings to Cursor JSON, and outputs `.cursor/`
ready for review.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at **$29**, then
$49 (rising as traction grows). One-time payment, every future tool in the
Foundry Practitioner Toolkit included free.

- [Grab a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
