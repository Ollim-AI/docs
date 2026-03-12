# Layer boundary checklist

Rules for auditing ollim-bot documentation against the three-layer composition chain. Each layer composes the behavior of the one below it — ollim-bot uses the Agent SDK, which uses Claude Code.

## The three layers

| Layer | Name | Purpose | Examples |
|-------|------|---------|----------|
| A | Claude Code | Foundation AI model and tool-use framework — tools, bash, MCP, file I/O | Tool calls, permissions, safety, environment context |
| B | Claude Agent SDK | Middleware — wraps Claude Code into an agent loop with sessions, compaction, streaming | `Agent.stream_chat()`, `StreamEvent`, session persistence, `setting_sources` |
| C | ollim-bot | Application — bridges Discord with Claude via the SDK | Discord tools, scheduling, forks, routines, user context |

**What is NOT a layer:** Python standard library, third-party Python packages (`python-dotenv`, `discord.py`), operating system features. These are infrastructure, not part of the three-layer model. Don't flag references to them as layer violations.

---

## Per-page rules

### Rule 1: Layer references need clear purpose statements

When a page introduces or references a layer, it should be clear what that layer does — at least one sentence. The first mention on a page should not be ambiguous.

This matters because readers (especially AI agents) can't infer what "the SDK handles it" means without context. Vague references force the reader to go find the answer elsewhere, which breaks the documentation's usefulness.

**Violation:** "The Agent SDK handles it"
**Clean:** "The Agent SDK manages the agent loop, persistent sessions, and streaming — ollim-bot calls its API but doesn't implement these."

Not every mention of a layer needs a full description — just the first reference on each page. If a page mentions "the SDK" ten times, only the first needs to establish what it does.

### Rule 2: Document the seam, not just the internals

When describing how ollim-bot interacts with the SDK or Claude Code, document the interface — what's exposed upward, what's consumed downward — rather than only the internal behavior.

The seam is where integration bugs live and where contributors need to understand the contract. Documenting only what a layer does internally, without explaining how other layers connect to it, leaves the reader unable to reason about changes or debug issues at the boundary.

**Violation:** Describing `setting_sources=["project"]` without explaining it's an SDK configuration option that controls where Claude Code looks for settings.
**Clean:** "ollim-bot passes `setting_sources=["project"]` to the SDK, which tells Claude Code to load settings from the project's `.claude/` directory."

### Rule 3: State what each layer delegates and to whom

When describing behavior that spans layers, explicitly name which layer handles it and which layer it delegates to.

Without delegation attribution, readers can't tell where a behavior is implemented. This matters for debugging ("is this an ollim-bot bug or an SDK bug?"), for contributing ("which repo do I change?"), and for AI agents acting on the docs ("which layer's API do I call?").

**Violation:** "The bot authenticates via OAuth" — which layer does the auth?
**Clean:** "ollim-bot delegates authentication to the Claude Agent SDK's bundled CLI, which handles OAuth with Claude Code's API."

### Rule 4: Document what crosses layer boundaries

When behavior involves data, errors, or config flowing between layers, document what crosses the boundary — not just that something happens.

Boundary-crossing data is the contract between layers. If the docs say "authentication fails and you get a DM" but don't explain what data flows from the SDK to ollim-bot to Discord, a contributor can't debug the flow and an agent can't reason about failure modes.

**Violation:** "If authentication fails, the bot sends you a DM with a link" — what data flows from SDK to bot to Discord?
**Clean:** "If the SDK's `is_authenticated()` returns false, ollim-bot extracts an OAuth URL from the SDK CLI's output and sends it as a Discord DM."

### Rule 5: No layer should document another layer's internals

C's docs can reference B's interface but should not explain how B works internally. The strictness depends on the page's audience:

- **User-facing pages** (getting-started/, core-usage/, scheduling/, integrations/, personalizing/, extending/, self-hosting/): Any SDK or Claude Code implementation detail is a violation. Users don't need to know how the SDK works — they need to know what ollim-bot does for them.
- **Developer-facing pages** (architecture/, development/): SDK *interface* details are acceptable — function signatures, config options, types that appear in ollim-bot's code. SDK *implementation* details are still violations — internal algorithms, undocumented behavior, how the SDK achieves its results.

The distinction between interface and implementation: if ollim-bot calls it, references it, or passes it as config, it's interface. If only the SDK touches it internally, it's implementation.

**Violation (user-facing):** "The SDK uses `install_agents()` to copy spec files and then `load_agent_tool_sets()` to discover them"
**Clean (user-facing):** "ollim-bot ships bundled subagent specs that are automatically available to the agent"

**Acceptable (developer-facing):** "ollim-bot's `install_agents()` copies specs to `~/.ollim-bot/.claude/agents/`, where the SDK discovers them via `setting_sources=["project"]`"
**Still a violation (developer-facing):** "The SDK internally calls `load_agent_tool_sets()` which scans directories and parses frontmatter to build tool manifests"

---

## Cross-page checks

These require reading multiple pages to detect. Per-page agents cannot run these.

### Layer attribution consistency

- The same capability must be attributed to the same layer across all pages
- If one page says "the SDK handles sessions" and another says "ollim-bot manages sessions," that's a contradiction — one of them is wrong

### Delegation consistency

- If page A says ollim-bot delegates X to the SDK, page B should not describe X as ollim-bot's own behavior without mentioning the delegation
- When summarizing delegated behavior on non-authoritative pages, link to the authoritative page rather than re-explaining the delegation chain
