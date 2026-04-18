# Revenue Execution Roadmap — Foundry Businesses
**Date**: 2026-04-18  
**Audience**: Shane (executive decisions + account access)  
**Status**: 4/4 businesses LIVE; 0 revenue converted; clear action items

---

## Dashboard Summary

| Business | Status | Live Since | Revenue | Next Blocker |
|---|---|---|---|---|
| **BringYour** | 🟢 LIVE + SELLING | 2026-04-18 | $0 (seed users only) | Shane: post to HN/Reddit/Twitter |
| **AI Dev Jobs** | 🟢 LIVE | 2025+ | $0 (265 companies contacted, zero claims) | Shane: analyze why zero conversion |
| **Not Human Search** | 🟢 LIVE | 2025+ | $0 (growing data, quality improving) | Shane: SEO verification + Postgres resize |
| **8bitconcepts** | 🟢 LIVE (consulting pivot) | 2026-04-17 | $0 (pipeline manual) | Shane: launch kit + cold outreach |

---

## BringYour — Highest Revenue Potential (URGENT)

**Product**: Commercial harness-migration tool + MCP server. Live payment links.

### Status ✅
- [x] Stripe integration live ($19/$29/$49 tiers)
- [x] Webhook processing (checkout.session.completed + charge.refunded)
- [x] License generation + issuance
- [x] CLI downloads + validation
- [x] Remote MCP server (tools/call round-trip verified)
- [x] 4/4 Fly secrets deployed
- [x] Foundry monitor probes every 30min (webhook drift + license round-trip)
- [x] 12 recipes + case study published with BringYour CTAs

### Revenue Blocker 🚨
**Zero paying customers yet** (only 1 smoke-test lead, pre-suppressed).

### Shane's Action Items
1. **Post to HackerNews** (early morning, weekend better)
   - Asset: `DISTRIBUTION_hn_advanced.md` (advanced angles focused on harness pain)
   - Target: #1 HN front page drives 5,000–20,000 clicks
   - Link: bringyour.ai or recipes repo with $19 CTA

2. **Post to r/MachineLearning + r/coding + r/learnprogramming**
   - Assets: `DISTRIBUTION_reddit_posts.md` (3 angles: automation, CLI tool, SDK)
   - Strategy: 10-15 upvotes each = 2,000–5,000 clicks
   - Cross-link to recipes, emphasize "automated harness migrations save engineering time"

3. **Tweet from personal account**
   - Asset: `DISTRIBUTION_twitter_thread.md` (20-tweet thread)
   - Target: Reach engineering audience, link to HN post + recipes
   - Timing: coordinate with HN submission (day after for momentum)

4. **LinkedIn article (optional, lower leverage)**
   - Asset: `DISTRIBUTION_linkedin_article.md`
   - Timing: post after HN/Reddit win to capture momentum

### Revenue Math
- 10k clicks to bringyour.ai
- 2% conversion (200 visitors to checkout)
- 5% checkout completion (10 purchases)
- **10 × $49 avg = $490 first week**

### Timeline
Do this **this week** before momentum decays. Each day of delay = opportunity cost.

---

## AI Dev Jobs — Sales Conversion Mystery

**Product**: Job aggregator for AI roles (8,618 jobs, 513 companies).

### Status ✅
- [x] 265 companies contacted (5 batches)
- [x] Auto follow-ups running (fires 4 days after each send)
- [x] Premium API tier shipped ($49/mo Pro plan)
- [x] Stripe webhook monitoring active
- [x] Job claim CTA deployed on 5,457 pages
- [x] /locations, /for-companies, 13 /hire/{role} landing pages

### Revenue Blocker 🚨
**Zero claims after 265 company contacts.** This suggests:
1. **Positioning problem**: Companies don't see ADB as their hiring tool (vs LinkedIn, Indeed, internal talent)
2. **Messaging problem**: Outreach email doesn't land the hook (clarity, proof, urgency missing?)
3. **Product problem**: Feature gaps prevent signup/purchase (missing integrations? pricing wrong?)
4. **Execution problem**: Email suppressed/spam folder (SPF records not set up)

