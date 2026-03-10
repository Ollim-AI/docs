---
name: doc-walkthrough
description: Walk through a doc page as a specific user role, following instructions literally with Playwright. Finds gaps, ambiguities, and broken steps.
argument-hint: <page-path> [--role <role>]
allowed-tools: Read, Glob, Grep, Bash, Agent, AskUserQuestion, mcp__plugin_playwright_playwright__*
---

# Doc walkthrough

Follow a documentation page's instructions **exactly as written** using Playwright. You are a literal instruction-follower — do only what the docs say. If a step is ambiguous, don't interpret it; flag it. If something is implied but not stated, don't do it; flag it.

## Arguments

- **page-path**: path to the MDX file (e.g., `getting-started/quickstart`)
- **--role**: role profile to adopt (default: `new-user`)

## Role profiles

Adopt the selected role's perspective when following instructions. This changes what you treat as "obvious" vs "unclear":

| Role | Assumes | Flags when docs... |
|------|---------|-------------------|
| `new-user` | Nothing. Zero technical knowledge. Reads every word. | Use jargon without defining it, skip steps, assume tool familiarity |
| `new-user:adhd-kid` | Short attention span, skims headings, skips walls of text | Are too dense, bury critical steps in paragraphs, lack visual structure |
| `new-user:grandma` | Unfamiliar with dev tools, Discord, terminals | Assume CLI comfort, use unexplained acronyms, skip "how to open X" |
| `new-user:busy-adult` | Will skim, wants fastest path, skips optional sections | Bury the happy path, mix optional and required steps, lack TL;DR |
| `developer` | Knows git, CLI, general dev concepts | Miss technical details, have wrong code examples, skip error handling |
| `agent` | Reads like an LLM — no context beyond the page | Are ambiguous, have implicit assumptions, unstated defaults, contradictions |

## Workflow

### 1. Load the page

Read the MDX file from the docs repo. Parse the instructions into discrete steps.

### 2. Open Playwright

Launch a browser. Navigate to `http://localhost:3000/<page-path>` to see the rendered page.

### 3. Follow each step literally

For each instruction in the doc:

1. **Read the instruction exactly as written**
2. **Do only what it says** — if it says "click the button", look for the button and click it. If no button exists, that's a gap.
3. **Stop and ask the user** when you encounter something you cannot do:
   - Logging into accounts (Discord, Google, etc.)
   - Actions requiring credentials you don't have
   - Physical-world steps ("plug in your device")
   - Say exactly what you need them to do and wait for confirmation before continuing
4. **Flag issues immediately** — don't fix or work around them. Categories:
   - **GAP**: step missing entirely ("install X" but no install command given)
   - **AMBIGUOUS**: multiple interpretations possible ("configure your settings")
   - **WRONG**: instruction doesn't match reality (button doesn't exist, command fails)
   - **JARGON**: unexplained term (role-dependent — `developer` won't flag "CLI")
   - **ASSUMED**: prerequisite not stated but required

### 4. Reflect

After completing (or getting stuck on) all steps, produce a report:

```
## Walkthrough report: <page-path>
**Role**: <role>
**Completed**: <yes/no/partial — stopped at step N>

### What worked
- <steps that were clear and correct>

### Issues found
| # | Type | Step | Description |
|---|------|------|-------------|
| 1 | GAP | "Run the bot" | No command provided — what do I actually run? |

### Documentation gaps
- <things the docs should cover but don't>

### Suggestions
- <concrete improvements, not vague "make it better">
```
