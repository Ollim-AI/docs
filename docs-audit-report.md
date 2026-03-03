# Documentation Audit Report

**Date:** 2026-03-02
**Scope:** Full audit of all 44 pages across 9 sections
**Method:** 3-agent adversarial debate — content strategist, source-code verifier, external docs benchmarker
**Benchmark sources:** Claude Code docs (59 pages), Anthropic developer platform

---

## Executive summary

**Overall grade: A-**

The documentation is exceptionally well-crafted. 95%+ technical accuracy with zero phantom features — every documented behavior exists in the source code. Structural consistency, terminology compliance, and dual-audience design are all strong. The primary issues are minor cross-page inconsistencies, a few coverage gaps, and opportunities to adopt patterns from Claude Code docs.

The docs have five competitive advantages over reference documentation (including Claude Code): real-world annotated examples, honest competitor comparisons, ADHD-aware voice, task-routing tables, and file-format reference as a first-class page. **All recommended changes must preserve these strengths.**

### Key principle from the debate

> Add structure around the voice, don't replace the voice with structure.

All recommendations below are either mechanical fixes or additive structural enhancements. None propose rewriting existing prose. The direct, honest, ADHD-aware voice is the documentation's competitive advantage.

---

## Tier 1 — Fix now

Quick fixes with high accuracy or consistency impact. Estimated total: ~30 minutes.

### 1.1 Cross-page `dontAsk` scoping inconsistency

| | |
|---|---|
| **Severity** | HIGH — contradictory information across pages |
| **Pages** | `core-usage/slash-commands.mdx:126-128`, `core-usage/permissions.mdx:40-42` |
| **Issue** | Slash commands page says "Permission mode is scoped per session. If you are in a fork, only the fork is affected." Permissions page correctly notes `dontAsk` is NOT fork-scoped (module-level flag). An agent parsing both pages gets contradictory information. |
| **Source evidence** | `permissions.py:39` — `_dont_ask: bool = True` is module-level, not a contextvar |
| **Fix** | Add one sentence after slash-commands.mdx line 127: "Exception: `dontAsk` mode is global — switching to or from it in a fork affects the main session too. See [Permissions](/core-usage/permissions#fork-scoping) for details." |
| **Consensus** | All 3 teammates agree. Content-strategist elevated from source-verifier's original finding. |

### 1.2 Add DRY principle to CLAUDE.md

| | |
|---|---|
| **Severity** | HIGH — prevents future cross-page drift |
| **File** | `CLAUDE.md` |
| **Issue** | The `dontAsk` inconsistency happened because behavioral details live in two places without a clear authority rule. |
| **Fix** | Add to CLAUDE.md writing standards: "Behavioral details should have one authoritative page. Other pages can summarize but must link to the authority and not add claims the authority page doesn't make." |
| **Consensus** | Content-strategist proposed, benchmarker endorsed. |

### 1.3 Fix title casing on landing page

| | |
|---|---|
| **Severity** | HIGH — most visible page, violates CLAUDE.md standard |
| **Page** | `getting-started/overview.mdx` |
| **Issue** | Title is "Ollim Bot" (title case). CLAUDE.md mandates sentence case. Every other page complies. |
| **Fix** | Change title to "ollim-bot" to match product name casing used everywhere else. |
| **Consensus** | All 3 teammates agree. |

### 1.4 Update page count in CLAUDE.md

| | |
|---|---|
| **Severity** | HIGH — meta-accuracy of project instructions |
| **File** | `CLAUDE.md` |
| **Issue** | States "41 pages across 9 sections" but 44 MDX files exist. Any contributor (human or AI) reading CLAUDE.md gets an incorrect mental model. |
| **Fix** | Update to "44 pages" or remove the specific count. |
| **Consensus** | All 3 teammates agree. |

### 1.5 Fix ampersand in title

| | |
|---|---|
| **Severity** | MEDIUM — consistency |
| **Page** | `core-usage/embeds-and-buttons.mdx` |
| **Issue** | Title is "Embeds & buttons" while every other title uses "and" or avoids conjunctions. Filename uses "and". |
| **Fix** | Change to "Embeds and buttons". |
| **Consensus** | All 3 teammates agree. |

