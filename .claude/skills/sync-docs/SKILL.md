---
name: sync-docs
description: Sync documentation with source repo changes using parallel workers, reviewers, and linear merge.
disable-model-invocation: true
argument-hint: [source-repo-path]
---

## Orchestration

Research first: launch Explore agents (foreground — you need results before proceeding) to understand the scope of source changes and the docs codebase. Decompose into independent units — each implementable in an isolated git worktree, mergeable on its own.

Spawn one background agent per unit — `isolation: "worktree"`, `run_in_background: true`, all in a single message block. Each prompt must be self-contained: overall goal, unit's specific task (commits, what changed), and codebase conventions.

## Track progress

After launching all workers, render an initial status table:

| # | Unit | Worker | Reviewer |
|---|------|--------|----------|
| 1 | <title> | running | — |

As background-agent completion notifications arrive, update the table with status (`done` / `failed`) and reviewer results (`pass`, `pass (N fixes)`, `failed`). When all agents have reported, render the final table and a one-line summary.

## Workflow

apply /mintlify on relevant pages.

1. review new changes in $ARGUMENTS
2. delegate each logical change (a set of commits) to a worker
3.a. each worker loads the /mintlify skill and reads the committed changes it was assigned
3.b. they then read the docs codebase to determine which files to modify
3.c. they update the docs to ensure no stale documentation
3.d. verify their updates match the goal of the git changes
3.e. re-read their updated files, invoke /simplify, then commit
3.f. write `REPORT.md` (git-untracked) in the worktree root — this is the handoff artifact the reviewer audits against:
  - **Assignment**: original task description and source commits
  - **Changes**: files modified and what changed
  - **Rationale**: why each change was made
  - **Evidence**: source-repo references (files, lines, commits) backing each change
4. when a worker finishes, you spawn a reviewer with the report file path and the worktree branch
4.a. reviewer loads /mintlify and reads `REPORT.md`
4.b. audits the diff against the report — do changes match rationale and evidence?
4.c. verifies completeness against the **Assignment** section — no assigned changes missed or partially applied
4.d. fixes issues directly, amend onto the worker's commit
4.e. escalate to you only if a fix requires judgment or clarification
5. use a subagent to merge their branch onto main branch with linear history, it uses /mintlify to resolve any conflicts.
6. verify work is completed, clean up the worktrees, and report back to me.

do not prescribe files or updates to the worker agents, they will have better judgement working in isolation.
