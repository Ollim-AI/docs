# Page review checklist

Deep analysis rules for reviewing Mintlify documentation pages. Organized into two scopes:

- **Page-local checks** — can be evaluated from a single page in isolation. Used by per-page review agents.
- **Cross-page checks** — require reading multiple pages to detect. Used by cross-cutting review agents.

Skip sections that don't apply (e.g., skip media checks if the page has no images or videos). Each rule is sourced from Mintlify's official guides.

---

# Page-local checks

## Accessibility (guides/accessibility)

**Images**
- All images have alt text: specific about what the image shows, 1–2 sentences
- Alt text does not start with "Image of" — screen readers already announce it as an image
- Include "Screenshot of" or "Diagram of" when that context matters

**Tables**
- Tables have headers so screen readers can associate data with columns
- Tables contain genuine tabular data with meaning inherited from headers — not used for layout

**Embeds**
- All iframes and video embeds have descriptive `title` attributes

**Video**
- Captions synchronized with audio
- Speaker identification for multiple speakers
- Transcripts provided as searchable text near the video
- If critical information appears only in video, equivalent text or written tutorial is provided

**Color**
- Body text: minimum 4.5:1 contrast ratio
- Large text: minimum 3:1 contrast ratio
- Interactive elements: minimum 3:1 contrast ratio
- Test in both light and dark modes
- Information is not conveyed by color alone — text labels or icons accompany color coding

**Code blocks**
- Long examples broken into smaller logical chunks
- Comments added for complex logic
- Text context before the code block describing what the code does

**Links**
- Link text is descriptive and makes sense out of context
- No "click here", "read more", "learn more", or bare URLs

**Headings**
- One H1 per page (from `title` frontmatter)
- Sequential order without skipping levels
- Unique names at the same hierarchy level

## Content type structure (guides/content-templates)

Identify the page's content type, then check against its structural expectations. Don't mix types on a single page.

**How-to guide**
- Title starts with a verb
- Description format: "[Do task] to [achieve outcome]"
- Prerequisites section listing only necessary items (setup, permissions, related features)
- Action-oriented headings describing the task
- If success is ambiguous: verification section explaining how to confirm it worked
- Optional: troubleshooting with "Problem: Solution" format
- Omit unnecessary context — get straight to the solution

**Tutorial**
- Title format: "[Action verb] [specific outcome]"
- Description: "Learn how to [outcome] by [method/approach]"
- Introduction explaining expected learnings and post-completion capabilities
- Prerequisites including time commitment
- Steps build sequentially with concrete actions
- Minimize decision points for the user
- Milestones showing progress throughout
- Next steps suggesting related tutorials, how-to guides, deeper resources

**Explanation**
- Title format: "About [concept or feature]"
- Description: "Understand [concept] and how it works within [context]"
- Plain-language definition of what it is, what it does, why it exists
- Section "How [concept] works"
- Section "Why [decision/approach]" discussing trade-offs
- Section "When to use [concept]" with specific scenarios
- Address common misconceptions
- Draw connections to related concepts

**Reference**
- Title format: "[Feature or API name] reference"
- Description: "Complete reference for [feature/API] properties, parameters, options"
- One-sentence opener describing what the feature/API does
- Properties with type, required status, brief descriptions
- Both basic and advanced usage examples
- For APIs: response structure with field names, types, descriptions

## Style & tone — page-scoped (guides/style-and-tone, guides/understand-your-audience)

**Voice**
- Second-person ("you"), active voice, direct language
- Imperative statements for instructions ("Create a file", not "A file should be created")

**Audience**
- Each page targets one specific audience — "writing for multiple audiences leads to compromises that satisfy no one"
- Define the reader before writing: what are they trying to accomplish? What's their prior knowledge?

**Scope**
- Don't document every edge case — excessive content reduces navigability
- Prioritize evergreen documentation; use changelogs for frequently changing content

**Avoid**
- Marketing language ("powerful", "seamless", "robust") — erodes trust, adds no information
- Filler phrases ("in order to", "it's important to note") — wastes attention
- Editorializing ("obviously", "simply", "just", "easily") — dismisses difficulty
- Spelling and grammar errors — "make it less credible and harder to read"
- Product-centric language — use language users are familiar with, not internal product terminology
- Colloquialisms or informal expressions

## Prose quality (revise anti-patterns)

Test each sentence: could it describe a different product with no changes? If yes, it carries no specific information. Flag it.

**Content — does every sentence carry specific information?**
- **1a. Significance inflation** — sentence claims importance without stating the specific impact. The language sounds meaningful but swaps in for any subject.
- **1b. Superficial analysis** — sentence ends with an "-ing" clause that editorializes rather than analyzes. If the analysis is real, it should be a specific claim.
- **1c. Promotional tone** — sentence describes how impressive something is rather than what it does. Emphasis words that add feeling but not fact.
- **1d. Vague attribution** — claim attributed to unnamed sources. Name the source or cut the claim.
- **1e. Challenge-and-prospect** — paragraph sets up a positive, introduces challenges, ends with vague optimism. No specific resolution.
- **1f. Gap speculation** — text discusses why information is absent rather than providing information. Silence is better than meta-commentary about gaps.

**Language — is the language plain and direct?**
- **2a. Copula avoidance** — complex verb phrase where "is" or "has" would work. The simplest verb is usually the right one.
- **2b. Elegant variation** — forced synonyms cycling to avoid repeating a word. Repetition is natural; variation that obscures is not.
- **2e. Inflating vocabulary** — words that add importance without adding meaning. One in a long text is fine; clusters are the problem. Test: does this word add meaning a plainer word wouldn't?

**Structure — does formatting serve the content?**
- **3a. Em dashes** — count them. One or two per page is fine. Five or more means overuse; most should be commas, parentheses, or colons.
- **3d. Section summaries** — sentence at the end of a section restating what was just said. The reader just read it.
- **3e. Didactic disclaimers** — sentence that frames a fact as important rather than stating the fact. The framing adds no information.
- **3g. Inline-header lists** — bold-term-colon-description format used mechanically. Only appropriate for genuinely parallel definitions.

## Linking — page-scoped (guides/linking)

- Internal links use root-relative paths without file extensions
- Related content linked naturally within context where valuable

## Media (guides/media)

- Media is supplementary — never the sole source of information
- Use sparingly and intentionally to avoid documentation debt
- Screenshots: when tasks are "difficult to explain with words"
- GIFs: for short, complex workflows
- Videos: for abstract concepts and lengthy workflows
- Evaluate whether updating outdated visuals justifies the effort before including media

---

# Cross-page checks

These require reading multiple pages to detect. Cannot be run by per-page agents.

## Terminology consistency (guides/style-and-tone)

- One term per concept across all pages — don't alternate (e.g., "API key" vs "API token")
- User-facing language, not internal product terminology

## Linking — cross-page (guides/linking)

- No circular links between the same pages
- When moving/renaming pages: update navigation config, add redirects, search entire docs for old paths, update all references, verify with `mint broken-links`

## Maintenance (guides/maintenance)

- Flag important docs not updated within three months as potentially stale
- Remove entirely inaccurate pages rather than keeping wrong information available
- Recognize that incremental fixes sometimes create more confusion than clarity, necessitating full rewrites
