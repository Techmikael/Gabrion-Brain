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
sys.exit(0)
