# How to migrate your Cursor agent to Aider

**TL;DR** — Cursor and Aider are both AI pair programmers, but they store
configuration in completely different ways. Cursor is **multi-file rules
(MDC format)** scoped by glob patterns; Aider is **one YAML config file**
with system-prompt-as-a-string. Migrating from Cursor to Aider means
consolidating all your `.cursor/rules/*.mdc` files into a single
`.aider.conf.yml` system prompt, deciding which globbed rules are
file-type-specific (and losing that auto-scoping), and accepting that
Aider has no equivalent to Cursor's project-local vs user-global split.

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

### Aider (destination)

```
<project-root>/
└── .aider.conf.yml           # single YAML config (auto-loaded per project)

~/.aider/
├── .aider.conf.yml           # user-level fallback (if project has none)
├── <model-name>.yaml         # optional model settings
└── prompts/                   # (rarely used; most go in system_prompt)
```

The structural challenge: **Aider has no multi-file rule system.** All your
rules—global and project-specific, file-type-specific and always-on—must
live in `.aider.conf.yml` as a single system prompt string. The
`globs: ["**/*.go"]` auto-scoping in Cursor becomes a comment or a
conditional prompt fragment you manage manually.

---

## Mapping each piece

### Cursor User Rules + `.cursorrules` → `.aider.conf.yml` system_prompt

Cursor's two-tier rule system (user-global + project-local) collapses into
Aider's single-file model.

**In Cursor:**
```
User Rules (Settings UI):
You are a Go expert. Always use context.Background() for root contexts...

.cursorrules (project file):
This is the authentication subsystem. Focus on session tokens and CSRF...
```

**In Aider:**
```yaml
# ~/.aider/or/project/.aider.conf.yml

system_prompt: |
  You are a Go expert. Always use context.Background() for root contexts...
  
  # Project context: This is the authentication subsystem.
  # Focus on session tokens and CSRF...
```

If you have many separate `.mdc` files in `.cursor/rules/`, you'll need to
manually decide which ones are fundamental (merge into system_prompt) vs
which are optional context (keep as comments, invoke them when relevant).

### `.cursor/rules/*.mdc` (multi-file rules) → system_prompt sections

Each `.cursor/rules/<name>.mdc` file contains a rule with front-matter:

```yaml
---
description: Use when reviewing Go code for correctness
globs: ["**/*.go"]
alwaysApply: false
---
Here's Go-specific review guidance...
```

**Convert to:** A section inside `.aider.conf.yml`'s system_prompt. Add a
comment describing the original scope (since Aider won't auto-apply):

```yaml
system_prompt: |
  # Go code review (originally scoped to **/*.go):
  When reviewing Go code for correctness, remember:
  - Check error handling patterns
  - Verify context propagation
  - Look for goroutine leaks
```

**If the rule was `alwaysApply: true`**, merge it unconditionally into the
prompt. **If `alwaysApply: false`**, add a comment like `# Optional: use
when X` so you can invoke the context manually in conversation.

### `.cursor/mcp.json` → Aider MCP support

Aider supports MCP servers via `.aider.conf.yml`:

```yaml
# Cursor:
# .cursor/mcp.json
{
  "mcpServers": {
    "mcp-server": {
      "command": "python",
      "args": ["-m", "mcp_server"]
    }
  }
}

# Aider:
# .aider.conf.yml
mcp_servers:
  - name: mcp-server
    command: python
    args:
      - -m
      - mcp_server
```

MCP tool interfaces transfer cleanly — both use JSON-RPC. Just reformat
the config from JSON object to YAML list.

---

## What you gain moving to Aider

- **Lighter-weight setup.** One file, one system prompt. No MDC parsing, no
  rule-scoping complexity. Aider works in any directory with or without
  `.aider.conf.yml`.

- **Simpler editing.** Plain YAML is easier to version-control and diff
  than Cursor's MDC format. No front-matter syntax gotchas.

- **Integrated code editing.** Aider edits your code directly in the
  terminal, no separate IDE. That's a workflow gain, not a config gain,
  but worth noting.

- **Cost-effective.** Aider is open-source and self-hosted by default.
  Cursor is proprietary.

## What you lose

- **Project-local vs user-global split.** Cursor distinguishes User Rules
  (global) from `.cursorrules` (per-project). Aider has an implicit split
  (user-level `~/.aider/` vs project-level `.aider.conf.yml`), but there's
  no clear "which rules apply where" until you run Aider.

- **Glob-based auto-scoping.** Cursor's `globs: ["**/*.go"]` auto-applies a
  rule to Go files. Aider has no equivalent. You lose automatic context
  routing; every conversation gets the full system prompt.

- **Multi-file rule organization.** Cursor's `.cursor/rules/` lets you
  break rules into separate files (one per concern). Aider consolidates
  everything into one prompt string, which gets long fast.

- **Rule versioning / loading order.** Cursor's MDC system allows
  front-matter metadata like `alwaysApply`, `description`, `globs`. Aider
  has no equivalent — everything is a flat prompt string.

---

## Things that will silently break

1. **`globs:` auto-scoping is gone.** If you had a rule that only applied
   to `**/*.go` files, Aider will include that text in *every* response,
   even for Python files. Comment it clearly and invoke manually when
   relevant.

2. **Separate rule descriptions become inline comments.** Cursor's
   `description: Use when reviewing Go code` field is lost. Add
   comment-style headers in the prompt so you remember what each section is
   for.

3. **`alwaysApply: false` rules need manual invocation.** If a Cursor rule
   was only sometimes relevant, you'll need to copy-paste or re-mention it
   in conversation. Aider doesn't have a way to conditionally include
   rules.

4. **Model assumptions.** If your Cursor rule mentioned "Claude 3.5
   Sonnet", Aider may use a different model (llama, GPT-4, Sonnet, etc.
   depends on user config). Remove model-specific hints.

