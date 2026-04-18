# Troubleshooting & Edge Cases

Common migration issues and solutions when moving between Claude Code, Cursor, Codex, and Aider.

## General Issues (All Migrations)

### "My API key works in [OLD TOOL] but fails in [NEW TOOL]"

**Cause:** Tools store and reference API keys differently.

**Solutions:**
1. **Verify key format** — Some tools expect different key prefixes:
   - Anthropic: `sk_` (Claude Code, Cursor use this)
   - OpenAI: `sk-` (Codex uses this)
   - Aider's LLM config: passes through to backend (validate via `aider --help | grep KEY`)

2. **Check environment variable names:**
   - Claude Code: `ANTHROPIC_API_KEY`
   - Cursor: `ANTHROPIC_API_KEY` (same)
   - Codex: `OPENAI_API_KEY`
   - Aider: `--openai-api-key` flag OR `OPENAI_API_KEY` env var

3. **Validate key permissions:**
   ```bash
   # For Anthropic keys (Claude Code, Cursor):
   curl -s -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/models | head
   
   # For OpenAI keys (Codex):
   curl -s -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models | head
   ```

4. **Re-enter key in new tool's settings** — Don't copy from old tool's config files; re-paste from your password manager. Copy-paste errors are common.

---

### "My keyboard shortcuts don't work in the new tool"

**Cause:** Each tool binds shortcuts to different command names and scopes.

**Solutions:**
1. **List all commands** in new tool:
   - Claude Code: `Ctrl+Shift+P` → search "show all commands"
   - Cursor: Same (`Ctrl+Shift+P`)
   - Codex: `Cmd+Shift+P` (macOS)
   - Aider: `!help` in chat to list commands

2. **Map by functionality, not name:**
   ```
   Claude Code: "claude.ask"           → Cursor: "cursor.ask"
   Claude Code: "claude.codeReview"    → Cursor: not built-in (use chat instead)
   Claude Code: "claude.edit"          → Cursor: "composer.edit"
   ```

3. **Test one shortcut at a time** — Set shortcut, test, verify it works before moving on.

4. **Check command scope** — Shortcuts may not work in certain contexts (terminal, diff editor, etc.):
   ```json
   // In keybindings.json, use "when" clause:
   {
     "key": "ctrl+l",
     "command": "editor.action.selectAll",
     "when": "editorTextFocus && !editorReadOnly"
   }
   ```

---

### "Tool keeps asking for auth/API key on restart"

**Cause:** Config file not found, or auth token expires between sessions.

**Solutions:**
1. **Verify config file location:**
   - Claude Code: `~/.claude/config.json` or settings UI
   - Cursor: `~/Library/Application\ Support/Cursor/settings.json` (macOS)
   - Codex: `~/.codex/config.json` or `~/.vscode/settings.json`
   - Aider: `~/.aider.conf.yml` or `AIDER_xxx` env vars

2. **Check file permissions:**
   ```bash
   ls -la ~/.claude/config.json  # Should be -rw------- (600)
   chmod 600 ~/.claude/config.json  # Fix if needed
   ```

3. **Verify API key is actually written to config:**
   ```bash
   # For Claude Code/Cursor (example):
   cat ~/.claude/config.json | grep -i "api\|key"
   ```

4. **Restart tool cleanly:**
   - Quit via menu (not force-quit)
   - Wait 2 seconds
   - Re-launch

---

### "Pasted config is malformed after migration"

**Cause:** JSON/YAML formatting, trailing commas, quote mismatches.

**Solutions:**
1. **Validate JSON** (Claude Code, Cursor configs):
   ```bash
   cat ~/.claude/config.json | jq . > /dev/null && echo "Valid" || echo "Invalid"
   ```

