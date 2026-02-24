# Documentation Authoring — Single Page

You are writing documentation for **ollim-bot**, an ADHD-friendly Discord bot with proactive reminders, powered by Claude. You will write exactly ONE documentation page per invocation.

The docs site is built with **Mintlify** (MDX + YAML frontmatter). The source code lives at `literal:../ollim-bot/`. The docs repo is your working directory.

---

## Phase 0 — Orient

1. Read `AGENTS.md` for operational context (source mapping, Mintlify syntax, conventions).
2. Read `SPEC.md` for page templates (§ Page Templates) and content priority order (§ Content Priority).
3. Search all `.mdx` files for pages that still contain `"Content coming soon."` — these are incomplete.

---

## Phase 1 — Select

From the incomplete pages, pick the **highest-priority** one using the priority order in SPEC.md § Content Priority (Phase 1 → Phase 4). Within a phase, follow the numbered order.

If **no incomplete pages remain**, output exactly:

```
ALL PAGES COMPLETE
```

Then stop. Do nothing else.

---

## Phase 2 — Study

Look up this page's entry in `AGENTS.md` § Source Mapping to find which source files to read.

Using **up to 5 parallel subagents**, read those source files from `literal:../ollim-bot/`. Also read the relevant sections of `literal:../ollim-bot/CLAUDE.md` — it contains authoritative architecture documentation.

**You must read the actual source code.** Extract:
- Function signatures, class fields, dataclass definitions
- YAML frontmatter schemas (field names, types, defaults)
- CLI argument parsers and subcommands
- Environment variable names and defaults
- Discord slash command definitions
- MCP tool names and parameters
- Default values, constants, and edge cases

Do not rely on memory or assumptions. The source is the single source of truth.

---

## Phase 3 — Write

Write the page content using the **correct template** from SPEC.md § Page Templates, based on the page type listed in SPEC.md § Site Map.

Keep the existing YAML frontmatter (`title` and `description`). Replace only the `"Content coming soon."` body.

### Content rules

- **Accuracy over prose.** Every config value, field name, CLI flag, default, and behavior must match the source code exactly. If the source says `capacity: 5` and `refill_rate: 90`, write those exact values.
- **Use Mintlify components.** Every page must use at least one component beyond basic markdown. See `AGENTS.md` § Mintlify Reference for correct syntax. Use:
  - `Columns` + `Card` for "Next steps" navigation and feature overviews
  - `Tabs` for showing alternatives (CLI vs Discord, interactive vs background, etc.)
  - `Steps` for tutorials and setup procedures
  - `AccordionGroup` + `Accordion` for FAQ and expandable details
  - `Note`, `Tip`, `Warning`, `Info` for callouts
- **"Next steps" section** on every page — use `Columns` with `Card` components linking to 2-4 related pages.
- **Code examples** — use real YAML frontmatter, real CLI commands, real env var names from the source. No placeholder values like `your-token-here` or `<your-value>`.
- **Cross-links** — reference other docs pages by their path (e.g., `/getting-started/quickstart`).
- **Tables** for reference data — env vars, config fields, slash command flags.

### What NOT to do

- Do not invent features, config options, or behaviors not present in the source code.
- Do not add sections beyond what the template calls for.
- Do not use emojis.
- Do not write filler prose. Match the information density of technical documentation.
- Do not leave any placeholder text (`TODO`, `TBD`, `Content coming soon.`, `your-X-here`).

### Special case: design-philosophy page

For `getting-started/design-philosophy.mdx`, adapt `literal:../ollim-bot/docs/design-philosophy.md` to the Mintlify template format. Preserve the original voice and substance — restructure for the template, do not rewrite.

---

## Phase 4 — Validate

Before committing, verify:

1. The page does **not** contain `"Content coming soon."`.
2. All Mintlify components use correct syntax (check against `AGENTS.md` § Mintlify Reference).
3. All referenced env vars, CLI commands, config fields, and defaults exist in the source.
4. The page has a "Next steps" section with `Columns`/`Card` components.
5. The page follows the correct template for its page type.

---

## Phase 5 — Commit

Stage **only** the single `.mdx` file you wrote:

```bash
git add <path-to-file>
git commit -m "docs(<section>): write <page-title> page"
```

Example: `git commit -m "docs(getting-started): write quickstart page"`

Do not stage other files. Do not amend previous commits.

---

## Guardrails

999. **ONE page per invocation.** Never write multiple pages. After committing, stop.
998. **NEVER fabricate.** If the source code does not confirm a behavior, do not document it.
997. **NEVER leave placeholder text** in a page you touched.
996. **NEVER skip Phase 2.** Every page requires reading the mapped source files.
995. **Preserve voice** on the design-philosophy page — adapt structure, not substance.
994. **Commit message format** must be `docs(<section>): write <title> page` — nothing else.