### 1.6 Standardize `<Note>` vs `<Info>` components

| | |
|---|---|
| **Severity** | MEDIUM — standards violation |
| **Pages** | `configuration/data-directory.mdx:82`, `development/cli-reference.mdx:358` |
| **Issue** | Two files use `<Info>` callouts. CLAUDE.md component table explicitly lists `<Note>`, `<Tip>`, `<Warning>` as the three approved callout types. `<Info>` renders identically to `<Note>` in Mintlify but violates the project's own conventions. |
| **Fix** | Replace 2 instances of `<Info>` with `<Note>`. Content unchanged — only the component tag. |
| **Consensus** | Content-strategist identified (M3), source-verifier confirmed as genuine standards violation with exact file locations. |

---

## Tier 2 — Do soon

Content fixes and missing documentation. Estimated total: ~1-2 hours.

### 2.1 Add `dismiss` button action to MCP tools reference

| | |
|---|---|
| **Severity** | MEDIUM — user-facing gap |
| **Page** | `extending/mcp-tools.mdx:29-34` |
| **Issue** | `dismiss` is a valid button action (`views.py:69,149`) that deletes the message. It's documented in `embeds-and-buttons.mdx:69` but missing from the MCP tools button actions table. Also missing: `purple` color from the button colors table. |
| **Source evidence** | `views.py:69` — `dismiss` action handler; `embeds.py` — purple color definition |
| **Fix** | Add `dismiss` row to button actions table; add `purple` to colors table. |
| **Consensus** | Source-verifier identified, self-corrected on cross-page scope. |

### 2.2 Document background fork failure notifications

| | |
|---|---|
| **Severity** | MEDIUM — users receive these DMs but docs don't explain them |
| **Pages** | `development/troubleshooting.mdx` or `scheduling/background-forks.mdx` |
| **Issue** | `_notify_fork_failure` in `forks.py:105-114` DMs the user when a background fork times out or crashes. Users may see these messages without understanding them. |
| **Source evidence** | `forks.py:105-114` — notification mechanism |
| **Fix** | Add a row to troubleshooting or a note to background-forks explaining what these messages mean. |
| **Consensus** | Source-verifier identified, benchmarker endorsed as user-facing. |

### 2.3 Revise frontmatter descriptions to be action-oriented

| | |
|---|---|
| **Severity** | MEDIUM — violates CLAUDE.md standard |
| **Pages** | `core-usage/slash-commands.mdx`, `core-usage/conversations.mdx`, `core-usage/forks.mdx` |
| **Issue** | Descriptions read as labels ("All Discord slash commands available in ollim-bot") rather than action-oriented summaries. CLAUDE.md says "Descriptions are action-oriented, 10-30 words." |
| **Fix** | Rephrase, e.g., "Use slash commands to manage sessions, permissions, forks, and configuration." |
| **Consensus** | Content-strategist identified. |

### 2.4 Add decision table to model-providers page

| | |
|---|---|
| **Severity** | MEDIUM — ADHD-friendly fast path on the longest page |
| **Page** | `self-hosting/model-providers.mdx` |
| **Issue** | This is the longest page in the docs. For an ADHD-friendly site, readers need a fast decision path before the deep content. |
| **Fix** | Add a decision table at the top: "I have a Claude subscription → done", "I want to save money → DeepSeek section", "I want privacy → self-hosted section". Do NOT split the page — preserves comparison shopping. |
| **Consensus** | Content-strategist diagnosed (M6), benchmarker proposed decision table, both agreed splitting would lose the comprehensive voice. |

### 2.5 Update architecture module map