2. **Validate YAML** (Aider configs):
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('~/.aider.conf.yml'))" && echo "Valid" || echo "Invalid"
   ```

3. **Look for common errors:**
   - Trailing commas in JSON: `{...,"key": "value",}` ← invalid
   - Unquoted strings in YAML: `key: value with spaces` ← needs quotes
   - Mixed tabs/spaces in YAML: use spaces only
   - Unicode characters: ensure UTF-8 encoding

4. **Use VS Code to validate** before pasting:
   - Paste into new `.json` or `.yaml` file
   - Check for red squigglies (syntax errors)
   - Fix, then move to actual config location

---

## Tool-Specific Issues

### Claude Code → Cursor

**Q: "My keyboard shortcuts are ignored in Cursor"**  
A: Cursor uses `keybindings.json` like VS Code. Shortcut name changes:
```
claude.ask              → cursor.ask (or use chat directly)
claude.codeReview       → No equivalent (use composer instead)
claude.edit            → composer.edit
claude.fixDiagnostics  → No equivalent
```

**Q: "Cursor chat is different from Claude Code"**  
A: True. Claude Code uses `@` mentions for context; Cursor uses a separate panel. No migration path—you need to re-learn UX.

**Q: "I lost my custom instructions"**  
A: Custom instructions (system prompt) live in:
- Claude Code: `.claude/config.json` → `customInstructions` field
- Cursor: Settings UI → Rules (top-right icon) → paste your instructions there

Re-paste instructions in Cursor's UI (no config file to copy from).

---

### Cursor → Claude Code

**Q: "Claude Code doesn't recognize my Cursor composer/codebase context"**  
A: Claude Code uses `@`-based mentions; Cursor uses a "codebase" sidebar. No equivalent migration:
- **Cursor `@codebase`** → Claude Code: highlight relevant files and use `@` mention in chat
- **Cursor `@documents`** → Claude Code: attach files via menu

**Q: "Where do I find my Cursor settings in Claude Code?"**  
A: Claude Code's settings are in:
- Extensions UI → Claude extension → gear icon
- Or: `~/.claude/config.json` (advanced)
- Or: menu → Settings

Copy your settings from Cursor's `settings.json`, translate values, paste into Claude Code UI.

---

### Claude Code/Cursor → Codex

**Q: "Codex shows an error about missing `@anthropic/sdk`"**  
A: Codex doesn't have native Anthropic support (it's OpenAI-first). You need:
1. Install OpenAI SDK: `pip install openai`
2. Migrate to use OpenAI API instead (get `OPENAI_API_KEY` from OpenAI)
3. Rewrite prompts for OpenAI models (`gpt-4`, `gpt-3.5-turbo`)

Anthropic code will **not** work in Codex without refactoring.

**Q: "How do I set up Codex with Claude models?"**  
A: You can't (directly). Use Anthropic SDK in your own agent, not Codex. Codex is OpenAI-specific.

---

### Aider ↔ All Others

**Q: "Aider's LLM config is different from the others"**  
A: True. Aider uses a `~/.aider.conf.yml` (or command-line flags) instead of VS Code settings:

```yaml
# Aider config
model: claude-3-5-sonnet-20241022
api-key: YOUR_ANTHROPIC_KEY

# vs. Claude Code (JSON)
{
  "anthropic": {
    "apiKey": "YOUR_ANTHROPIC_KEY"
  }
}
```

**Migration:** Copy API key to `OPENAI_API_KEY` (Aider env var) or `~/.aider.conf.yml`, restart Aider.

**Q: "I'm in Aider chat. How do I ask it to edit a file like Cursor?"**  
A: Use Aider's built-in `/ask` and file mentions:
```
/ask "refactor this function" --file myfile.py
```

Or: `aider` at CLI with `--file myfile.py`, then use chat naturally.

---

## Data Loss Scenarios (Most Common)

### Scenario 1: "I lost my custom LLM model config"

**Prevention:** Model settings are NOT synced between tools.
- **Tool A:** custom model + temperature + top-p settings
- **Tool B:** defaults (Claude 3 Sonnet + temperature 0.7)

**Recovery:** Re-enter model config in Tool B:
1. Open Tool B settings
2. Look for "Model" or "LLM" section
3. Set to same model + parameters as Tool A

**Verification:**
```bash
# Claude Code/Cursor: check keybindings for model name
grep -i "model\|claude" ~/.claude/config.json

