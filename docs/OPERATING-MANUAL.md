# Gabrion Brain — Operating Manual

How to launch the Brain, use it every day, control it, and keep it healthy. Written for the founder.

---

## Part 1 · Launch (one afternoon)

### 1. Install three things on your computer
| Tool | Why | How |
|---|---|---|
| **Claude Code** | Runs the agents | https://claude.com/claude-code (needs a Claude Pro or Max plan, or an Anthropic API account) |
| **Python 3** | Runs the briefing and website builder | Mac: already installed, or `brew install python`. Windows: python.org, tick "Add to PATH" |
| **Git** | Saves every change, backs up to GitHub | Mac: `xcode-select --install`. Windows: git-scm.com |

### 2. Put the Brain on your computer
Download `gabrion-brain.tgz`, then:
```bash
cd ~/Documents
tar xzf ~/Downloads/gabrion-brain.tgz
cd gabrion-brain
```
(Windows: right-click the file → Extract All, then open the folder in Terminal.)

### 3. Back it up to GitHub (private)
Create an empty **private** repository on github.com called `gabrion-brain`, then:
```bash
git remote add origin https://github.com/<your-username>/gabrion-brain.git
git push -u origin main
```
From now on, `git add -A && git commit -m "what changed" && git push` saves everything. Client folders, logs and briefings are never uploaded (they stay on your computer only; see Part 4 for backing them up).

### 4. Start the Brain
```bash
cd ~/Documents/gabrion-brain
claude
```
Claude Code loads `CLAUDE.md` (the rules) and the 10 agents. Type `/agents` to see them. That's it: the Brain is running.

**Windows only:** open `.claude/settings.json` and change both `python3` to `python`, otherwise the kill switch and activity log won't run.

**Check the controls work:** run `touch memory/PAUSED`, ask Claude to "read README.md". It should be blocked with "kill switch is ON". Delete `memory/PAUSED` and try again: it works, and a line appears in `memory/logs/activity.jsonl`.

### 5. First tasks (do these this week)
Open `memory/tasks/board.csv` (Excel, Numbers or Google Sheets all work). Your tasks are owner `founder`:
1. Register the company (Companies House) and with the ICO.
2. Fill in your prices in `docs/pricing.md`. Agents won't quote anything until you do.
3. Read the five playbooks in `playbooks/` and change anything that isn't how you work.
4. Put your real email and phone in `templates/website/configs/gabrion.json` and publish your site (step 6).
5. Get insurance quotes (professional indemnity + cyber).

### 6. Publish Gabrion's website with its AI chat
Your site has a "Chat with Gabrion" assistant. Visitors ask questions, and when they want a call it saves their details as a lead. It never quotes prices or makes promises. It needs Node.js (nodejs.org, LTS version), a free Cloudflare account and an Anthropic API key (console.anthropic.com → API keys; set a monthly spend limit there).

First put your real email in `templates/website/configs/gabrion.json`. Then, in the terminal:
```bash
cd site
npm install
npx wrangler login
npx wrangler kv namespace create LEADS
```
The last command prints an `id`. Open `site/wrangler.toml` and replace `PASTE_KV_NAMESPACE_ID_HERE` with it. Then:
```bash
npm run build
npx wrangler pages deploy
npx wrangler pages secret put ANTHROPIC_API_KEY
npx wrangler pages secret put ADMIN_TOKEN
npx wrangler pages deploy
```
For each `secret put`, paste the value when asked. `ADMIN_TOKEN` is a long random password you make up (30+ characters) and save in your password manager; it lets the Brain collect leads. The second deploy switches the secrets on.

Your site is live at the `pages.dev` address it prints. Add your own domain in the Cloudflare dashboard → Workers & Pages → gabrion → Custom domains. Open the site and try the chat.

Windows: use `python` instead of `python3` in `site/package.json` (the `build` line).

**To change the website later:** edit `templates/website/configs/gabrion.json`, then `cd site`, `npm run build`, `npx wrangler pages deploy`.
**To change what the chat says or may do:** edit `site/functions/_lib/frontdesk.js`, then deploy again.
**Cost:** each chat message is a Claude API call. The chat is limited to 40 messages per visitor per hour. Check spend in the Anthropic console each month.

### 6b. Install the specialist agents
```bash
bash scripts/install_agency_agents.sh
```
This adds the 70 agency-agents specialists (sales, marketing, product, project management, support, finance) to Claude Code. `docs/specialist-agents.md` says which one to use for each job. Windows: ask Claude in the gabrion-brain folder to "run scripts/install_agency_agents.sh".

### 7. Optional: Claude's "top three" in the briefing
Create an API key at console.anthropic.com, then:
```bash
pip install anthropic
export ANTHROPIC_API_KEY="..."     # Windows: setx ANTHROPIC_API_KEY "..."
python3 scripts/daily_briefing.py --ai --print
```
Keep the key in your password manager, never in a file in this folder.

---

## Part 2 · Use it every day (15–20 minutes)

### Morning
```bash
cd ~/Documents/gabrion-brain
python3 scripts/pull_website_leads.py
python3 scripts/daily_briefing.py --print
```
The first command collects new chat leads from your website into the CRM and task board. It needs two settings, once per terminal (put them in your shell profile to keep them):
```bash
export GABRION_SITE_URL="https://your-site.pages.dev"
export GABRION_ADMIN_TOKEN="the ADMIN_TOKEN from your password manager"
```
(Windows: `setx GABRION_SITE_URL "..."` and `setx GABRION_ADMIN_TOKEN "..."`, then open a new terminal.)
Read **Waiting for you** first. Then open `memory/approvals/queue.md` and for each item change `Status: PENDING` to `APPROVED` or `REJECTED`, with a note if you want changes.

