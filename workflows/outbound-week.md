# Workflow: outbound week

**Lead:** sales · **Ends with:** a batch of first messages in the approval queue

| # | Step | Who | Reviewer | Output |
|---|---|---|---|---|
| 1 | Pick this week's segment from the ideal client profile | sales with `sales-outbound-strategist` | | Segment and reason |
| 2 | Find 10–20 prospects on public sources | sales with `sales-outreach` | | New rows in `memory/crm/leads.csv` |
| 3 | Research each: visible problems, decision maker | sales | `testing-reality-checker`: facts are real and sourced | Notes per lead |
| 4 | Write the offer and the sequence (message + follow-ups) | `sales-offer-lead-gen-strategist`, `sales-outbound-strategist` | `sales-coach` | Drafts in `memory/outbox/` |
| 5 | Check consent rules (UK PECR; Denmark: no cold e-mail or SMS) | sales | `support-legal-compliance-checker` | Channel per lead |
| 6 | Add the batch to the approval queue as `first-message` | sales | | Queue items |
| 7 | Friday: pipeline review | `sales-pipeline-analyst` | | Two-line summary for the briefing |
