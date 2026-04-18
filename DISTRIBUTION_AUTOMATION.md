# Distribution Automation

Executable submission workflows for high-impact distribution channels.

## Quick Start (for Shane)

### 1. Awesome Lists (5 minutes, 3 high-impact submissions)

```bash
# Dry run first (shows what would happen)
python tools/submit-awesome-lists.py --dry-run

# Submit to all three lists
python tools/submit-awesome-lists.py

# Or submit to one specific list
python tools/submit-awesome-lists.py --list awesome-cli-apps
```

**What it does:**
- Forks sindresorhus/awesome-cli-apps, imteekay/awesome-developer-tools, sindresorhus/awesome
- Edits README files to add AI Harness Migration Recipes entry
- Commits, pushes, creates PRs
- Provides PR links for verification

**Expected outcome:**
- 3 PRs created across 8k+ potential reach
- Each takes 3-7 days for maintainer review/merge
- Once merged, update main README.md with badges

**Example completion tracking:**
```
✓ awesome-cli-apps (PR #123) — merged 2026-04-20
  → Added 'Featured in awesome-cli-apps' badge to README
✓ awesome-developer-tools (PR #45) — pending review
✓ awesome-ai (PR #789) — merged 2026-04-19
```

---

## Manual Workflows (for channels requiring account login)

All workflows below require Shane's personal accounts. See DISTRIBUTION_TRACKER.md for details.

### Social Media

**Twitter** (requires @bringyour or personal account)
```
Use copy-paste text from DISTRIBUTION_twitter_thread.md
Paste into Twitter composer → Post
```

**dev.to** (requires account + email signup)
```
1. Sign up at dev.to
2. Settings → API Keys → copy API key
3. Paste text from DISTRIBUTION_devto_article.md into editor
4. Publish → links to GitHub repo
```

**HackerNews** (requires HN account)
```
1. Create HN account (email signup)
2. Visit news.ycombinator.com/submit
3. Paste GitHub repo link: https://github.com/unitedideas/ai-harness-migration-recipes
4. Title: "AI Harness Migration Recipes: Hand-written migrations between Claude Code, Cursor, Codex, Aider"
5. Submit
```

**Reddit** (requires account + posting to multiple subreddits)
```
Subreddits (use copy-paste from DISTRIBUTION_reddit_posts.md):
- r/learnprogramming
- r/coding  
- r/MachineLearning
- r/ArtificialIntelligence

Use reddit.com/submit, paste markdown from DISTRIBUTION_reddit_posts.md
```

**LinkedIn** (requires personal profile)
```
Use text from DISTRIBUTION_linkedin_article.md
Paste into LinkedIn article editor → Publish
```

**Mastodon** (requires fosstodon.org account)
```
1. Create account at fosstodon.org
2. Paste thread from DISTRIBUTION_mastodon_post.md
3. Post as 3-part thread
```

---

## Directory Submissions (Browser-only, no automation)

All submissions below require browser login. See DISTRIBUTION_TRACKER.md for full list.

**High-priority** (if time permits):
- Glama.ai: Register both NHS + BringYour MCPs
- hesreallyhim/awesome-claude-code: Submit via GitHub issue template
- Cursor Marketplace: List BringYour product

**Lower-priority** (9 others listed in DISTRIBUTION_TRACKER.md):
- Smithery, MCP Market, LobeHub, publicmcpregistry, cursor.directory, PulseMCP, thataicollection, aiagentslist

---

## Success Metrics

### Awesome Lists
- [ ] awesome-cli-apps PR created & linked
- [ ] awesome-developer-tools PR created & linked  
- [ ] awesome-ai PR created & linked
- [ ] Track # of merged PRs + date merged
- [ ] Monitor referral traffic from awesome lists to GitHub repo

