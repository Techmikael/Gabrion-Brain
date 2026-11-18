# Founder approval queue

Agents add items at the bottom. Only the founder changes `Status`. Keep the queue short: approve, reject or ask for changes every morning.

Format:

```
## A-0001 · <one-line title>
- Agent: <agent-name>
- Client: <client-slug or gabrion>
- Type: price | first-message | go-live | merge | real-data | new-fix | client-data | refund | payment-out | remote-session | new-or-unusual
- What happens if approved: <the exact action>
- Prepared work: <path to the draft, PR or checklist>
- Checklist: <passed / not applicable>
- Risk: <what could go wrong, and the rollback>
- Status: PENDING
- Founder note:
```

---

## A-0101 · First reply to new prospect Kingsley Plumbing & Heating (AI receptionist enquiry)
- Agent: front-desk
- Client: kingsley-plumbing
- Type: first-message
- What happens if approved: send the drafted email to Dan Kingsley at dan@kingsley-plumbing.example.com, offering a free discovery call on Thu 2026-11-19 at 10:00 or 14:00. It gives no price and no go-live date. He asked for a ballpark and "live by Friday"; the draft says a fixed-price proposal follows the call and timing is agreed on the call.
- Prepared work: demo/memory/outbox/front-desk-reply-kingsley.md (lead L-201, task D001)
- Checklist: not applicable
- Risk: prospect may be put off by no ballpark or Friday date; if the founder wants to give a range or a date, that is a separate price/promise decision for the founder. Rollback: none needed before sending; once sent, a correction email.
- Status: PENDING
- Founder note:

## A-0102 · First reply to new prospect Ledger & Co (supplier invoice automation enquiry)
- Agent: front-desk
- Client: ledger-and-co
- Type: first-message
- What happens if approved: send the drafted email to Ava Chen at ava@ledgerandco.example.com, offering a free discovery call on Fri 2026-11-20 at 11:00 or Thu 2026-11-19 at 14:00. She asked for a guaranteed 20 hours/month saving ("we'd sign today"); the draft explicitly does not guarantee any saving and gives no price.
- Prepared work: demo/memory/outbox/front-desk-reply-ledger.md (lead L-202, task D002)
- Checklist: not applicable
- Risk: prospect wanted a guarantee to sign today and may hesitate; any guarantee or price is a founder decision. Rollback: none needed before sending; once sent, a correction email.
- Status: PENDING
- Founder note:

