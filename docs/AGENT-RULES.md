# Agent rules: roles, tiers, teamwork and learning

Gabrion runs like a company. The founder owns it. Ten **Gabrion agents** lead departments. Under them sit
283 **specialists** from the agency-agents library, each with one department, one manager and one tier.
`CLAUDE.md` still overrides everything here.

## 1. Who is who

| Level | Who | What they do |
|---|---|---|
| Owner | The founder | Sets goals, approves everything in `memory/approvals/queue.md`, corrects work |
| Leads | The 10 Gabrion agents (`.claude/agents/*.md`) | Own a job end to end, follow the playbook, call in specialists, check their work |
| Specialists, on duty | 78 agents in `.claude/agents/specialists/` | Expert help on one piece of work, inside their tier |
| Specialists, bench | In `agents-library/`, listed in the roster | Hired on duty with `python3 scripts/team.py hire <name>` |
| Specialists, reserve | In `agents-library/` | Kept for later markets or client industries (games, GIS, China platforms, healthcare) |

The org chart is `docs/ORG-CHART.md`. The source of truth is `memory/org/roster.csv`: the founder may change any
department, manager, tier or status there, then run `python3 scripts/team.py apply`.

## 2. Tiers: what each agent may do

| Tier | Tools | May | Never |
|---|---|---|---|
| **advise** | read, search, web | Give advice in its reply | Change files |
| **draft** | + write, edit | Write drafts and notes: `memory/outbox/`, the job's folder, task notes | Send, publish, pay |
| **build** | + terminal | Build and test on branches and staging | Merge to main, deploy live, touch real client data |

No tier may send a message, quote a price, spend money or go live. That always goes through the approval queue,
prepared by the lead agent for the job.

## 3. How they work together

1. **The lead owns the job.** Work arrives at the Chief of Staff, who gives it to one lead agent and a workflow from `workflows/`.
2. **Specialists are called in by name** for the steps the workflow lists, e.g. "use `sales-outbound-strategist` to draft the sequence".
3. **Every draft gets a second pair of eyes before the founder sees it.** The workflow names the reviewer
   (Sales Coach for outreach, Code Reviewer for code, Brand Guardian and Finish Gate for websites, Reality Checker for claims).
4. **The lead checks the result against the playbook** and only then adds it to the approval queue.
5. **One job, one trail.** Every step is written in the task's row on `memory/tasks/board.csv` (who did what, where the draft is).

Specialists don't talk to each other directly: the lead (or the founder's session) passes work between them.
That keeps every hand-over visible and logged.

## 4. How they learn

Agents don't remember between sessions on their own. Gabrion gives them a written memory in `memory/lessons/`:

| File | Who writes | Who reads |
|---|---|---|
| `memory/lessons/<agent>.md` | That agent after each task; its reviewer; the founder | That agent, before every task |
| `memory/lessons/shared.md` | The Chief of Staff, when a lesson matters to everyone | Every agent, before every task |

**Format:** one line per lesson, newest last:
`- 2026-11-18 · founder · Danish prospects: never e-mail first; LinkedIn message or phone only.`

**Sources, strongest first:** `founder` (always wins) → `reviewer` (a teacher's feedback) → `self` (the agent's own note).

**The learning loop:**
1. Before a task: read `shared.md` and your own lessons file.
2. After a task: add one lesson if something worked or failed.
3. When a reviewer corrects a draft: the reviewer adds a `reviewer` lesson to the drafter's file. That is how specialists teach the leads and each other.
4. When the founder marks an approval `CHANGE` or `REJECTED` with a note: the agent that prepared it turns the note into a `founder` lesson.
5. Every Friday the Chief of Staff reads the week's lessons. A lesson seen three times, or any founder lesson that changes how a job is done,
   becomes a proposed playbook change in the approval queue (type `new-or-unusual`). Playbooks change only when the founder approves.

Never put client names, client data or secrets in a lessons file. Write the lesson in general terms.

## 5. Control

| You want to | Do this |
|---|---|
| Stop every agent | Create the file `memory/PAUSED` |
| Stop one agent | Create `memory/paused/<agent-name>` |
| Stop a whole department | Create `memory/paused/team-<name>`: `team-leadership`, `team-front-desk`, `team-sales`, `team-marketing`, `team-solutions`, `team-web`, `team-automation`, `team-engineering`, `team-security`, `team-operations` or `team-finance` |
| Put a specialist on or off duty | `python3 scripts/team.py hire <name>` or `bench <name>`, then `python3 scripts/team.py apply` |
| Change a role, manager or tier | Edit `memory/org/roster.csv`, then `python3 scripts/team.py apply` |
| See who is where | `python3 scripts/team.py list` or `docs/ORG-CHART.md` |
| See what an agent learned | `python3 scripts/team.py show <name>` |

Only the founder deletes pause files, changes tiers, or changes the library's pinned version in `scripts/team.py`.
