---
name: sync-docs
description: Sync documentation with source repo changes using parallel workers, reviewers, and linear merge.
disable-model-invocation: true
argument-hint: [source-repo-path]
---

`$ARGUMENTS` is the path to the source repo (e.g., `~/ollim-bot`).

## Phase 1: Research

Launch Explore agents (foreground — you need results before proceeding):

1. Identify new source commits since the last docs sync — compare `git log` in `$ARGUMENTS` against the latest changelog entry or doc commits.
2. Read the docs codebase structure, navigation, and conventions.

Decompose changes into independent units — each implementable in an isolated git worktree, mergeable on its own. Three rules for decomposition:

1. **One worker per feature area** — group by the doc pages affected, not by source commit. If two commits both affect the Gmail page, they belong to one unit.
2. **Changelog is shared** — every unit that adds user-visible changes includes a changelog bullet. Assign changelog edits to each worker (they each edit the same file), and let the merge agent resolve conflicts. Do NOT create a separate "changelog-only" worker.
3. **Cross-cutting page detection** — two passes:
   - **Keyword search**: `Grep` across `*.mdx` for terms related to each change. If a page already mentions the topic, include it in the worker's assignment.
   - **Purpose scan**: review the doc site structure and identify pages whose *purpose* implies they should cover the change, even if they don't mention it yet. A self-hosting guide should cover platform compatibility; a CLI reference should list every user-facing flag; an architecture page should reflect new subsystems. These pages need NEW sections, which keyword search cannot discover.

   Include ALL pages from both passes in the worker's assignment. Do not assume workers will discover cross-cutting pages on their own.

**Scope boundary**: workers document only what changed in the new source commits. Do not reorganize, restructure, or rewrite existing documentation — even if it could be improved.

## Phase 2: Delegate

Spawn one background agent per unit — `isolation: "worktree"`, `run_in_background: true`, all in a single message block.

Each worker prompt must include:
- The overall sync goal and the worker's specific assignment (commits, what changed, source diffs)
- Docs codebase conventions — copy these verbatim from CLAUDE.md into the prompt: **Writing standards**, **Terminology** table, **Component usage** table, and **Frontmatter requirements**. Workers cannot read CLAUDE.md from within worktrees.
- Instruction to load /mintlify and /revise skills
- The source repo path (`$ARGUMENTS`) for verification reads
- The exact doc file paths the worker should read and potentially edit (worktree-absolute)
- An explicit negative file constraint: the worker may ONLY edit the listed files — no other files should be modified, even if they appear inaccurate or outdated

### Worktree path constraint

Workers run in an isolated worktree at a path like `<repo>/.claude/worktrees/<id>/`. All Read and Edit calls must use **absolute paths within the worktree**, not the main repo. Workers should check their cwd on startup and use it as the base for all doc file paths.

### Background agent behavior

You will be automatically notified when each background agent completes — do NOT sleep, poll, or spawn agents to check on progress. Continue rendering status updates as notifications arrive.

### Worker steps

1. Load /mintlify skill. Read assigned source commits in `$ARGUMENTS` to verify understanding.
2. Read relevant docs pages (using worktree-absolute paths) to determine what to update.
3. Edit ONLY the assigned doc files listed above — do not modify, delete, or create any other files, even if they appear inaccurate or outdated. Verify edits match the goal of the assigned commits.
   - **No extrapolation** — document only what the source explicitly states or tests. If CI runs on `ubuntu-latest` and `windows-latest`, write "Ubuntu and Windows" — not "Linux" (extrapolation) or "Linux, macOS, and Windows" (fabrication). Every factual claim must trace to a specific source file, test, or config line.
   - **Changelog specificity** — changelog bullets must include specific technical identifiers from the source: function names, format strings, error types, CLI flags. Write `%-I strftime directive` not `encoding and path handling`. Vague summaries lose the detail that makes changelogs useful.
   - **Numeric verification** — for numeric claims (line counts, test counts, file counts), verify with actual commands (`wc -l`, `grep -c "^def test_"`) in the source repo. Do not estimate or count manually.
4. Re-read updated files. Invoke /revise. Stage edited files by name — do NOT use `git add .` or `git add -A`. Commit.
5. Write `REPORT.md` in the worktree root (after the commit — REPORT.md is git-excluded and must never be staged):
   - **Assignment**: task description and source commits
   - **Changes**: files modified and what changed
   - **Rationale**: why each change was made
   - **Evidence**: source-repo references — file paths, line numbers, and commit hashes in `$ARGUMENTS`

## Phase 3: Review

As each worker completes (you receive an automatic notification), spawn a reviewer agent (foreground) with the REPORT.md path and worktree branch.

### Reviewer steps

1. Load /mintlify skill. Read `REPORT.md`.
2. **Scope check** — run `git diff main..HEAD --name-only`. If any changed files are not in the worker's assignment, revert them with `git checkout main -- <file>` and amend the commit before continuing.
3. Audit the git diff against the report — do changes match rationale and evidence?
4. **Source verification** — read the full `git diff` for the worker's branch. Identify every new factual claim: platform names, numeric counts, capability statements, behavioral descriptions. For EACH claim, read the supporting source file in `$ARGUMENTS` to confirm accuracy. Pay special attention to claims that have no cited source — these are the highest fabrication risk. If a claim cannot be traced to a specific source file, line, or test, remove it.
5. Verify completeness against the **Assignment** section — no assigned changes missed or partially applied.
6. Fix issues directly, amend onto the worker's commit.
7. Escalate to the orchestrator only if a fix requires judgment or clarification.

### Failure handling

- **Worker fails or makes no changes**: Stop it. Do the work directly or re-delegate with more specific instructions (include file paths and exact edits needed).
- **Worker completes but reviewer finds major issues**: Reviewer escalates. Orchestrator decides whether to fix directly or re-delegate.
- **Skill not available** (/mintlify, /revise): Worker continues without it — these improve quality but are not blocking.

## Phase 4: Merge

Use a subagent to merge each reviewed branch onto main with linear history (`git rebase`). If there are conflicts, the subagent loads /mintlify and resolves them.

Clean up worktrees and branches after merge.

## Phase 5: Report

Render the final status table and a one-line summary. The summary must be accurate — count actual files changed from `git diff --stat`, not estimated.

| # | Unit | Files changed | Worker | Reviewer |
|---|------|--------------|--------|----------|
| 1 | title | file1.mdx, file2.mdx | done | pass |

### Status table

Render an initial table after launching workers. Update it as completion notifications arrive — `done` / `failed` for workers, `pass` / `pass (N fixes)` / `failed` for reviewers.
