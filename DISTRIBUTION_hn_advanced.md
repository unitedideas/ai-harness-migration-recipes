# HackerNews Post (Advanced Angle)

## Title Options

### High-engagement angle:
**"I documented every AI coding agent migration so you don't lose your config again"**

### Technical angle:
**"12 bidirectional harness migrations: Claude Code ↔ Cursor ↔ Codex ↔ Aider"**

### Problem-first angle:
**"Why moving between Claude Code, Cursor, Codex, and Aider breaks everything (and how to fix it)"**

---

## Post Text

I'm an AI agent infrastructure engineer. This week I had to migrate my entire agent harness (identity, skills, memory, hooks) from Claude Code to Cursor, and it was a nightmare—silent breakages, unmapped config fields, relative paths that snapped.

So I documented all 12 bidirectional migrations hand-written and hand-tested. Every tool stores your agent differently:

- **Claude Code**: `~/.claude/CLAUDE.md` (system prompt) + `agents/*.md` (subagents) + `skills/` (context modules) + `hooks/*.py` (automation)
- **Cursor**: `.cursorrules` + `.cursor/rules/*.mdc` (no equivalent for memory/hooks)
- **Codex**: `~/.codex/config.md` + `~/.codex/skills/` (no agents or hooks)
- **Aider**: CONVENTIONS.md + `.aider.conf.yml` (no memory or hooks)

The silent killers:
- Template variable syntax differs (Claude Code: `${VAR}`, Cursor: `<variable>`)
- Relative paths in skills break on copy
- Model name references (gpt-4o, claude-opus-4-7) aren't standardized
- Some features vanish entirely on the destination

All 12 recipes are here: one per migration pair, source/dest layouts, field mappings, breakage warnings, and checklists. CC BY 4.0.

https://github.com/unitedideas/ai-harness-migration-recipes

And if you're tired of doing this manually, there's also a CLI: `npx portable migrate --from claude-code --to cursor` (first 10 early-bird slots at $19).

---

## Discussion Angles (for replies)

If asked about automation:
> "The repo is the reference. The CLI ($19) does the mapping automatically. I built it because doing this by hand is error-prone and I needed it repeatable."

If asked about missing tools:
> "Happy to add more tools—these 4 (Claude Code, Cursor, Codex, Aider) are where most agents run. If you use Windsurf, VS Code Copilot, or another tool, the same breakage patterns apply."

If asked about license/reposting:
> "CC BY 4.0—attribute to bringyour.ai if you repost the recipes elsewhere (dev.to, blog, etc). We're also submitting to awesome lists this week."

If asked about edge cases:
> "Good catch. Recipes capture the common patterns. If you hit something undocumented, file an issue—we're steadily expanding the edge cases."

---

## Submission Timing

**Best day/time**: Tuesday–Thursday, 9am–3pm PT (peak HN activity before weekend). Avoid Monday (crowded) and Friday afternoon (tails off).

**Best group size**: Solo story (not "I built this with X people") performs better on HN.

**Expected reach**: If ranked on front page for 12+ hours, 5k–15k views. If #1 position, 20k–50k. Referral traffic to GitHub: usually 10% of views.

---

## Tracking

After posting, monitor:
- [x] Story submitted → check HN job board for post
- [x] First 2 hours → engage with early comments
- [x] Peak rank (usually 4–8 hours) → screenshot for social proof
- [x] GitHub referral traffic → check analytics (Issues tab → /traffic if public repo)
- [ ] Final position after 24h → update DISTRIBUTION_TRACKER.md