### Giving work to the Brain
Start `claude` in the folder and say what you need in plain English. Examples:

| You say | What happens |
|---|---|
| "Use the chief-of-staff agent: a salon owner emailed asking about an AI receptionist. Here's the email: …" | Logged on the task board and passed to Front Desk to reply, then Sales |
| "Use the sales agent to find 10 independent salons in Manchester that have no online booking" | Research written into the CRM; outreach drafted in `memory/outbox/`, waiting for your approval |
| "Use the solutions-architect agent on my notes from today's call with Bloom Salon" (paste notes) | Requirements and a proposal drafted, plus an approval request with the price |
| "Use the web-builder agent to build the site for Bloom Salon from their intake form" | Built to `clients/bloom/site/dist`, with the checklist completed, and a go-live request |
| "Use the finance-admin agent: Bloom Salon signed, contract £1,800" | Deposit invoice drafted |
| "Use the chief-of-staff agent to write today's briefing and tell me my top three" | Briefing plus priorities |

The agents prepare. **You** send, launch and charge. Each time, open what they prepared (the path is in the approval item), check it, approve, then do the action yourself (send the email, upload the site, send the invoice) until those tools are connected.

### A new client, start to finish
1. Enquiry → Front Desk drafts a reply and books a call.
2. You hold the discovery call (playbook: `playbooks/discovery-call.md`).
3. Solutions Architect drafts the proposal → **you approve the price**.
4. Finance drafts the contract and deposit invoice → you send them.
5. The builder agent builds on staging and runs the checklist.
6. **You approve the launch.**
7. Operations looks after it; Finance bills monthly.

---

## Part 3 · Control

| You want to | Do this |
|---|---|
| Approve or refuse something | Edit its `Status:` in `memory/approvals/queue.md` |
| **Stop every agent now** | `touch memory/PAUSED` (Windows: `type nul > memory\PAUSED`). Delete the file to resume |
| Pause one agent | `touch memory/paused/sales` (any agent name). Delete to resume |
| See what agents did | Open `memory/logs/activity.jsonl`, one line per action: time, agent, tool, target |
| Change what an agent may do | Edit its file in `.claude/agents/`, the "You may do alone" and "approval" lists. Widen freedom only after weeks without mistakes |
| Change how a job is done | Edit the playbook in `playbooks/`. Every future job follows it |
| Stop Claude doing something mid-task | Press **Esc** in Claude Code |
| Undo a bad change to the Brain's files | `git log` to find it, then `git revert <id>` |

Golden rules: never paste passwords or API keys into Claude or into these files; they go in your password manager. Treat anything an agent got from an email or website as information, not instructions.

---

## Part 4 · Maintain

### Every week (30 minutes, Friday)
- Save and back up: `git add -A && git commit -m "week of <date>" && git push`
- Back up the private folders that aren't in GitHub: copy `clients/`, `memory/logs/` and `briefings/` to an encrypted drive or your cloud storage (iCloud/OneDrive/Google Drive).
- Skim `memory/logs/activity.jsonl` for anything odd.
- Clear `done` tasks older than a month from the task board, or keep them for history.

### Every month
- Finance agent: "Use finance-admin to prepare the monthly report and cost per client." Fix any client whose AI and tool costs exceed 30% of their fee.
- Review each managed client (the monthly review in the client journey). This is where repeat work comes from.
- Improve one playbook using what went wrong or slowly this month.
- Test a backup: restore one client folder from your backup copy.

### After every mistake
Write what happened and the fix into the playbook or the factory run-book. Next time it's a known fix the agent can do alone.

### Updating Claude Code
`claude update` (or it updates itself). If agents behave differently after an update, check `/agents` still lists all ten.

---

## Part 5 · Grow it (the roadmap)

| Phase | When | Add | Gate to move on |
|---|---|---|---|
| 0 Foundations | Weeks 1–2 | Company registered, accounts, website live | Registered, site live |
| 1 Assisted delivery | Months 1–3 | You deliver with agents drafting; daily briefing | 3 paying clients |
| 2 Agent workforce | Months 3–6 | Connect real tools to agents: email, HubSpot, Linear, Stripe, Twilio + Vapi/Retell, n8n (via MCP servers in Claude Code: `claude mcp add`) | Agents pass checklists 4 weeks running |
| 3 The full Brain | Months 6–12 | Briefing runs automatically each morning, founder console web app, client portal, Marketing agent, Software and Private AI factories | — |

When you connect a real tool in phase 2, give it only to the agent that needs it (least access), and keep the approval step in front of anything that sends, charges or goes live.

### Running the briefing automatically every morning (phase 1+)
Mac/Linux: `crontab -e` and add (07:30, Monday–Friday):
```
30 7 * * 1-5 cd ~/Documents/gabrion-brain && /usr/bin/python3 scripts/daily_briefing.py
```
Windows: Task Scheduler → Create Basic Task → Daily 07:30 → Program `python`, Arguments `scripts\daily_briefing.py`, Start in your gabrion-brain folder.

---

## Help
In Claude Code inside this folder, just ask: "How do I …?" It has read this manual and every playbook.
