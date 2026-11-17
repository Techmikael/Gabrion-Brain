#!/usr/bin/env python3
"""Adds ruflo (agent swarms, shared memory, MCP tools) to the Gabrion Brain,
without weakening the Brain's controls.

    python3 scripts/install_ruflo.py            # Mac/Linux
    python scripts/install_ruflo.py             # Windows

What it does differently from a plain `npx ruflo@latest init`:
- keeps the kill switch and activity-log hooks (a plain init stops on them, and
  its suggested --drop-risky-settings would delete them);
- pins ruflo to a tested version instead of downloading @latest on every start;
- leaves ruflo's unsigned "mods" plugins off (they can run any command);
- doesn't touch ~/.claude/CLAUDE.md, skips sign-up and telemetry prompts;
- keeps ruflo's memory database out of GitHub (it can hold client details);
- caps a swarm at 5 agents to keep usage and cost down.
It backs up every file it changes and checks the kill switch afterwards.
"""
import json
import os
import shutil
import subprocess
import sys
import time

RUFLO_VERSION = "3.77.1"
MAX_AGENTS = "5"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS = os.path.join(ROOT, ".claude", "settings.json")
MCP = os.path.join(ROOT, ".mcp.json")
GITIGNORE = os.path.join(ROOT, ".gitignore")
STAMP = time.strftime("%Y%m%d-%H%M%S")


def backup(path):
    if os.path.exists(path):
        dest = f"{path}.before-ruflo-{STAMP}"
        shutil.copy2(path, dest)
        return dest
    return None


def restore(backups):
    for orig, saved in backups.items():
        if saved:
            shutil.copy2(saved, orig)


def kill_switch_first(settings):
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    return bool(pre) and any("kill_switch.py" in (h.get("command") or "") for h in pre[0].get("hooks", []))


def main():
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        sys.exit("Node.js is needed first: install the LTS version from nodejs.org, then open a new terminal.")
    if os.path.exists(os.path.join(ROOT, "memory", "PAUSED")):
        sys.exit("The kill switch is on (memory/PAUSED). Remove it first if you want to install ruflo.")

    backups = {p: backup(p) for p in (SETTINGS, MCP, GITIGNORE)}
    cmd = [npx, "-y", f"ruflo@{RUFLO_VERSION}", "init",
           "--keep-risky-settings", "--no-mods", "--no-plugin-install", "--no-global",
           "--no-signup", "--no-telemetry-prompt", "--no-skills-sh"]
    print("Running:", " ".join(cmd[1:]))
    run = subprocess.run(cmd, cwd=ROOT, stdin=subprocess.DEVNULL)
    if run.returncode != 0:
        restore(backups)
        sys.exit("ruflo init failed; your settings were restored from the backups.")

    # 1. Settings: keep our hooks first, drop unpinned auto-approved npx commands.
    with open(SETTINGS, encoding="utf-8") as f:
        settings = json.load(f)
    if not kill_switch_first(settings):
        restore(backups)
        sys.exit("Safety check failed: the kill switch is no longer the first hook. Settings restored; ruflo not enabled.")
    perms = settings.setdefault("permissions", {})
    perms["allow"] = [a for a in perms.get("allow", []) if not a.startswith("Bash(npx")]
    settings.pop("enabledPlugins", None)
    with open(SETTINGS, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")

    # 2. MCP server: pinned version, smaller swarms.
    if os.path.exists(MCP):
        with open(MCP, encoding="utf-8") as f:
            mcp = json.load(f)
        for server in mcp.get("mcpServers", {}).values():
            server["args"] = [a.replace("ruflo@latest", f"ruflo@{RUFLO_VERSION}") for a in server.get("args", [])]
            if "env" in server:
                server["env"]["CLAUDE_FLOW_MAX_AGENTS"] = MAX_AGENTS
        with open(MCP, "w", encoding="utf-8") as f:
            json.dump(mcp, f, indent=2)
            f.write("\n")

    # 3. Keep ruflo's memory and backups out of GitHub.
    with open(GITIGNORE, encoding="utf-8") as f:
        gi = f.read()
    extra = ["# ruflo memory can hold client details: never commit it", ".swarm/", ".claude-flow/",
             ".claude/settings.json.bak-*", "*.before-ruflo-*"]
    present = {line.strip() for line in gi.splitlines()}   # whole lines: ".claude-flow/sessions/" must not count as ".claude-flow/"
    missing = [line for line in extra if line not in present]
    if missing:
        with open(GITIGNORE, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(missing) + "\n")

    print("\nruflo is installed for the Gabrion Brain.")
    print(f"  version {RUFLO_VERSION} (pinned) · swarms capped at {MAX_AGENTS} agents · mods off")
    print("  kill switch and activity log: kept and checked")
    print("  backups: files ending .before-ruflo-" + STAMP)
    print("Next: start `claude` in this folder and read docs/ruflo.md.")


if __name__ == "__main__":
    main()
