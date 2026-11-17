# ruflo in the Gabrion Brain

ruflo (github.com/ruvnet/ruflo) is an "agent harness" for Claude Code. It lets several agents work as a **swarm** on one job, gives them a **shared memory** that carries across sessions, and adds its own MCP tools and about 17 agents. Those agents are mostly for software work: coders, testers, reviewers and coordinators.

## Where it helps Gabrion
| Use it for | Example |
|---|---|
| Software and SaaS factory | "Use a ruflo swarm to build the booking portal in clients/bloom/app on a branch, with tests. Don't merge." |
| Website and automation builds | "Use a ruflo swarm to check templates/website for bugs and add tests." |
| Remembering what worked | ruflo's memory recalls patterns from earlier jobs, so the 20th build goes faster than the first |

For sales, finance, support and daily running, keep using the 10 Gabrion agents and the agency-agents specialists. ruflo adds little there and costs more, because a swarm is several agents billing at once.

## Install (once)
Needs Node.js (nodejs.org, LTS). In the gabrion-brain folder:
```bash
python3 scripts/install_ruflo.py
```
(Windows: `python scripts/install_ruflo.py`.) Then restart `claude`. Approve the `claude-flow` MCP server when Claude Code asks.

Don't use the plain `npx ruflo@latest init` from ruflo's README in this folder. It stops on your kill switch, and the fix it suggests (`--drop-risky-settings`) deletes the kill switch and the activity log.

## The rules don't change
- Swarm agents follow `CLAUDE.md`: drafts and branches only. Merges, go-lives, client messages and prices still go to the approval queue.
- The kill switch (`memory/PAUSED`) stops ruflo's tool calls too, because they run through Claude Code's hooks.
- ruflo's memory (`.swarm/`, `.claude-flow/`) can contain client details. It stays on your computer and is never committed. Back it up with `clients/`.
- Swarms are capped at 5 agents. Raise `CLAUDE_FLOW_MAX_AGENTS` in `.mcp.json` only if you need to, and watch your usage.

## Turning it off or removing it
- Off for a session: run `/mcp` in Claude Code and disable `claude-flow`.
- Remove: delete `.mcp.json`, `.swarm/`, `.claude-flow/` and the ruflo folders in `.claude/agents/` (browser, consensus, core, sparc, swarm, testing), `.claude/commands/`, `.claude/helpers/`, `.claude/skills/`. Then restore `.claude/settings.json` from its `.before-ruflo-…` backup.

## Updating ruflo
The version is pinned in `scripts/install_ruflo.py` (`RUFLO_VERSION`) and `.mcp.json`. To update, change both to the new version, read ruflo's CHANGELOG for anything touching settings or hooks, then re-run the installer. Don't turn on ruflo "mods" (`--mods`): they're unsigned plugins that can run any command.
