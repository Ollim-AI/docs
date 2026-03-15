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

Decompose changes into independent units — each implementable in an isolated git worktree, mergeable on its own.

## Phase 2: Delegate

Spawn one background agent per unit — `isolation: "worktree"`, `run_in_background: true`, all in a single message block.

Each worker prompt must include:
- The overall sync goal and the worker's specific assignment (commits, what changed, source diffs)
- Docs codebase conventions (from CLAUDE.md)
- Instruction to load /mintlify and /revise skills
- The source repo path for verification reads

### Worktree path constraint

Workers run in an isolated worktree at a path like `<repo>/.claude/worktrees/<id>/`. All Read and Edit calls must use **absolute paths within the worktree**, not the main repo. Workers should check their cwd on startup and use it as the base for all doc file paths.

### Background agent behavior

You will be automatically notified when each background agent completes — do NOT sleep, poll, or spawn agents to check on progress. Continue rendering status updates as notifications arrive.

### Worker steps

1. Load /mintlify skill. Read assigned source commits in `$ARGUMENTS` to verify understanding.
2. Read relevant docs pages (using worktree-absolute paths) to determine what to update.
3. Edit docs to reflect the source changes. Verify edits match the goal of the assigned commits.
4. Re-read updated files. Invoke /revise. Commit.
5. Write `REPORT.md` (git-untracked) in the worktree root:
   - **Assignment**: task description and source commits
   - **Changes**: files modified and what changed
   - **Rationale**: why each change was made
   - **Evidence**: source-repo references — file paths, line numbers, and commit hashes in `$ARGUMENTS`

## Phase 3: Review

As each worker completes (you receive an automatic notification), spawn a reviewer agent (foreground) with the REPORT.md path and worktree branch.

### Reviewer steps

1. Load /mintlify skill. Read `REPORT.md`.
2. Audit the git diff against the report — do changes match rationale and evidence?
3. Verify completeness against the **Assignment** section — no assigned changes missed or partially applied.
4. Fix issues directly, amend onto the worker's commit.
5. Escalate to the orchestrator only if a fix requires judgment or clarification.

### Failure handling

- **Worker fails or makes no changes**: Stop it. Do the work directly or re-delegate with more specific instructions (include file paths and exact edits needed).
- **Worker completes but reviewer finds major issues**: Reviewer escalates. Orchestrator decides whether to fix directly or re-delegate.
- **Skill not available** (/mintlify, /revise): Worker continues without it — these improve quality but are not blocking.

## Phase 4: Merge

Use a subagent to merge each reviewed branch onto main with linear history (`git rebase`). If there are conflicts, the subagent loads /mintlify and resolves them.

Clean up worktrees and branches after merge.

## Phase 5: Report

Render the final status table and a one-line summary:

| # | Unit | Worker | Reviewer |
|---|------|--------|----------|
| 1 | title | done | pass |

### Status table

Render an initial table after launching workers. Update it as completion notifications arrive — `done` / `failed` for workers, `pass` / `pass (N fixes)` / `failed` for reviewers.
