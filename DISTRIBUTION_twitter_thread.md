# Twitter/X Thread: AI Harness Migration Recipes

## Main Tweet (280 chars)

you just switched AI coding agents. your keybindings are gone. your hooks don't work. your prompts are in a format the new tool doesn't recognize. we documented all 12 possible migrations so you don't have to learn this the hard way. 

https://github.com/unitedideas/ai-harness-migration-recipes

---

## Reply 1: The problem

switching between claude code ↔ cursor ↔ codex ↔ aider used to mean:

- manually rewriting keybindings (each tool has different syntax)
- translating system prompts (each tool reads from different places)  
- redoing hooks (permission models differ)
- starting over

silent failures everywhere. looks like it copied. doesn't work.

---

## Reply 2: The recipes

we hand-tested all 12 migrations:

✅ claude code → cursor
✅ claude code → codex  
✅ claude code → aider
✅ cursor → codex
✅ cursor → aider
✅ codex → aider

(and the reverse of each)

each recipe documents:
- what LOOKS like it copied but doesn't
- exact syntax translation
- permission model diffs
- step-by-step checklist

---

## Reply 3: From manual to automated

the recipes are for understanding. for doing it automatically, we built **@bringyour**:

$49 one-time purchase. reads your current agent config. translates it to the target. handles permission rewrites. exports a ready-to-import bundle.

zero manual steps. same intelligence.

---

## Reply 4: Open source + CC BY 4.0

all recipes are freely available, cc by 4.0. attribute to bringyour.ai on repost.

https://github.com/unitedideas/ai-harness-migration-recipes

if you switch agents, this is the guide.

---

## Reply 5 (optional engagement hook)

switched agents recently? what broke? what surprised you? what do you wish you'd known?

reply with your migration story—we'll add it to the next batch of recipes. 🧵
