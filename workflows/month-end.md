# Workflow: month end

**Lead:** finance-admin · **Ends with:** the month report in the briefing; payments out in the approval queue

| # | Step | Who | Reviewer | Output |
|---|---|---|---|---|
| 1 | Invoices for signed work; chase late ones | finance-admin with `support-finance-tracker` | | Drafts in `memory/finance/` |
| 2 | Book costs, incl. AI and tool cost per client | finance-admin with `accounts-payable-agent` | | `costs.csv` |
| 3 | Cash and forecast | `finance-fpa-analyst` | `finance-bookkeeper-controller` | Month report |
| 4 | Tax and VAT notes (confirm with your accountant) | `finance-tax-strategist` | | Notes |
| 5 | Payments out to the approval queue | finance-admin | | Queue items `payment-out` |