### Shane's Analysis Tasks
1. **Email deliverability**
   - Check: do SPF records exist for aidevboard.com?
   - Action: Add `v=spf1 include:amazonses.com ~all` TXT record in GoDaddy DNS (BLOCKING: needs Shane's DNS access)
   - Impact: 20–30% of emails likely landing in spam without this

2. **Outreach message audit**
   - Question: what was the exact email sent to 265 companies?
   - Look for: is it clear what ADB does? Does it mention price? Does it have a call-to-action?
   - Hypothesis: if the email doesn't say "you can list jobs for $X/month" + proof (case study, customer logos), it won't convert
   - Fix: A/B test 2 versions on the next batch (once SPF is live)

3. **Pricing/product audit**
   - Question: why would a company pay for ADB vs Indeed/LinkedIn Jobs?
   - Check: does the /for-companies page clearly explain ROI? (Time to hire? Cost per hire? Niche audience access?)
   - Hypothesis: Pro tier ($49/mo) may be too aggressive for cold outreach; maybe free tier exists but companies don't know

4. **Competitive positioning**
   - Is ADB positioned as "for AI job seekers" (passive) or "for companies hiring AI talent" (active)?
   - If passive (seeker-first), companies won't buy because they want hiring tools, not seeker tools
   - If active (company-first), the message + landing page must emphasize "find engineers faster"

### Recommended Action
- **Week 1**: Fix SPF records (Shane + DNS access)
- **Week 2**: Pull the first outreach email, analyze it, run 1-week A/B test with a revised version
- **Week 3**: Measure: did claims increase? If yes, roll out new message to remaining 200 companies

### Revenue Math (conservative)
- 265 companies → 5% conversion = 13 claims
- 13 × $49/mo × 6 months (before churn) = **$3,822**
- If message fix works (10% conversion) = **$7,644** in first half-year

---

## Not Human Search — Quality ✓, Growth Blocked

**Product**: AI agent search engine (1,990 indexed sites, high-quality).

### Status ✅
- [x] Scraper: 553 sources, daily refresh, zero spam
- [x] Quality: isSpam() filter, OR-tsquery fallback, agentic_score/75 floor
- [x] Verify-MCP v1.5.0: 8 tools, JSON-RPC probing
- [x] Foundry monitor: probes MCP round-trip every 30min
- [x] API: /health + /status endpoints return 200
- [x] SEO: llms.txt, robots.txt, sitemap.xml, OG+Twitter tags

### Revenue Blocker 🟡
**Postgres OOM** (2026-04-15 confirmed + recurred this session on bulk-submit spike).

**Current**: shared-cpu-1x:256MB (Fly default)  
**Issue**: crashes under 500+ QPS, recovers in 30s, customers see timeout  
**Solution**: bump to ≥1GB (`fly machine update --vm-memory 1024 <id> -a nothumansearch-db`)  
**Cost**: ~$4–5/mo more (~4x on that line)  
**Downtime**: <1min during resize

### Shane's Approval Needed
1. **Spend approval**: Confirm cost increase is acceptable
2. **Timing**: Schedule resize during low-traffic window (late evening UTC)

### SEO Blockers
1. **Google Search Console**: NHS needs DNS TXT verification (not currently verified)
   - Unblocks: 7,200+ sitemap URLs from indexing
   - Shane's action: GSC → NHS domain → add DNS record at GoDaddy
2. **SPF + DKIM**: If NHS sends transactional emails (alerts, saved searches), needs SPF
   - Blocker: not urgent unless email feature ships

### Revenue Potential
Once Postgres is healthy + GSC verified:
- Organic search traffic → premium features (saved searches, alerts, API Pro) 
- Current: free model. Potential: $9/mo premium tier (advanced filters + API)
- Unblocked by: data + product, not by tech

---

## 8bitconcepts — Consulting Pivot (Manual Pipeline)

**Product**: AI consulting + advisory (4 research papers published, 11 page website).

### Status ✅
- [x] /work-with-us, /case-studies, /faq, /diagnostic pages live
- [x] 6 consulting-funnel research papers published + linked
- [x] Local hub + 4 city pages (Vancouver, Portland, Tigard, Seattle)
- [x] All SEO tags, llms.txt, ai-plugin.json deployed
- [x] Resend domain verified for transactional email

### Revenue Blocker 🟠
**Launch kit incomplete** (blocking cold outreach & warm lead capture).

Required (blocking):
1. **Google Business Profile** (local biz listing for "8bitconcepts AI consulting")
   - Action: GBP claim at Google My Business, phone verify (Shane only)
   - Impact: local search visibility (Vancouver, Portland, Tigard area)

2. **Chamber of Commerce memberships** (credibility + referral source)
   - Cost: ~$1,500/yr (Vancouver + Portland + Tigard)
   - Decision: Shane's approval on spend

3. **Cal.com integration** (lead-form CTA → 30-min intro call booking)
   - Asset: link prepared, just needs config
   - Action: Shane creates Cal.com account, updates /work-with-us CTA to Cal link

4. **Cold outreach campaign** (31-entry SMB CSV: PNW targets)
   - Top 3 targets: Sean Gregory, Chris Harlow, Paige Campbell
   - Strategy: 10–15 emails/week from Shane's personal email (ADB reputation is bad per `project_aidevboard_email_spam.md`)
   - Timeline: 6–8 weeks to first meeting

Optional (higher leverage, later):
- Research paper drip email (newsletter signup on all 11 papers)
- Gated whitepaper (email for premium paper) = lead magnet

### Revenue Math
- 31 cold outreach targets
- 5% response rate = 1.5 conversations
- 20% close rate = 0.3 deals
- $25k avg deal = **$7,500 Q2** (conservative, real deals are $50k–100k)

### Timeline
- **Week 1**: Create GBP + set up Cal.com
- **Week 2**: Start cold outreach (10 emails)
- **Week 4**: First warm call (response lag)
- **Week 8**: First contract (if luck + skill align)

---

## Unified Action Priority (Shane Only)

### 🚨 IMMEDIATE (This Week)
1. **BringYour: Post to HN + Reddit + Twitter** 
   - Effort: 30 mins
   - Expected ROI: $500–2,000 first week
   - Assets ready: `DISTRIBUTION_hn_advanced.md`, `DISTRIBUTION_reddit_posts.md`, `DISTRIBUTION_twitter_thread.md`

2. **AI Dev Jobs: SPF DNS record**
   - Effort: 5 mins (add TXT record in GoDaddy)
   - Expected ROI: +20% email deliverability
   - Blocks: 265 company follow-ups from landing in spam

### 📋 THIS WEEK (2-3 hours)
3. **NHS: Postgres resize approval + 8bitconcepts: Launch kit setup**
   - Effort: 1 hour decision + approval
   - Expected ROI: NHS stability → future customers, 8bc credibility → first meetings

4. **ADB: Analyze first 265 emails + plan A/B test**
   - Effort: 30 mins analysis + 1 hour revised copy
   - Expected ROI: 5–10% conversion on next batch = $500–2,000 annualized

### 📅 THIS MONTH
5. **8bitconcepts: Cold outreach blitz** (10–15 emails/week, 6–8 weeks)
   - Effort: 15 mins/week
   - Expected ROI: $7,500+ Q2 if 1 deal closes

6. **Google Search Console verification** (NHS + ADB)
   - Effort: 15 mins each
   - Expected ROI: +40% organic search over 6 months

---

## Key Metrics (Monthly Review)

Track these on a dashboard or spreadsheet:

| Business | Metric | Target | Current | Trend |
|---|---|---|---|---|
| BringYour | New customers | 10/mo | 0 | TBD (post-marketing) |
| BringYour | MRR | $500 | $0 | 🔴 |
| ADB | Claims/mo | 10 | 0 | 🔴 |
| ADB | API Pro subscriptions | 5 | 0 | 🔴 |
| NHS | Organic sessions | 1,000 | TBD | TBD |
| 8bc | Warm meetings | 2 | 0 | 🔴 |
| 8bc | Proposals out | 2 | 0 | 🔴 |
| 8bc | Contracts signed | 0.5 | 0 | 🔴 |

---

## System Health (Last Verified 2026-04-18)

| System | Status | Last Check | Note |
|---|---|---|---|
| Foundry Monitor (30min cadence) | ✅ Green | 14:30 UTC | webhook drift + license round-trip probes active |
| BringYour Stripe | ✅ Live | 14:25 UTC | payment links verified, webhook processed 1 test transaction |
| ADB Scraper | ✅ Green | 14:22 UTC | 8,618 jobs, 513 companies, last refresh 2h ago |
| NHS Postgres | 🟡 Fragile | 14:20 UTC | 256MB, OOM crashes on spikes; pending resize approval |
| 8bc Website | ✅ Live | 14:18 UTC | all pages 200, SEO tags verified |
| CI/Recipes | ✅ Green | 14:15 UTC | 12/12 recipes validated, all green |

---

## Next Agent/Session

1. Once Shane completes action items above → measure outcomes (1 week)
2. If BringYour gets traction (>5 customers) → scale marketing
3. If ADB still at zero → pivot messaging or try B2B SaaS platform (G2, ProductHunt)
4. If 8bc gets warm lead → support first deal close (proposal, contract, onboarding)

