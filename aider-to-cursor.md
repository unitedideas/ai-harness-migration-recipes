# How to migrate your Aider agent to Cursor

**TL;DR** — Aider uses a single monolithic `system_prompt` in `.aider.conf.yml`;
Cursor uses multi-file MDC rules scoped by glob patterns. Migrating means splitting
your Aider prompt into logical pieces (core identity, domain-specific rules, project
context) and wrapping each in Cursor's MDC format with `globs:` and `alwaysApply:`
directives. You gain fine-grained file-type scoping and the ability to toggle rules
on/off; you lose the simplicity of a single-file config.

---

## The file layouts

### Aider (source)

```
<project-root>/
├── .aider.conf.yml           # per-project config (YAML)
├── CONVENTIONS.md            # optional: broader project context (not Aider-native)
└── .aiderignore              # exclusions (gitignore syntax)

~/.aider/
├── .aider.conf.yml           # user-level fallback config
├── prompts/                   # optional: reusable prompt files
└── <model-name>.yaml         # optional: per-model settings
```

### Cursor (destination)

```
<project-root>/
├── .cursorrules              # project-level rules (plain text, auto-loaded)
└── .cursor/
    ├── rules/
    │   ├── <name>.mdc        # MDC-format rule + front-matter
    │   └── ...
    └── mcp.json              # MCP server configuration

<cursor-user-settings>/       # Cursor Settings UI
└── User Rules                # global rules (textarea in Settings)
```

**Structural challenge:** Aider's single `system_prompt` string must be split
into multiple Cursor `.mdc` files. You'll manually decide which parts are:
- **Always-on identity** (`alwaysApply: true` in one core rule)
- **File-type-specific** (scoped via `globs: ["**/*.go"]`, etc.)
- **Optional/contextual** (`alwaysApply: false`, activated per-conversation)

---

## Mapping each piece

### `.aider.conf.yml` system_prompt → Cursor rules

Aider's monolithic prompt becomes Cursor's rule hierarchy.

**In Aider (`~/.aider/or/project/.aider.conf.yml`):**
```yaml
system_prompt: |
  You are a senior Python engineer with 10 years of experience.
  
  ## Core principles
  - Always write comprehensive docstrings
  - Prefer type hints over comments
  - Validate all external inputs
  
  ## Django expertise
  When working with Django:
  - Use Django ORM; avoid raw SQL
  - Test with Django's TestCase, not unittest
  - Follow the MTV pattern
  
  ## Project context
  This is a payment processing service. Security is non-negotiable.
  - Validate all card data against PCI standards
  - Log all transaction events
  - Never log PII or card numbers
```

**In Cursor:** Split into multiple rules.

**User Rules (Cursor Settings):**
```
You are a senior Python engineer with 10 years of experience.

Core principles:
- Always write comprehensive docstrings
- Prefer type hints over comments
- Validate all external inputs
```

**`.cursor/rules/django-best-practices.mdc`:**
```yaml
---
description: Django framework best practices
globs: ["**/*.py"]
alwaysApply: true
---

When working with Django:
- Use Django ORM; avoid raw SQL
- Test with Django's TestCase, not unittest
- Follow the MTV pattern
- Keep views thin; move logic to services
```

**`.cursor/rules/payment-security.mdc`:**
```yaml
---
description: Payment processing security guidelines
globs: ["**/payments/**", "**/*payment*.py", "**/*billing*.py"]
alwaysApply: true
---

This is a payment processing service. Security is non-negotiable:
- Validate all card data against PCI standards
- Log all transaction events
- Never log PII or card numbers
- Encrypt sensitive fields at rest
- Use HTTPS for all external payment API calls
```

**Decisions you must make:**
- **Core identity** → User Rules (no globs needed; always visible)
- **File-type rules** → named `.mdc` files with glob patterns + `alwaysApply: true`
- **Project-specific context** → scoped `.mdc` files with `alwaysApply: true` or `false` depending on whether it should auto-apply

---

### `.aider.conf.yml` model setting → Cursor model selection

Aider specifies the model in `.aider.conf.yml`:
```yaml
model: claude-3-5-sonnet-20241022
```

Cursor doesn't store model in config; instead, you select it in:
- **Settings → Default Model** (user-level, affects all projects)
- **Bottom-right dropdown** in the editor (per-conversation override)

**Migration:** No file change needed. Just set your model in Cursor Settings
and close any `.aider.conf.yml` references.

---

### `.aider.conf.yml` auto-commits → Cursor (no equivalent)

Aider has an `auto_commits` option to auto-commit after each change:
```yaml
auto_commit: true
auto_commit_message: "Aider auto-commit: {summary}"
```

Cursor has **no equivalent.** You'll need to:
- Manually commit with Git after a Cursor session
- OR use a pre-commit hook to auto-commit (same as any editor)

**Recommendation:** Set up a post-save hook in your `.git/hooks/post-commit`
to commit automatically if you want that behavior:
```bash
#!/bin/bash
# .git/hooks/post-commit
git add -A && git commit -m "auto-commit" || true
```

