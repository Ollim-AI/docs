---
name: batch-review
description: Batch review multiple documentation pages against the mintlify page-review-checklist. Use when reviewing a section, a glob of pages, or the entire docs site for quality violations. Also use when the user says "review all pages", "audit the docs", "check docs quality", or mentions reviewing documentation across multiple files.
argument-hint: <glob, section name, or page list> [--fix]
allowed-tools: Read, Glob, Grep, Bash, Agent, AskUserQuestion
---

# Batch docs review

Review multiple documentation pages in parallel against the mintlify page-review-checklist. Spawns per-page agents for page-local checks and a cross-cutting agent for issues that only surface when comparing pages.

## 1. Resolve target pages

Turn the user's input into a list of MDX file paths:

| Input type | How to resolve |
|-----------|---------------|
| Glob pattern (`core-usage/*.mdx`) | Glob directly |
| Section name (`getting-started`) | Read `docs.json`, find the matching navigation group, extract page paths, glob for their `.mdx` files |
| Explicit list | Use as-is |
| Nothing / "all" | Glob `**/*.mdx` in the docs root |

If the resolved set is empty, stop and tell the user — don't spawn agents with no targets.

## 2. Read the checklist

Read `.claude/skills/mintlify/page-review-checklist.md`. It has two sections:

- **Page-local checks** — accessibility, content type structure, style & tone (page-scoped), media. Each per-page agent runs these.
- **Cross-page checks** — terminology consistency, cross-page linking, maintenance. The cross-cutting agent runs these.

## 3. Spawn per-page agents

Spawn one background `page-reviewer` agent per target page. If the target set is >15 pages, chunk into batches of 10–15 and wait for each batch to complete before starting the next. All agents in a batch launch in a single message.

Each agent's prompt — keep it compact; the agent definition has the methodology:

```
Page: <absolute-path-to-mdx-file>
```

## 4. Spawn cross-cutting agent

In the same message as the per-page agents (or the first batch), spawn one background general-purpose agent for cross-page checks. It reads ALL target pages.

```
Review these documentation pages for cross-page issues using the cross-page checks in the checklist.

Page paths:
<list all absolute paths, one per line>

Checklist path: <absolute-path-to-page-review-checklist.md>

Steps:
1. Read the "Cross-page checks" section of the checklist
2. Read all listed pages
3. Check terminology consistency — scan for alternating terms for the same concept across pages
4. Check linking — look for circular links between the same pages
5. Check maintenance — flag pages that appear stale or contain information that contradicts other pages
6. Output ONLY a findings table — no preamble, no summary

If no violations found, output: "No violations found."

Output format (one row per violation):
| Category | Pages affected | Violation | Checklist rule |

- Category: the checklist section (e.g., "Terminology consistency", "Linking")
- Pages affected: which page(s) have the issue
- Violation: what's wrong
- Checklist rule: the specific rule from the checklist that's violated (quote it)
```

For large page sets (>30 pages), the cross-cutting agent may hit context limits. If it fails or returns incomplete results, split the page set into overlapping groups (overlap by 5 pages to catch cross-group issues) and spawn one cross-cutting agent per group.

## 5. Track progress

Render a status table after launching agents. Update it as completion notifications arrive:

```
| # | Scope | Target | Status |
|---|-------|--------|--------|
| 1 | page-local | getting-started/quickstart.mdx | done (3 findings) |
| 2 | page-local | getting-started/installation.mdx | running... |
| 3 | cross-page | all 6 pages | done (1 finding) |
```

## 6. Aggregate results

Once all agents complete, produce the summary report:

```
## Batch review: <target description>

**Pages reviewed**: N
**Total findings**: N page-local, N cross-page

### Per-page findings

#### <page-path>
| Category | Location | Violation | Checklist rule |
|----------|----------|-----------|----------------|
(paste agent output)

#### <page-path>
(repeat for each page with findings — skip pages with no violations)

### Cross-page findings
| Category | Pages affected | Violation | Checklist rule |
|----------|---------------|-----------|----------------|
(paste cross-cutting agent output)

### Clean pages
- <list pages with no violations>
```

## 7. Fix mode (if `--fix` passed)

If the user passed `--fix`, after presenting the report, offer to fix violations:

1. Present the report first — the user should see what will change before anything is modified
2. Ask which findings to fix (all, specific pages, specific categories)
3. For each page with approved fixes, load the /mintlify skill and apply corrections
4. Re-run the per-page agent on modified pages to verify fixes didn't introduce new issues

Do not fix cross-page issues automatically — they require judgment about which page is authoritative. Present them for the user to decide.
