# ollim-bot documentation

## Project context

- **Product**: ollim-bot — ADHD-friendly Discord bot powered by the Claude Agent SDK. Single-user by design, proactive over reactive, file-based storage, no database.
- **Audience**: Dual-purpose — these docs serve both human users and AI agents (including ollim-bot itself). Content must be easily navigable and unambiguous for both. Human audience is mainly non-technical, avoid jargon.
- **Source repo**: `~/ollim-bot/` (Python 3.11+, uv, discord.py, Claude Agent SDK). The source `docs/CLAUDE.md` is the authoritative architecture reference.
- **Format**: MDX files with YAML frontmatter, Mintlify components
- **Config**: `docs.json` — theme, navigation (4 tabs: Guide, Customizing, Reference, Changelog), branding (Discord blurple `#4752C4`)
- **Dev server**: `mint dev` → localhost:3000
- **44 pages** across 9 sections: getting-started, core-usage, scheduling, integrations, extending, configuration, architecture, development, self-hosting

## Working relationship

- Push back on ideas when they'd hurt documentation quality — cite sources and explain reasoning
- ALWAYS ask for clarification rather than making assumptions
- NEVER lie, guess, or make up anything
- Verify technical claims against the source repo at `~/ollim-bot/` before documenting

## docs.json

- Refer to the [docs.json schema](https://mintlify.com/docs.json) when building the docs.json file and site navigation
- Navigation uses tabs with icon-labeled groups — match existing patterns when adding pages

## Frontmatter requirements

Every MDX file must have exactly:

```yaml
---
title: "Page title"
description: "Concise summary for SEO/navigation."
---
```

- Titles use sentence case: "Configuration reference", not "Configuration Reference"
- Descriptions are action-oriented, 10–30 words

## Writing standards

- **Accuracy is the #1 priority** — wrong information is far worse than missing information. It cascades into bad decisions for both human readers and agents acting on the docs. When uncertain, leave it out or flag it.
- Second-person voice ("you")
- Direct, conversational tone — punchy opening sentences that explain "why" not "what"
- ADHD-aware vocabulary where relevant — proactivity, reducing cognitive load, context quality
- Honest about tradeoffs, acknowledge design choices and their reasoning
- Explicit over implicit — agents can't infer from context the way humans can. State constraints, defaults, and edge cases directly rather than implying them.
- Behavioral details should have one authoritative page. Other pages can summarize but must link to the authority and not add claims the authority page doesn't make.
- Prerequisites at start of procedural content
- Match style and formatting of existing pages — read neighboring files before writing
- Em dashes for inline clarifications — like this
- Bold for key concepts and UI elements: **background fork**, **ping budget**
- Inline code for variables, filenames, function names, tools: `ping_user`, `sessions.json`
- Language tags on all code blocks (bash, python, yaml, json)
- Relative paths for internal links: `[Forks](/core-usage/forks)` with descriptive anchor text, never "click here"

## Component usage

Follow existing patterns — read a similar page before adding components:

| Component | Use for | Example |
|-----------|---------|---------|
| `<Card>` with `title`, `icon`, `href` | Navigation, next steps, feature cards | End-of-page "Next steps" sections |
| `<Columns cols={2\|3}>` | Grid layouts wrapping Cards | Feature overviews |
| `<Steps>` + `<Step title="...">` | Sequential procedures | Setup guides, quickstarts |
| `<Tabs>` + `<Tab title="...">` | Alternative approaches side-by-side | CLI vs MCP tool, slash command vs tool |
| `<Accordion>` / `<AccordionGroup>` | Optional deep dives, expandable detail | Exit strategies, advanced config |
| `<Note>`, `<Tip>`, `<Warning>` | Callouts for important info | Auth notes, gotchas, best practices |
| Markdown tables | Reference material, parameters, env vars | Heavily used — 200+ across docs |

## Content strategy

- Document just enough for user success — not too much, not too little
- Search for existing content before adding anything new — avoid duplication
- Every page ends with a "Next steps" section using `<Card>` components
- Overview pages use task-routing tables: "I want to... → Go to"
- Cross-link extensively with descriptive anchor text
- Verify against source code when documenting behavior — never document assumed behavior
- Structure for both audiences: humans scan headings and cards, agents parse structured content (tables, code blocks, explicit parameter lists). Both benefit from consistent patterns.

## Terminology (use consistently)

| Term | Not |
|------|-----|
| background fork | bg fork, background session |
| interactive fork | foreground fork |
| ping budget | notification budget, ping limit |
| routine | scheduled task, cron job (when referring to ollim-bot routines) |
| reminder | alarm, timer |
| main session | primary session, root session |
| context compaction | context compression, summarization |

## Git workflow

- NEVER use `--no-verify` when committing
- Ask how to handle uncommitted changes before starting
- Create a new branch when no clear branch exists for changes
- Commit frequently throughout development
- Keep commits bite-sized

## Do not

- Skip frontmatter on any MDX file
- Use absolute URLs for internal links
- Include untested code examples
- Make assumptions — always ask for clarification
- Add pages without updating `docs.json` navigation
- Use emoji in documentation prose
- Document features that don't exist in the source repo
