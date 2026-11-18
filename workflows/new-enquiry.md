# Workflow: new enquiry

**Lead:** front-desk · **Playbook:** `playbooks/discovery-call.md` (booking part) · **Ends with:** a reply in the approval queue

| # | Step | Who | Reviewer | Output |
|---|---|---|---|---|
| 1 | Read the enquiry; add or update the lead in `memory/crm/leads.csv` | front-desk | | Lead row, source, language |
| 2 | Qualify: fit, size, country, urgency | front-desk with `sales-discovery-coach` | | 3–5 questions still open |
| 3 | Draft the reply (Danish leads: in Danish, I/jer form) | front-desk with `support-support-responder` (`language-translator` for Danish) | `sales-coach`: clear, warm, one next step | Draft in `memory/outbox/` |
| 4 | Add to the approval queue as `first-message` | front-desk | | Queue item |
| 5 | After approval: send, then book the call | front-desk | | Task row updated |

Never quote a price. Never promise a date the founder hasn't agreed.
