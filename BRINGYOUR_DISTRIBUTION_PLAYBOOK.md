# BringYour Distribution & Buyer Acquisition Playbook

**Product**: bringyour.ai (portable harness migration tool + remote MCP server)  
**Status**: Live, selling early-bird tiers ($19/$29/$49)  
**Goal**: Drive traffic to checkout, maximize early-bird adoption  
**Timeline**: 2-4 weeks to customer saturation  
**Owner**: Shane (requires personal accounts + distribution channels)

---

## Product Narrative (Use This in All Posts)

**Problem**: Migrating AI agent harnesses between Claude Code, Cursor, Codex, Aider is manual, error-prone, and time-consuming.

**Solution**: BringYour portable migrate tool automates the translation. One command exports from your current tool, another imports into the destination. No hand-editing config, no lost state.

**Price**: Early-bird $19 (Founding 10 left), $29 (Early 10 left), then $49 (lifetime). Every week, price rises.

**Call-to-action**: "Lock in your tier at [bringyour.ai](https://bringyour.ai) before prices go up."

---

## Phase 1: Warm Outreach (Days 1-3)
### Target: High-intent communities where people actively migrate tools

**Discord/Slack Communities** (personal reach via Shane's networks)
- Claude community Slack, Anthropic forums
- Cursor Discord, r/cursor_so
- Aider community
- LiteLLM Discord
- Pydantic AI Slack

**Email list outreach** (if you have any)
- Prior BringYour beta testers
- Newsletter subscribers interested in AI tooling

**Copy template:**
```
Subject: BringYour is live — migrate your AI harness in 1 command

Hi {name},

I shipped BringYour this week. It's a CLI tool + remote MCP server that 
automates harness migrations between Claude Code, Cursor, Codex, Aider.

Instead of hand-editing config files, you export from one tool and 
import into another. One command.

Early-bird pricing: $19 (Founding tier, 10 slots), then $29 (Early, 10 slots), 
then $49 (lifetime). Price goes up weekly.

[BringYour → https://bringyour.ai]

Works with local harnesses + remote MCP (for agents in Claude Code, Cursor extensions).

— Shane
```

**Expected**: 10-30 warm leads, 3-10 conversions (30-50% intent rate)

---

## Phase 2: Public Social Media (Days 1-7)
### Owner: Shane
### Channels: HN, dev.to, Twitter, Reddit, LinkedIn

### 1. HackerNews (target: 200-400 upvotes, 100-300 visitors)

**When to post**: Tuesday-Thursday, 9:30am Pacific (optimal HN window)

**Title**: 
```
BringYour: Automate AI Harness Migrations Between Claude Code, Cursor, Codex
```

**URL**: `https://bringyour.ai`

**Immediate comment (paste this as first reply to your own post):**
```
Hi HN,

I shipped BringYour this week. It's a CLI tool that automates migrations 
of AI agent harnesses between Claude Code, Cursor, Codex, and Aider.

The problem: when you switch AI tools, you lose your harness config 
(tool-specific settings, prompt engineering, model tuning). Hand-editing 
is error-prone.

BringYour translates your harness automatically. One export command, 
one import command. Works locally + as a remote MCP server.

Early pricing: $19 (Founding), $29 (Early), $49 (lifetime). Tiers fill weekly.

[https://bringyour.ai]

Open source recipes at: [https://github.com/unitedideas/ai-harness-migration-recipes]

Feedback welcome.
```

**Follow-up angles** (if commenters ask):
- "How is this different from just exporting JSON?" → Show config complexity
- "Does it handle X tool?" → List supported tools: Claude Code, Cursor, Codex, Aider, LiteLLM
- "Can I use the free recipes instead?" → Yes, recipes are free (open source). BringYour CLI is the paid automation.

---

### 2. dev.to (target: 500-2k views, 10-50 comments)

**When to post**: Tuesday-Wednesday  
**URL to link**: `https://bringyour.ai`

**Article title**: "BringYour: Stop Hand-Editing AI Harness Migrations"

**Outline** (write as dev.to article):
```
# BringYour: Stop Hand-Editing AI Harness Migrations

## The Problem

You're using Claude Code. Your agent works beautifully. Then you try Cursor.

You export your harness. It's a YAML file. But Cursor uses a different format.

Now you're manually rewriting:
- Tool-specific settings
- Model parameters  
- Prompt engineering
- Rate limits, auth config
- Everything

One mistake breaks your agent. Hours wasted.

## The Solution: BringYour

BringYour is a CLI tool (+ remote MCP server) that automates the translation.

```bash
# Export your harness from Claude Code
bringyour export --from claude-code > agent.yaml

# Import into Cursor
bringyour import --to cursor < agent.yaml
```

Done. Your harness works in Cursor, with zero hand-editing.

## How It Works

1. **Parses** your current harness config
2. **Translates** tool-specific settings to the destination format
3. **Validates** the new harness before writing
4. **Signs** the output (detects tampering)

## Supported Tools

- Claude Code (.claude/context.json)
- Cursor (.cursor/rules)
- Codex (codex.yaml)
- Aider (.aider.conf.md)
- Custom tools (plug your own translator)

## Pricing

- **$19**: Founding tier (10 slots) — sign up first
- **$29**: Early tier (10 slots) — second wave  
- **$49**: Lifetime tier — price goes up as we grow

All tiers include:
- CLI tool (portable migrate, export, import, etc.)
- Remote MCP server (for Claude Code extensions, Cursor plugins)
- License key (offline validation)
- Email support

## Open Source + Commercial

Harness migration recipes are free: [github.com/unitedideas/ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes)

BringYour CLI automates the process. For people who want the tool, not DIY.

## Try It

[BringYour → bringyour.ai]

Questions? Reply here or email [shane@bringyour.ai](mailto:shane@bringyour.ai).
```

---

### 3. Twitter Thread (target: 1k-5k impressions, 20-100 retweets)

**When to post**: Tuesday-Thursday, 8-10am Pacific

**Thread:**
```
Thread: I shipped BringYour this week.

It's a CLI tool that solves a painful problem:
migrating AI agent harnesses between tools.

Let me explain why you should care.
/1

---

You're using Claude Code. Your AI agent works.

Then you try Cursor. Or Codex. Or Aider.

You export your harness. It's config files.

But each tool uses a different format.

Now you're hand-editing everything.
/2

---

Tool-specific settings that don't translate.
Model parameters that conflict.
Prompt engineering that breaks.
Rate limits, auth config, custom rules.

One mistake and your agent is broken.
Hours wasted.
/3

---

BringYour solves this.

```
bringyour export --from claude-code > agent.yaml
bringyour import --to cursor < agent.yaml
```

Done. Your harness works in Cursor.

Zero hand-editing.
No mistakes.
/4

---

Why?

Because migrating between AI tools is the new reality.

Claude Code → Cursor → Codex → Aider.

Developers want to experiment. Teams want to standardize.

The tools are commoditizing.

The real cost is migration.
/5

---

BringYour handles the translation.

- Parses your current harness
- Translates to destination format
- Validates before writing
- Signs output (detects tampering)

Supports Claude Code, Cursor, Codex, Aider, and custom tools.
/6

---

Pricing:
$19 (Founding, 10 slots)
$29 (Early, 10 slots)  
$49 (Lifetime)

Each tier fills weekly. Once 10 are gone, price goes up.

[BringYour → bringyour.ai]

Open source recipes: [github.com/unitedideas/ai-harness-migration-recipes]
/7

---

Built for teams that:
- Migrate between Claude Code/Cursor/Codex
- Run AI agents in multiple environments  
- Need portable harness config
- Don't want to hand-edit migrations

If that's you, lock in early.
/8

Reply with questions. I'm shipping fast and listening to feedback.

Ready to move your harness? [bringyour.ai]
/9
```

**Mention**: @anthropic @cursor_so @codex_co @aider_ai @literalai (optional, don't spam)

---

### 4. Reddit Posts (target: 200-1k upvotes each, 50-300 visitors per post)

**Posts to submit** (adapt slightly for each community):

#### r/learnprogramming
```
Title: BringYour — Automate AI Harness Migrations Between Claude Code, Cursor, Codex

Hi r/learnprogramming,

I built BringYour to solve a problem I had:

I use Claude Code for one project. Cursor for another. Codex for a third.
Each has different agent harness config. When I switch tools, I manually 
hand-edit everything.

It's error-prone and slow.

BringYour automates it. One export command, one import command.

[bringyour.ai](https://bringyour.ai)

Free recipes if you want to DIY: [github.com/unitedideas/ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes)

Early-bird pricing: $19, $29, $49 (tiers fill weekly).

Would love feedback on whether this solves your problem.
```

#### r/MachineLearning
```
Title: BringYour CLI — Portable Harness Migrations for AI Agent Workflows

Hi r/MachineLearning,

Quick question: how many of you run AI agents across multiple tools?

Claude Code for experimentation.
Cursor for production.
Codex for custom use cases.
Aider for local development.

My team does, and migrating harness config between them was manual.

I built BringYour to automate the translation.

[bringyour.ai](https://bringyour.ai)

Works as a CLI tool + remote MCP server. Supports Claude Code, Cursor, Codex, Aider.

Open source recipes: [github.com/unitedideas/ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes)

Curious if this is valuable in your workflows.
```

#### r/coding
```
Title: BringYour: Stop Hand-Editing AI Harness Migrations Between Tools

If you've switched between Claude Code, Cursor, Codex, or Aider, you know 
the pain:

Each tool has a different harness format. Migrating is manual. Easy to break.

I built BringYour to automate it.

[bringyour.ai](https://bringyour.ai)

CLI tool + remote MCP server. Early-bird pricing: $19–$49.

Free recipes if you want to see how migrations work:
[github.com/unitedideas/ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes)

Would appreciate feedback.
```

---

### 5. LinkedIn (target: 200-1k views, 20-100 engagement)

**Post:**
```
Just shipped BringYour: a tool that automates AI harness migrations.

The problem: When you switch between Claude Code, Cursor, Codex, or Aider, 
you lose your harness config. Tool-specific settings, prompt engineering, 
model tuning—all manual re-entry.

BringYour translates your harness automatically.

One export command. One import command. Your agent works in the new tool.

Early-bird pricing: $19 → $29 → $49. Tiers fill weekly.

🔗 [bringyour.ai](https://bringyour.ai)

Open source recipes: [github.com/unitedideas/ai-harness-migration-recipes](https://github.com/unitedideas/ai-harness-migration-recipes)

For teams that migrate between AI tools and want portable harness config.

#AITools #Developers #CodingAgents #Claude #Cursor #Automation
```

---

## Phase 3: Awesome Lists & Directories (Days 8-14)
### Owner: Shane (browser-based)

### High-Value Awesome Lists

**awesome-claude-code** (39k stars)
- Link: https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
- Required: Issue template, human checkbox
- **Entry:**
  ```
  **BringYour** — Automate AI harness migrations between Claude Code, 
  Cursor, Codex, Aider. CLI tool + remote MCP server. 
  [bringyour.ai](https://bringyour.ai)
  ```

**appcypher/awesome-mcp-servers** (5.4k stars)
- Link: https://github.com/appcypher/awesome-mcp-servers
- **Entry:**
  ```
  - **BringYour** — Remote MCP server for portable harness migrations.
    Supports Claude Code, Cursor, Codex, Aider.
    [https://registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io)
  ```

**awesome-developer-tools** (3.1k stars)
- **Entry:**
  ```
  - **BringYour** — CLI tool + MCP server for automating AI harness 
    migrations. Move your agent config between Claude Code, Cursor, Codex, Aider.
  ```

### MCP Registries (10 min each, browser login)

1. **MCP Market** (mcpmarket.com/submit)
2. **Glama** (glama.ai/mcp/servers) — dual submission (recipes + BringYour)
3. **Smithery** (smithery.ai)
4. **Cursor Marketplace** (cursor.com/marketplace)
5. **LobeHub** (lobehub.com/mcp)
6. **publicmcpregistry** (publicmcpregistry.com)
7. **cursor.directory** (cursor.directory/plugins/new)
8. **thataicollection** (thataicollection.com)
9. **aiagentslist** (aiagentslist.com)
10. **PulseMCP** (pulsemcp.com/submit)

**Total effort**: ~100 minutes → 10 registrations → 50k+ potential reach

---

## Phase 4: Post-Launch Engagement (Days 15-21)

1. **Monitor comments** on HN, dev.to, Reddit (respond to questions, ask for feedback)
2. **Track metrics**: Website traffic, checkout conversions, refund rate
3. **Collect testimonials** from first buyers (email them within 24h of purchase)
4. **Create case study**: "How I built BringYour in 3 weeks" (link from bringyour.ai footer)
5. **Email early-bird buyers**: "What migrations would you like us to support next?"

---

## Success Metrics (30 days)

- [ ] 50+ early-bird sales ($950–$2,450 revenue)
- [ ] 5k+ website visits
- [ ] 200+ GitHub stars on recipes repo
- [ ] 2+ HN front-page days
- [ ] 500+ Reddit upvotes aggregate
- [ ] 10+ awesome-list submissions accepted
- [ ] 50+ email signups (for post-launch features)

---

## Channel Performance History (from AI Dev Jobs / NHS)

| Channel | Visitors | Conversions | ROI |
|---------|----------|-------------|-----|
| HN (front page) | 500–2k | 5–20 | High |
| dev.to | 300–1k | 3–10 | Medium |
| Twitter | 100–500 | 2–5 | Low (awareness only) |
| Reddit | 200–1k | 5–15 | High |
| Awesome lists | 50–200/week | 2–10 | High |

**Strategy**: Prioritize HN, Reddit, awesome lists. Twitter for awareness. dev.to for SEO.

---

## Quick Checklist (Shane's Action Items)

### Phase 1 (Days 1-3): Social Media
- [ ] Post to HN (Tuesday 9:30am PT)
- [ ] Publish dev.to article (Tuesday)
- [ ] Post Twitter thread (Wednesday 8am PT)
- [ ] Post to r/learnprogramming, r/MachineLearning, r/coding (Thursday)
- [ ] Post LinkedIn article (Thursday)
- [ ] Email warm leads (Discord, Slack, personal networks)

### Phase 2 (Days 4-7): Awesome Lists
- [ ] Submit to hesreallyhim/awesome-claude-code (GitHub issue)
- [ ] Submit to appcypher/awesome-mcp-servers (PR or issue)
- [ ] Submit to awesome-developer-tools (PR or issue)

### Phase 3 (Days 8-14): MCP Directories
- [ ] Register on 10 MCP/directory platforms (10 min each, ~100 min total)

### Phase 4 (Days 15+): Monitor & Iterate
- [ ] Monitor HN/Reddit/dev.to comments
- [ ] Respond to questions with genuine answers
- [ ] Collect early-bird testimonials
- [ ] Identify next feature requests
- [ ] Publish case study

---

## Notes

- All copy is templates — personalize with real stories if possible
- Early-bird pricing is a scarcity signal: use "tiers fill weekly" language
- Link the free recipes repo in every post (drives awareness, separates free/paid value)
- CTA is always the checkout link: https://bringyour.ai
- Monitor Stripe dashboard for purchase data (which channels convert best)

---

**Ready to launch?** Start with Phase 1 (HN + dev.to + Twitter + Reddit). Expect first sales within 48 hours.
