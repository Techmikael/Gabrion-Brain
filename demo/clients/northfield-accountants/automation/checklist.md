# Factory checklist: Northfield invoice capture (DEMO), 2026-11-18
Factory: `factories/automation.md` · Task: D013 · Built by automation-builder · Environment: sandbox, test data only

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Runs end to end on test data 5 times without error | **PASS (simulator)** | `python3 -I simulate.py`: 5 runs, 0 failed, identical output each run (digest 660be1cfa10e). `output/simulator-runs-2026-11-18.txt`, `output/run-1..5-*.json` |
| 2 | Error branch notifies operations-support | **PASS (simulator)** | invoice-004.txt (not an invoice) sent to error branch every run, alert addressed to operations-support. In n8n every failure path (no PDF, invalid, duplicate, PDF read, Xero error, crash via Error Trigger) is wired to "Build ops alert" → "Notify operations-support" |
| 3 | No personal data stored outside the client's own tools | **PASS** | Bills go to Northfield's Xero; email stays in Northfield's mailbox. Alerts carry file name / message ID and reasons only. n8n saves no successful-execution data. Simulator output stays in the client vault |
| 4 | Credentials come from the password manager, not pasted into nodes | **PASS** | JSON references `Client – Northfield / n8n sandbox`, `Client – Northfield / Xero demo org`, `Gabrion / ops alerts SMTP` by name, empty IDs; secret scan of the JSON found none |
| 5 | Monthly run volume and cost estimated for Finance | **PASS** | See below |
| 6 | Run-book written: what it does, how to pause, how to re-run a failed item | **PASS** | `run-book.md` sections 1, 3, 4 |

## Test results (each of the 5 runs)
| File | Supplier | Invoice no | Date | Net | VAT | Total | Route |
|---|---|---|---|---|---|---|---|
| invoice-001.txt | Aqua Office Supplies Ltd | AQ-5512 | 2026-11-03 | 189.50 | 37.90 | 227.40 | Xero DRAFT bill |
| invoice-002.txt | Brightwire IT Services | 000981 | 2026-11-07 | 450.00 | 90.00 | 540.00 | Xero DRAFT bill |
| invoice-003.txt | Coffee Corner Catering | CC/2026/118 | 2026-11-12 | 86.00 | 0.00 | 86.00 | Xero DRAFT bill (no VAT, not VAT registered) |
| invoice-004.txt | none | none | none | none | none | none | Error branch → operations-support (not an invoice) |

The n8n Code node uses a JavaScript port of the same rules; run under Node 22 against the four files it gave identical fields and errors. All Code-node scripts pass a syntax check.

## Limits of this test (be honest)
- There is **no real n8n or Xero access** in this run. "Sandbox" here means the Python simulator on the four test files; the workflow JSON has been built and statically checked (valid JSON, every connection points to an existing node, JS syntax OK) but not imported or executed in n8n. Before switch-on, the sandbox steps in run-book section 2 must be done and the 5 runs repeated in n8n against the "Northfield DEMO" Xero org.
- Test files are plain text; live invoices are PDFs. Scanned (image-only) PDFs have no text layer and will go to the error branch; OCR is not included.
- Four test files is a small sample. Expect some real supplier layouts to fail extraction at first; they fail safe (error branch, no bill created).
- The intake names no separate credential for the sandbox mailbox; the workflow assumes `Client – Northfield / n8n sandbox` holds it. Confirm in the password manager.

## Monthly volume and cost estimate (for Finance)
| Item | Estimate per month | Basis |
|---|---|---|
| Invoices processed | ~250 | Intake |
| n8n executions | ~275–300 | 250 invoice emails + ~10–20% non-invoice mail, duplicates and failures; empty polls do not create executions |
| Ops alerts | ~25–50 | Error branch, higher in the first month |
| Xero API calls | ~500–550 | 2 per invoice (duplicate check + create); well inside Xero's per-org daily limits |
| Microsoft Graph calls | ~9,000 polls + ~300 moves | Every 5 minutes; no charge on the client's M365 |
| n8n hosting | **£22.00** | Existing cost line 2026-11-05 "n8n cloud instance share" for this client; confirm it covers ~300 executions/month on the plan |
| Xero / M365 | £0 to Gabrion | Client's own subscriptions |
| AI / OCR | £0 | Rule-based extraction, no AI calls |
| **Total running cost to Gabrion** | **~£22/month** | Against the contract's £60/month managed fee from switch-on |

Finance should record no new cost until switch-on; this is an estimate, not a price.
