# Documentation Audit — Single Page

You are auditing documentation for **ollim-bot** against the actual source code at `../ollim-bot/`. You will audit exactly ONE page per invocation.

The source code is the single source of truth. If the docs and source disagree, fix the docs.

---

## Rules

1. Audit ONE unchecked page from `AUDIT.md`, then stop.
2. Read the mapped source files before judging any claim.
3. Fix only proven discrepancies — do not rewrite prose for style.
4. Run the verifier after any edits.
5. Mark the page in `AUDIT.md` and commit.
6. If no unchecked pages remain, output `AUDIT COMPLETE` and stop.

---

## Phase 0 — Orient

1. Read `AUDIT.md` to find the next unchecked page (first `- [ ]` line, top to bottom).
2. Read `AGENTS.md` for the source file mapping and Mintlify conventions.
3. If all pages are checked, output exactly:

```
AUDIT COMPLETE
```

Then stop. Do nothing else.

---

## Phase 1 — Study

Read the page's mapped source files from `../ollim-bot/`. Use up to 5 parallel subagents.

Also read the relevant sections of `../ollim-bot/CLAUDE.md` — it contains authoritative architecture documentation.

Extract every verifiable fact: identifier names, default values, field types, CLI flags, behaviors, constraints.

---

## Phase 2 — Audit

Read the documentation page. Compare every factual claim against the source code:

- **Identifier names**: env vars, constants, class names, dataclass field names, function names, MCP tool names, CLI flags, slash commands, session event types, enum values
- **Default values**: every documented default must match source
- **Field types and constraints**: must match dataclass/TypedDict definitions
- **CLI flags**: must match argparse definitions (flag names, choices, defaults)
- **Behavior descriptions**: must match actual code logic
- **File paths and directory structures**: must match storage.py constants

If you find a discrepancy, edit the MDX file to match the source.
If nothing is wrong, do not edit the file.

---

## Phase 3 — Verify

Run the mechanical verifier:

```bash
uv run python verify_docs.py --page <page-path>
```

The verifier must report 0 unresolved identifiers for this page. If it reports issues:
- If the identifier is a genuine doc error, fix the page and re-run
- If the identifier is a legitimate external term not in the truth index, it is fine — the verifier's allowlist covers most cases

---

## Phase 4 — Record and Commit

1. In `AUDIT.md`, check off the page:
   Change `- [ ] page/path.mdx` to `- [x] page/path.mdx`

2. Update the "Pages audited" counter at the top.

3. Stage and commit:

```bash
git add AUDIT.md
git add <page-path-if-modified>
git commit -m "audit(<section>): verify <page-name>"
```

Example: `git commit -m "audit(scheduling): verify reminders"`

---

## Guardrails

999. **ONE page per invocation.** Audit one, commit, stop.
998. **NEVER fabricate.** If you aren't sure whether a claim is wrong, leave it and note it in the commit message.
997. **The source code is truth.** Always read the actual source before judging docs.
996. **Run the verifier.** Do not skip Phase 3.
995. **Do not rewrite for style.** Only fix factual errors. Do not add content, change wording, or restructure sections.
994. **Commit message format** must be `audit(<section>): verify <page-name>`.
