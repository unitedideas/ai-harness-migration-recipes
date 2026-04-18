# Distribution & Submissions Tracker

All 12 recipes complete. This tracker monitors submission status across distribution channels.

## Assets Ready

| Asset | Status | Location |
|---|---|---|
| dev.to article | ✓ Ready to publish | DISTRIBUTION_devto_article.md |
| Twitter thread | ✓ Ready to post | DISTRIBUTION_twitter_thread.md |
| HN post | ✓ Ready to submit | DISTRIBUTION_hn_post.md |
| Reddit post (r/learnprogramming, r/coding, r/MachineLearning) | ✓ Ready to submit | DISTRIBUTION_reddit_post.md |
| LinkedIn article | ✓ Ready to post | DISTRIBUTION_linkedin_article.md |
| Mastodon thread | ✓ Ready to post | DISTRIBUTION_mastodon_post.md |

## Distribution Channels

### Social Media (Blocked on Shane's accounts)
| Channel | Status | Notes |
|---|---|---|
| Twitter/X | ⏳ Blocked | Needs Shane's dev account + Twitter dev app |
| dev.to | ⏳ Blocked | Needs Shane's dev.to account (email signup OK, but needs API key in settings) |
| Mastodon (fosstodon.org/@bringyour) | ⏳ Blocked | Needs account + posting |
| HackerNews | ⏳ Blocked | Needs HN account (email signup, then submit link) |
| Reddit | ⏳ Blocked | Needs Shane posting to r/learnprogramming, r/MachineLearning, r/coding |
| LinkedIn | ⏳ Blocked | Needs personal profile posting |

### Awesome Lists & Directories

#### CLI/PR-Based (Potentially doable)
| Repo | Status | Approach | Blocker |
|---|---|---|---|
| [appcypher/awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers) (5.4k★) | ⏳ Branch ready | Branch exists; needs PR permissions | PR access blocked (fork perms?) |
| [ripienair/free-for-dev](https://github.com/ripienair/free-for-dev) (121k★) | ⏳ PR blocked | Entry prepared for "APIs, Data, ML" | Repo rejects LLM-written PRs (honeypot checkbox); needs Shane |

#### Browser/Identity Required (Blocked on Shane)
| Directory | Stars | Status | Notes |
|---|---|---|---|
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 39k | ⏳ Blocked | Issue template requires browser + human checkbox |
| [Smithery](https://smithery.ai) | — | ⏳ Blocked | Dashboard login required |
| [Cursor Marketplace](https://cursor.com/marketplace) | — | ⏳ Blocked | Browser login required |
| [MCP Market](https://mcpmarket.com/submit) | 10k servers | ⏳ Blocked | Cloudflare blocks curl; browser form |
| [LobeHub MCP](https://lobehub.com/mcp) | 10k servers | ⏳ Blocked | Browser login required |
| [publicmcpregistry.com](https://publicmcpregistry.com/dashboard/mcps) | — | ⏳ Blocked | Dashboard login required |
| [cursor.directory](https://cursor.directory/plugins/new) | — | ⏳ Blocked | Browser-only submission (429 on CLI) |
| [Glama](https://glama.ai/mcp/servers) | — | ⏳ Blocked | Browser registration required |
| [PulseMCP](https://www.pulsemcp.com/submit) | — | ⏳ Blocked | Browser form (Cloudflare blocks curl) |
| [thataicollection.com](https://thataicollection.com/submit) | — | ⏳ Blocked | Browser form |
| [aiagentslist.com](https://aiagentslist.com/dashboard/submit) | — | ⏳ Blocked | Browser dashboard |

## Content Distribution Strategy

### Phase 1: Core Social (this week)
- Post Twitter thread (Shane's account)
- Publish dev.to article (Shane's account)
- Post to Mastodon, LinkedIn (if personal accounts available)

### Phase 2: Awesome Lists (this week–next)
- Submit HackerNews story link (Shane)
- Submit to awesome-claude-code via GitHub issue (Shane)
- Attempt appcypher/awesome-mcp-servers PR (check perms)

### Phase 3: MCP Directories (this week–next)
- Glama registration for both NHS + BringYour (Shane)
- Cursor Marketplace listing (Shane, BringYour product)
- Smithery, MCP Market, LobeHub (all browser/Shane-only)

### Phase 4: Content Expansion (ongoing)
- Create HN post copy (unique angle: "Hand-written harness migrations for AI tools")
- Create Reddit posts (r/learnprogramming, r/coding: "Migrating your AI agent config between Claude Code, Cursor, Codex, Aider")
- Create LinkedIn article linking to recipes
- Create case study: "How we built BringYour: automating harness migrations"

## Metrics
- GitHub stars: currently unknown (public? private?)
- npm downloads (if BringYour CLI tracked)
- dev.to views, reactions, comments
- Twitter impressions, engagement
- PR interest in awesome lists

## Action Items (Shane)
- [ ] Publish dev.to article (link goes to GitHub repo)
- [ ] Post Twitter thread (cite @bringyour)
- [ ] Submit to HackerNews
- [ ] Register Glama for NHS + BringYour MCPs
- [ ] Check appcypher/awesome-mcp-servers PR eligibility
- [ ] Submit to hesreallyhim/awesome-claude-code via issue
