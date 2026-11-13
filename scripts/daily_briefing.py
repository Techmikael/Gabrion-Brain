#!/usr/bin/env python3
"""Chief of Staff daily briefing.

Reads the Command Centre memory (CRM, task board, finance, approval queue,
activity log) and writes briefings/YYYY-MM-DD.md with the five areas the
blueprint asks for: Sales, Delivery, Clients, Money, Agents.

    python3 scripts/daily_briefing.py              # numbers only, no API call
    python3 scripts/daily_briefing.py --ai         # adds a short prioritised note from Claude
    python3 scripts/daily_briefing.py --memory demo/memory --date 2026-11-13

--ai needs `pip install anthropic` and an ANTHROPIC_API_KEY (or `ant auth login`).
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def num(v):
    try:
        return float(str(v).replace(",", "").replace("£", "").strip() or 0)
    except ValueError:
        return 0.0


def day(v):
    try:
        return datetime.strptime((v or "").strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def gbp(x):
    return f"£{x:,.0f}"


def build(memory, today):
    leads = read_csv(os.path.join(memory, "crm", "leads.csv"))
    tasks = read_csv(os.path.join(memory, "tasks", "board.csv"))
    invoices = read_csv(os.path.join(memory, "finance", "invoices.csv"))
    costs = read_csv(os.path.join(memory, "finance", "costs.csv"))
    cash = read_csv(os.path.join(memory, "finance", "cash.csv"))
    queue_path = os.path.join(memory, "approvals", "queue.md")
    queue = open(queue_path, encoding="utf-8").read() if os.path.exists(queue_path) else ""
    week_ago = today - timedelta(days=7)
    month_start = today.replace(day=1)

    # Sales
    stages = Counter((l.get("stage") or "").strip().lower() for l in leads)
    open_stages = {"enquiry", "qualified", "call-booked", "proposal", "negotiation"}
    pipeline = sum(num(l.get("value_gbp")) for l in leads if (l.get("stage") or "").lower() in open_stages)
    overdue_follow = [l for l in leads if (l.get("stage") or "").lower() in open_stages
                      and (d := day(l.get("next_date"))) and d < today]

    # Delivery
    open_tasks = [t for t in tasks if (t.get("status") or "").lower() != "done"]
    late = [t for t in open_tasks if (d := day(t.get("due"))) and d < today]
    due_today = [t for t in open_tasks if day(t.get("due")) == today]
    waiting = [t for t in open_tasks if (t.get("status") or "").lower() == "waiting-approval"]
    blocked = [t for t in open_tasks if (t.get("status") or "").lower() == "blocked"]
    founder = [t for t in open_tasks if (t.get("owner") or "").lower() == "founder"]

    # Approvals: each "## A-xxxx" block with Status: PENDING
    pending = []
    queue = re.sub(r"```.*?```", "", queue, flags=re.S)  # ignore the format example
    for block in re.split(r"\n(?=## A-)", queue):
        m = re.match(r"## (A-\d+)\s*·?\s*(.*)", block.strip())
        if m and re.search(r"Status:\s*PENDING", block, re.I):
            agent = re.search(r"Agent:\s*(.+)", block)
            pending.append((m.group(1), m.group(2).strip(), agent.group(1).strip() if agent else "?"))

    # Clients and money
    managed = [l for l in leads if (l.get("stage") or "").lower() == "won" and num(l.get("monthly_gbp")) > 0]
    mrr = sum(num(l.get("monthly_gbp")) for l in managed)
    unpaid = [i for i in invoices if (i.get("status") or "").lower() not in ("paid", "void", "draft")]
    overdue = [i for i in unpaid if (d := day(i.get("due"))) and d < today]
    cash_now = num(sorted(cash, key=lambda r: r.get("date", ""))[-1]["balance_gbp"]) if cash else None
    month_costs = [c for c in costs if (d := day(c.get("date"))) and d >= month_start]
    ai_tool_cost = sum(num(c.get("amount_gbp")) for c in month_costs
                       if (c.get("category") or "").lower() in ("ai", "tools", "software", "hosting"))
    cost_by_client = Counter()
    for c in month_costs:
        cost_by_client[(c.get("client") or "gabrion").strip()] += num(c.get("amount_gbp"))
    margin_flags = [(l.get("company") or l.get("name"), cost_by_client.get(l.get("company", ""), 0), num(l.get("monthly_gbp")))
                    for l in managed
                    if cost_by_client.get(l.get("company", ""), 0) > 0.3 * num(l.get("monthly_gbp"))]

    # Agents: activity log, last 24 hours
    log_path = os.path.join(memory, "logs", "activity.jsonl")
    since = datetime.combine(today - timedelta(days=1), datetime.min.time())
    by_agent = Counter()
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    ts = datetime.fromisoformat(e["ts"]).replace(tzinfo=None)
                except Exception:
                    continue
                if ts >= since:
                    by_agent[e.get("agent") or "main"] += 1
    paused_all = os.path.exists(os.path.join(memory, "PAUSED"))
    paused_dir = os.path.join(memory, "paused")
    paused = sorted(n for n in os.listdir(paused_dir) if not n.startswith(".")) if os.path.isdir(paused_dir) else []
    agent_done = Counter((t.get("owner") or "").lower() for t in tasks if (t.get("status") or "").lower() == "done")

    def lines(items, fmt, limit=8):
        out = [fmt(x) for x in items[:limit]]
        if len(items) > limit:
            out.append(f"- …and {len(items) - limit} more")
        return out or ["- none"]

    md = [f"# Daily briefing · {today.isoformat()}", ""]
    if paused_all:
        md += ["> **Kill switch is ON** (memory/PAUSED): all agents are paused.", ""]

    md += ["## Waiting for you", f"**{len(pending)} approval(s)** in `memory/approvals/queue.md`"]
    md += lines(pending, lambda p: f"- {p[0]} · {p[1]} ({p[2]})")
    md += ["", f"**Your tasks:** {len(founder)} open, {sum(1 for t in founder if t in late)} late"]
    md += lines(sorted(founder, key=lambda t: t.get("due") or "9999"), lambda t: f"- {t['id']} {t['title']} (due {t.get('due') or '—'})", 6)

    md += ["", "## Sales",
           f"- Pipeline value: {gbp(pipeline)} across {sum(stages[s] for s in open_stages)} open leads",
           f"- Enquiries: {stages['enquiry']} · calls booked: {stages['call-booked']} · proposals out: {stages['proposal']} · won: {stages['won']} · lost: {stages['lost']}",
           f"- Follow-ups overdue: {len(overdue_follow)}"]
    md += lines(overdue_follow, lambda l: f"  - {l.get('company') or l.get('name')}: {l.get('next_action')} (was due {l.get('next_date')})", 5) if overdue_follow else []

    md += ["", "## Delivery",
           f"- Open tasks: {len(open_tasks)} · due today: {len(due_today)} · late: {len(late)} · waiting approval: {len(waiting)} · blocked: {len(blocked)}"]
    md += lines(late, lambda t: f"  - LATE {t['id']} {t['title']} → {t.get('owner')} (due {t.get('due')})", 6) if late else []
    md += lines(blocked, lambda t: f"  - BLOCKED {t['id']} {t['title']} → {t.get('owner')}: {t.get('notes')}", 6) if blocked else []

    md += ["", "## Clients",
           f"- Managed clients: {len(managed)} · monthly recurring revenue: {gbp(mrr)}",
           "- Systems up / open tickets / time to fix: connect monitoring and the ticket inbox (phase 2)"]

    md += ["", "## Money",
           f"- Cash in bank: {gbp(cash_now) if cash_now is not None else 'not recorded (add a row to memory/finance/cash.csv)'}",
           f"- Unpaid invoices: {len(unpaid)} totalling {gbp(sum(num(i.get('amount_gbp')) for i in unpaid))} · overdue: {len(overdue)}",
           f"- AI and tool costs this month: {gbp(ai_tool_cost)}"]
    md += [f"  - Margin warning: {c} costs {gbp(cost)} vs fee {gbp(fee)}" for c, cost, fee in margin_flags]

    md += ["", "## Agents",
           f"- Tool actions in the last 24h: {sum(by_agent.values())}" + (" (" + ", ".join(f"{a} {n}" for a, n in by_agent.most_common()) + ")" if by_agent else ""),
           f"- Tasks completed (all time): " + (", ".join(f"{a} {n}" for a, n in agent_done.most_common()) or "none"),
           f"- Escalated to you (pending approvals): {len(pending)}",
           f"- Paused agents: {', '.join(paused) if paused else 'none'}"]
    return "\n".join(md) + "\n"


def ai_note(briefing):
    """Ask Claude for the founder's top three priorities from the numbers above."""
    import anthropic

    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model="claude-opus-5-5",
        max_tokens=2000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "low"},
        system=(
            "You are the Chief of Staff agent for Gabrion, a one-founder AI services company. "
            "From the briefing, write at most three numbered priorities for the founder today, "
            "one line each, most urgent first. Pending approvals come first because agents are "
            "waiting on them. Use only facts in the briefing; do not invent clients or numbers. "
            "UK English, no preamble."
        ),
        messages=[{"role": "user", "content": briefing}],
    )
    if response.stop_reason == "refusal":
        return None
    return "".join(b.text for b in response.content if b.type == "text").strip()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--memory", default=os.path.join(ROOT, "memory"))
    p.add_argument("--out", default=os.path.join(ROOT, "briefings"))
    p.add_argument("--date", help="YYYY-MM-DD, default today")
    p.add_argument("--ai", action="store_true", help="add Claude's top-three priorities")
    p.add_argument("--print", action="store_true", help="also print to the terminal")
    a = p.parse_args()

    today = day(a.date) if a.date else date.today()
    text = build(a.memory, today)
    if a.ai:
        try:
            note = ai_note(text)
            if note:
                text = text.replace("\n## Waiting for you", f"\n## Today's top three\n{note}\n\n## Waiting for you", 1)
        except Exception as e:  # briefing still useful without the note
            print(f"AI note skipped: {e}", file=sys.stderr)
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"{today.isoformat()}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text if a.print else f"Briefing written to {path}")


if __name__ == "__main__":
    main()
