# Agents — ollim-bot Documentation

Operational context for documentation authoring. Read this file at the start of every iteration.

## Source Mapping

Each doc page maps to specific source files in `literal:../ollim-bot/`. Read these files (and the relevant sections of `CLAUDE.md` at the repo root) before writing each page.

All source paths are relative to `literal:../ollim-bot/` unless noted otherwise.

### Getting Started

| Page | Source Files |
|------|-------------|
| `getting-started/overview` | `CLAUDE.md` (full file — architecture, features, philosophy) |
| `getting-started/quickstart` | `src/ollim_bot/main.py`, `src/ollim_bot/config.py` |
| `getting-started/setup` | `src/ollim_bot/main.py`, `src/ollim_bot/config.py`, `src/ollim_bot/google/auth.py`, `src/ollim_bot/bot.py` |
| `getting-started/how-it-works` | `src/ollim_bot/agent.py`, `src/ollim_bot/sessions.py`, `src/ollim_bot/forks.py`, `src/ollim_bot/prompts.py` |
| `getting-started/design-philosophy` | `docs/design-philosophy.md` |

### Core Usage

| Page | Source Files |
|------|-------------|
| `core-usage/conversations` | `src/ollim_bot/bot.py`, `src/ollim_bot/agent.py`, `src/ollim_bot/streamer.py`, `src/ollim_bot/sessions.py` |
| `core-usage/slash-commands` | `src/ollim_bot/agent.py`, `src/ollim_bot/bot.py` |
| `core-usage/forks` | `src/ollim_bot/forks.py`, `src/ollim_bot/agent.py`, `src/ollim_bot/views.py` |
| `core-usage/embeds-and-buttons` | `src/ollim_bot/embeds.py`, `src/ollim_bot/agent_tools.py`, `src/ollim_bot/views.py`, `src/ollim_bot/inquiries.py` |
| `core-usage/permissions` | `src/ollim_bot/permissions.py` |

### Scheduling

| Page | Source Files |
|------|-------------|
| `scheduling/overview` | `src/ollim_bot/scheduling/scheduler.py`, `src/ollim_bot/scheduling/preamble.py` |
| `scheduling/routines` | `src/ollim_bot/scheduling/routines.py`, `src/ollim_bot/scheduling/routine_cmd.py` |
| `scheduling/reminders` | `src/ollim_bot/scheduling/reminders.py`, `src/ollim_bot/scheduling/reminder_cmd.py` |
| `scheduling/background-forks` | `src/ollim_bot/forks.py`, `src/ollim_bot/agent_tools.py` |
| `scheduling/ping-budget` | `src/ollim_bot/ping_budget.py`, `src/ollim_bot/agent_tools.py` |

### Integrations

| Page | Source Files |
|------|-------------|
| `integrations/google-overview` | `src/ollim_bot/google/auth.py`, `src/ollim_bot/google/__init__.py` |
| `integrations/google-tasks` | `src/ollim_bot/google/tasks.py` |
| `integrations/google-calendar` | `src/ollim_bot/google/calendar.py` |
| `integrations/google-gmail` | `src/ollim_bot/google/gmail.py`, `src/ollim_bot/subagent_prompts.py` |
| `integrations/webhooks` | `src/ollim_bot/webhook.py` |

### Extending

| Page | Source Files |
|------|-------------|
| `extending/overview` | `src/ollim_bot/agent_tools.py`, `src/ollim_bot/prompts.py`, `CLAUDE.md` |
| `extending/mcp-tools` | `src/ollim_bot/agent_tools.py` |
| `extending/subagents` | `src/ollim_bot/subagent_prompts.py`, `src/ollim_bot/agent.py` |
| `extending/system-prompt` | `src/ollim_bot/prompts.py`, `src/ollim_bot/subagent_prompts.py` |
| `extending/adding-integrations` | `CLAUDE.md`, `src/ollim_bot/google/auth.py`, `src/ollim_bot/agent_tools.py` |

### Configuration

| Page | Source Files |
|------|-------------|
| `configuration/reference` | `src/ollim_bot/config.py`, `src/ollim_bot/storage.py`, `CLAUDE.md` |
| `configuration/data-directory` | `src/ollim_bot/storage.py` |
| `configuration/file-formats` | `src/ollim_bot/scheduling/routines.py`, `src/ollim_bot/scheduling/reminders.py`, `src/ollim_bot/webhook.py`, `src/ollim_bot/sessions.py` |

