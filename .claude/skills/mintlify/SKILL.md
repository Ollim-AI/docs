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

### 1. Understand the project

Read `docs.json` in the project root first. It defines navigation structure, theme, colors, links, API specs, and all site-wide settings.

Understanding `docs.json` tells you:
- What pages exist and how they're organized
- What navigation groups and patterns are used
- What theme and configuration the site uses

### 2. Check for existing content

Search the docs before creating new pages — because creating a new page when content already exists causes duplication and navigation confusion, and merging duplicate pages later is costly while adding a section to an existing page is trivial. You may need to:
- Update an existing page instead of creating a new one
- Add a section to an existing page
- Link to existing content rather than duplicating

If the user requests a new page that substantially overlaps with existing content, flag the overlap and suggest updating the existing page instead.

### 3. Read surrounding pages

Before writing, read 2-3 similar pages to understand the site's voice, structure, formatting conventions, and level of detail. Match the existing style — even when it diverges from this skill's conventions (see priority ordering above).

### 4. Choose components

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

### 5. Write content

Identify the page's content type — this shapes the writing approach:
- **Tutorial**: Learning-oriented, step-by-step, assumes no prior knowledge. Focus on concrete actions, minimize choices.
- **How-to guide**: Task-oriented, assumes some knowledge. Get straight to the solution, omit unnecessary context.
- **Reference**: Information-oriented, scannable, concise. Prioritize consistency and copy-pasteable examples.
- **Explanation**: Understanding-oriented, provides context and rationale. Draw connections, acknowledge alternatives.

Most early-stage docs are how-to guides or reference pages. Don't mix types on a single page — a tutorial that detours into reference material loses the reader.

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

**Defaults** (follow unless the existing site establishes a different pattern):
- Second-person voice ("you"), active voice, direct language
- Sentence case for headings ("Getting started", not "Getting Started")
- Lead with context: explain what something is before how to use it
- Prerequisites at the start of procedural content
- Descriptive alt text on all images — be specific about what the image shows (1-2 sentences), don't start with "Image of" (screen readers already announce it). Include "Screenshot of" or "Diagram of" when that context matters.
- Descriptive link text — `[configure authentication](/auth)`, not `[click here](/auth)` or `[learn more](/auth)`. Link text should make sense out of context.
- Text context around code blocks — describe what the code does before the block so screen readers and skimmers can follow
- Media is supplementary — never rely on images alone to convey information. If a workflow is clear in text, skip the screenshot. Every image is maintenance debt when the UI changes.
- Consistent terminology — pick one term for each concept and use it across all pages

**Avoid** (these degrade documentation quality regardless of context):
- Marketing language ("powerful", "seamless", "robust") — because it erodes reader trust and adds no information
- Filler phrases ("in order to", "it's important to note") — because they waste reader attention
- Editorializing ("obviously", "simply", "just", "easily") — because they dismiss reader difficulty

**Code examples:**
- Keep examples simple and practical with realistic values (not "foo" or "bar")
- One clear example is better than multiple variations
- Test that code works before including it

### 6. Choose navigation pattern

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

### 7. Document APIs (if applicable)

Choose based on what exists:
- **Have an OpenAPI spec?** Add to `docs.json` with `"openapi": ["openapi.yaml"]`. Pages auto-generate. Reference in navigation as `GET /endpoint`. This is the most efficient and easiest to maintain.
- **No spec?** Write endpoints manually with `api: "POST /users"` in frontmatter. More work but full control.
- **Hybrid** — OpenAPI for most endpoints, manual pages for complex workflows.

### 8. Update navigation

When you create a new page, add it to the appropriate group in `docs.json` — pages not in navigation won't appear in the sidebar. Hidden pages (accessible by URL but not in sidebar) are intentionally omitted from navigation.

### 9. Customize appearance (if needed)

**Where to customize what:**
- **Brand colors, fonts, logo** → `docs.json` — see [global settings](https://mintlify.com/docs/settings/global)
- **Component styling, layout tweaks** → `custom.css` at project root
- **Dark mode** → enabled by default; only disable with `"appearance": "light"` if brand requires it
- **Redirects** → `"redirects": [{"source": "/old", "destination": "/new"}]` in `docs.json`

Start with `docs.json`. Only add `custom.css` when config doesn't support the styling you need — because custom CSS creates a maintenance burden that scales with Mintlify updates.

### 10. Verify

Run through before submitting. Fix any failures and re-verify. If issues persist after two fix attempts, stop and report the remaining failures to the user.

**Structural checks** (every page):
- [ ] Frontmatter includes `title` and `description`
- [ ] All code blocks have language tags
- [ ] Internal links use root-relative paths without file extensions
- [ ] New pages are added to `docs.json` navigation
- [ ] Headings are sequential (no skipped levels) with unique names at each level
- [ ] TODOs are clearly marked for anything uncertain
- [ ] `mint broken-links` passes
- [ ] `mint validate` passes

**Content quality analysis** — read `page-review-checklist.md` and run the sections relevant to the page. Skip sections that don't apply (e.g., skip media checks if no images, skip video checks if no embeds). Key areas:
- [ ] Accessibility: alt text, table headers, embeds, color contrast, code block context
- [ ] Content type structure: page follows the structural expectations for its type (how-to, tutorial, explanation, reference)
- [ ] Style & tone: consistent terminology, single audience, no marketing language or filler, user-facing language
- [ ] Linking: no circular links, descriptive link text
- [ ] SEO: title/description length, keywords in headings and alt text
- [ ] Media: supplementary only, appropriate type for the content
- [ ] Content matches the style of surrounding pages

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

**Don't ask when:**
- The navigation pattern is already established in `docs.json` — match it
- The task is clearly a new page in an existing section
- The question is about component choice or formatting — proceed with reasonable defaults
