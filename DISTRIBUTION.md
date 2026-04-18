# Distribution Strategy

Target: Place this repo in front of developers who switch between AI coding agents.
Goal: Become the reference guide for agent migration knowledge work.

## Awesome Lists (CLI submission targets)

| List | Relevance | Status | Notes |
|---|---|---|---|
| **awesome-cli-apps** | ⭐⭐⭐ High | TODO | CLI tool discovery; 3k+ stars |
| **awesome-developer-tools** | ⭐⭐⭐ High | TODO | Broader dev tools; 3k+ stars |
| **awesome-ai-tools** | ⭐⭐⭐ High | TODO | AI-specific; 2k+ stars |
| **awesome-migration-tools** | ⭐⭐ Medium | TODO | Niche but directly relevant |
| **awesome-coding-agents** | ⭐⭐ Medium | TODO | Emerging category; may not exist yet |

## High-impact reference submissions

| Target | Type | Friction | Impact |
|---|---|---|---|
| **Hacker News (Show HN)** | Community vote | Low (self-post) | 1-5k visibility if top 30 |
| **dev.to** | Long-form article | Low (manual) | 500-2k reach + backlink |
| **Lobsters** | Community vote | Low (self-post) | 500-1k visibility if top-page |
| **Product Hunt** | Launch | Medium (signup+review) | 5-10k visibility if featured |
| **Twitter/X** | Thread | Low | Organic reach in dev circles |

## Awesome list submission strategy

### Step 1: Identify list maintainers + rules
```bash
# Check if repo has CONTRIBUTING.md or submission guidelines
# Examples:
# - awesome-cli-apps: Minimal criteria (GitHub stars, active maintenance)
# - awesome-developer-tools: Broader scope, friendly to migration guides
```

### Step 2: Craft submissions (generic template)

```markdown
## AI harness migration recipes

**Description:**
Hand-written, tested migrations for moving your AI coding agent's 
configuration between Claude Code ↔ Cursor ↔ Codex ↔ Aider.
Covers 9/11 pairs (55%+). Each recipe documents silent breakages, 
format differences, and step-by-step checklists.

**Why it's useful:**
- Developers switching AI coding tools lose config, skills, hooks on each move
- Current state: no guides. Copy-paste breaks silently.
- This repo is the manual. One-command automation via [BringYour](https://bringyour.ai).

**Repo:** https://github.com/unitedideas/ai-harness-migration-recipes
**License:** CC BY 4.0
```

### Step 3: Which lists first (priority order)

1. **awesome-cli-apps** — lowest friction, good visibility
2. **awesome-developer-tools** — broader reach
3. **awesome-ai-tools** — specific audience
4. **awesome-migration-tools** — niche but direct hit

### Step 4: Earn mentions through content

- **dev.to article:** "Migrating your AI agent config between Claude Code, Cursor, Codex, and Aider"
  - Publish on dev.to → backlink to repo → boosts SEO + discoverability
  
- **HN Show HN:** Post under "Show HN" when distribution live
  - Goal: top 30 (gets 500-2k upvotes and 1-5k visibility)

- **Lobsters:** "Migrating between AI coding agent tools"
  - Niche but high-quality dev audience

## Timeline

- **Week 1:** Submit to 2-3 awesome lists (cli-apps, developer-tools, ai-tools)
- **Week 2:** Write dev.to article + post on HN + tweet thread
- **Week 3:** Monitor traction, update ROADMAP with community PRs

## Success metrics

- [ ] 50+ stars (baseline)
- [ ] 100+ stars (good)
- [ ] 200+ stars (excellent — means people are finding + sharing)
- [ ] 1-3 community PRs for missing recipes (Codex ↔ Aider pairs)
- [ ] Backlink from 2+ awesome lists
- [ ] 20k+ monthly site traffic to repo

## What NOT to do

- ❌ Don't claim "complete" — 5/11 pairs are missing
- ❌ Don't hide the blockers (need Codex/Aider installed for testing)
- ❌ Don't oversell: this is a reference guide, not a tool
- ❌ Don't submit to lists with low visibility (<1k stars) unless niche fit is perfect