### Architecture

| Page | Source Files |
|------|-------------|
| `architecture/overview` | `CLAUDE.md` (architecture section — full module map) |
| `architecture/session-management` | `src/ollim_bot/sessions.py`, `src/ollim_bot/agent.py` |
| `architecture/context-flow` | `src/ollim_bot/forks.py`, `src/ollim_bot/prompts.py`, `src/ollim_bot/scheduling/preamble.py` |
| `architecture/streaming` | `src/ollim_bot/streamer.py` |

### Development

| Page | Source Files |
|------|-------------|
| `development/guide` | `CLAUDE.md` (dev commands section), `pyproject.toml` |
| `development/testing` | `tests/` directory (list files and read test examples) |
| `development/cli-reference` | `src/ollim_bot/main.py`, `src/ollim_bot/scheduling/routine_cmd.py`, `src/ollim_bot/scheduling/reminder_cmd.py` |
| `development/troubleshooting` | `src/ollim_bot/sessions.py`, `src/ollim_bot/config.py`, `src/ollim_bot/storage.py` |

### Self-Hosting

| Page | Source Files |
|------|-------------|
| `self-hosting/guide` | `src/ollim_bot/config.py`, `src/ollim_bot/main.py`, `CLAUDE.md` |
| `self-hosting/discord-bot-setup` | `src/ollim_bot/bot.py`, `src/ollim_bot/config.py` |
| `self-hosting/google-oauth-setup` | `src/ollim_bot/google/auth.py` |

### Changelog

| Page | Source Files |
|------|-------------|
| `changelog` | Git log (`git log --oneline` in `literal:../ollim-bot/`) |

---

## Mintlify Reference

Correct component syntax. Use these exactly — do not guess at props or nesting.

### Cards and Columns

```mdx
<Columns cols={2}>
  <Card title="Page title" icon="rocket" href="/getting-started/quickstart">
    Short description of what the linked page covers.
  </Card>
  <Card title="Another page" icon="code" href="/development/guide">
    Short description.
  </Card>
</Columns>
```

Props: `cols` accepts `{2}`, `{3}`, or `{4}`. `Card` accepts `title`, `icon` (Font Awesome name), `href`, and optional `horizontal`.

### Tabs

```mdx
<Tabs>
  <Tab title="CLI">
    Content for CLI usage.
  </Tab>
  <Tab title="Discord">
    Content for Discord usage.
  </Tab>
</Tabs>
```

### Steps

```mdx
<Steps>
  <Step title="Install dependencies">
    ```bash
    uv sync
    ```
  </Step>
  <Step title="Configure environment">
    Copy `.env.example` to `.env` and fill in values.
  </Step>
</Steps>
```

### Accordion

```mdx
<AccordionGroup>
  <Accordion title="Question or topic">
    Answer or expandable content.
  </Accordion>
  <Accordion title="Another question">
    More content.
  </Accordion>
</AccordionGroup>
```

### Callouts

```mdx
<Note>Important context the reader should be aware of.</Note>

<Tip>Best practice or recommendation.</Tip>

<Warning>Gotcha, pitfall, or destructive action warning.</Warning>

<Info>Background context or supplementary information.</Info>
```

### Code Blocks

````mdx
```yaml title="routines/daily-review.md"
---
id: daily-review
cron: "0 9 * * 1-5"
description: Morning task review
---
```

```bash
uv run ollim-bot routine list
```

```python
from ollim_bot.config import OLLIM_USER_NAME
```
````

### Tables

```mdx
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | Yes | — | Discord bot token |
| `OLLIM_USER_NAME` | Yes | — | Your display name |
```

---

## Conventions

Patterns to follow for consistency across all pages.

- Use relative links between docs pages: `/getting-started/quickstart`, not full URLs
- Code blocks specify language: `yaml`, `bash`, `python`, `json`
- YAML examples use realistic values from the source (not `example-value` placeholders)
- Tables use `—` (em dash) for "no default" or "not applicable"
- Each page ends with a "Next steps" section using `Columns` + `Card`
- Callouts (`Note`, `Tip`, `Warning`) are used sparingly — max 3 per page
- Page descriptions in YAML frontmatter are kept as-is (already written in the stubs)
