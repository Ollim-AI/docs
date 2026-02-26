# Documentation Audit — Single Page

You are auditing documentation for **ollim-bot** against the actual source code at `../ollim-bot/`. You will audit exactly ONE page per invocation.

The source code is the single source of truth. If the docs and source disagree, fix the docs.

---

## Constraints (in priority order)

1. **Never modify source code, the verifier, or unrelated doc pages** — you may only edit the target MDX page and `AUDIT.md`. Modifying source to match docs would introduce bugs; modifying other pages risks cascading errors across iterations.
2. **Never fabricate a fix.** If you aren't sure whether a claim is wrong, leave it unchanged and note the uncertainty in the commit body — a fabricated fix is worse than a stale doc, because it creates a lie that looks authoritative.
3. **Source code is truth.** Read the actual source before judging any doc claim — not CLAUDE.md summaries, not other doc pages, not comments. The Python source is the canonical reference.
4. **Fix only proven discrepancies.** Do not rewrite prose for style, add content, change wording, or restructure sections — style edits create noisy diffs that obscure real fixes in review.
5. **ONE page per invocation.** Audit one, commit, stop — fresh context windows prevent error accumulation across pages.
6. **Always run the verifier** (Phase 3), whether or not you made edits — it catches pre-existing errors too.
7. **If all pages are already audited**, output exactly `AUDIT COMPLETE` and stop. Do nothing else.

---

## Phase 0 — Orient

1. Read `AUDIT.md` to find the next unchecked page (first `- [ ]` line, top to bottom).
2. Read `AGENTS.md` for the source file mapping and Mintlify conventions.
3. If all pages are checked, output `AUDIT COMPLETE` and stop.

---

## Phase 1 — Study

Read the page's mapped source files from `../ollim-bot/`. Use up to 5 parallel subagents for speed.

Also read the relevant sections of `../ollim-bot/CLAUDE.md` — it contains authoritative architecture notes, but the Python source overrides it if they disagree.

For each source file, extract every verifiable fact: identifier names, default values, field types, CLI flags, enum values, behavioral logic, constraints.

---

## Phase 2 — Audit

Read the documentation page. For every factual claim, find the corresponding source code and verify it matches. Check these categories:

- **Identifier names**: env vars, constants, class names, dataclass field names, function names, MCP tool names, CLI flags, slash commands, session event types, enum values
- **Default values**: every documented default must match the source literal
- **Field types and constraints**: must match dataclass/TypedDict definitions
- **CLI flags**: must match argparse definitions (flag names, choices, defaults)
- **Behavior descriptions**: must match actual code logic (trace the execution path)
- **File paths and directory structures**: must match `storage.py` constants

If you find a proven discrepancy, edit the MDX file to match the source.
If nothing is wrong, do not edit the file.

---

## Phase 3 — Verify

Run the mechanical verifier:

```bash
uv run python verify_docs.py --page <page-path>
```

The verifier must report 0 unresolved identifiers for this page.

- If it reports a genuine doc error → fix the page and re-run
- If it reports a legitimate external term not in the truth index → acceptable, the allowlist covers most cases
- **If the verifier itself crashes** (import error, missing file, Python traceback) → do not proceed to Phase 4. Report the error in your output and stop.

---

## Phase 4 — Record and Commit

1. In `AUDIT.md`, change `- [ ] page/path.mdx` to `- [x] page/path.mdx`

2. Update the "Pages audited" counter at the top.

3. Stage and commit:

```bash
git add AUDIT.md
git add <page-path-if-modified>
git commit -m "audit(<section>): verify <page-name>" -m "<findings-summary>"
```

The **findings summary** (second `-m`) is one line per finding. Examples:

```
audit(scheduling): verify reminders
- Fixed: default max_chain was documented as 5, source shows 3
- Fixed: --no-thinking flag was --disable-thinking in argparse
- Checked: 14 identifiers, 6 defaults, 3 behavioral claims — all correct
```

If no edits were needed:
```
audit(scheduling): verify ping-budget
- No discrepancies found. Checked: 8 identifiers, 4 defaults, 2 behavioral claims.
```

**If the commit fails** (e.g., hook rejection): read the error, fix the issue (usually commit message format), and retry once. If it fails again, report the error in your output and stop.
