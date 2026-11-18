# Founder approval queue

Agents add items at the bottom. Only the founder changes `Status`: `APPROVED`, `CHANGE` (with a note: the agent redoes it and saves the note as a founder lesson) or `REJECTED`. Keep the queue short: approve, reject or ask for changes every morning.

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