---

### `.aider.conf.yml` MCP servers → `.cursor/mcp.json`

Aider (≥v0.75) supports MCP servers in `.aider.conf.yml`:
```yaml
mcp_servers:
  - name: filesystem
    command: npx
    args:
      - "@modelcontextprotocol/server-filesystem"
      - /path/to/root
```

Cursor's equivalent is `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-filesystem",
        "/path/to/root"
      ]
    }
  }
}
```

**Migration:** Convert from Aider's YAML list format to Cursor's JSON object format.
The server definitions are identical; only the wrapper changes.

---

### `.aiderignore` → Cursor ignore patterns

Aider uses `.aiderignore` (gitignore syntax) to exclude files from context:
```
*.log
__pycache__/
.env
node_modules/
venv/
```

Cursor doesn't have a built-in ignore file. Instead, use:
- **Project `.cursor/settings.json`** (if you create one):
  ```json
  {
    "excludePatterns": ["*.log", "__pycache__/", ".env", "node_modules/", "venv/"]
  }
  ```
- OR respect `.gitignore` by default (Cursor does this automatically)

**Migration path:** Delete `.aiderignore`; rely on `.gitignore`. If you need
per-project exclusions, create `.cursor/settings.json` (Cursor checks this
before global settings).

---

## What you gain moving to Cursor

- **Glob-based scoping.** Rules can target specific file types:
  `globs: ["**/*.go"]`, `globs: ["**/*.py", "**/*.pyi"]`, etc. Aider forces
  you to manually invoke context when file type matters.

- **Toggle-able rules.** Rules with `alwaysApply: false` can be selectively
  enabled mid-conversation. Aider forces you to either rewrite the prompt or
  start a new session.

- **Multi-file rules.** Each rule is its own file, making version control and
  team sharing easier. No merging a monolithic system prompt.

- **MDC syntax.** Front-matter (YAML) + body (Markdown). Cursor's parser
  understands the structure, enabling future UI features (rule enable/disable,
  per-rule settings).

---

## What you lose moving to Cursor

- **Single source of truth.** Your identity now lives in 3 places: User Rules
  (Settings), `.cursorrules`, and `.cursor/rules/*.mdc`. Keeping them in
  sync requires discipline.

- **Simplicity.** One YAML file was easier to understand and version-control
  than a directory of `.mdc` files. More files = more merge conflicts if teams
  edit rules together.

- **Easy conditional logic.** Aider's prompt is a string; you can write
  `if this is a Go project, remember X`. Cursor's rules are text blobs; you
  can't conditionally include them based on project state (only on glob match).

---

## Migration checklist

- [ ] Extract **core identity** (engineer level, philosophy, hard constraints)
      → Cursor Settings → User Rules
- [ ] Extract **file-type-specific guidance** → `.cursor/rules/<topic>.mdc`
      with appropriate `globs:`
- [ ] Extract **project context** → `.cursor/rules/project-context.mdc` with
      high-specificity globs (e.g., `globs: ["src/**"]`) or `alwaysApply: false`
- [ ] Convert **MCP servers** from `.aider.conf.yml` → `.cursor/mcp.json`
- [ ] Delete **`.aiderignore`** (Cursor uses `.gitignore` by default)
- [ ] Delete or archive **`.aider.conf.yml`** (no longer needed)
- [ ] Test: Open a conversation in Cursor, verify rules load and match your intent
- [ ] Commit `.cursor/rules/` and `.cursor/mcp.json` to version control

---

## Pitfalls

**Silent breakage 1: Forgetting `.cursorrules`**
Cursor can load rules from either `.cursorrules` (project-level, plain text)
or `.cursor/rules/*.mdc` (multi-file, MDC format). If you migrate to `.cursor/rules/`
and forget that `.cursorrules` takes precedence if it exists, old rules will
shadow your new ones. **Always delete `.cursorrules` or merge it into `.cursor/rules/`.**

**Silent breakage 2: Glob patterns not matching**
If a rule is `globs: ["**/*.go"]` but you're editing `handler.ts`, the rule
won't apply. Test by opening different file types and checking that relevant
rules appear in the rule panel (View → Rule Panel if available).

**Silent breakage 3: alwaysApply: false and forgetting to invoke**
If you set `alwaysApply: false` for optional context (e.g., a rarely-needed
security checklist), you'll need to manually mention it in conversation. Aider
let you always reference it by name. In Cursor, you're responsible for
activating the rule. Consider `alwaysApply: true` for anything you'd want in
every conversation.

**Silent breakage 4: User Rules vs .cursorrules vs .cursor/rules/**
Cursor loads in this order (first match wins):
1. `.cursorrules` (project-level, plain text)
2. `.cursor/rules/*.mdc` (project-level, multi-file MDC)
3. User Rules (Settings UI, global)

If you have both `.cursorrules` and `.cursor/rules/`, the `.cursorrules`
shadow the `.mdc` files. **Use one system or the other, not both.**
