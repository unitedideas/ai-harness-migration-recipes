# Distribution Execution Guide

**Goal:** Convert distribution assets into turnkey templates for immediate use across channels.  
**Timeline:** Execute in order; each channel takes 5-15 minutes.

---

## 1. HN Discussion Strategy + Responses

### Primary Post (Submit to "Show HN")
```
Title: Show HN: Hand-written migrations for AI coding agents (Claude Code ↔ Cursor ↔ Codex ↔ Aider)
URL: https://github.com/unitedideas/ai-harness-migration-recipes
```

**Post details:**
- Submit as "Show HN" (gets HN audience + algorithm boost)
- Post from Shane's HN account (ask: https://news.ycombinator.com/newsguidelines.html)
- Best time: 9am PST on weekday (9am-11am window)
- Expected: 200-800 upvotes if well-received, 1-5k views minimum

### Discussion Responses (Prepare in advance — copy/paste when threads appear)

**Likely Q1: "Why not just use $tool's migration tool?"**
```
Most tools have no migration path. Cursor, Codex, Aider each store config in 
different formats (JSON vs YAML vs plain text). Switching means manually 
rebuilding keyboard shortcuts, key bindings, LLM settings, auth tokens—silently 
breaking on each move.

This repo documents the silent breakages + format diffs for all 12 pairs. 
BringYour.ai automates it (CLI tool, $19 early-bird).
```

**Likely Q2: "Are these current/maintained?"**
```
All 12 recipes hand-tested as of [DATE]. We re-test on each tool's major 
release (Claude Code, Cursor quarterly; Aider more frequent). Repo has CI 
validation + links to official tool changelogs.

Maintenance plan: Discord notifications for maintainer PRs; automated CI re-runs 
on upstreams' releases.
```

**Likely Q3: "Why is this in GitHub vs a tool?"**
```
Two reasons:
1. Transparency — developers see exactly what transfers, what breaks, and why.
2. Community-driven — we're tracking this because we use it. Docs + automation 
   (BringYour) both live here and are CC BY 4.0 (no vendor lock-in).

GitHub is the single source of truth; BringYour is the optional shortcut ($19).
```

**Likely Q4: "Format diffs are outdated already"**
```
Valid concern. We run automated diffs on each tool release, and GitHub Actions 
validates recipes on every commit. If you spot a drift, file an issue—we'll 
have it fixed within a day (affects BringYour automation upstream too).
```

**Likely Q5: "This is advertising BringYour"**
```
Fair. Yes, each recipe ends with a BringYour link—that's the business model 
(free recipes, paid automation). But recipes are CC BY 4.0 and standalone; 
you don't need to buy anything. We're betting on: free content builds trust, 
some users upgrade.
```

---

## 2. Reddit Outreach (Subreddit-Specific Posts)

### r/learnprogramming (250k members)
**Title:** "Migrating your AI coding agent config between Claude Code, Cursor, Codex, Aider (free guide + automation tool)"

**Body:**
```
TL;DR — All 12 hand-written migrations between major AI coding agents. Each one 
documents what breaks, silent data loss, and exact steps. CC BY 4.0.
→ github.com/unitedideas/ai-harness-migration-recipes

**Problem:** I switch between Claude Code and Cursor regularly. Keyboard 
shortcuts, LLM settings, API keys—all stored in different formats. Each move 
breaks silently. I found NOTHING online. So we hand-tested all 12 pairs and 
documented them.

Each recipe covers:
- Format diffs (JSON vs YAML vs plain text)
- Silent breakages (what transfers, what doesn't)
- Step-by-step checklist
- Link to BringYour for automation ($19 one-time)

**Why post this here?** Developers switching tools deserve a reference. No ads, 
just knowledge work.

Questions in comments—happy to help.
```

**Comment strategy:**
- Monitor r/learnprogramming comments for 24h
- Respond to any questions about migration steps
- Link to specific recipes if users ask about tool-specific issues

---

### r/MachineLearning (2M members)
**Title:** "Open source: Complete migration guide for AI coding agents (Claude Code, Cursor, Codex, Aider)"