5. **Tool references.** Cursor rules might reference `@Codebase`,
   `@Web`, `@Docs`. Aider's tool set is different — `git`, `web`, `bash`,
   `python`. Rewrite any tool assumptions.

6. **PII.** Grep for the previous company's name, domain, project slugs.
   Scrub before the move.

7. **File size explosion.** One long YAML prompt is hard to navigate and
   review. If you had 10 separate MDC rules, expect a 500-line system
   prompt that's tedious to edit later.

---

## Doing this by hand

1. **Create `.aider.conf.yml`** in your project root:
   ```bash
   touch .aider.conf.yml
   ```

2. **Extract Cursor's User Rules:**
   - Open Cursor Settings → Rules → User Rules
   - Copy the entire text
   - Paste into `.aider.conf.yml` under `system_prompt:`

3. **Add project-specific rules from `.cursorrules`:**
   - If `.cursorrules` exists, append its content to `system_prompt` with a
     comment like `# Project-specific context:`

4. **Extract each `.cursor/rules/*.mdc` file:**
   - For each file, read the front-matter (`description`, `globs`, `alwaysApply`)
   - If `alwaysApply: true`, merge unconditionally into `system_prompt`
   - If `alwaysApply: false`, add a section header + comment explaining when to use it
   - Replace any `@Codebase`, `@Web`, `@Docs` with Aider's tool names (`git`, `web`, `bash`)

5. **Port MCP config:**
   - Convert `.cursor/mcp.json` to YAML format under `mcp_servers:` in `.aider.conf.yml`

6. **Clean up:**
   - Delete or rename `.cursor/` directory (keep backup if paranoid)
   - Grep system_prompt for PII, company names, project slugs → scrub
   - Test: run `aider .` and verify the system prompt is applied

**Typical `.aider.conf.yml` structure:**

```yaml
system_prompt: |
  You are a Go backend engineer with 10 years of experience.
  
  # Global rules:
  - Always check error returns
  - Use structured logging
  - Context propagation is non-negotiable
  
  # Go code review (originally scoped to **/*.go):
  When reviewing Go code:
  - Verify goroutine cleanup
  - Check for race conditions
  
  # Project context (from .cursorrules):
  This is the auth subsystem. Focus on:
  - Session token lifecycle
  - CSRF protection
  - Login/logout flows
  
  # Test guidelines (originally alwaysApply: false):
  # Invoke this when writing tests:
  - 100% coverage for security-sensitive paths
  - Use table-driven tests for parser functions

mcp_servers:
  - name: github
    command: python
    args:
      - -m
      - mcp_github
```

**Time:** 30-60 minutes depending on rule count and complexity.

---

## Doing this with one command

[BringYour](https://bringyour.ai) does the whole thing in a single command:

```bash
npx portable migrate --from cursor --to aider
```

Reads your Cursor project + User Rules, extracts all `.mdc` rules, merges
them into a single system prompt (with comments preserving original scope),
converts MCP config to YAML, and outputs `.aider.conf.yml` for review.

Launch pricing: first 10 buyers at **$19** lifetime, next 10 at **$29**,
then $49 (rising as traction grows). One-time payment, every future tool in the Foundry
Practitioner Toolkit included free.

- [Grab a $19 slot →](https://bringyour.ai/buy)
- [See how it works →](https://bringyour.ai/how-it-works)
