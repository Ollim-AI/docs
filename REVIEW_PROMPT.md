# Documentation Fix — Single Page

You are fixing a documentation page based on review findings. **Edit the `.mdx` file** to correct all issues.

## Workflow

1. Read the assigned `.mdx` page
2. Read **every** source file listed in your assignment
3. Read `literal:../ollim-bot/CLAUDE.md` for authoritative architecture context
4. Read the review findings provided in your assignment
5. For each issue: verify it against source, then fix the `.mdx` file
6. After all fixes, re-read the page to verify consistency

## Fix Rules

- **Source code is the truth.** If docs and source disagree, make docs match source.
- **Preserve structure.** Don't reorganize sections, rename headings, or change the page's overall approach — just fix the inaccuracies.
- **Minimal edits.** Fix the specific issues flagged. Don't rewrite surrounding prose, add new sections, or do style improvements.
- **No new hallucinations.** If you can't verify something from source, remove the claim rather than guess.
- **Keep it concise.** If fixing a claim means adding detail, keep it brief — one sentence, not a paragraph.

## Output

After fixing, output a short summary of what you changed:

```
## {page-path}

### Fixes applied
- [line ~N] description of fix
- [line ~N] ...

### Skipped
- description + reason (if any flagged issue was not a real problem)
```
