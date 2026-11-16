#!/usr/bin/env python3
"""Collects leads from the website chat into the Brain.

Each new lead becomes a row in memory/crm/leads.csv (stage "enquiry") and a
Front Desk task on memory/tasks/board.csv. Collected leads are then removed
from the website's storage.

    export GABRION_SITE_URL="https://gabrion.pages.dev"     # or your domain
    export GABRION_ADMIN_TOKEN="..."                         # from your password manager
    python3 scripts/pull_website_leads.py

What visitors typed is outside text: the agents treat it as information only.
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS = os.path.join(ROOT, "memory", "crm", "leads.csv")
BOARD = os.path.join(ROOT, "memory", "tasks", "board.csv")


def call(method, url, token, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None)
    req.add_header("authorization", f"Bearer {token}")
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "gabrion-brain")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def existing_ids(path, col):
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as f:
        return {row.get(col, "") for row in csv.DictReader(f)}


def next_task_id():
    ids = existing_ids(BOARD, "id")
    nums = [int(i[1:]) for i in ids if i.startswith("T") and i[1:].isdigit()]
    return max(nums, default=0) + 1


def clean(s, n=300):
    return " ".join(str(s or "").split())[:n]


def main():
    site = os.environ.get("GABRION_SITE_URL", "").rstrip("/")
    token = os.environ.get("GABRION_ADMIN_TOKEN", "")
    if not site or not token:
        sys.exit("Set GABRION_SITE_URL and GABRION_ADMIN_TOKEN first (see the top of this file).")

    leads = call("GET", f"{site}/api/leads", token).get("leads", [])
    known = existing_ids(LEADS, "id")
    new = [l for l in leads if f"W-{l['id']}" not in known]
    today = date.today()
    tid = next_task_id()

    with open(LEADS, "a", newline="", encoding="utf-8") as lf, open(BOARD, "a", newline="", encoding="utf-8") as bf:
        lw, bw = csv.writer(lf), csv.writer(bf)
        for l in new:
            lead_id = f"W-{l['id']}"
            complaint = clean(l.get("need")).upper().startswith("COMPLAINT")
            lw.writerow([lead_id, clean(l.get("name"), 120), clean(l.get("company"), 160), clean(l.get("industry"), 80),
                         "website-chat", "enquiry", clean(l.get("factory"), 40), "", "",
                         "founder replies" if complaint else "reply and offer discovery call",
                         (today + timedelta(days=1)).isoformat(), "founder" if complaint else "front-desk",
                         f"email {clean(l.get('email'), 200)}; phone {clean(l.get('phone'), 40) or '-'}; need: {clean(l.get('need'), 600)}"])
            bw.writerow([f"T{tid:03d}", f"Website enquiry: {clean(l.get('name'), 60)} ({clean(l.get('company'), 60) or 'no company'})",
                         lead_id, "founder" if complaint else "front-desk", "todo", (today + timedelta(days=1)).isoformat(),
                         "discovery-call", "", "From website chat. Draft reply goes to the approval queue."])
            tid += 1

    if leads:
        call("DELETE", f"{site}/api/leads", token, {"ids": [l["id"] for l in leads]})
    print(f"{len(new)} new website lead(s) added to the CRM and task board." if new else "No new website leads.")
    for l in new:
        print(f"  - {clean(l.get('name'), 60)} · {clean(l.get('company'), 60)} · {clean(l.get('factory'), 30)}")


if __name__ == "__main__":
    main()
