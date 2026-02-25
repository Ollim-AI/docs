# Documentation Audit Checklist

Status: IN PROGRESS
Pages audited: 38 / 40

## Getting Started

- [x] `getting-started/overview.mdx` — Sources: `CLAUDE.md`
- [x] `getting-started/quickstart.mdx` — Sources: `main.py`, `config.py`
- [x] `getting-started/setup.mdx` — Sources: `main.py`, `config.py`, `google/auth.py`, `bot.py`
- [x] `getting-started/how-it-works.mdx` — Sources: `agent.py`, `sessions.py`, `forks.py`, `prompts.py`
- [x] `getting-started/design-philosophy.mdx` — Sources: `docs/design-philosophy.md`

## Core Usage

- [x] `core-usage/conversations.mdx` — Sources: `bot.py`, `agent.py`, `streamer.py`, `sessions.py`
- [x] `core-usage/slash-commands.mdx` — Sources: `agent.py`, `bot.py`
- [x] `core-usage/forks.mdx` — Sources: `forks.py`, `agent.py`, `views.py`
- [x] `core-usage/embeds-and-buttons.mdx` — Sources: `embeds.py`, `agent_tools.py`, `views.py`, `inquiries.py`
- [x] `core-usage/permissions.mdx` — Sources: `permissions.py`

## Scheduling

- [x] `scheduling/overview.mdx` — Sources: `scheduling/scheduler.py`, `scheduling/preamble.py`
- [x] `scheduling/routines.mdx` — Sources: `scheduling/routines.py`, `scheduling/routine_cmd.py`
- [x] `scheduling/reminders.mdx` — Sources: `scheduling/reminders.py`, `scheduling/reminder_cmd.py`
- [x] `scheduling/background-forks.mdx` — Sources: `forks.py`, `agent_tools.py`
- [x] `scheduling/ping-budget.mdx` — Sources: `ping_budget.py`, `agent_tools.py`

## Integrations

- [x] `integrations/google-overview.mdx` — Sources: `google/auth.py`, `google/__init__.py`
- [x] `integrations/google-tasks.mdx` — Sources: `google/tasks.py`
- [x] `integrations/google-calendar.mdx` — Sources: `google/calendar.py`
- [x] `integrations/google-gmail.mdx` — Sources: `google/gmail.py`, `subagent_prompts.py`
- [x] `integrations/webhooks.mdx` — Sources: `webhook.py`

## Extending

- [x] `extending/overview.mdx` — Sources: `agent_tools.py`, `prompts.py`, `CLAUDE.md`
- [x] `extending/mcp-tools.mdx` — Sources: `agent_tools.py`
- [x] `extending/subagents.mdx` — Sources: `subagent_prompts.py`, `agent.py`
- [x] `extending/system-prompt.mdx` — Sources: `prompts.py`, `subagent_prompts.py`
- [x] `extending/adding-integrations.mdx` — Sources: `CLAUDE.md`, `google/auth.py`, `agent_tools.py`

## Configuration

- [x] `configuration/reference.mdx` — Sources: `config.py`, `storage.py`, `CLAUDE.md`
- [x] `configuration/data-directory.mdx` — Sources: `storage.py`
- [x] `configuration/file-formats.mdx` — Sources: `scheduling/routines.py`, `scheduling/reminders.py`, `webhook.py`, `sessions.py`

## Architecture

- [x] `architecture/overview.mdx` — Sources: `CLAUDE.md`
- [x] `architecture/session-management.mdx` — Sources: `sessions.py`, `agent.py`
- [x] `architecture/context-flow.mdx` — Sources: `forks.py`, `prompts.py`, `scheduling/preamble.py`
- [x] `architecture/streaming.mdx` — Sources: `streamer.py`

## Development

- [x] `development/guide.mdx` — Sources: `CLAUDE.md`, `pyproject.toml`
- [x] `development/testing.mdx` — Sources: `tests/` directory
- [x] `development/cli-reference.mdx` — Sources: `main.py`, `scheduling/routine_cmd.py`, `scheduling/reminder_cmd.py`
- [x] `development/troubleshooting.mdx` — Sources: `sessions.py`, `config.py`, `storage.py`

## Self-Hosting

- [x] `self-hosting/guide.mdx` — Sources: `config.py`, `main.py`, `CLAUDE.md`
- [x] `self-hosting/discord-bot-setup.mdx` — Sources: `bot.py`, `config.py`
- [ ] `self-hosting/google-oauth-setup.mdx` — Sources: `google/auth.py`

## Changelog

- [ ] `changelog.mdx` — Sources: git log
