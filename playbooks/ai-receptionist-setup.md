# Playbook: AI receptionist setup

**Owner:** voice-chat-builder · **Factory:** `factories/ai-receptionist.md` · **Approval:** going live on the client's real number

1. **Intake.** In `clients/<slug>/intake.md`: business hours, services and prices to quote, booking rules, calendar, who to transfer to and when, emergency and complaint handling, voice and greeting, number to forward.
2. **Template.** Copy `templates/ai-receptionist/config.example.yaml` and `knowledge-base.example.md` into `clients/<slug>/receptionist/` and fill them in. Use the industry notes in the template README.
3. **Build on a test number.** Load the prompt (`templates/ai-receptionist/system-prompt.md` with the config filled in) and knowledge base into the voice platform (Vapi or Retell) on a Gabrion test number. Connect the calendar in test mode.
4. **Test calls.** Run every script in `templates/ai-receptionist/test-calls.md`. Record pass/fail and the call recording link in `clients/<slug>/receptionist/checklist.md`.
5. **Client trial.** Client rings the test number for 2–3 days and sends changes.
6. **Approval.** Add an approval item: type `go-live`, prepared work = config + checklist.
7. **Launch.** After APPROVED: set call forwarding on the client's number (out of hours first, then all calls if they want), monitoring on, hand to operations-support.
8. **Review at 2 weeks.** Read 20 call summaries, fix the knowledge base, report bookings made and calls answered.
