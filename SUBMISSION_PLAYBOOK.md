# Awesome List Submission Playbook

This playbook provides exact copy-paste commands for Shane to submit to high-impact awesome lists. Each submission takes 5-10 minutes.

## Entry Template (Use for all submissions below)

```markdown
- [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Hand-written, tested migrations between Claude Code ↔ Cursor ↔ Codex ↔ Aider. All 12 bidirectional pairs with format diffs, breakage warnings, and step-by-step checklists. CC BY 4.0. [Automation via BringYour](https://bringyour.ai).
```

---

## #1: awesome-cli-apps (3.2k★)

**Why first:** Lowest friction, strong visibility. "AI coding agent config tool" fits perfectly.

### Steps

1. **Fork & clone (or use web UI)**
   ```bash
   # Option A: CLI-based (faster)
   gh repo fork sindresorhus/awesome-cli-apps --clone
   cd awesome-cli-apps
   
   # Option B: Web UI (easier first time)
   # Go to github.com/sindresorhus/awesome-cli-apps → Fork → Clone your fork
   ```

2. **Edit `readme.md`** (section: "Tools")
   - Find section like `## Related` or `## Tools`
   - Look for AI/agent tools subsection (might be under "Development" or "Code Generators")
   - If no AI subsection, add one: `### AI Agents`
   - Add entry (use template above)

3. **Verify format**
   ```bash
   # Check if it's in alphabetical order within section
   # Should be: `[AI Harness...]` before any entries starting with letters after 'A'
   ```

4. **Commit & push**
   ```bash
   git add readme.md
   git commit -m "Add AI Harness Migration Recipes"
   git push origin main
   ```

5. **Create PR**
   ```bash
   gh pr create \
     --title "Add: AI Harness Migration Recipes" \
     --body "Adds hand-written migrations for AI coding agent config between Claude Code, Cursor, Codex, Aider. All 12 pairs, tested, CC BY 4.0. https://github.com/unitedideas/ai-harness-migration-recipes"
   ```

   Or via web: github.com/YOUR_USERNAME/awesome-cli-apps → Compare & Pull Request

---

## #2: awesome-developer-tools (3.1k★)

**Why second:** Broader scope. Fits "productivity", "development", or "agent tools" sections.

### Steps (same pattern as above)

1. **Fork & clone**
   ```bash
   gh repo fork imteekay/awesome-developer-tools --clone
   cd awesome-developer-tools
   ```

2. **Edit `README.md`**
   - Find "Code Generators" or "Agent Tools" or "Development" section
   - If no AI subsection, add one under "Development"
   - Add entry using template

3. **Commit & push**
   ```bash
   git add README.md
   git commit -m "Add: AI Harness Migration Recipes"
   git push origin main
   ```

4. **Create PR**
   ```bash
   gh pr create \
     --title "Add: AI Harness Migration Recipes (Agent Config Tool)" \
     --body "Adds comprehensive migration guides for developers switching AI coding agents. Covers Claude Code, Cursor, Codex, Aider. All 12 pairs tested. https://github.com/unitedideas/ai-harness-migration-recipes"
   ```

---

## #3: awesome-ai-tools (2.2k★)

**Why third:** AI-specific audience. Look for "Development" or "Agent" category.

### Steps

1. **Fork & clone**
   ```bash
   gh repo fork sindresorhus/awesome-ai #OR# sindresorhus/awesome
   # (Check which awesome list is the main one)
   ```

2. **Locate AI tools/agents section**
   - Usually near top or under "Development"
   - Look for entries like "Claude", "Cursor", "GitHub Copilot"

3. **Add entry**
   ```markdown
   - [AI Harness Migration Recipes](https://github.com/unitedideas/ai-harness-migration-recipes) - Hand-written migrations between AI coding agents (Claude Code, Cursor, Codex, Aider). 12 bidirectional pairs, tested, with format diffs & breakage warnings. CC BY 4.0.
   ```

4. **Commit & push**
   ```bash
   git add README.md
   git commit -m "Add: AI Harness Migration Recipes"
   git push origin main
   ```

5. **Create PR**
   ```bash
   gh pr create \
     --title "Add: AI Harness Migration Recipes" \
     --body "Adds resource for developers switching between AI coding tools. All major agents covered (Claude Code, Cursor, Codex, Aider). CC BY 4.0. https://github.com/unitedideas/ai-harness-migration-recipes"
   ```

---

## #4: awesome-migration-tools (niche but direct)

**If it exists**, follow the same pattern. Search GitHub for "awesome-migration" first.

---

## Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| Fork already exists in your account | `gh repo view --web` to navigate, or `gh repo delete` and re-fork |
| PR gets auto-closed for low quality | Check repo's CONTRIBUTING.md, ensure entry matches section style |
| Entry not in alphabetical order | Reorder and re-push (PR updates automatically) |
| Merge conflict | Rebase: `git fetch upstream && git rebase upstream/main && git push -f` |

---

## Success Metrics

After submission:
- [ ] PR created for awesome-cli-apps
- [ ] PR created for awesome-developer-tools
- [ ] PR created for awesome-ai-tools
- [ ] All entries follow repo's existing format/style
- [ ] Wait for maintainer review (usually 3-7 days)
- [ ] Update README.md in main repo with "Featured in" badges once merged

---

## Next Phase (Post-Merge)

Once 1-2 lists accept the PR:
1. **Update main README.md** with badge linking to awesome lists
2. **Update DISTRIBUTION_TRACKER.md** with merge dates
3. **Post on HN/Twitter** about the awesome-list mentions (social proof)
4. **Track referral traffic** from awesome lists → GitHub repo

---

## One-Liner Summary

Three awesome-list submissions (cli-apps, developer-tools, ai-tools) = 8k+ potential reach. Each takes 5-10 min with exact steps above. Highest ROI distribution activity Shane can do today.