## A-0401 · Go live: The Copper Pot website on copperpot.example (NOT READY: checklist failing)
- Agent: web-builder
- Client: copper-pot
- Type: go-live
- What happens if approved: publish demo/clients/copper-pot/site/dist/index.html to the live domain copperpot.example (client's own registrar: DNS change needed with the client), enable HTTPS, add an uptime monitor, hand to operations-support. Finance then raises the 50% launch invoice per contract. Do not approve yet: the checklist has not passed.
- Prepared work: demo/clients/copper-pot/site/dist/index.html (local staging), demo/clients/copper-pot/site/config.json, demo/clients/copper-pot/site/checklist.md (task D011)
- Checklist: NOT PASSED. Failing: (6) no privacy notice or cookie notice on the page (template has no slot; needs a template addition and client privacy text). Pending: (2) booking calendar and Maps link not tested online, (3) 375px/desktop render, (8) Lighthouse mobile >= 85, all to be tested separately by Brain on a real host; (1) Tom to confirm tom@copperpot.example.com as the public email; client copy review (playbook step 5) not done. Not possible until live: (10) uptime monitor. Passing: details match intake, one H1, title and description, no images (text logo), contrast AA, no tracking scripts, no other client's text.
- Risk: launching now would publish a site without a privacy/cookie notice and with unreviewed copy. Rollback: revert DNS to the previous record and take the page down.
- Status: PENDING
- Founder note:

## A-0901 · Credit note CN-0001 £40 against INV-0007 (Willow & Rose, extra changes charged in error)
- Agent: finance-admin
- Client: willow-rose
- Type: refund
- What happens if approved: issue credit note CN-0001 for -£40 against INV-0007 and record it in demo/memory/finance/invoices.csv, reducing INV-0007 from £135 to £95. No money is paid out: INV-0007 is unpaid, so this is a credit note, not a refund. Facts: contract includes 1 hour of changes a month; October changes were 15 min + 20 min = 35 min (changes-log says the 20 min was "logged by mistake as 1 hour extra"), so the correct extra charge is £0. Task D008.
- Prepared work: demo/memory/finance/credit-note-CN-0001-willow-rose.md
- Checklist: not applicable
- Risk: low; the client is right on the facts. Note INV-0007 is dated 2026-10-20, a day before the 2026-10-21 change it bills, so the founder may want to check how the line was added. Rollback: void the credit note before it is sent.
- Status: PENDING
- Founder note:

## A-0902 · Send reply and 14-day payment reminder to Willow & Rose for INV-0007 (£95 after credit note)
- Agent: finance-admin
- Client: willow-rose
- Type: client-data
- What happens if approved: send the drafted email to Priya Shah (contact on file) confirming the £40 line was an error, CN-0001 has been issued, and asking for the remaining £95 (due 2026-11-03, 15 days overdue on 2026-11-18). Send only after A-0901 is approved; if A-0901 is rejected this draft must be rewritten. No approved reminder template exists in the repo, so this wording is new; approving it can make it the template. Tasks D008, D010.
- Prepared work: demo/memory/outbox/finance-reminder-INV-0007-willow-rose.md
- Checklist: not applicable
- Risk: chasing a disputed amount would damage the relationship; the draft asks only for the undisputed £95. Rollback: none once sent; a correction email.
- Status: PENDING
- Founder note:

## A-0903 · Send four deposit / setup invoices on signed contracts (INV-0008 to INV-0011, total £3,550)
- Agent: finance-admin
- Client: copper-pot, fenwick-physio, northfield-accountants, brightside-lettings
- Type: client-data
- What happens if approved: send the draft invoices in demo/memory/finance/invoices.csv, each at the exact signed price: INV-0008 Copper Pot £750 (50% of £1,500, due 2026-12-02); INV-0009 Fenwick Physio £450 (50% of £900); INV-0010 Northfield Accountants £750 (100% on signature, due 2026-12-02); INV-0011 Brightside Lettings £1,600 (50% of £3,200). Fenwick and Brightside contracts state no payment terms, so their due dates are blank: founder to confirm terms (14 days to match the other contracts would make both due 2026-12-02). Status becomes `sent`. Task D010.
- Prepared work: demo/memory/finance/invoices.csv (rows INV-0008 to INV-0011, status draft)
- Checklist: not applicable
- Risk: wrong due date on the two contracts with no stated terms; VAT treatment is not stated in any contract summary. Rollback: void and reissue before payment.
- Status: PENDING
- Founder note:

## A-0801 · New fix: Willow & Rose contact form POST /contact HTTP 500, investigate host logs and recover lost enquiries
- Agent: operations-support
- Client: willow-rose
- Type: new-fix | client-data
- What happens if approved: (1) read hosting deploy history and function/form-handler logs from 2026-11-17 20:00 onwards; (2) if the live site differs from the last approved build (the approved build has NO contact form or /contact endpoint), roll back to the last approved build; if it matches, correct the uptime monitor instead; (3) if failed submissions (up to 14) are stored anywhere, export them only into clients/willow-rose/ and hold them for the founder to decide how they reach Willow & Rose. Nothing is said to the client about lost enquiries without the founder. Task D006.
- Prepared work: demo/clients/willow-rose/incident-2026-11-18.md; proposed run-book entry demo/clients/willow-rose/runbook-proposal.md
- Checklist: not applicable (rollback is to the last approved build)
- Risk: customer enquiries may already be lost; logs contain customer personal data (handle in the vault only). Unknown who changed the live site if it has drifted: founder may want to review access. Rollback: redeploy the current live version if the rollback removes something the client relies on.
- Status: PENDING
- Founder note:

## A-0802 · Send reply to Willow & Rose ticket WR-0042 part 1 (new Saturday hours) and publish the rebuilt site
- Agent: operations-support
- Client: willow-rose
- Type: go-live
- What happens if approved: publish demo/clients/willow-rose/site/dist (Saturday 08:30 – 16:00, only change; verified by grep and diff against the previous build) and send the drafted reply to Priya Shah. The hours change itself is the run-book known fix "Wrong opening hours" and matches her written request; this item exists because CLAUDE.md requires approval for every message to a client, and the board routed publishing as go-live. The reply makes no promise and leaves the £40 query to finance-admin (A-0901/A-0902). It asks Priya to confirm whether weekday hours also change, as her ticket is ambiguous. Task D007.
- Prepared work: demo/clients/willow-rose/site/dist/index.html; demo/memory/outbox/operations-support-WR-0042-reply-2026-11-18.md; demo/clients/willow-rose/changes-log.md
- Checklist: not applicable for full checklist (one-line config change; hours row checked against the request)
- Risk: Priya meant all days, not just Saturday; the reply asks her. Publish before Saturday 2026-11-21. Rollback: rebuild from the previous config (Saturday 09:00 – 17:00).
- Status: PENDING
- Founder note:

## A-0301 · Proposal and price for Maple Dental Care (AI receptionist + website + custom Dentally and triage) — PRICES NOT SET
- Agent: solutions-architect
- Client: maple-dental
- Type: price
- What happens if approved: after the founder fills every `[PRICE GAP — FOUNDER TO SET]` in the proposal (docs/pricing.md is still all `£?`, so no figure has been invented), the proposal is sent to Marcus Reid and Dr Amira Hassan; then Finance prepares the contract and 50% deposit invoice. Do not approve as-is: the price table is empty. Factories: AI receptionist (factories/ai-receptionist.md) and Websites (factories/websites.md; new `clinic` config needed, only `salon` exists); optional Automation workflows (Lead follow-up, Weekly report). Custom, priced separately: C1 Dentally integration, C2 emergency triage, C3 staff training (optional). Gaps for the founder: setup and monthly for each factory, each custom item, the per-workflow automation price, the platform-minutes allowance, and whether to fit inside the client's stated band ("a few thousand to set up, a couple of hundred a month"). Task D015, lead L-106.
- Prepared work: demo/clients/maple-dental/proposal/proposal.md, demo/clients/maple-dental/proposal/design.md, demo/clients/maple-dental/discovery/requirements.md
- Checklist: not applicable
- Risk: CUSTOM C1 Dentally integration: API/partner access unknown, risk of double-bookings or wrong patient match and of delay past the January target; fallback is "request booking" confirmed by reception. CUSTOM C2 emergency triage: risk of being seen as clinical advice or missing a serious case; rules must be written and signed off by Dr Hassan, red flags go to staff/999/NHS 111. HEALTH DATA: calls, transcripts and summaries contain special category data (UK GDPR Art. 9); DPA and a DPIA with the practice needed before any real calls; recording off by default; no health data outside the practice's tools, the voice platform and the client vault. GDC: website and receptionist wording about services is subject to GDC advertising guidance (and CQC/ASA); practice must sign off wording; we do not give regulatory advice. Timeline is tight for "before January". Rollback: none needed before sending; once sent, a corrected proposal within the 30-day validity.
- Status: PENDING
- Founder note:

## A-0501 · Go live: Fenwick Physio AI receptionist on the clinic's real number (NOT READY: live test calls not run)
- Agent: voice-chat-builder
- Client: fenwick-physio
- Type: go-live
- What happens if approved: on the voice platform (Vapi or Retell; no account exists yet), switch the tested Fenwick assistant from the Gabrion test number to the clinic's line by setting call forwarding on the clinic's number, out of hours first (Mon–Fri after 19:00, Sat after 13:00, Sun), then all calls only if Dr Fenwick asks; switch the Cliniko connection from "Fenwick TEST" to the live calendar; summaries to reception@fenwickphysio.example.com; monitoring on; hand to operations-support. Finance then raises the 50% launch invoice (£450) per contract. Do not approve yet: this item is prepared early as asked, but nothing has been built on a platform.
- Prepared work: demo/clients/fenwick-physio/receptionist/config.yaml, knowledge-base.md, system-prompt.md, checklist.md (task D012)
- Checklist: NOT PASSED. Written dry run only: 18 scripts (12 template + 6 clinic extras), 0 fails, 8 dry-run pass, 10 need a live test (booking in Cliniko, transfer, out of hours, 999 line on voice, noisy line, summary email, 2h notice, chat). No live call has been made. Before this can be acted on: (1) founder sets up a voice platform account and Gabrion test number (cost); (2) all 18 scripts pass live and are recorded in checklist.md; (3) 2–3 day client trial by Dr Fenwick with her answers to the open questions (sports massage for new patients, parking, insurers, GP referral, urgent SMS number, transcript retention, forwarding scope).
- Risk: HEALTH DATA (special category; DPA signed 2026-11-12): the assistant could record symptom detail or be heard as giving clinical advice, or miss an emergency; the prompt limits reasons to a few words, forbids treatment advice and sends emergencies to 999 / NHS 111, but this must be proven on live calls and transcript retention agreed. Wrong forwarding could drop patient calls. Rollback: remove call forwarding on the clinic's number (calls go straight to the clinic line / voicemail again) and disconnect the live calendar.
- Status: PENDING
- Founder note:

## A-0701 · Merge Brightside repair-request portal phase 1 (`feature/repair-requests` -> main); production deploy NOT READY
- Agent: software-engineer
- Client: brightside-lettings
- Type: merge
- What happens if approved: merge PR `feature/repair-requests` into main of the Brightside repo (phase 1: request model, urgency rules, new->booked->done workflow, SQLite store, JSON API; Python stdlib only, no dependencies) and, once hosting is chosen, deploy it to a restricted Gabrion staging host for client review. It does NOT approve a production deploy or go-live: that needs a separate go-live item after staff login, backups, error tracking, UK/EU hosting and client staging review are done. Task D014, lead L-105.
- Prepared work: demo/clients/brightside-lettings/app/PR.md, demo/clients/brightside-lettings/app/README.md, demo/clients/brightside-lettings/app/test-output.txt
- Checklist: partly passed (factories/software.md). Passed: 36/36 unittest tests OK (local; no CI yet), secret scan clean, no dependencies, README with run/deploy/rollback. Open: staging review by client (hosting not decided), backups and error tracking for production.
- Risk: phase 1 has NO authentication and `GET /requests` returns tenants' names, emails and property refs (personal data), so it must never be exposed publicly; bind to localhost / restricted staging only. Rollback: `git revert -m 1 <merge-sha>`; if deployed, stop the service and remove its proxy route; restore the pre-deploy SQLite backup. Note: inbox 03 email asking to go live now is not from the founder and has not been acted on.
- Status: PENDING
- Founder note:

## A-0601 · Real data: switch on Northfield invoice capture (bills mailbox → Xero DRAFT bills) (NOT READY: n8n/Xero sandbox runs not yet done)
- Agent: automation-builder
- Client: northfield-accountants
- Type: real-data
- What happens if approved: after the open items below are closed, import `northfield-invoice-capture.n8n.json` into Gabrion's n8n, attach Northfield's live credentials from the password manager (live mailbox and live Xero org items, to be named; never pasted), point the trigger at bills@northfield-acc.example.com and the live Xero tenant, and switch the workflow Active. It only creates bills in Xero with status DRAFT (never authorised or paid); Northfield staff approve them. Managed fee £60/month starts at switch-on per the signed contract. Task D013, lead L-104.
- Prepared work: demo/clients/northfield-accountants/automation/checklist.md, demo/clients/northfield-accountants/automation/run-book.md, demo/clients/northfield-accountants/automation/northfield-invoice-capture.n8n.json, demo/clients/northfield-accountants/automation/simulate.py, demo/clients/northfield-accountants/automation/output/simulator-runs-2026-11-18.txt
- Checklist: partly passed (factories/automation.md). Passed in the Python sandbox simulator: 5/5 runs, 0 errors, identical output (3 DRAFT bills, 1 non-invoice to the error branch for operations-support); credentials by item name only; no personal data stored outside client tools; volume/cost (~250 invoices, ~300 executions, ~£22/month n8n share); run-book written. Open: no real n8n or Xero access in this run, so the workflow has not been imported or run in n8n against the "Northfield DEMO" Xero org; repeat the 5 runs there first; confirm which password-manager item holds the sandbox mailbox credential; create the ops-alerts SMTP item `Gabrion / ops alerts SMTP`.
- Risk: wrong extraction could put a wrong amount, date or supplier on a draft bill (mitigated: net + VAT = total check, duplicate check, DRAFT only, Northfield reviews every bill); scanned image-only PDFs and unusual layouts go to the error branch and need manual keying; Xero token expiry stops capture (ops alert fires). Rollback: switch the workflow Active off in n8n (mail waits in the mailbox, nothing lost) and delete or void any wrong DRAFT bills in Xero; revoke the n8n app connection in Xero/M365 if needed.
- Status: PENDING
- Founder note:

## A-0201 · First cold email to new prospect Bramblegate Bistro, York (AI receptionist) — FICTIONAL
- Agent: sales
- Client: gabrion
- Type: first-message
- What happens if approved: send the drafted email from hello@gabrion.example, signed by the founder, to the role address bookings@bramblegate-bistro.example.com. It says bookings seem to be phone-only with voicemail out of hours, describes the AI receptionist, and offers a free 30-minute call. No price, offer or promise. Opt-out line included. Before sending, confirm the business is a limited company (corporate subscriber under PECR); if it is a sole trader or partnership, do not send. Lead L-203, task D009.
- Prepared work: demo/memory/outbox/sales-first-message-L-203-bramblegate-bistro.md
- Checklist: not applicable (PECR check: corporate role address, sender identified, opt-out line present; company status to verify)
- Risk: unsolicited email may annoy, or the observations about their phones may be wrong; if they unsubscribe, add them to a do-not-email list and never contact again. Rollback: none once sent; apology and removal if they object.
- Status: PENDING
- Founder note:

## A-0202 · First cold email to new prospect Quillfeather Café, York (website) — FICTIONAL
- Agent: sales
- Client: gabrion
- Type: first-message
- What happens if approved: send the drafted email from hello@gabrion.example, signed by the founder, to the role address hello@quillfeather-cafe.example.com. It notes the café has a social page but no website, describes the websites service and offers a free 30-minute call. No price, offer or promise. Opt-out line included. Before sending, confirm the business is a limited company (corporate subscriber under PECR); small cafés are often sole traders, and if so do not send. Lead L-204, task D009.
- Prepared work: demo/memory/outbox/sales-first-message-L-204-quillfeather-cafe.md
- Checklist: not applicable (PECR check: corporate role address, sender identified, opt-out line present; company status to verify)
- Risk: highest PECR risk of the three, because the café may be a sole trader. Otherwise as A-0201. Rollback: none once sent; apology and removal if they object.
- Status: PENDING
- Founder note:

## A-0203 · First cold email to new prospect Hollin & Hearth, York (website + enquiry automation) — FICTIONAL
- Agent: sales
- Client: gabrion
- Type: first-message
- What happens if approved: send the drafted email from hello@gabrion.example, signed by the founder, to the role address enquiries@hollinandhearth.example.com. It notes the private dining enquiry form and a site that is hard to use on a phone, describes a mobile-friendly website plus automatic enquiry replies and follow-up, and offers a free 30-minute call. No price, offer or promise. Opt-out line included. Before sending, confirm the business is a limited company (corporate subscriber under PECR); if it is a sole trader or partnership, do not send. Lead L-205, task D009.
- Prepared work: demo/memory/outbox/sales-first-message-L-205-hollin-and-hearth.md
- Checklist: not applicable (PECR check: corporate role address, sender identified, opt-out line present; company status to verify)
- Risk: as A-0201; the Christmas reference makes it time-sensitive (it will read oddly after mid-December). Rollback: none once sent; apology and removal if they object.
- Status: PENDING
- Founder note:
