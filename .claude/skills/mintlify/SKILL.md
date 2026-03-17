---
name: mintlify
description: Build and maintain Mintlify documentation sites. Use when creating or editing MDX pages, configuring docs.json, choosing components, setting up navigation, or documenting APIs.
argument-hint: [task or page topic]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Mintlify Documentation

Build and maintain documentation sites with Mintlify. MDX files with YAML frontmatter become documentation pages; `docs.json` configures everything site-wide.

**Fetch current Mintlify docs when using unfamiliar components, configuration options, or features** — Mintlify evolves and training data may be stale. Start by fetching the [documentation index](https://www.mintlify.com/docs/llms.txt) to discover available pages, then fetch specific pages as needed. For routine edits to existing pages (typos, wording, adding a paragraph), fetching is unnecessary. Full `docs.json` schema at [mintlify.com/docs.json](https://mintlify.com/docs.json).

## Priority when rules conflict

1. **Don't break existing pages** — a broken build or missing navigation entry affects the live site
2. **Match the existing site's patterns** — a second convention creates permanent inconsistency that's expensive to unify later, while deferring a style improvement only delays a benefit
3. **Follow this skill's conventions** — these are Mintlify best practices, but the site's established voice wins over generic standards
4. **Apply general writing best practices**

## ollim-bot conventions

- Verify behavior against `~/ollim-bot/src/ollim_bot/` before documenting — trust code over docstrings
- Path references use `~/.ollim-bot/` with a one-line `~` explainer per page — no platform tables or OS tabs
- One authoritative page per behavior — other pages summarize and link, never add new claims
- Use project terminology: background fork, interactive fork, ping budget, routine, main session, context compaction

## Workflow

Each step produces a **named output** — state it in your response before moving on. Later steps consume earlier outputs, so do not skip ahead.

### 1. Understand the project

Read `docs.json` in the project root first. It defines navigation structure, theme, colors, links, API specs, and all site-wide settings.

**Output → navigation context**: what pages exist, how they're organized, what navigation groups and patterns are used, what theme the site uses.

### 2. Check for existing content

Search the docs before creating new pages — creating a new page when content already exists causes duplication and navigation confusion, and merging duplicate pages later is costly while adding a section to an existing page is trivial. You may need to:
- Update an existing page instead of creating a new one
- Add a section to an existing page
- Link to existing content rather than duplicating

If the user requests a new page that substantially overlaps with existing content, flag the overlap and suggest updating the existing page instead.

**Output → overlap assessment**: whether to create a new page or update an existing one, and why.

### 3. Define audience

Before writing, define who this page is for. Each page targets one specific persona — writing for multiple audiences leads to compromises that satisfy no one.

State:
- **Who** is reading this page?
- **What** are they trying to accomplish?
- **Prior knowledge** — what do they already know?

For ollim-bot: both humans and agents read these docs. Structure for both — humans scan headings and cards, agents parse tables, code blocks, and explicit parameter lists. Both benefit from consistent patterns. The human audience is mainly non-technical; avoid jargon.

**Output → audience statement**: one sentence naming the persona, their goal, and their knowledge level.

### 4. Read surrounding pages

Read 2-3 similar pages to understand the site's voice, structure, formatting conventions, and level of detail. Match the existing style — even when it diverges from this skill's conventions (see priority ordering above).

**Output → style notes**: voice, formatting patterns, detail level, and component usage observed in neighbor pages.

### 5. Assign content type

Classify the page into exactly one content type. Do not mix types on a single page — a tutorial that detours into reference material loses the reader.

| Type | Orientation | Structural template |
|------|-------------|-------------------|
| **How-to guide** | Task-oriented | Title starts with a verb. Description: "[Do X] to [achieve Y]". Prerequisites section. Action-oriented headings. Optional: verification section, troubleshooting ("Problem → Solution"). |
| **Tutorial** | Learning-oriented | Title: "[Verb] [specific outcome]". Description: "Learn how to [outcome] by [method]". Intro with expected learnings. Prerequisites with time commitment. Sequential steps with milestones. Next steps. |
| **Explanation** | Understanding-oriented | Title: "About [concept]". Description: "Understand [concept] and how it works within [context]". Plain-language definition. "How [concept] works" section. "Why [approach]" with trade-offs. "When to use [concept]" with scenarios. |
| **Reference** | Information-oriented | Title: "[Feature] reference". One-sentence opener. Properties with type, required status, descriptions. Basic and advanced examples. For APIs: response structure. |

Most early-stage docs are how-to guides or reference pages.

**Output → content type + template**: the chosen type and which structural elements from the template apply to this page.

### 6. Choose components

When using components you haven't used recently in this session, fetch the [components overview](https://mintlify.com/docs/components) to verify current syntax. Common decision points:

| Need | Use |
|------|-----|
| Hide optional details | `<Accordion>` |
| Long code examples | `<Expandable>` |
| User chooses one option | `<Tabs>` |
| Linked navigation cards | `<Card>` in `<Columns>` |
| Sequential instructions | `<Steps>` |
| Code in multiple languages | `<CodeGroup>` |
| API parameters | `<ParamField>` |
| API response fields | `<ResponseField>` |

**Callouts by severity:**

| Component | Use for |
|-----------|---------|
| `<Note>` | Supplementary info, safe to skip |
| `<Info>` | Helpful context such as permissions |
| `<Tip>` | Recommendations or best practices |
| `<Warning>` | Potentially destructive actions |
| `<Check>` | Success confirmation |

### 7. Write or edit content

Determine the task type, then execute the matching action:

- **New page** → Write the page from scratch using the **audience statement**, **style notes**, and **content type template** from earlier steps.
- **New section on existing page** → Edit the existing file to add the section. Re-read the file after editing to confirm the change is in place.
- **Review / fix existing page** → Edit the existing file to apply fixes. Every fix must be applied with `Edit` — do not just report violations without changing the file. Re-read after editing to confirm changes landed. Then produce a summary of what was changed and why.

**Frontmatter** — every page requires `title`. Include `description` for SEO and navigation. Keep titles under 60 characters and descriptions under 160 characters for search engine display:

```yaml
---
title: "Clear, descriptive title"
description: "Concise summary for SEO and navigation."
---
```

Optional frontmatter: `sidebarTitle`, `icon`, `tag`, `mode` (`default`, `wide`, `custom`), `keywords`.

**File conventions:**
- Match existing naming patterns; default to kebab-case: `getting-started.mdx`
- Root-relative paths without file extensions for internal links: `/getting-started/quickstart` — because Mintlify resolves these paths internally, and relative paths (`../`) break when pages move
- Never use relative paths (`../`) or absolute URLs for internal pages
- Link to page sections with anchor links: headings auto-generate anchors (lowercase, spaces to hyphens, special characters removed — e.g., `## API Authentication` → `#api-authentication`). Cross-page: `/page-path#heading-anchor`.
- Store images in `/images`, reference as `/images/example.png`

**Hard requirements** (Mintlify will break or degrade without these):
- All code blocks must have language tags — Mintlify uses them for syntax highlighting and the copy button
- Every MDX file must have `title` in frontmatter
- New pages must be added to `docs.json` navigation to appear in the sidebar
- Headings must follow sequential order — one H1 per page (from `title` frontmatter), then H2, H3 in order without skipping levels. Headings at the same level must have unique names.

**Writing standards:**
- Second-person voice ("you"), active voice, direct language
- Imperative for instructions: "Create a file", not "A file should be created"
- Sentence case for headings ("Getting started", not "Getting Started")
- Lead with context: explain what something is before how to use it
- Prerequisites at the start of procedural content
- Descriptive alt text on all images — be specific about what the image shows (1-2 sentences), don't start with "Image of" (screen readers already announce it). Include "Screenshot of" or "Diagram of" when that context matters.
- Descriptive link text — `[configure authentication](/auth)`, not `[click here](/auth)` or `[learn more](/auth)`. Link text should make sense out of context.
- Text context around code blocks — describe what the code does before the block so screen readers and skimmers can follow
- Media is supplementary — never rely on images alone to convey information. If a workflow is clear in text, skip the screenshot. Every image is maintenance debt when the UI changes.
- Consistent terminology — pick one term for each concept and use it across all pages. Check the CLAUDE.md terminology table.
- Scannability — use headings for orientation, keep paragraphs short, use lists where appropriate

**Avoid** (these degrade documentation quality regardless of context):
- Marketing language ("powerful", "seamless", "robust") — erodes reader trust, adds no information
- Filler phrases ("in order to", "it's important to note") — wastes reader attention
- Editorializing ("obviously", "simply", "just", "easily") — dismisses reader difficulty
- Colloquialisms or informal expressions — harms clarity, especially if docs are localized
- Product-centric jargon — use language users are familiar with, not internal terminology
- Spelling and grammar errors — makes docs less credible and harder to read

**Code examples:**
- Keep examples simple and practical with realistic values (not "foo" or "bar")
- One clear example is better than multiple variations
- Test that code works before including it

### 8. Choose navigation pattern

The `navigation` property in `docs.json` controls site structure. Match the existing pattern, or choose one when building from scratch:

| Pattern | When to use |
|---------|-------------|
| **Groups** | Default. Single audience, straightforward hierarchy |
| **Tabs** | Distinct sections with different audiences or content types |
| **Anchors** | Persistent section links at sidebar top; good for external resources |
| **Dropdowns** | Multiple doc sections users switch between, not distinct enough for tabs |
| **Products** | Multi-product company with separate docs per product |
| **Versions** | Multiple API/product versions simultaneously |
| **Languages** | Localized content |

**Within your primary pattern:**
- **Groups** — organize related pages; can nest but keep hierarchy shallow
- **Menus** — dropdown navigation within tabs for quick jumps
- **`expanded: false`** — collapse nested groups by default for reference sections
- **`openapi`** — auto-generate pages from OpenAPI spec at group/tab level

### 9. Document APIs (if applicable)

Choose based on what exists:
- **Have an OpenAPI spec?** Add to `docs.json` with `"openapi": ["openapi.yaml"]`. Pages auto-generate. Reference in navigation as `GET /endpoint`. This is the most efficient and easiest to maintain.
- **No spec?** Write endpoints manually with `api: "POST /users"` in frontmatter. More work but full control.
- **Hybrid** — OpenAPI for most endpoints, manual pages for complex workflows.

### 10. Update navigation

When you create a new page, add it to the appropriate group in `docs.json` — pages not in navigation won't appear in the sidebar. Hidden pages (accessible by URL but not in sidebar) are intentionally omitted from navigation.

### 11. Customize appearance (if needed)

**Where to customize what:**
- **Brand colors, fonts, logo** → `docs.json` — see [global settings](https://mintlify.com/docs/settings/global)
- **Component styling, layout tweaks** → `custom.css` at project root
- **Dark mode** → enabled by default; only disable with `"appearance": "light"` if brand requires it
- **Redirects** → `"redirects": [{"source": "/old", "destination": "/new"}]` in `docs.json`

Start with `docs.json`. Only add `custom.css` when config doesn't support the styling you need — because custom CSS creates a maintenance burden that scales with Mintlify updates.

### 12. Verify

Run through before submitting. Fix any failures and re-verify. If issues persist after two fix attempts, stop and report the remaining failures to the user.

**Which passes to run** — tier by task size:

| Task | Passes |
|------|--------|
| **Quick edit** (typo, wording, adding a paragraph) | Pass 1 only |
| **New section** (adding a section to an existing page) | Passes 1–3 |
| **New page** (creating a new page from scratch) | All 6 passes |

#### Pass 1: Structural (must-pass — blocks publishing)

- [ ] Frontmatter includes `title` and `description`
- [ ] Description is 10–30 words, action-oriented
- [ ] All code blocks have language tags
- [ ] Internal links use root-relative paths without file extensions
- [ ] New pages are added to `docs.json` navigation
- [ ] Headings are sequential (no skipped levels) with unique names at each level
- [ ] No TODOs left unmarked
- [ ] `mint broken-links` passes
- [ ] `mint validate` passes

#### Pass 2: Content type compliance

Using the **content type + template** from step 5:

- [ ] Page follows one content type — no mixing
- [ ] Title matches the type's format (verb for how-to, "About X" for explanation, etc.)
- [ ] Description matches the type's format
- [ ] All required structural sections from the template are present
- [ ] No structural sections from a different type bleed in

Flag: missing required sections, wrong title format, type mixing.

#### Pass 3: Style and tone

- [ ] Second-person voice ("you"), active voice throughout
- [ ] Imperative for instructions ("Create", not "You should create")
- [ ] No marketing language ("powerful", "seamless", "robust")
- [ ] No filler phrases ("in order to", "it's important to note", "it should be noted")
- [ ] No editorializing ("obviously", "simply", "just", "easily")
- [ ] No colloquialisms or informal expressions
- [ ] No product-centric jargon — uses language the audience knows
- [ ] Terminology matches CLAUDE.md terminology table (background fork, not bg fork; routine, not scheduled task; etc.)
- [ ] Scannable — headings break up content, paragraphs are short, lists used where appropriate
- [ ] Spelling and grammar are correct
- [ ] Matches the voice and detail level from the **style notes** (step 4)

#### Pass 4: Audience and scope

- [ ] Page targets the one audience from the **audience statement** (step 3)
- [ ] Content matches that audience's prior knowledge — not too advanced, not too basic
- [ ] Not over-documented — excessive edge cases reduce navigability. Prioritize evergreen content.
- [ ] No time-specific references that will go stale (use changelogs for that)
- [ ] For ollim-bot: dual-audience structure works for both humans (scannable headings, cards) and agents (tables, code blocks, explicit parameters)

#### Pass 5: Accessibility

Skip individual checks that don't apply (no images → skip alt text). But do not skip the entire pass.

- [ ] Images: alt text is specific (1-2 sentences), doesn't start with "Image of", includes "Screenshot of"/"Diagram of" when relevant
- [ ] Tables: have headers, contain genuine tabular data (not used for layout)
- [ ] Embeds: iframes and video embeds have descriptive `title` attributes
- [ ] Video (if any): captions synchronized, speaker ID for multiple speakers, transcript provided as searchable text
- [ ] Links: descriptive text that makes sense out of context — no "click here", "read more", bare URLs
- [ ] Code blocks: text context before each block describing what the code does
- [ ] Color: information not conveyed by color alone

#### Pass 6: Maintenance signals

- [ ] Technical claims verified against source code at `~/ollim-bot/src/ollim_bot/`
- [ ] No references to features that may have changed without verification
- [ ] If editing an existing page: check `git log` for last modification date — flag if unmodified 3+ months as potentially stale
- [ ] Prefer removing inaccurate content over keeping it — wrong docs are worse than missing docs
- [ ] If page has accumulated incremental fixes that make it incoherent, flag for full rewrite rather than patching further

**Report format**: for each pass, state pass/fail with specific findings. Classify findings as **must-fix** (blocks publishing), **should-fix** (degrades quality), or **note** (minor improvement). Fix all must-fix items before submitting.

## Reusable content (snippets)

**When to use snippets:**
- Exact content appears on more than one page
- Complex components you want to maintain in one place

**When NOT to use snippets:**
- Slight variations needed per page — leads to complex props

Import snippets with `import { Component } from "/path/to/snippet-name.jsx"`.

## Deploy

Mintlify deploys automatically when changes are pushed to the connected Git repository.

**What agents can configure:**
- Redirects in `docs.json`
- SEO indexing: `"seo": {"indexing": "all"}` to include hidden pages in search

**Requires dashboard setup (human task):**
- Custom domains and subdomains
- Preview deployment settings
- DNS configuration

## CLI reference

| Command | Purpose |
|---------|---------|
| `npm i -g mint` | Install the Mintlify CLI |
| `mint dev` | Local preview at localhost:3000 |
| `mint broken-links` | Check internal links |
| `mint a11y` | Check accessibility issues |
| `mint a11y --skip-contrast` | Check alt text only |
| `mint a11y --skip-alt-text` | Check contrast only |
| `mint rename` | Rename/move files and update references |
| `mint validate` | Validate documentation builds |

## Gotchas

1. **Never use `mint.json`** — it is deprecated. Only use `docs.json`.
2. **JSX components need explicit import** — MDX components (Mintlify built-ins) don't need imports; JSX components from snippets do.
3. **Frontmatter required** — every MDX file needs `title` at minimum.
4. **Code block language required** — always specify the language identifier.
5. **New pages must be in `docs.json`** — a page that isn't in the navigation array won't appear in the sidebar.
6. **Root-relative paths only** — use `/section/page`, never `../page` or `https://yourdomain.com/section/page` for internal links.

## Migrations

If migrating to Mintlify from ReadMe or Docusaurus, use the [@mintlify/scraping](https://www.npmjs.com/package/@mintlify/scraping) CLI. For other platforms, manually convert content to MDX pages.

## When to ask for clarification

**Ask when:**
- The task affects navigation structure and the intent is ambiguous
- Multiple navigation patterns could work and the tradeoffs matter
- The page topic overlaps with existing content and it's unclear whether to update or create

**Push back when:**
- The user requests content that duplicates an existing page — suggest updating instead
- The user asks for marketing language or promotional tone — explain why it degrades reader trust
- The request would break site navigation or leave orphaned pages
- Content is visibly outdated or inaccurate — wrong docs are worse than missing docs because they waste reader time and erode trust. Flag it and suggest updating or removing.
- Incremental patches have made a page incoherent — suggest a full rewrite instead of further patching

**Don't ask when:**
- The navigation pattern is already established in `docs.json` — match it
- The task is clearly a new page in an existing section
- The question is about component choice or formatting — proceed with reasonable defaults

ultrathink
