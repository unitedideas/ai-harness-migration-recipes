# Market Researcher Expertise

## Severity Calibration
- Star count alone does not imply submission success. Maintainer gatekeeping is the real filter.
- "CLI PR accepted" means: no browser-only issue template, no anti-LLM honeypot, no maintainer-only merge lock.
- Awesome list PRs go stale fast — verify repo last-commit date before submitting.

## False Positives / Anti-patterns
- sourcegraph/awesome-code-ai: ARCHIVED Feb 2026, read-only. Do not submit here.
- hesreallyhim/awesome-claude-code (39k stars): Blocks all external PRs explicitly. Only Claude can submit PRs. Submission = browser issue template only.
- ripienaar/free-for-dev (121k stars): Rejects LLM-written PRs via honeypot checkbox. Human-only submission.
- Lists with >30k stars routinely implement submission walls (issue templates, maintainer-only PRs). High stars != easy submission.

## Awesome List Gatekeeping Patterns (discovered 2026-04-18)
- **Maintainer-lock pattern**: repo states "only [maintainer/bot] may open PRs." External PRs auto-rejected. Example: hesreallyhim/awesome-claude-code.
- **Issue-template-only pattern**: contribution route is browser issue form, not PR. CLI `gh issue create` with template flags works but must match template exactly.
- **Anti-LLM honeypot**: checkbox in PR template reads "I confirm this is not AI-generated." Ticking it is a lie; not ticking causes rejection. Example: ripienaar/free-for-dev.
- **Branch-target pattern**: github/awesome-copilot requires PRs against `staged` branch not `main`. CLI PRs to main are rejected.
- **Open PR pattern**: standard fork+PR, no restrictions stated. Most smaller lists (<5k stars). Example: jamesmurdza/awesome-ai-devtools, ikaijua/Awesome-AITools.
- Merge rate signal: 187 merged PRs on jamesmurdza/awesome-ai-devtools = active, maintainer-responsive list.

## Spaces Researched

### AI Harness Migration / CLI Config Portability for AI Coding Agents (2026-04-18)
**Context**: BringYour/Portable product — CLI tool for migrating harness configs between Claude Code, Cursor, Aider, Codex.

Top 5 Awesome Lists ranked by fit + star count:
1. jamesmurdza/awesome-ai-devtools — 3.7k stars, open PR, "Configuration & Context Management" category confirmed, has merged config-portability tools (vsync, rule-porter, Not Human Search). BEST TARGET.
2. github/awesome-copilot — 30.3k stars, CLI PR to `staged` branch required (not main), no anti-LLM clause found. High reach but Copilot-centric audience.
3. ikaijua/Awesome-AITools — 5.8k stars, open PR via issue template, broad AI tools audience, no dedicated config-migration section (would need to propose placement).
4. hesreallyhim/awesome-claude-code — 39.6k stars, BROWSER ISSUE ONLY (blocked for agent submission). Shane must submit manually.
5. bradAGI/awesome-cli-coding-agents — 223 stars, open PR, "Harnesses & orchestration" section exists, scope is terminal agents not migration tools (marginal fit, low reach).

**Did not qualify**:
- VoltAgent/awesome-agent-skills (16.2k stars): skills-only, no infra tools
- ai-boost/awesome-harness-engineering (338 stars): framework theory, not CLI tooling
- caramaschiHG/awesome-ai-agents-2026 (324 stars): too small, no migration section
- Prat011/awesome-llm-skills (1.1k stars): skills-only, no portability tooling

## APIs Confirmed
- No specific API research for this space (awesome lists are GitHub PRs, not API-gated)

## Competitors Mapped
- vsync: CLI tool syncing Skills/MCP across Claude Code, Cursor, OpenCode, Codex — listed on jamesmurdza/awesome-ai-devtools
- rule-porter: converts AI IDE rule files between Cursor/CLAUDE.md/other formats — same list
- LynxPrompt: manages AI IDE configuration files — same list

## Submission Success Rate Notes
- jamesmurdza/awesome-ai-devtools: 187 merged PRs, recently merged config-portability tools, maintainer actively reviewing. High confidence in acceptance.
- github/awesome-copilot: active community (30k stars, GitHub-org backed), staged-branch requirement is the only friction. Scope overlap is partial (Copilot-centric but "Tools" section exists for cross-agent infra).
- ikaijua/Awesome-AITools: welcome note says "submit pull requests" with template. No explicit restrictions found. Medium confidence.
