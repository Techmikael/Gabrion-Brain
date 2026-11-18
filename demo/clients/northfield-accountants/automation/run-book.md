# Run-book: Northfield Accountants, invoice capture (DEMO)
Owner: automation-builder (build) · operations-support (run) · Factory: `factories/automation.md` (Invoice capture)
Workflow file: `northfield-invoice-capture.n8n.json` · Sandbox simulator: `simulate.py`
Status 2026-11-18: built and tested in the sandbox only. **Not switched on for real data** until approval A-0601 is `APPROVED` by the founder.

## 1. What it does
1. **Trigger**: every 5 minutes, n8n checks the bills mailbox (Microsoft 365) for new mail with attachments. Sandbox: test mailbox; live: bills@northfield-acc.example.com (only after approval).
2. **Split**: one item per PDF attachment. An email with no PDF goes to the error branch.
3. **Read PDF text** and **Extract invoice fields**: supplier, invoice number, invoice date (converted to ISO YYYY-MM-DD; UK dd/mm/yyyy assumed), net, VAT, total, currency (GBP). Same rules as `simulate.py`.
   - VAT 0.00 is accepted only if the invoice says "no VAT" / "not VAT registered".
   - Net is taken from a "Net"/"Subtotal" label, otherwise total minus VAT.
   - Check: net + VAT must equal total (to 1p).
4. **Duplicate check**: looks up the invoice number and supplier in Xero; if it already exists, the item goes to the error branch, not Xero again.
5. **Xero**: creates an Accounts Payable bill in status **DRAFT** (never authorised, never paid). Northfield staff review and approve bills in Xero themselves.
6. The email is moved to the folder `Gabrion/Processed`.

**Error branch** (any of: no PDF, not an invoice, missing field, totals do not add up, duplicate, PDF unreadable, Xero error, workflow crash via the Error Trigger): builds an alert holding only the file name or message ID, the reasons and the execution ID (never the email body or the attachment), emails it to operations-support (`Gabrion / ops alerts SMTP`), and moves the email to `Gabrion/Needs review`.

Credentials (attach in n8n from the password manager; never paste values into nodes):
- `Client – Northfield / n8n sandbox` (Microsoft 365 mailbox OAuth in the sandbox)
- `Client – Northfield / Xero demo org` (Xero OAuth, sandbox org "Northfield DEMO")
- `Gabrion / ops alerts SMTP` (Gabrion alert mailbox)
Live credentials will be separate items, named when the switch-on is approved.

Data: supplier names and amounts only (business data). n8n keeps no data for successful executions (`saveDataSuccessExecution: none`). Failed executions are kept so they can be re-run; delete them once they are resolved (section 4).

## 2. After import (one-off setup in the sandbox)
1. Import the JSON in n8n (Workflows → Import from file). It imports **inactive**.
2. Attach the three credentials above by item name.
3. Replace the placeholders: `REPLACE_WITH_SANDBOX_INBOX_FOLDER_ID`, `REPLACE_WITH_PROCESSED_FOLDER_ID`, `REPLACE_WITH_NEEDS_REVIEW_FOLDER_ID`, `REPLACE_WITH_SANDBOX_TENANT_ID` (Config node), and set Settings → Error workflow to this workflow (`REPLACE_WITH_THIS_WORKFLOW_ID_AFTER_IMPORT`).
4. Send the four sandbox test invoices (as PDFs) to the sandbox mailbox and check you get 3 DRAFT bills and 1 ops alert, the same as `python3 simulate.py`.

## 3. How to pause it
- **Pause now**: in n8n open the workflow and switch **Active** off. Mail keeps arriving in the mailbox and simply waits; nothing is lost. Switch it back on to resume; the trigger picks up mail received while it was off.
- **Emergency (all Gabrion agents)**: the founder creates `memory/PAUSED`; for this agent only, `memory/paused/automation-builder`. Agents never delete these files.
- Switching it **on** for real client data needs founder approval in `memory/approvals/queue.md`. Operations-support may pause it alone; turning it back on after an incident is a rollback to the last approved version.

## 4. How to re-run a failed item
1. Read the ops alert: it names the item, the reason(s) and the execution ID.
2. Open n8n → Executions → that execution ID.
3. Fix the cause:
   - *Not an invoice / no PDF*: leave it in `Gabrion/Needs review`; tell Northfield's contact through the normal ticket reply (no promises). Nothing to re-run.
   - *Missing field / totals do not add up / PDF unreadable (e.g. scanned image)*: Northfield keys the bill in Xero by hand, or the supplier resends a text PDF. Changing extraction rules is a new fix: it needs founder approval and a sandbox re-test (`simulate.py`, 5 runs).
   - *Duplicate*: check the existing draft in Xero; usually nothing to do.
   - *Xero error (token expired, rate limit, Xero down)*: reconnect the Xero credential from the password manager or wait, then re-run.
4. **Re-run**: in the execution view click **Retry → With currently saved workflow**, or move the email from `Gabrion/Needs review` back to the inbox so the trigger picks it up again. The duplicate check stops a second draft bill being created.
5. Confirm a DRAFT bill appeared in Xero (or the item is closed), then delete the failed execution.
6. Write what happened, the fix and how to prevent it into this run-book (known fixes list below).

## 5. Known fixes
- (none yet)

## 6. Sandbox simulator
`python3 -I simulate.py` (Python 3, standard library only) runs the extraction on `../sandbox/*.txt` 5 times, writes `output/run-N-draft-bills.json` and `output/run-N-ops-notifications.json`, and exits non-zero if any run fails or the runs disagree. Last recorded output: `output/simulator-runs-2026-11-18.txt`.