### Social Media
- [ ] Twitter thread posted (track impressions, engagement)
- [ ] dev.to article published (track views, reactions)
- [ ] HackerNews submitted (track votes, #1 on frontpage?)
- [ ] Reddit posts submitted to 4 subreddits
- [ ] LinkedIn article published
- [ ] Mastodon thread posted

### Combined Impact
- Social reach: 50k+ impressions (estimate from Twitter + HN + Reddit)
- GitHub stars: Track daily growth rate pre/post distribution
- Referral traffic: Segment by source in GitHub
- BringYour.ai traffic: Segment by utm_source=github-recipes, utm_medium=distribution

---

## Distribution Calendar

### Week 1 (2026-04-18 to 2026-04-24)
- [ ] **Mon-Wed**: Awesome-list submissions (automated script)
- [ ] **Wed**: Social media posts (Twitter, dev.to, HN, Reddit, LinkedIn, Mastodon)
- [ ] **Thu**: Monitor PR status on awesome lists
- [ ] **Fri**: Post "featured in awesome lists" announcement if 1+ merged

### Week 2 (2026-04-25 to 2026-05-01)
- [ ] Track merge status on awesome-list PRs
- [ ] Directory submissions (browser-based, low priority)
- [ ] Update README badges once lists merge
- [ ] Optional: Post on BringYour.ai about distribution success

### Post-Merge
- [ ] Update README.md with "Featured in" badges:
  ```markdown
  [![Featured in awesome-cli-apps](https://img.shields.io/badge/featured%20in-awesome--cli--apps-blue)](https://github.com/sindresorhus/awesome-cli-apps)
  [![Featured in awesome-developer-tools](https://img.shields.io/badge/featured%20in-awesome--developer--tools-blue)](https://github.com/imteekay/awesome-developer-tools)
  ```
- [ ] Post social proof: "Just got featured in awesome-cli-apps, awesome-developer-tools, and awesome 🎉"

---

## Troubleshooting

### Awesome-list Script Errors

**"Fork already exists"**
```bash
# Use existing fork
python tools/submit-awesome-lists.py --list awesome-cli-apps
# If that fails, manually delete fork and re-run
gh repo delete YOUR_USERNAME/awesome-cli-apps --confirm
python tools/submit-awesome-lists.py
```

**"Section not found in README"**
- Check the actual section name (might be `## Development` vs `### Development`)
- Edit LISTS config in submit-awesome-lists.py with correct section name
- Re-run script

**"PR already exists"**
- Close the stale PR in GitHub UI
- Delete local fork: `rm -rf awesome-cli-apps`
- Re-run script

### Social Media Not Loading
- dev.to might need email confirmation — check inbox + spam folder
- HN requires account age 24+ hours — create account Wednesday, submit Friday
- Reddit requires subreddit participation history — may need manual posting

### No Traction After 1 Week
- Check DISTRIBUTION_TRACKER.md for additional channels
- Consider paid promotion on HN or ProductHunt
- Expand to alternative platforms (Stack Overflow, dev blogs, email lists)

---

## Next Phase (Post-Distribution)

Once distribution is shipped and metrics are tracked:

1. **Write post-mortem**: What worked, what didn't, traffic sources
2. **Update BringYour.ai**: Link to "GitHub Recipes" from homepage with distribution stats
3. **Plan next distribution cycle**: Expand to YouTube, podcasts, conference talks
4. **Monitor ongoing**: Set up weekly email alert tracking GitHub stars, BringYour traffic

---

## Files Reference

| File | Purpose |
|---|---|
| `DISTRIBUTION_twitter_thread.md` | Ready-to-post Twitter thread |
| `DISTRIBUTION_devto_article.md` | Ready-to-publish dev.to article |
| `DISTRIBUTION_hn_post.md` | Ready-to-submit HN post |
| `DISTRIBUTION_hn_advanced.md` | Alternative HN post with discussion angles |
| `DISTRIBUTION_reddit_posts.md` | Reddit posts for 4 subreddits |
| `DISTRIBUTION_linkedin_article.md` | Ready-to-post LinkedIn article |
| `DISTRIBUTION_mastodon_post.md` | Ready-to-post Mastodon thread |
| `SUBMISSION_PLAYBOOK.md` | Manual step-by-step awesome-list submission guide |
| `DISTRIBUTION_TRACKER.md` | Status of all distribution channels |
| `tools/submit-awesome-lists.py` | Automated awesome-list submission (Python) |
| `tools/submit-awesome-lists.sh` | Shell version of submission automation |