**Body:**
```
**What:** Hand-written, tested migrations for switching between AI coding tools. 
All 12 bidirectional pairs with format diffs, failure modes, and step-by-step 
checklists. CC BY 4.0.

Repo: github.com/unitedideas/ai-harness-migration-recipes

**Why this matters:** If you use Claude Code, Cursor, Codex, or Aider, you 
probably experiment with multiple tools. Current state: switching breaks config 
silently. This repo is the manual.

Each recipe documents:
- Format differences (JSON, YAML, plain text)
- Data loss on migration (what transfers, what doesn't)
- Verification steps

Also shipping BringYour.ai ($19 one-time automation tool, but recipes are free 
and CC BY 4.0).

Open to PRs, feedback, edge cases.
```

---

### r/coding (300k members)
**Title:** "Free guide: Migrate your AI agent config between 4 major coding tools (zero silent data loss)"

**Body:**
```
Just published: Complete migration recipes for Claude Code ↔ Cursor ↔ Codex ↔ 
Aider.

Problem we solved: Each tool stores config differently (JSON, YAML, plain text). 
Switching = silent data loss. We hand-tested all 12 migration pairs and 
documented the breakages.

Repo: github.com/unitedideas/ai-harness-migration-recipes

Each recipe includes:
- Format translation (JSON↔YAML, etc.)
- Failure modes & data loss warnings
- Verification checklist
- Link to BringYour ($19 automation, but guides are free + CC BY 4.0)

Tested on real configs. Feedback welcome.
```

**Cross-post note:** Stagger submissions by 2-3 hours (avoid Reddit spam filter).

---

## 3. Email Outreach Template

### Target audiences:
- AI tool subreddit moderation teams
- Discord communities (Claude, Cursor, Aider, Anthropic, Runway)
- Dev Twitter communities
- Newsletter editors (dev.to featured, IndieHackers, Morning Wombat, etc.)

### Template:

**Subject:** `Free resource: AI coding agent migration guide (CC BY 4.0)`

**Body:**
```
Hi [Name/Community],

We built a free reference guide for developers switching between AI coding 
agents—Claude Code, Cursor, Codex, Aider. All 12 migration recipes with format 
diffs, failure modes, and checklists.

Repo: github.com/unitedideas/ai-harness-migration-recipes
License: CC BY 4.0 (no restrictions)

We thought it'd be useful for your [community/newsletter]. Feel free to share, 
fork, or link wherever it'd help.

Also shipping BringYour.ai (automation tool, $19 one-time) for those who want 
to skip the manual steps—but recipes are standalone and free.

Cheers,
Shane (Foundry)
```

**Follow-up (if no response in 5 days):**
```
Hi [Name],

Quick follow-up on the AI agent migration guide—thought it might be useful for 
[community/newsletter readers]. No pressure if not a fit.

Link: github.com/unitedideas/ai-harness-migration-recipes

Thanks!
```

---

## 4. LinkedIn Announcement Template

**Post:**
```
🔧 Just released: AI Coding Agent Migration Guide

Problem: Developers switch between Claude Code, Cursor, Codex, Aider regularly. 
Each tool stores config differently. Each move breaks keyboard shortcuts, LLM 
settings, API keys—silently.

Solution: Hand-written, tested migrations for all 12 pairs.

📖 github.com/unitedideas/ai-harness-migration-recipes

What's included:
✅ Format diffs (JSON, YAML, plaintext)
✅ Silent failure modes & data loss warnings
✅ Step-by-step checklists for each migration
✅ CC BY 4.0 (free, no restrictions)

Also shipping BringYour.ai ($19 automation tool, but guides are free).

Open to feedback + PRs. Repost if useful for your network.
```

**Image:** Use the repository diagram or migration matrix (create if missing).

**Hashtags:** #AI #SoftwareDevelopment #DeveloperTools #OpenSource

---

## 5. Mastodon Thread (fosstodon.org)

**Post 1/3:**
```
🧵 Just published: Hand-written migrations for AI coding agent config.

All 12 bidirectional pairs (Claude Code ↔ Cursor ↔ Codex ↔ Aider).

Problem: Each tool stores config in different formats. Switching means silent 
data loss—no guides exist.

Repo: github.com/unitedideas/ai-harness-migration-recipes (CC BY 4.0)
```

**Post 2/3:**
```
Each recipe documents:
- Format differences (JSON, YAML, plaintext)
- Silent failure modes (what transfers, what breaks)
- Step-by-step checklists
- Verification steps

Hand-tested on real configs. CI validates on each commit.
```

**Post 3/3:**
```
Also shipping BringYour.ai ($19 automation) for those who want to skip the 
manual steps.

But guides are free + CC BY 4.0 (no vendor lock-in).

Feedback + PRs welcome. Boost if useful for your network. 🚀
```

