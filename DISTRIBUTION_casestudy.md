# Case Study: How We Built BringYour — Automating Harness Migrations for AI Coding Agents

**Audience:** AI agent developers, DevTools founders, automation-curious engineers  
**Platform:** dev.to, Medium, LinkedIn, Indie Hackers  
**CTA:** "Migrate your harness in 5 minutes — BringYour.ai"

---

## The Problem (Hook)

Every AI coding agent works differently. Switching tools means:
- **Claude Code** → `claude_code.json` config
- **Cursor** → `.cursor/config.json` + settings rules  
- **Aider** → `.aider.conf.yml` + chat history
- **Codex** → proprietary format

Developers lose **project context, custom rules, API keys, chat history.** A 6-month setup takes 30 minutes to rebuild by hand. We built a tool that does it in 90 seconds.

---

## The Solution (Build Story)

### 1. Map the Terrain (2 weeks research)

We hand-tested migrations between all 4 agents — Cursor → Claude Code → Aider → Codex → back. We found:
- **Format fragmentation**: Claude Code uses JSON, Cursor uses YAML + binary rules, Aider uses plaintext config
- **Lossy conversions**: No standard for "system prompt" across tools
- **Edge cases**: API keys (which ones), project structure (mono-repo vs multi-folder), chat history (portable or tool-specific?)

**Output:** 12 **definitive migration guides** (all bidirectional pairs), CC BY 4.0, open-source at `github.com/unitedideas/ai-harness-migration-recipes`.

### 2. Build the Automated Migration Engine (3 weeks dev)

We wrapped the manual guides into a CLI tool:
```bash
portable migrate --from cursor --to claude-code
```

Inside:
- **Exporters** — read from each tool's native config (JSON parsing, YAML, file system)
- **Normalizer** — convert to a unified "harness" schema (project settings, rules, API keys, context)
- **Importers** — write to the target tool's format (special handling for binary Cursor rules, Aider's plaintext syntax)
- **Validators** — verify round-trip fidelity (catch lossy conversions before they hit users)

**Stack:**
- **Language:** Go (CLI tooling, file I/O, cross-platform)
- **Distribution:** Homebrew + direct binary downloads
- **Testing:** 40+ unit tests covering every tool pair + edge cases

### 3. Add Commercial Layer (1 week)

We created **BringYour.ai** — a commercial harness-migration SaaS:
- **Free tier:** CLI (`portable migrate`), 1 harness/month, open-source only
- **Early-bird pricing:** $19/$29/$49 tiers with reserved seats
- **Paywall:** Ed25519 license keys (locally validated, zero server calls)
- **Remote MCP:** Cursor, Claude Code agents can call migrations programmatically

**Selling:** Real Stripe checkout + email key delivery, live since Apr 18, 2026.

### 4. Monitoring & Trust (ongoing)

Edge case: Fly.io secrets drift (we once forgot to set `GEN_LICENSE_KEYPAIR` on deploy). Now:
- **Automated probes** — every 30 min, foundry-monitor tests a real end-to-end license key generation
- **Drift detection** — if production key ≠ CLI key, alert immediately
- **Webhook signature verification** — Stripe webhook integrity checked on every refund

This caught 2 real drift incidents during private beta.

---

## Results

| Metric | Value |
|---|---|
| **Time to migrate** | 90 sec (vs 30 min manual) |
| **Format coverage** | 4/4 agents (Claude Code, Cursor, Codex, Aider) |
| **Bidirectional pairs** | 12/12 (all combinations) |
| **Recipe tests** | 40+ unit tests + CI validation on every commit |
| **Open-source adoption** | MIT/CC BY 4.0 dual licensed |
| **Live since** | Apr 18, 2026 |
| **Tiers** | Free CLI + 3 commercial (Early-bird, Founding, Lifetime) |

---

## Key Learnings

### 1. **Format Fragmentation is Real**
Every agent decided independently how to store config. No standard. This is actually an opportunity — we're becoming the bridge.

### 2. **Determinism Matters**
Developers will round-trip migrations: Cursor → Claude Code → Cursor. Lossless conversion is non-negotiable. We test for it.

### 3. **Paywall at the CLI**
We keep the core open-source (trust), but gate the license keys. Developers can inspect the tool, fork it, but the remote MCP and reserved seats require a key. Works.

### 4. **Ops Risk: Secrets Drift**
When you have 2+ sources of truth (Fly.io secrets, local CLI keyring, GitHub Actions), they **will** diverge. Automated monitoring isn't optional.

### 5. **Cold Start Marketing**
Launch a project that solves YOUR pain first. We switched agents 6 times — the problem was real and urgent to us. That authenticity converts better than market research.

---

## What's Next

- **GitHub integration:** Detect when a `.cursor/` folder exists, suggest migration to Claude Code
- **Agent plugin ecosystem:** Let Claude Code, Cursor plugins call `portable migrate` in workflows
- **Cloud harness sync:** Optional (users opt-in) — sync harnesses across devices without storing keys
- **Audit trail:** Track which harness versions exist, who modified them, when

---

## For Builders

If you're thinking about tooling in the AI-agent space:
1. **Fragmentation is friction** — standardize OR bridge it
2. **Open-source trust, commercial convenience** — layer them
3. **Automate your own monitoring** — especially for secrets, keys, drift
4. **Test for round-trip fidelity** — lossy conversions kill adoption

**Try it:** https://bringyour.ai — $19 early-bird, all tiers include CLI + MCP access.

---

**Original recipes:** https://github.com/unitedideas/ai-harness-migration-recipes  
**Tool:** https://bringyour.ai  
**Free CLI:** `brew install portable` (coming soon) or `go install github.com/unitedideas/portable@latest`
