# Migration Recipes Roadmap

## Completed (9/11 pairs)

| From | To | Status | Notes |
|---|---|---|---|
| Claude Code | Cursor | ✅ DONE | [claude-code-to-cursor.md](claude-code-to-cursor.md) |
| Claude Code | Aider | ✅ DONE | [claude-code-to-aider.md](claude-code-to-aider.md) |
| Claude Code | Codex | ✅ DONE | [claude-code-to-codex.md](claude-code-to-codex.md) |
| Cursor | Claude Code | ✅ DONE | [cursor-to-claude-code.md](cursor-to-claude-code.md) |
| Cursor | Aider | ✅ DONE | [cursor-to-aider.md](cursor-to-aider.md) |
| Cursor | Codex | ✅ DONE | [cursor-to-codex.md](cursor-to-codex.md) |
| Codex | Claude Code | ✅ DONE | [codex-to-claude-code.md](codex-to-claude-code.md) |
| Codex | Cursor | ✅ DONE | [codex-to-cursor.md](codex-to-cursor.md) |
| Aider | Claude Code | ✅ DONE | [aider-to-claude-code.md](aider-to-claude-code.md) |

## Missing (2 pairs) — Blocked on tool access

| From | To | Blocker | Notes |
|---|---|---|---|
| Aider | Cursor | ⛔ No Aider | Need Aider installed for hand-verification |
| Aider | Codex | ⛔ No Aider | Need Aider installed for hand-verification |

## Contributing Guidelines

All recipes must be **hand-verified**. Contributors should:

1. Have both source and destination tools installed
2. Complete an actual migration (not theoretical)
3. Document what silent breaks occurred
4. Follow the structure in [claude-code-to-cursor.md](claude-code-to-cursor.md)
5. Submit as PR with evidence of testing

## Next Steps

- **For Shane**: Install Codex + Aider, hand-verify remaining 5 pairs, or recruit contributors with those tools
- **For distribution**: Submit this repo to Awesome lists (awesome-cli-tools, awesome-migration-tools, etc.)
- **For tooling**: Consider `bringyour migrate --validate` subcommand to test user migrations post-run

## Stats

- Recipes: 9/11 complete (82%)
- Coverage: All Claude Code pairs done; Cursor pairs done; Codex pairs done; Aider partially done
- Last update: 2026-04-18 (Aider→Claude Code, Cursor→Codex, Codex→Cursor recipes added)