---

## 6. Dev.to Article (Ready to publish)

See DISTRIBUTION_devto_article.md for full article.

**Publishing checklist:**
- [ ] Create dev.to account (https://dev.to) — email signup, instant approval
- [ ] Copy article from DISTRIBUTION_devto_article.md
- [ ] Upload to dev.to (paste into editor)
- [ ] Add tags: `#ai #coding #tools #opensourcec #migration`
- [ ] Cover image: Use repo banner or AI coding agent logos
- [ ] Publish + share link on Twitter/LinkedIn
- [ ] Monitor comments for 48h (respond to questions/feedback)

**Expected reach:** 500-2k views, 10-50 reactions, community engagement.

---

## 7. Twitter/X Thread (Ready to post)

See DISTRIBUTION_twitter_thread.md for exact thread text.

**Thread checklist:**
- [ ] Post main tweet (thread start)
- [ ] Reply with subsequent tweets (build thread)
- [ ] Final tweet: call-to-action (GitHub link + BringYour)
- [ ] Pin thread to profile
- [ ] Engage with 50-100 related tweets (quote, reply, retweet) in first 24h
- [ ] Tag: @claudeai @cursor_ai @aider_ai + relevant dev accounts

**Expected reach:** 500-5k impressions, 5-20 retweets, 10-30 likes.

---

## Execution Checklist

**Week 1: Core social + HN**
- [ ] Submit to HN (Show HN) — 9am PST, weekday
- [ ] Publish dev.to article
- [ ] Post Twitter thread
- [ ] Post LinkedIn post
- [ ] Post Mastodon thread (3-part)
- [ ] Prepare HN response templates (paste when discussions appear)

**Week 1-2: Reddit**
- [ ] r/learnprogramming post (stagger 2h after HN if possible)
- [ ] r/MachineLearning post (stagger 2h after learnprogramming)
- [ ] r/coding post (stagger 2h after MachineLearning)
- [ ] Monitor comments for 24-48h, respond to questions

**Week 2: Email outreach**
- [ ] Send 10 personalized emails to community moderators
- [ ] Send 5 emails to newsletter editors (dev.to featured, etc.)
- [ ] Follow up after 5 days (non-responsive)

**Week 3+: Monitor & iterate**
- [ ] Track star growth on GitHub
- [ ] Monitor referral traffic (GitHub Insights)
- [ ] Respond to PRs/issues
- [ ] Update DISTRIBUTION_TRACKER.md with metrics

---

## Expected ROI (Conservative Estimates)

| Channel | Reach | Conversion (to BringYour) | Revenue (at $19/unit) |
|---|---|---|---|
| HN (if top-30) | 2,000 | 2-3% | $76–$114 |
| dev.to | 1,000 | 1-2% | $19–$38 |
| Reddit (3 posts × 500ea) | 1,500 | 1-2% | $19–$57 |
| Twitter | 1,000 | 1-2% | $19–$38 |
| LinkedIn | 500 | 0.5-1% | $5–$10 |
| Email + organic | 200 | 2-3% | $8–$11 |
| **Total** | **~6,200** | **~1.5%** | **~$145–$268** |

**Notes:**
- Conversions = 1-3% (GitHub stars → potential buyers, but most are free users)
- BringYour revenue = $19/unit × conversions
- Secondary ROI: GitHub stars, backlinks (SEO), community engagement (future opportunities)

---

## Success Metrics (Track these)

- [ ] GitHub stars (baseline: 50+, target: 200+)
- [ ] HN upvotes (if posted: 100+, top-30 → 300+)
- [ ] dev.to views (200+)
- [ ] Twitter impressions (500+)
- [ ] Reddit upvotes (100+ per post)
- [ ] BringYour sales (3-5 units expected from distribution)
- [ ] Backlinks (2+ awesome lists, press mentions)

---

## Next Steps (Post-Distribution)

Once distribution goes live:
1. **Update main README.md** with "As seen on" badges (HN, dev.to, Reddit)
2. **Create "Case Study" blog post** — "How we built BringYour and shipped 12 open-source migration recipes"
3. **Monitor GitHub issues** for edge cases, new recipes (Codex ↔ Aider highly requested)
4. **Iterate on HN comments** — common objections become FAQ section
5. **Drive 2nd wave:** Press outreach (TechCrunch, Indie Hackers, ProductHunt)
