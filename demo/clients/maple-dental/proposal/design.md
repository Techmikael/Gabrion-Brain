# Design — Maple Dental Care (DEMO, fictional)

Internal design note, 2026-11-18, solutions-architect. From `clients/maple-dental/discovery/requirements.md`. Not for the client until the proposal is approved.

## Factories used
| Part | Factory | Owner | Template |
|---|---|---|---|
| AI receptionist | `factories/ai-receptionist.md` | voice-chat-builder | `templates/ai-receptionist/` + practice FAQs and Dentally calendar |
| Website | `factories/websites.md` | web-builder | new `clinic` config copied from `salon.json` (clinic listed as "to add") |
| Optional: missed-call follow-up, weekly report | `factories/automation.md` | automation-builder | library workflows "Lead follow-up", "Weekly report" |

## Custom (not covered by any factory; priced separately; risks in approval)
| # | Item | Why custom | Risk | Mitigation |
|---|---|---|---|---|
| C1 | Dentally integration (read free slots, create/move check-up and hygiene bookings) | No Dentally connector in any factory; "Booking sync" only copies bookings to a calendar | Dentally API access/partner terms unknown; double-bookings; wrong patient matched; delivery delay before January | Confirm API access first; fall back to "request booking" (AI takes details, reception confirms in Dentally) if no write access; test on a Dentally sandbox/test practice only |
| C2 | Emergency triage flow to the emergency slot list | Factory only transfers or takes an urgent message; triage rules are clinical | AI seen as giving clinical advice; a serious case (swelling affecting breathing/swallowing, trauma, uncontrolled bleeding) not escalated | Rules written and signed off by Dr Hassan; AI asks set questions only, never diagnoses; red-flag answers direct to 999/NHS 111 and the urgent line; test-call scripts for each path |
| C3 | Staff onboarding session (nice-to-have) | Not in a factory | Low | Short session plus one-page guide |

## How it fits together
1. Practice line forwards on busy, no answer and after 17:30 to the AI receptionist number (forwarding the real number is a go-live approval).
2. Greeting gives "Maple Dental Care" and says it is an AI assistant when asked; natural voice chosen with Marcus.
3. Intents: book/move check-up or hygiene (C1), NHS availability (knowledge base; practice can change wording), emergency (C2), other (message to reception).
4. Summaries go to a practice-controlled mailbox only; recording off unless the practice decides otherwise and the notice is given.
5. Website: clinic config, mobile-first, online booking button to Dentally's patient booking page (if enabled) or to the request form; GDC/CQC details and privacy notice; no tracking before consent.

## Data design (health data)
- Controller: the practice. Gabrion: processor under a DPA. DPIA completed with the practice before real data.
- Health data stays in Dentally, the voice platform (EU/UK region if available) and the practice mailbox; nothing in Gabrion repo, logs or other vaults. Retention of transcripts set short and agreed.
- Credentials (Dentally, phone platform) only in the password manager, referred to by item name.

## Build order and timeline (target live before January rush)
- Week 1 (from deposit): confirm Dentally access and phone forwarding; knowledge base; triage rules drafted for Dr Hassan.
- Week 2: receptionist on a Gabrion test number; all test calls; website on staging.
- Week 3: practice review of both; fixes; checklists passed.
- Week 4: approved launch (go-live approvals for number forwarding and website).
- Dependency: if Dentally write access is not available in week 1, launch with request-booking fallback and add C1 later.

## Cost check for Finance
- About 160 calls/week; AI expected to handle the 30–40 missed plus out-of-hours calls, more if the practice routes more. Platform minutes and AI costs must stay under 30% of the monthly fee (pricing rule); minutes allowance is `?` on the pricing sheet.
