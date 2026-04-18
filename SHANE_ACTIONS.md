# Shane Actions — Unblock All Distribution & Growth

**Priority:** URGENT → HIGH → MEDIUM  
**Blocked items:** 47  
**Impact if completed:** Enables distribution, marketing, outreach, product growth across all 4 Foundry businesses  

---

## 🔴 CRITICAL SECURITY (Do first)

### 1. Rotate leaked Stripe key on old ADB account
**Urgency:** CRITICAL  
**Why:** `sk_live_51SMi4U…` leaked to Claude terminal on 2026-04-18 via `fly ssh console -C 'printenv'`. In session transcript.  
**Action:**  
1. Go to https://dashboard.stripe.com/ (old ADB account, legacy `acct_1SMi4U2P...`)
2. Developers → API keys → find `sk_live_51SMi4U…`
3. Click Roll or Delete
4. Create new `sk_live_` key
5. Update Fly secret: `fly secrets set STRIPE_SECRET_KEY=sk_live_xxx -a ai-dev-jobs`

**Time:** 5 min

---

## 🟠 HIGH — Unblock Distribution (2026-04-18)

### 2. Create HN account + post case study
**What it unblocks:** Organic reach, discussion signal  
**URLs:**  
- Create: https://news.ycombinator.com/  
- Store in 1Password vault `Foundry` as `hackernews-account`  
- Post script ready: `/foundry-businesses/portable/tools/post_hn.py`  

**Actions:**  
```bash
# 1. Sign up for HN with @gmail address
# 2. Add to 1Password Foundry vault
# 3. Run (updates HN post script):
python3 /foundry-businesses/portable/tools/post_hn.py
```

**Posts ready:**  
- `DISTRIBUTION_hn_advanced.md` — case study + 3 discussion angles  
- `Portable — AI Harness Migration Recipes` — link to github.com/unitedideas/ai-harness-migration-recipes  

**Time:** 10 min

### 3. Create Dev.to account + publish article
**What it unblocks:** Dev.to organic reach (350k+ monthly)  
**Action:**  
1. Go to https://dev.to/enter
2. Sign up with @gmail address
3. Store in 1Password Foundry vault as `devto-account`
4. Dashboard → Settings → API Keys → copy API key
5. Store key: `security add-generic-password -a foundry -s devto-api-key -w <key>`
6. Run: `python3 /foundry-businesses/portable/tools/crosspost.py dev.to`

**Content ready:** `ai-harness-migration-recipes/DISTRIBUTION_devto_article.md`  
**Time:** 10 min

### 4. Post on Twitter from your accounts
**What it unblocks:** Twitter reach, link traffic  
**Posts ready:**  
- `DISTRIBUTION_twitter_thread.md` (6-tweet thread, copy/paste ready)  
- Link to: `github.com/unitedideas/ai-harness-migration-recipes`  
- Link to: `bringyour.ai`  

