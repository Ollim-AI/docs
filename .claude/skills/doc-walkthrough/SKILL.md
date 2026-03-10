---
name: doc-walkthrough
description: Walk through a doc page as a specific user role, following instructions literally with Playwright. Finds gaps, ambiguities, and broken steps.
argument-hint: <page-path> [--role <role>]
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, mcp__plugin_playwright_playwright__*
---

# Doc walkthrough

**Act, don't narrate.** You are literally performing the setup described in the docs. If the docs say "go to Google Cloud Console" — you open that URL in Playwright. If they say "click New Project" — you click it. If they say "run mkdir -p ..." — you run it in Bash. You are not reviewing the docs. You are following them.

## Arguments

- **page-path**: path to the MDX file (e.g., `getting-started/quickstart`)
- **--role**: role profile to adopt (default: `new-user`)

## Role profiles

| Role | Assumes | Flags when docs... |
|------|---------|-------------------|
| `new-user` | Nothing. Zero technical knowledge. | Use jargon, skip steps, assume tool familiarity |
| `new-user:adhd-kid` | Short attention span, skims headings | Are too dense, bury critical steps, lack visual structure |
| `new-user:grandma` | No dev tools, Discord, or terminal knowledge | Assume CLI comfort, use unexplained acronyms |
| `new-user:busy-adult` | Skims, wants fastest path | Bury the happy path, mix optional and required steps |
| `developer` | Knows git, CLI, general dev concepts | Miss technical details, have wrong code, skip error handling |
| `agent` | No context beyond the page | Are ambiguous, have implicit assumptions, unstated defaults |

## Workflow

### 1. Load

Read the MDX source. Navigate Playwright to `http://localhost:3000/<page-path>`. This is **tab 1 — the docs tab**. It stays open for the entire walkthrough so you can re-read instructions at any point.

### 2. Walk through — the loop

This is a **loop**. You repeat this cycle for every single instruction on the page, from first to last:

```
LOOP (for each instruction on the page):
  1. SAY   → quote the instruction you're about to follow (one line)
  2. DO    → ACTUALLY PERFORM IT (see rules below)
  3. SEE   → browser_snapshot, then describe what you see
  4. FLAG  → note issues from the role's perspective (or skip if none)
  5. NEXT  → go back to step 1 with the next instruction
```

#### DO rules

You are the role. You only know what the docs tell you and what the role would know.

- **"Go to [URL]"** → open a NEW TAB, then `browser_navigate` to that URL
- **"Click X"** → `browser_click` on X in the active tab
- **"Enter/type X"** → `browser_fill_form` or `browser_type`
- **"Run [command]"** → execute in Bash
- **"Navigate to X > Y"** → find and click X in the UI, then click Y. Do NOT type a direct URL — the role doesn't know the URL. Navigate the way the docs describe: clicking sidebar links, menu items, buttons. If the docs say "in the left sidebar," click things in the left sidebar.

External sites open in new tabs. The docs tab (tab 1) stays open — switch back to it whenever you need to re-read the next instruction.

**Do what the docs say, not what you think is correct.** If the docs say "add scopes on the Scopes page" and there is no Scopes page, that's a WRONG flag — you don't skip it because you know scopes work differently now. Try to do it, fail, report the failure.

#### SEE rules

**Every** DO must be followed by `browser_snapshot` before you describe anything. No exceptions. Do not describe what you see from memory or from the previous tool call's response text.

#### FLAG issue types

- **GAP**: step missing ("install X" but no command)
- **AMBIGUOUS**: multiple interpretations ("configure your settings")
- **WRONG**: doesn't match reality (button missing, command fails)
- **JARGON**: unexplained term (role-dependent)
- **ASSUMED**: unstated prerequisite

#### Blocking actions

When you hit something you can't do (login, OAuth, credentials, downloading a file to the user's machine, physical action, anything requiring the user's account or environment): use `AskUserQuestion` to tell the user exactly what you need them to do. It pauses until they respond — then resume the loop.

Do not skip blocking steps. Do not narrate what *would* happen. Every later step depends on earlier ones completing.

#### Completeness

**You do not decide when the walkthrough is done.** The loop ends when:
- You reach the last instruction on the page, or
- You hit a blocking action and stop

You may NOT stop early because you "have enough data" or "the main issues are clear." Every step matters — a step that looks fine might have a subtle UI mismatch you'd only catch by doing it. If steps 3-6 are performable, perform them.

#### Pacing

**Never batch.** One instruction per loop iteration. Never group multiple instructions into one pass. If you catch yourself writing two SAY lines before a DO, you've broken the loop.

### 3. Reflect

After all steps (or getting stuck), produce:

```
## Walkthrough report: <page-path>
**Role**: <role>
**Completed**: <yes/no/partial — stopped at step N>

### What worked
- <steps that were clear and executed successfully>

### Issues found
| # | Type | Step | Description |
|---|------|------|-------------|
| 1 | GAP | "Run the bot" | No command given — what do I run? |

### Documentation gaps
- <what the docs should cover but don't>

### Suggestions
- <concrete fixes>
```
