---
name: layer-audit
description: Audit documentation pages for layer boundary violations across the three-layer composition chain (Claude Code → Agent SDK → ollim-bot). Use when reviewing layer attribution, delegation documentation, or boundary-crossing behavior. Also use when the user says "audit layers", "check layer boundaries", "layer violations", "check layer docs", or wants to verify that docs correctly describe which layer handles what.
argument-hint: <glob, section name, or page list> [--fix]
allowed-tools: Read, Glob, Grep, Bash, Agent, AskUserQuestion, WebFetch
---

# Layer audit

Audit documentation pages against the layer boundary checklist. ollim-bot is built on a three-layer composition chain — each layer composes the behavior of the one below it:

| Layer | Name | Role |
|-------|------|------|
| A | Claude Code | Foundation — AI model, tools, bash, MCP, file I/O |
| B | Claude Agent SDK | Middleware — agent loop, sessions, compaction, streaming |
| C | ollim-bot | Application — Discord integration, scheduling, forks, user context |

Documentation should respect these boundaries: each page documents its own layer, attributes behavior to the correct layer, and describes what crosses boundaries rather than how other layers work internally.

## 1. Resolve target pages

Turn the user's input into a list of MDX file paths:

| Input type | How to resolve |
|-----------|---------------|
| Glob pattern (`core-usage/*.mdx`) | Glob directly |
| Section name (`extending`) | Read `docs.json`, find the matching navigation group, extract page paths, glob for their `.mdx` files |
| Explicit list | Use as-is |
| Nothing / "all" | Glob `**/*.mdx` in the docs root |

If the resolved set is empty, stop and tell the user.

## 2. Read the checklist

Read `.claude/skills/layer-audit/layer-boundary-checklist.md` — the 5 rules, what counts as a layer, cross-page checks.

## 3. Classify page audience

For each target page, determine its audience from its location:

| Location | Audience | Rule 5 strictness |
|----------|----------|-------------------|
| `architecture/`, `development/` | Developer-facing | SDK *interface* details OK, SDK *implementation* details still violations |
| Everything else | User-facing | Any SDK/Claude Code implementation detail is a violation |

This classification matters because developer-facing pages legitimately reference SDK function names and config options — that's not a violation. Describing how the SDK internally implements those functions is.

## 4. Spawn per-page agents

Spawn one background Explore agent per target page. If >15 pages, batch into groups of 10–15 and wait for each batch before starting the next. All agents in a batch launch in a single message.

Each agent's prompt:

```
Audit this documentation page for layer boundary violations.

Page path: <absolute-path-to-mdx-file>
Checklist path: <absolute-path-to-layer-boundary-checklist.md>
Page audience: <user-facing|developer-facing>

The three layers:
- Layer A (Claude Code): Foundation — AI model, tools, bash, MCP, file I/O
- Layer B (Claude Agent SDK): Middleware — agent loop, sessions, compaction, streaming
- Layer C (ollim-bot): Application — Discord integration, scheduling, forks, user context

Steps:
1. Read the page and the checklist
2. For each rule, determine if it applies (skip rules about layers the page doesn't mention)
3. Verify claims against official docs — when the page attributes behavior to the SDK or Claude Code
   and you're not sure the attribution is correct, use the WebFetch tool to ground your judgment.

   Only fetch when genuinely uncertain about a claim — don't fetch for every layer mention.
   Typical triggers: SDK-specific function names, config options, behavioral claims about how
   another layer works, or ambiguous delegation descriptions.

   a. **Discover**: Call WebFetch to get the full URL index, then pick the relevant URL yourself.

      For SDK claims:
      WebFetch(
        url: "https://platform.claude.com/llms.txt",
        prompt: "Return all URLs that contain 'agent-sdk' in the path. One per line, no other text."
      )

      For Claude Code claims:
      WebFetch(
        url: "https://docs.anthropic.com/en/docs/claude-code/llms.txt",
        prompt: "Return all URLs. One per line, no other text."
      )

      Then scan the returned URLs and select the one most relevant to the claim.

   b. **Verify**: Call WebFetch on the specific doc URL from step (a).

      WebFetch(
        url: "<URL returned from step a>",
        prompt: "Quote verbatim all sections relevant to: <TOPIC FROM THE CLAIM, e.g. 'hooks', 'session persistence', 'setting_sources'>. Include headings for context. Return only the quoted sections, no commentary."
      )

4. For Rule 5, calibrate strictness based on audience:
   - User-facing: any SDK/Claude Code internals are violations
   - Developer-facing: SDK interface details (function signatures, config options) are acceptable;
     SDK implementation details are still violations
5. Output ONLY a findings table — no preamble, no summary

If no violations found, output: "No violations found."

Output format (one row per violation):
| Rule | Location | Violation | Verified against | Suggested fix |

- Rule: which rule number and short name (e.g., "Rule 5: cross-layer internals")
- Location: heading name or line content where the violation occurs
- Violation: what's wrong — quote the problematic text
- Verified against: URL fetched to confirm, or "checklist only" if no fetch needed
- Suggested fix: how to rewrite it to respect the layer boundary
```

## 5. Spawn cross-cutting agent

In the same message as the per-page agents (or the first batch), spawn one background Explore agent for cross-page checks.

```
Check these documentation pages for layer attribution consistency.

Page paths:
<list all absolute paths, one per line>

Checklist path: <absolute-path-to-layer-boundary-checklist.md>

Steps:
1. Read the "Cross-page checks" section of the checklist
2. Read all listed pages
3. Check: is the same capability attributed to the same layer across all pages?
4. Check: if page A says ollim-bot delegates X to the SDK, does page B describe X as ollim-bot's own behavior?
5. Check: are there pages that describe layer-spanning behavior without any attribution where other pages do attribute it?
6. Output ONLY a findings table — no preamble, no summary

If no violations found, output: "No violations found."

Output format (one row per violation):
| Pages affected | Inconsistency | Suggested resolution |

- Pages affected: which page(s) have conflicting or missing attribution
- Inconsistency: what the contradiction or gap is — quote from each page
- Suggested resolution: which page should be authoritative and what the others should say
```

For large page sets (>30 pages), split into overlapping groups (5-page overlap) with one cross-cutting agent per group.

## 6. Track progress

Render a status table after launching agents. Update as completion notifications arrive:

```
| # | Scope | Target | Status |
|---|-------|--------|--------|
| 1 | per-page | architecture/overview.mdx | done (2 findings) |
| 2 | per-page | extending/skills.mdx | running... |
| 3 | cross-page | all 8 pages | done (1 finding) |
```

## 7. Aggregate results

Once all agents complete, produce the summary report:

```
## Layer audit: <target description>

**Pages audited**: N
**Total findings**: N per-page, N cross-page

### Per-page findings

#### <page-path> (audience)
| Rule | Location | Violation | Suggested fix |
|------|----------|-----------|---------------|
(paste agent output)

#### <page-path> (audience)
(repeat for each page with findings — skip clean pages)

### Cross-page findings
| Pages affected | Inconsistency | Suggested resolution |
|---------------|---------------|---------------------|
(paste cross-cutting agent output)

### Clean pages
- <list pages with no violations>
```

## 8. Fix mode (if `--fix` passed)

If the user passed `--fix`, after presenting the report:

1. Present the full report first — the user sees what will change before anything is modified
2. Ask which findings to fix (all, specific pages, specific rules)
3. For each page with approved fixes, load the /mintlify skill and apply corrections
4. Re-run the per-page agent on modified pages to verify fixes didn't introduce new violations

Do not fix cross-page inconsistencies automatically — they require judgment about which page is authoritative. Present them for the user to decide.