# Aider: check config
cat ~/.aider.conf.yml | grep -i "model"
```

---

### Scenario 2: "My context windows got lost"

**Prevention:** Context size (max tokens) is tool-specific:
- Claude Code/Cursor: Automatic (matches tool version)
- Codex: Fixed (4k, 8k, or 16k depending on plan)
- Aider: Configurable (`--max-tokens` flag or config)

**Recovery:** Check Tool A's max-tokens value:
```bash
# Claude Code: Settings → Claude → Max Tokens (default: 4096)
# Cursor: Same UI as Claude Code
# Aider: aider --help | grep -i max
```

Set the same value in Tool B if it supports custom context.

---

### Scenario 3: "File exclusions/ignores are missing"

**Prevention:** Tool A might have:
- `.gitignore` entries respected automatically
- Custom ignore patterns in settings

Tool B might not respect the same rules.

**Recovery:**
1. **Copy `.gitignore`** from Tool A to Tool B's project root (both tools respect it)
2. **Check Tool B settings for custom ignore patterns:**
   - Claude Code: `.claude/config.json` → `exclude` field
   - Cursor: VS Code → `files.exclude` setting
   - Aider: `--skip-rules` flag or `~/.aider.conf.yml`

3. **Test:** Tool B should now skip files listed in `.gitignore`

---

## Performance Issues After Migration

### "Tool is slow/laggy after migration"

**Cause:** Large files, too much context, conflicting extensions.

**Solutions:**
1. **Clear cache:**
   ```bash
   # Claude Code/Cursor: Remove cache directory
   rm -rf ~/.vscode/Cache
   rm -rf ~/Library/Application\ Support/Cursor/Cache
   
   # Restart tool
   ```

2. **Reduce context:**
   - Remove large binary files from project root
   - Exclude `node_modules`, `.git`, etc. in settings
   - Disable chat history (can grow large)

3. **Check extensions:**
   - Disable non-essential extensions
   - Some extensions conflict with AI tools (especially linters)

4. **Monitor memory:**
   ```bash
   # macOS
   top -l 1 | grep "Claude Code\|Cursor\|Code"
   ```

---

## Security Checklist After Migration

After migration, verify:

- [ ] **API keys are stored securely** (not in git, not in text files)
- [ ] **Old tool configs are cleared** (if switching completely):
  ```bash
  # If switching away from Claude Code:
  rm -rf ~/.claude
  
  # If switching away from Cursor:
  rm -rf ~/Library/Application\ Support/Cursor
  ```

- [ ] **Auth tokens are not shared** between tools (each should have its own)
- [ ] **Chat history is private** (not synced to cloud unless intended)
- [ ] **No API keys in environment** after tool closes:
  ```bash
  unset ANTHROPIC_API_KEY OPENAI_API_KEY  # Clear from shell
  ```

---

## FAQ: "Did I lose data?"

**The safe answer:** Check the old tool:
1. Quit old tool
2. Launch new tool (verify it works)
3. Launch old tool again (verify your data is still there)
4. If both work, migration succeeded
5. If old tool breaks, you may have a misconfigured API key (restart old tool, re-enter key)

**What's NOT lost:**
- Your API keys (they're stored locally, tool-specific)
- Your project files (still on disk)
- Your git history (untouched)

**What might be lost:**
- Chat history (tool-specific, not synced between tools)
- Custom keybindings (must be re-entered)
- Custom instructions (tool-specific format)

---

## Report a New Edge Case

Found an issue not listed here?
1. File an issue on GitHub: https://github.com/unitedideas/ai-harness-migration-recipes/issues/new
2. Include:
   - Your migration path (e.g., "Claude Code → Cursor")
   - The exact error message
   - Steps to reproduce
   - Your OS + tool versions

We'll add it to this guide and ship a fix in the next update.

---

## Contact / Support

- **GitHub Issues:** Quick fixes + documentation updates
- **GitHub Discussions:** General questions + troubleshooting
- **BringYour Support:** If using the automation tool, use in-app support

Most issues are one-liner fixes. Don't hesitate to ask.
