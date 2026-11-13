# Factory: Automation
Owner: automation-builder · Run: managed monthly, or handed over

## Tested workflow library (build each once, reuse)
| Workflow | Trigger | Does |
|---|---|---|
| Invoice capture | Email with PDF invoice | Extracts supplier, date, amount → accounting draft bill |
| Lead follow-up | New web form or missed call | Sends acknowledgement, adds to CRM, reminds owner after 24h |
| Booking sync | New booking | Copies to calendar, sends confirmation and reminder |
| Weekly report | Monday 07:00 | Pulls key numbers, emails a one-page summary |

## Checklist
- [ ] Runs end to end on test data 5 times without error
- [ ] Error branch notifies operations-support
- [ ] No personal data stored outside the client's own tools
- [ ] Credentials come from the password manager, not pasted into nodes
- [ ] Monthly run volume and cost estimated for Finance
- [ ] Run-book written: what it does, how to pause it, how to re-run a failed item
