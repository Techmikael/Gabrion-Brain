#!/usr/bin/env python3
"""Kill switch: blocks every tool call while memory/PAUSED exists.

memory/paused/<agent-name> pauses one agent. That needs Claude Code to report
which subagent is calling (agent_type in the hook input); when it does not, only
the global switch applies.
"""
import json, os, sys

root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
try:
    event = json.load(sys.stdin)
except Exception:
    event = {}

if os.path.exists(os.path.join(root, "memory", "PAUSED")):
    print("Gabrion kill switch is ON (memory/PAUSED). All agents are paused by the founder.", file=sys.stderr)
    sys.exit(2)

agent = event.get("agent_type") or event.get("subagent_type")
if agent and os.path.exists(os.path.join(root, "memory", "paused", agent)):
    print(f"Agent '{agent}' is paused by the founder (memory/paused/{agent}).", file=sys.stderr)
    sys.exit(2)

# memory/paused/team-<department> pauses a whole department (see memory/org/roster.csv).
LEADS = {"chief-of-staff": "leadership", "front-desk": "front-desk", "sales": "sales",
         "solutions-architect": "solutions", "web-builder": "web", "automation-builder": "automation",
         "voice-chat-builder": "automation", "software-engineer": "engineering",
         "operations-support": "operations", "finance-admin": "finance"}
DEPTS = {"Leadership & Operations": "leadership", "Front Desk & Customer Care": "front-desk", "Sales": "sales",
         "Marketing": "marketing", "Solutions & Proposals": "solutions", "Web & Design": "web",
         "Automation & AI": "automation", "Engineering": "engineering", "Quality & Testing": "engineering",
         "Security & Compliance": "security", "Operations & Support": "operations", "Finance": "finance"}
if agent:
    team = LEADS.get(agent)
    if not team:
        try:
            import csv
            with open(os.path.join(root, "memory", "org", "roster.csv"), newline="") as fh:
                for row in csv.DictReader(fh):
                    if row["agent"] == agent:
                        team = DEPTS.get(row["department"])
                        break
        except OSError:
            pass
    if team and os.path.exists(os.path.join(root, "memory", "paused", "team-" + team)):
        print(f"The {team} team is paused by the founder (memory/paused/team-{team}).", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
