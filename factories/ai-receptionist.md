# Factory: AI receptionist
Owner: voice-chat-builder · Run: managed monthly
Built from: `templates/ai-receptionist/` + the client's FAQs and calendar

## Checklist
- [ ] All scripts in `templates/ai-receptionist/test-calls.md` pass
- [ ] Says it is an AI assistant when asked; gives the business name in the greeting
- [ ] Never quotes a price that is not in the knowledge base
- [ ] Emergencies and complaints transfer to a human or take a message marked urgent
- [ ] Bookings land in the right calendar with name, phone and service
- [ ] Call summaries reach the client's chosen email
- [ ] Call recording notice given if recording is on
- [ ] Out-of-hours behaviour tested

## Run-book
- Calls not answered: check forwarding on the client's line, then platform status; fall back to voicemail forwarding.
- Wrong answer given: add the correct answer to the knowledge base, re-run the related test call.
