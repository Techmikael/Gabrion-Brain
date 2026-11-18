#!/usr/bin/env bash
# Installs the agency-agents library into the Brain as Gabrion's specialist workforce.
# All agents are copied into agents-library/ (pinned version, MIT licence); the ones on
# duty in memory/org/roster.csv are installed into .claude/agents/specialists/ with their
# Gabrion department, manager, tier and rules. See docs/AGENT-RULES.md.
# Re-run any time: your roster choices are kept.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/team.py sync
python3 scripts/team.py apply
echo
echo "Older installs copied specialists into ~/.claude/agents. Those copies have no Gabrion rules."
echo "If you used the old installer, remove them once with:  python3 scripts/team.py cleanup-old"
