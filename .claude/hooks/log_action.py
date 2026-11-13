#!/usr/bin/env python3
"""Appends every tool call to memory/logs/activity.jsonl (who, what, when).

Logs the tool name and a short target (file path, command or URL), never file
contents or tool output, so secrets and client data stay out of the log.
"""
import json, os, sys
from datetime import datetime, timezone

root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
try:
    event = json.load(sys.stdin)
except Exception:
    sys.exit(0)

inp = event.get("tool_input") or {}
target = inp.get("file_path") or inp.get("path") or inp.get("url") or inp.get("command") or inp.get("pattern") or inp.get("description") or ""
entry = {
    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "session": event.get("session_id"),
    "agent": event.get("agent_type") or "main",
    "tool": event.get("tool_name"),
    "target": str(target)[:200],
}
os.makedirs(os.path.join(root, "memory", "logs"), exist_ok=True)
with open(os.path.join(root, "memory", "logs", "activity.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")
sys.exit(0)
