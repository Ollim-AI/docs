# Documentation Audit Checklist

Status: IN PROGRESS
Pages audited: 1 / 40

## Getting Started

- [x] `getting-started/overview.mdx` — Sources: `CLAUDE.md`
- [ ] `getting-started/quickstart.mdx` — Sources: `main.py`, `config.py`
- [ ] `getting-started/setup.mdx` — Sources: `main.py`, `config.py`, `google/auth.py`, `bot.py`
- [ ] `getting-started/how-it-works.mdx` — Sources: `agent.py`, `sessions.py`, `forks.py`, `prompts.py`
- [ ] `getting-started/design-philosophy.mdx` — Sources: `docs/design-philosophy.md`

## Core Usage

- [ ] `core-usage/conversations.mdx` — Sources: `bot.py`, `agent.py`, `streamer.py`, `sessions.py`
- [ ] `core-usage/slash-commands.mdx` — Sources: `agent.py`, `bot.py`
- [ ] `core-usage/forks.mdx` — Sources: `forks.py`, `agent.py`, `views.py`
- [ ] `core-usage/embeds-and-buttons.mdx` — Sources: `embeds.py`, `agent_tools.py`, `views.py`, `inquiries.py`
- [ ] `core-usage/permissions.mdx` — Sources: `permissions.py`

## Scheduling

- [ ] `scheduling/overview.mdx` — Sources: `scheduling/scheduler.py`, `scheduling/preamble.py`
- [ ] `scheduling/routines.mdx` — Sources: `scheduling/routines.py`, `scheduling/routine_cmd.py`
- [ ] `scheduling/reminders.mdx` — Sources: `scheduling/reminders.py`, `scheduling/reminder_cmd.py`
- [ ] `scheduling/background-forks.mdx` — Sources: `forks.py`, `agent_tools.py`
- [ ] `scheduling/ping-budget.mdx` — Sources: `ping_budget.py`, `agent_tools.py`

## Integrations

- [ ] `integrations/google-overview.mdx` — Sources: `google/auth.py`, `google/__init__.py`
- [ ] `integrations/google-tasks.mdx` — Sources: `google/tasks.py`
- [ ] `integrations/google-calendar.mdx` — Sources: `google/calendar.py`
- [ ] `integrations/google-gmail.mdx` — Sources: `google/gmail.py`, `subagent_prompts.py`
- [ ] `integrations/webhooks.mdx` — Sources: `webhook.py`

## Extending

- [ ] `extending/overview.mdx` — Sources: `agent_tools.py`, `prompts.py`, `CLAUDE.md`
- [ ] `extending/mcp-tools.mdx` — Sources: `agent_tools.py`
- [ ] `extending/subagents.mdx` — Sources: `subagent_prompts.py`, `agent.py`
- [ ] `extending/system-prompt.mdx` — Sources: `prompts.py`, `subagent_prompts.py`
- [ ] `extending/adding-integrations.mdx` — Sources: `CLAUDE.md`, `google/auth.py`, `agent_tools.py`

## Configuration

- [ ] `configuration/reference.mdx` — Sources: `config.py`, `storage.py`, `CLAUDE.md`
- [ ] `configuration/data-directory.mdx` — Sources: `storage.py`
- [ ] `configuration/file-formats.mdx` — Sources: `scheduling/routines.py`, `scheduling/reminders.py`, `webhook.py`, `sessions.py`

## Architecture

- [ ] `architecture/overview.mdx` — Sources: `CLAUDE.md`
- [ ] `architecture/session-management.mdx` — Sources: `sessions.py`, `agent.py`
- [ ] `architecture/context-flow.mdx` — Sources: `forks.py`, `prompts.py`, `scheduling/preamble.py`
- [ ] `architecture/streaming.mdx` — Sources: `streamer.py`

## Development

- [ ] `development/guide.mdx` — Sources: `CLAUDE.md`, `pyproject.toml`
- [ ] `development/testing.mdx` — Sources: `tests/` directory
- [ ] `development/cli-reference.mdx` — Sources: `main.py`, `scheduling/routine_cmd.py`, `scheduling/reminder_cmd.py`
- [ ] `development/troubleshooting.mdx` — Sources: `sessions.py`, `config.py`, `storage.py`

## Self-Hosting

- [ ] `self-hosting/guide.mdx` — Sources: `config.py`, `main.py`, `CLAUDE.md`
- [ ] `self-hosting/discord-bot-setup.mdx` — Sources: `bot.py`, `config.py`
- [ ] `self-hosting/google-oauth-setup.mdx` — Sources: `google/auth.py`

## Changelog

- [ ] `changelog.mdx` — Sources: git log
