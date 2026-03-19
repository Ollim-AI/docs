---
name: accuracy
description: Scan documentation for accuracy issues by cross-referencing claims against source code. Use when the user says "check accuracy", "find accuracy issues", "verify docs against source", or wants to ensure documentation matches the implementation.
argument-hint: <glob, section name, or "all"> [--fix]
allowed-tools: Agent, Read, Glob, Grep, Bash, Edit, AskUserQuestion
---

# Accuracy scanner

Launch parallel subagents to find documentation claims that don't match the source code, then fix on approval.

## 1. Resolve target pages

Turn the user's input into a list of MDX file paths:

| Input type | How to resolve |
|-----------|---------------|
| Glob pattern (`core-usage/*.mdx`) | Glob directly |
| Section name (`scheduling`) | Read `docs.json`, find matching nav group, extract page paths, glob for `.mdx` files |
| Explicit list | Use as-is |
| Nothing / "all" | Glob `**/*.mdx` in docs root, exclude `.claude/` |

If the resolved set is empty, stop and tell the user.

## 2. Recon — map the source repo

Read the source repo's architecture reference (`~/ollim-bot/CLAUDE.md`). Extract:
- **Architecture map**: module names, key files, what each file does
- **Key source paths**: where defaults, config, tools, commands, and behavior live
- **Terminology**: canonical names for concepts

This map gets injected into every scanner prompt. Without it, agents waste time searching for the wrong files.

## 3. Launch parallel scanner agents

Spawn **3 scanner agents** simultaneously (single message, all `run_in_background=true`). Each gets:
1. The page list from step 1
2. The architecture map from step 2
3. Its specific checklist below
4. The output format

For >15 target pages: chunk pages across multiple instances per dimension (10-15 pages each). The cross-reference scanner always gets ALL pages (chunk with 5-page overlap if >30).

### Scanner specializations

**Code-claims scanner** — checks literal values against source

Every concrete claim: default values, parameter names, env var names, file paths, command syntax, tool names, argument lists, numerical constants.

For each claim:
1. Find the specific assertion in the doc (e.g., "default is 5", "the parameter is called `capacity`")
2. Search source code for the actual value
3. If they don't match, report it

FP guidance: only flag when the doc states a specific value/name and the source disagrees. Do NOT flag omissions, style, or vague descriptions.

**Behavior-claims scanner** — checks logic descriptions against implementation

Behavioral claims: "when X happens, Y occurs", "the bot does X before Y", "if X is set, behavior changes to Y". Trace each claim through the actual code logic.

For each claim:
1. Identify the behavioral assertion
2. Find the source code that implements it
3. Walk the code path — does the described behavior match?

FP guidance: only flag when the doc describes a specific sequence or condition and the code does something different. Do NOT flag simplified explanations that are technically correct but omit edge cases.

**Cross-reference scanner** — checks inter-page consistency

When multiple pages describe the same concept, check they agree on: default values, parameter names, behavioral descriptions, terminology, numerical claims (timeouts, counts, limits).

This scanner reads ONLY documentation pages (no source code). For each inconsistency, cite both pages and note which is likely correct.

FP guidance: only flag actual conflicts where both statements can't be true. Do NOT flag pages that cover different aspects of the same topic.

### Scanner prompt template

```
You are a specialized [CATEGORY] accuracy scanner.

**Documentation pages to check** (read ALL of these):
[list of absolute paths]

**Source code repo**: ~/ollim-bot/
**Architecture map**:
[paste from step 2]

IMPORTANT: Read every listed doc page completely. For code-claims and behavior scanners, search the source repo to verify each claim.

Scan for these accuracy patterns:
[numbered checklist from the specialization above]

Report format — for EACH confirmed finding:
- **Doc file**: path and line number
- **Claim**: what the doc says (quote it)
- **Source file**: path and line where the truth is [code-claims/behavior only]
- **Actual**: what the source says / what the other page says
- **Severity**: wrong (factually incorrect) | outdated (was correct, source changed) | contradiction (two pages disagree)

Rules:
- Only report confirmed mismatches — cite both the doc AND the source/other page
- Do NOT report style issues, missing documentation, or subjective opinions
- Do NOT report simplified explanations that are technically correct
- If you find zero issues, say so — do not invent findings

End with a summary table: | # | Doc file:line | Claim summary | Severity |
```

## 4. Triage results

After all agents complete:

1. **Verify every finding** — read the cited doc line AND the cited source line yourself. Scanners misread code or miss context. For each finding:
   - Confirm the doc actually says what the scanner claims
   - Confirm the source actually says something different
   - Check if surrounding context (comments, related functions) resolves the apparent mismatch
2. **Deduplicate** — code-claims and behavior scanners may flag the same issue from different angles. Note convergence (high confidence).
3. **Filter** — discard findings where the scanner misread the code, missed context, or where the doc is a valid simplification.
4. **Rank** — order by severity: wrong > outdated > contradiction.

## 5. Report

Present the triaged findings:

```markdown
## Accuracy scan — [target description]

**Pages scanned**: N
**Findings**: X confirmed (Y false positives filtered)

### Findings

| # | Page | Line | Claim | Actual (source) | Severity |
|---|------|------|-------|-----------------|----------|
| 1 | ... | ... | ... | ... | wrong |

### Details

#### Finding 1: [short description]
**Doc** (`path:line`): "quoted claim"
**Source** (`path:line`): actual value/behavior
**Fix**: [what the doc should say]

### Filtered false positives
[list each discarded finding with one-line reason]
```

## 6. Fix (if `--fix` passed or user approves)

After presenting the report:

1. Ask which findings to fix (all, specific numbers, skip)
2. For each approved fix, apply the correction with the Edit tool
3. Read the edited line to confirm the fix reads naturally in context
4. Summarize what was changed

Do NOT auto-fix without approval — accuracy fixes change meaning, not just style.