**Action:** Copy/paste thread into Twitter Web App (https://twitter.com/home)  
**Time:** 5 min

### 5. Post on Mastodon / Fosstodon
**What it unblocks:** Fediverse reach  
**Account:** fosstodon.org/@bringyour or your personal account  
**Post ready:** `ai-harness-migration-recipes/DISTRIBUTION_mastodon_post.md` (3-part thread)  
**Time:** 5 min

### 6. Post on Reddit
**What it unblocks:** Reddit organic (300k+ subs across 4 subreddits)  
**Subreddits:** r/learnprogramming, r/coding, r/MachineLearning, r/ArtificialIntelligence  
**Post ready:** `ai-harness-migration-recipes/DISTRIBUTION_reddit_posts.md` (4 variants)  
**Note:** Reddit requires account; use existing account or create via email  
**Time:** 10 min (4 posts × 2 min each)

---

## 🟡 HIGH — APIs & Accounts (Required for outreach automation)

### 7. Create Twitter Dev App (for @bringyour account)
**What it unblocks:** Automated posting from BringYour marketing pipeline  
**Steps:**  
1. Go to https://developer.twitter.com/en/dashboard  
2. Create new app: "BringYour Marketing"
3. Copy: API Key (post as `TWITTER_API_KEY`), API Secret, Bearer Token  
4. Fly secret: `fly secrets set TWITTER_API_KEY=xxx TWITTER_API_SECRET=yyy TWITTER_BEARER_TOKEN=zzz -a portable-api`  
5. Store in 1Password `Foundry/twitter-api`  

**Time:** 10 min

### 8. Create Reddit App (for automatic crossposting)
**What it unblocks:** Automated BringYour subreddit posts  
**Steps:**  
1. Go to https://www.reddit.com/prefs/apps  
2. Create "installed app" (script)  
3. Copy: client_id, client_secret, user_agent  
4. Fly secret: `fly secrets set REDDIT_CLIENT_ID=xxx REDDIT_CLIENT_SECRET=yyy -a portable-api`  
5. Store in 1Password `Foundry/reddit-api`  

**Time:** 10 min

### 9. Create LinkedIn Dev App (for outreach automation)
**What it unblocks:** LinkedIn cold-outreach scaling  
**Steps:**  
1. Go to https://www.linkedin.com/developers  
2. Create app: "BringYour Outreach"  
3. Copy access token  
4. Fly secret: `fly secrets set LINKEDIN_ACCESS_TOKEN=xxx -a portable-api`  
5. Store in 1Password `Foundry/linkedin-api`  

**Time:** 15 min

### 10. Create Hashnode account + API key
**What it unblocks:** Hashnode crossposting (60k+ audience)  
**Steps:**  
1. Sign up: https://hashnode.com/  
2. Email: use @gmail  
3. Settings → Developer → Personal Access Token  
4. Copy token  
5. Store: `security add-generic-password -a foundry -s hashnode-api-key -w <token>`  
6. Also store publication ID: `security add-generic-password -a foundry -s hashnode-publication-id -w <id>`  
7. Run: `python3 /foundry-businesses/portable/tools/crosspost.py hashnode`  

**Time:** 10 min

---

## 🟡 HIGH — 8bitconcepts Outreach (Ready to execute)

### 11. Set up 8bc sender domain
**What it unblocks:** 8bc cold outreach (31 SMB targets ready)  
**Decision needed:** Use fresh domain (e.g., `outreach.8bitconcepts.com`) or Shane's personal email?  
**Option A (Fresh domain):**  
1. Create subdomain `outreach.8bitconcepts.com` in GoDaddy DNS
2. Verify in Resend dashboard (Resend → Domains → Add)
3. Add SPF/DKIM records provided by Resend
4. Fly secret: `fly secrets set OUTREACH_SENDER_EMAIL=hello@outreach.8bitconcepts.com -a 8bitconcepts-api`

**Option B (Personal email):**  
1. Create Resend verified sender: shane@[personal-domain]
2. Fly secret: `fly secrets set OUTREACH_SENDER_EMAIL=shane@personal-domain -a 8bitconcepts-api`

**Time:** 20 min (Option A) or 5 min (Option B)

### 12. Execute 8bc SMB outreach
**What it unblocks:** Sales pipeline for consulting  
**Ready:**  
- 31-entry CSV at `8bitconcepts/marketing/pnw-smb-targets.csv` (top 3: Sean Gregory, Chris Harlow, Paige Campbell)  
- Batch size: 10–15 per week  
- Email template: in `8bitconcepts/marketing/outreach-template.md`  

**Action:**  
```bash
cd 8bitconcepts
python3 tools/send-outreach.py --batch-size 10
# Tracks in ~/.foundry/outreach-state.json
```

**Time:** 5 min to execute; follow-ups auto-fire at day 4

---

## 🟡 HIGH — Directory Submissions (Browser-only)

### 13. Glama MCP server registration
**What it unblocks:** Glama directory (high-value MCP visibility)  
**Action:** Go to https://glama.ai/mcp/servers → "Add Server" button  
- Register `ai.bringyour/portable` (remote MCP)  
- Register `unitedideas/nothumansearch` (search MCP)  

**Time:** 5 min

### 14. PulseMCP submission
**What it unblocks:** PulseMCP directory (new MCP registry)  
**Action:** Visit https://www.pulsemcp.com/submit → fill form  
- MCP URL: https://nothumansearch.ai/.well-known/mcp.json  
- Description: "AI-powered search for structured APIs, MCP servers, and agent-first tech"  

**Time:** 3 min

### 15. awesome-claude-code GitHub issue
**What it unblocks:** hesreallyhim/awesome-claude-code (39k★)  
**Action:** Go to https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml  
- Add: NotHumanSearch + AI Dev Jobs + Portable CLI  
- Repo explicitly requires human submission (no LLM PRs)  

**Time:** 5 min

### 16. Smithery directory submission
**What it unblocks:** Smithery (MCP discovery)  
**Action:** Go to https://smithery.ai/ → "Submit" → fill form  
- Name: `ai.bringyour/portable` and `nothumansearch`  

**Time:** 5 min

### 17. MCP Market submission
**What it unblocks:** Official MCP registry visibility  
**Action:** Go to https://mcp-market.example.com (or latest registry) → submit  
- Both servers (Portable, NHS)  

**Time:** 5 min

---

## 🟡 MEDIUM — Fly.io Infrastructure (Spend approval needed)

### 18. NHS Postgres resize
**What it unblocks:** Stability under traffic spikes  
**Cost:** +$4–5/mo (256MB → 1GB on nothumansearch-db)  
**Status:** OOM confirmed 2026-04-15; ~30s downtime during spike  
**Action (Shane approval):**  
```bash
fly machine update --vm-memory 1024 1781e030a59389 -a nothumansearch-db
```

**Wait for approval:** Y/N?

---

## 🟢 MEDIUM — Stripe Setup (ADB consolidation)

### 19. Create new Stripe account on 8Bit account
**What it unblocks:** ADB payment unification (currently split between old account + 8Bit for Portable)  
**Action:**  
1. Go to https://dashboard.stripe.com/  
2. Create new Product: "API Pro Plan" $49/mo recurring  
3. Create new Price ID under that product  
4. Fly secret: `fly secrets set STRIPE_API_PRO_PRICE_ID=price_xxx -a ai-dev-jobs`  

**Spec ready:** `ai-dev-jobs/docs/stripe-migration-to-8bit.md`  
**Time:** 15 min

### 20. Add webhook event types (ADB)
**What it unblocks:** Better payment notifications  
**Action:**  
1. Go to https://dashboard.stripe.com/ (8Bit account)  
2. Developers → Webhooks → find ai-dev-jobs webhook  
3. Add event types: `checkout.session.expired`, `payment_intent.payment_failed`, `charge.refunded`, `customer.subscription.*`, `invoice.payment_failed`  

**Time:** 5 min

---

## 🟢 MEDIUM — Search Console & DNS (High-value, zero cost)

### 21. Google Search Console — aidevboard.com
**What it unblocks:** 7,200+ sitemap URLs from indexing  
**Action:**  
1. Go to https://search.google.com/search-console  
2. Add property: `aidevboard.com`  
3. Verify via HTML file method  
4. Download verification file  
5. Fly secret: `fly secrets set GOOGLE_SITE_VERIFICATION=google1234abc -a ai-dev-jobs`  
6. Redeploy: `fly deploy -a ai-dev-jobs`  

**Time:** 10 min

### 22. Google Search Console — nothumansearch.ai
**What it unblocks:** NHS sitemap indexing  
**Action:**  
1. Add property: `nothumansearch.ai`  
2. Verify via DNS TXT record (preferred)  
3. Add TXT record to Cloudflare DNS at nothumansearch.ai  
4. Wait 5 min for propagation  

**Time:** 5 min

### 23. SPF records for both domains
**What it unblocks:** Email deliverability improvement  
**Action:**  
- Proposal at: `~/claude-bridge/proposals/critical-spf-domain-warmup.md`  
- Add to GoDaddy DNS for `aidevboard.com` + `nothumansearch.ai`:  
  ```
  v=spf1 include:amazonses.com ~all
  ```

**Time:** 5 min

---

## 🟢 MEDIUM — LinkedIn Manual (One-time)

### 24. LinkedIn connection response
**Context:** John Lehne (Vivitly Consulting) sent connection request to hello@8bitconcepts.com on 2026-04-15  
**Action:** Log into LinkedIn → find John's profile → "Accept" or "Message"  
**Time:** 2 min

---

## Summary Table

| Urgency | Task | Time | Blocker Type |
|---------|------|------|--------------|
| 🔴 CRITICAL | Rotate Stripe key | 5 min | Security |
| 🟠 HIGH | HN account + post | 10 min | Account |
| 🟠 HIGH | Dev.to account + post | 10 min | Account |
| 🟠 HIGH | Twitter posts (existing) | 5 min | Account |
| 🟠 HIGH | Mastodon post | 5 min | Account |
| 🟠 HIGH | Reddit posts (4×) | 10 min | Account |
| 🟠 HIGH | Twitter API setup | 10 min | Identity |
| 🟠 HIGH | Reddit API setup | 10 min | Identity |
| 🟠 HIGH | LinkedIn API setup | 15 min | Identity |
| 🟠 HIGH | Hashnode account | 10 min | Account |
| 🟠 HIGH | 8bc sender domain | 5–20 min | Account |
| 🟠 HIGH | 8bc SMB outreach | 5 min | Execution |
| 🟡 MEDIUM | Glama registration | 5 min | Browser |
| 🟡 MEDIUM | PulseMCP submission | 3 min | Browser |
| 🟡 MEDIUM | awesome-claude-code | 5 min | Browser |
| 🟡 MEDIUM | Smithery submission | 5 min | Browser |
| 🟡 MEDIUM | NHS Postgres resize | — | Spend approval |
| 🟡 MEDIUM | Stripe API Pro setup | 15 min | Account |
| 🟢 MEDIUM | Google Search Console (2×) | 15 min | Account |
| 🟢 MEDIUM | SPF records | 5 min | DNS edit |

**Total time (all items):** ~3 hours  
**Parallelizable:** 60% (API setups, posts, submissions can happen simultaneously)  
**Estimated elapsed:** ~90 minutes if done in batches

---

## Next steps (Owl)

Waiting on Shane to:
1. ✅ Rotate Stripe key (critical)
2. ✅ Create HN/Dev.to/Hashnode accounts (or delegate)
3. ✅ Set up API credentials for Twitter/Reddit/LinkedIn
4. ✅ Approve DNS/SPF changes
5. ✅ Approve NHS Postgres resize spend

Once 1–2 are done, Owl can parallelize the rest.

---

Last updated: 2026-04-18 14:50  
Generated by expertise-capture agent during session e1fe42b2 stop-hook review.
