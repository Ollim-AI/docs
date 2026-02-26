# ollim-bot-docs

Documentation site for [ollim-bot](https://github.com/Ollim-AI/ollim-bot), built with [Mintlify](https://mintlify.com).

## Development

Install the Mintlify CLI:

```bash
npm i -g mint
```

Run the local dev server:

```bash
mint dev
```

Preview at [localhost:3000](http://localhost:3000).

## Structure

```
docs.json               # Site config: theme, navigation, branding
llms.txt                # Machine-readable page index
getting-started/        # Overview, quickstart, setup, concepts
core-usage/             # Conversations, commands, forks, embeds, permissions
scheduling/             # Routines, reminders, background forks, ping budget
integrations/           # Google (Tasks, Calendar, Gmail), webhooks
extending/              # MCP tools, subagents, system prompt, adding integrations
configuration/          # Env vars, data directory, file formats
architecture/           # Module map, sessions, context flow, streaming
development/            # Dev guide, testing, CLI reference, troubleshooting
self-hosting/           # Hosting guide, Discord setup, Google OAuth setup
changelog.mdx           # Version history
```
