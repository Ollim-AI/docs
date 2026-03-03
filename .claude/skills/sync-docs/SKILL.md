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
3.e. re-read their updated files and
3.f. invoke /simplify, then commit
4. you spawn the reviewer after the worker finishes. subagents cant spawn their own subagents. spawn agents in non-blocking mode in the background. chain reviewer subagents to verify their work using /mintlify.
5. use a subagent to merge their branch onto main branch with linear history, it uses /mintlify to resolve any conflicts.
6. verify work is completed, clean up the worktrees, and report back to me.

do not prescribe files or updates to the worker agents, they will have better judgement working in isolation.