| | |
|---|---|
| **Severity** | MEDIUM — accuracy of reference material |
| **Page** | `architecture/overview.mdx` (accordion) |
| **Issue** | Claims "34 modules" but actual count is 36. Missing: `fork_state.py` (223 lines, extracted from `forks.py` — handles all fork state via contextvars and dataclasses) and `agent_context.py` (extracted from `agent.py` — message context helpers, timestamps, ThinkingConfig). Additionally, `forks.py` description is outdated — it still claims to handle fork state, which was extracted. |
| **Source evidence** | `src/ollim_bot/fork_state.py`, `src/ollim_bot/agent_context.py` — both real modules, not trivial helpers |
| **Fix** | Add `fork_state.py` and `agent_context.py` to the module map, update `forks.py` description, change count from 34 to 36. |
| **Consensus** | Source-verifier identified with exact counts, content-strategist endorsed for accuracy. |

### 2.6 Permission modes table obscures architectural distinction

| | |
|---|---|
| **Severity** | MEDIUM — teaches wrong mental model despite being technically accurate |
| **Page** | `core-usage/permissions.mdx:15-20` |
| **Issue** | The four permission modes (`dontAsk`, `default`, `acceptEdits`, `bypassPermissions`) are presented in a flat table as peers. In reality, `dontAsk` is a custom ollim-bot layer checked in `handle_tool_permission()` BEFORE the SDK fires, while the other three are SDK-native modes passed to `set_permission_mode()`. The flat presentation leads users to think "four equivalent choices" when the architecture is "one custom layer + three SDK modes." |
| **Source evidence** | `permissions.py:39` — `_dont_ask` is module-level bool; `agent.py:155-163` — other modes use `set_permission_mode()` |
| **Fix** | Restructure the table presentation — either use a two-tier grouping or add a brief note explaining the architectural distinction. The `<Note>` at lines 22-26 partially addresses this but comes after the misleading flat table. |
| **Consensus** | Source-verifier identified during debate (Challenge #1: "do accurate findings obscure the mental model?"). Only case found where accuracy masks architecture. |

---

## Tier 3 — When bandwidth allows

Structural enhancements and pattern adoption. These improve an already-good site.

### 3.1 Add comparison tabs to extending/overview

| | |
|---|---|
| **Pages** | `extending/overview.mdx` |
| **Pattern source** | Claude Code features-overview: "Skill vs Subagent" tabs |
| **What** | Below the existing decision matrix, add `<Tabs>` with side-by-side comparison tables: "Routines vs Reminders", "Skills vs System Prompt", "Webhooks vs Routines". Each tab: 4-5 row comparison table + one-paragraph recommendation. |
| **Why** | The decision matrix answers "which mechanism?" but not "what's the difference between two I'm torn between?" Serves both audiences: humans scan the table, agents parse structured comparison data. |
| **Debate note** | Benchmarker proposed as Tier 1, content-strategist endorsed as HIGH, benchmarker later demoted to "nice to have." All agree it adds value but isn't urgent. |

### 3.2 Add context cost table to context-flow

| | |
|---|---|
| **Page** | `architecture/context-flow.mdx` |
| **Pattern source** | Claude Code features-overview: "Context cost by feature" section |
| **What** | A table showing what the agent sees in each execution mode (main session, interactive fork, background fork, isolated background fork). Columns: Mode / System prompt / History / Tools available / Skills loaded / Context cost. |
| **Why** | ollim-bot IS an agent system with context window dynamics. The bot itself reads these docs via MCP. A context cost table helps the bot make better decisions about fork mode and model selection. |
| **Source data** | Source-verifier confirmed all values: tool restrictions in `tool_policy.py:201-207`, fork context in `forks.py`, preamble building in `preamble.py`. |

### 3.3 Add architecture-to-development cross-links

| | |
|---|---|
| **Pages** | `architecture/streaming.mdx`, `architecture/session-management.mdx` |
| **What** | Add links to `development/guide.mdx` from architecture pages where code modification is a natural next step. |
| **Why** | A reader who understands how streaming works wants to know where to modify it. Currently requires manual navigation to the development section. |

### 3.4 Add example interactions to Guide pages

| | |
|---|---|
| **Pages** | `core-usage/conversations.mdx`, `core-usage/forks.mdx` |
| **Pattern source** | Claude Code common-workflows: copy-pasteable example prompts |
| **What** | Add 2-3 "Try saying..." examples showing real message interactions. For conversations: starting a topic, interrupting, using replies. For forks: naturally entering a fork, returning to main. |
| **Why** | These pages explain mechanics but don't show the conversational experience. The examples page does this brilliantly for scheduling — extend the pattern. |
| **Debate note** | Benchmarker originally proposed a separate cookbook page, then conceded and narrowed to inline examples on existing pages. |

### 3.5 Add structured "Key values" summaries to setup pages

| | |
|---|---|
| **Pages** | `self-hosting/discord-bot-setup.mdx`, `self-hosting/google-oauth-setup.mdx` |
| **What** | Add a brief table at the top listing the key outcomes: required permissions, token locations, OAuth scopes, etc. Use the existing direct voice ("What you'll have after this"). |
| **Why** | These pages are purely human-oriented step-by-step procedures. An AI agent reading them gains very little actionable information. Structured summaries serve the dual audience without compromising the guide format. |

### 3.6 Restructure changelog

| | |
|---|---|
| **Page** | `changelog.mdx` |
| **What** | Add date anchors or group by week/milestone. Consider the Mintlify changelog format. |
| **Why** | Currently 18 days and 340 commits in one long scroll with no structure. Inconsistent granularity across entries. |

### 3.7 Expand examples pattern to non-scheduling workflows

| | |
|---|---|
| **What** | Extend the annotated-real-config pattern from `scheduling/examples.mdx` to non-scheduling use cases: fork workflows, webhook-driven notifications, skill composition. |
| **Why** | The examples page is best-in-class (benchmarker: "nothing like it in Claude Code docs"). The gap is that similar real-world annotation only exists for scheduling. Cross-cutting workflows (forks + skills, webhooks + routines) lack composed examples. |

---

## What to preserve — competitive advantages

The debate identified six aspects of the documentation that are stronger than the reference docs (Claude Code, Anthropic developer platform). Any changes must not degrade these:

| Strength | Where | Why it matters |
|----------|-------|---------------|
| Real-world annotated examples | `scheduling/examples.mdx` | Shows actual routines from a real data directory with "Key Patterns" annotations. Claude Code has nothing equivalent. |
| Honest competitor comparison | `getting-started/coming-from-other-assistants.mdx` | "What you give up" is as detailed as "What you gain." Builds trust and helps users self-select. |
| ADHD-aware voice | Throughout, especially `architecture/design-philosophy.mdx` | Not marketing — documented in actual routine prompts. Explains WHY features exist for the specific audience. |
| Task-routing tables | Overview pages | "I want to... → Go to" tables are more scannable and machine-parseable than AccordionGroups. |
| File-format reference | `configuration/file-formats.mdx`, `configuration/data-directory.mdx` | Treats storage formats as first-class documentation. Appropriate for a file-based system. |
| Direct, honest tone | Throughout | Design philosophy page acknowledges tradeoffs directly. No corporate voice. |

---

## Source accuracy summary

| Metric | Result |
|--------|--------|
| Technical accuracy | 95%+ — all numerical values, defaults, timeouts match source |
| Phantom features (documented but don't exist) | 0 |
| Cross-page inconsistencies | 3 (dontAsk scoping, dismiss button coverage, purple color coverage) |
| Mental model issues | 1 (permissions flat table obscures dontAsk vs SDK-mode distinction) |
| Coverage gaps (exist in source, not documented) | 3 user-facing (dismiss action, bg fork failure DMs, image format details) |
| Coverage gaps (implementation detail) | 4 (conceded as not needing documentation) |
| Outdated references | 1 (module map count and descriptions) |
| Terminology violations | 0 across all 44 pages |

---

## If only 3 things get done

1. **Fix the `dontAsk` cross-page inconsistency** (Tier 1.1) — 5 minutes, highest accuracy impact
2. **Fix meta-accuracy** (Tier 1.3 + 1.4) — title casing and page count — 5 minutes, credibility impact
3. **Add decision table to model-providers** (Tier 2.4) — 15 minutes, highest UX impact for ADHD audience

Everything else is improvement, not correction. The docs are already very good.
