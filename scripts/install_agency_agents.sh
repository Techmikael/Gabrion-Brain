#!/usr/bin/env bash
# Installs the agency-agents specialists (marketing, sales, product,
# project management, support, finance) into ~/.claude/agents so every
# Claude Code session, including the Gabrion Brain, can use them.
# Re-run any time to update them.
set -euo pipefail
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --depth 1 https://github.com/msitarzewski/agency-agents "$TMP/agency-agents"
mkdir -p "$HOME/.claude/agents"
count=0
for d in marketing sales product project-management support finance; do
  for f in "$TMP/agency-agents/$d"/*.md; do
    cp "$f" "$HOME/.claude/agents/"
    count=$((count+1))
  done
done
echo "Installed $count specialist agents into $HOME/.claude/agents"
