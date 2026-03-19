---
name: accuracy
description: Scan documentation for accuracy issues by cross-referencing claims against source code. Use when the user says "check accuracy", "find accuracy issues", "verify docs against source", or wants to ensure documentation matches the implementation.
argument-hint: <glob, section name, or "all"> [--fix]
allowed-tools: Agent, Read, Glob, Grep, Bash, Edit
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

For >15 target pages: chunk by architectural subsystem, not arbitrary page ranges. Use `docs.json` nav groups to keep related pages together (pages that cross-reference each other must be in the same chunk). Aim for 8-12 pages per chunk — smaller chunks mean more thorough per-page examination. The cross-reference scanner always gets ALL pages (chunk with 5-page overlap if >30).

### Scanner specializations

**Code-claims scanner** — checks literal values against source

Systematically verify every concrete claim by type:

| Claim type | What to check | Where to look in source |
|-----------|---------------|------------------------|
| Numerical counts | "N modules", "N tools", "N events" | Count actual items in source (list lengths, enum members, registered handlers) |
| Default values | "default is X", "defaults to X" | Find the variable/parameter definition, check its default |
| Parameter/field names | `` `param_name` ``, table columns listing fields | Find the actual parameter in function signatures, dataclass fields, YAML schemas |
| File paths | `` `~/.ollim-bot/foo` ``, "stored in X" | Check filesystem layout in source, path constants |
| Command syntax | `` `/command arg` ``, CLI examples | Find command registration, argument parsing |
| Enum/list membership | "one of: A, B, C", event type tables | Find the Literal type, enum class, or list constant |
| Tool names/counts | "N tools", tool name references | Count registered tools in MCP server setup |

For each claim:
1. Classify it by type from the table above
2. Find the specific assertion in the doc (quote it)
3. Search source code for the actual value — use the "where to look" column to guide your search
4. If they don't match, report it

FP guidance: only flag when the doc states a specific value/name and the source disagrees. Do NOT flag omissions, style, or vague descriptions.

**Behavior-claims scanner** — checks logic descriptions against implementation

Systematically verify behavioral claims by type:

| Claim type | What to check | Verification approach |
|-----------|---------------|----------------------|
| Conditional behavior | "if X is set, Y happens" | Find the condition in source, trace both branches |
| Sequence ordering | "X happens before Y", "first X, then Y" | Find both operations, verify call order |
| State transitions | "when X, state changes to Y" | Find the state variable, trace all transitions |
| Config-dependent behavior | "when config X is true, behavior changes to Y" | Find where config is read, trace the conditional path |
| Restriction/constraint claims | "X only works when Y", "X is limited to Y" | Find the guard/check in source, verify it exists |
| Fallback/recovery | "if X fails, falls back to Y" | Find the error handler, verify fallback logic |

For each claim:
1. Classify it by type from the table above
2. Identify the behavioral assertion (quote it)
3. Find the source code that implements it
4. Walk the code path using the verification approach — read surrounding context (comments, related functions, config loading) to understand the full behavior
5. Only flag if the described behavior genuinely differs from implementation

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

End with TWO tables:

1. Per-page attestation (REQUIRED — one row per assigned page, no exceptions):
| Page | Claims checked | Findings |
For pages with 0 findings, briefly note what you checked (e.g., "verified 3 numerical counts, 2 defaults — all correct").

2. Findings summary: | # | Doc file:line | Claim summary | Severity |
```

## 4. Triage results

**WAIT for ALL scanner agents to complete before starting triage.** Do not begin verifying, reporting, or fixing based on partial results — a scanner that finishes later may find issues that change your triage decisions. Only proceed once every launched agent has returned.

After all agents complete:

1. **Coverage check** — review each scanner's per-page attestation table. If any scanner skipped a page (no attestation row) or reported 0 claims checked on a page, read that page yourself and spot-check its top 3-5 verifiable claims against source. Scanners under-examine "quiet" pages when grouped with pages that have obvious issues.
2. **Verify every finding** — read the cited doc line AND the cited source line yourself. Scanners misread code or miss context. For each finding:
   - Confirm the doc actually says what the scanner claims
   - Confirm the source actually says something different
   - Check if surrounding context (comments, related functions) resolves the apparent mismatch
3. **Re-verify numerical claims independently** — for any finding that changes a count, list, or enumeration (e.g., "N modules", "N tools"), do NOT trust the scanner's number. Miscounts are the most common scanner-introduced inaccuracy. Follow this exact procedure:
   1. Use Grep or Glob to list the actual items in source (e.g., `Glob("*.py")` for module counts, `Grep` for registered tools)
   2. Paste the full enumerated list in your reasoning
   3. Count the pasted list — this is your verified number
   4. If your count differs from the scanner's, use yours. If you cannot enumerate the items, flag the finding as unverified rather than guessing.
4. **Deduplicate** — code-claims and behavior scanners may flag the same issue from different angles. Note convergence (high confidence).
5. **Filter** — discard findings where the scanner misread the code, missed context, or where the doc is a valid simplification.
6. **Rank** — order by severity: wrong > outdated > contradiction.

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

## 6. Fix

**When `--fix` is passed**: apply all confirmed findings automatically after presenting the report. Do not ask for approval — the flag is the approval.

**When `--fix` is NOT passed**: present the report and stop. The user will decide which findings to fix.

For each fix:
1. Apply the correction with the Edit tool
2. Read the edited line AND its surrounding paragraph to confirm:
   - The fix reads naturally in context
   - The new value matches what you verified in source during triage (step 4) — not what the scanner reported
   - The fix doesn't introduce a new inaccuracy (e.g., changing a count to the scanner's number without independent verification)
3. **Ripple check** — after fixing a claim, scan the same page for other claims affected by the same underlying change. Example: fixing a tool count from 7 to 11 should also trigger checking prose paragraphs, bullet lists, and tables on the same page that reference those tools or their names. A single source change (e.g., new tools added) often affects multiple claims on the same page.
4. After all fixes, summarize what was changed
