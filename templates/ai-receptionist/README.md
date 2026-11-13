# AI receptionist template

Platform-neutral: the same files load into Vapi, Retell or any voice-agent platform that takes a system prompt, a knowledge base and tool/function definitions. Phone numbers come from Twilio (or the platform's own).

| File | What it is |
|---|---|
| `config.example.yaml` | Per-client settings: business details, hours, transfer rules, booking, voice |
| `system-prompt.md` | The receptionist's instructions with `{{placeholders}}` filled from the config |
| `knowledge-base.example.md` | FAQ format the client's answers go into |
| `tools.json` | Function definitions: check availability, book, take message, transfer |
| `test-calls.md` | The test-call scripts that make up the go-live checklist |

## Industry notes
- **Salon / beauty:** patch test 48h before colour; deposits for long appointments; stylist preference.
- **Trades:** emergency triage first (gas smell → hang up and call 0800 111 999; water → stop-tap); collect postcode and photos by text.
- **Clinic:** never give medical advice; 999 / NHS 111 for urgent symptoms; minimum data on the call (name, number, reason in a few words).
- **Restaurant:** party size, date, time, dietary needs; large groups → message to manager.
