# Gabrion Brain

The operating system for Gabrion: one founder plus an AI workforce, built from the Operating Blueprint (`docs/blueprint.pdf`). **Start here: `docs/OPERATING-MANUAL.md`** (launch, daily use, control, maintenance).

Open this folder in Claude Code and the rules in `CLAUDE.md` and the ten agents in `.claude/agents/` load automatically.

## What's here
| Blueprint layer | Where it lives |
|---|---|
| The brain: 10 agents with fixed limits | `.claude/agents/` (Marketing joins in phase 3: `docs/marketing-agent-phase3.md`) |
| Memory: CRM, task board, approvals, finance, logs | `memory/` (the Command Centre, as plain CSV and Markdown) |
| Playbooks | `playbooks/`: discovery call, proposal, website build, AI receptionist setup, client onboarding |
| Solution factories | `factories/`: websites, AI receptionist, automation, software, private AI, each with its checklist |
| Client vaults | `clients/<slug>/` from `clients/_template/` (git-ignored: client data never goes into git) |
| Founder controls | approval queue, kill switch, activity log (below) |
| Demo templates | `templates/website/` (salon demo + Gabrion's own site), `templates/ai-receptionist/` |

## Your daily routine
```bash
python3 scripts/daily_briefing.py --print
```
Then work through `memory/approvals/queue.md`: change `Status: PENDING` to `APPROVED` or `REJECTED` and add a note. Agents act only on items you approved.

Add `--ai` for a "top three for today" note from Claude (needs `pip install anthropic` and an Anthropic API key).

## Giving work to the brain
In Claude Code, in this folder:
> Use the chief-of-staff agent: new enquiry from a salon owner who misses calls while cutting hair.

The Chief of Staff puts it on the board and hands it to the right agent. Or call an agent directly: "Use the solutions-architect agent to draft a proposal from clients/bloom/discovery/notes.md".

## Founder controls
- **Approvals:** every action touching money, clients or production stops at `memory/approvals/queue.md`.
- **Kill switch:** `touch memory/PAUSED` stops every agent's tool use; delete the file to resume. `touch memory/paused/sales` pauses one agent where Claude Code reports which agent is calling.
- **Activity log:** every tool call is appended to `memory/logs/activity.jsonl` (tool and target only, never contents).
- **Least access:** each agent has only the tools in its file; for example, Sales has no shell and Front Desk can't browse the web.

## Build the demo sites
```bash
python3 templates/website/build.py templates/website/configs/gabrion.json --out templates/website/dist/gabrion
python3 templates/website/build.py templates/website/configs/salon.json --out templates/website/dist/salon
```
`dist/` is plain HTML: drag it into Cloudflare Pages, Netlify or Vercel. Replace `hello@example.com` and the phone placeholder before publishing.

## What still needs you
See `memory/tasks/board.csv`, owner `founder`: register the company and with the ICO, open the tool accounts, set prices in `docs/pricing.md`, insurance, and push this repo to a private GitHub repository.
