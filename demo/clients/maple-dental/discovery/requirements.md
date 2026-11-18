# Requirements — Maple Dental Care (DEMO, fictional)

Source: `clients/maple-dental/discovery/call-notes-2026-11-17.md` (call 2026-11-17, founder + Marcus Reid, practice manager). Written 2026-11-18 by solutions-architect per `playbooks/discovery-call.md`. Status: draft, internal.

## The practice today
- 2 dentists, 1 hygienist, 2 reception staff; Harrogate; NHS and private.
- About 160 calls a week; reception estimate 30–40 unanswered, mostly 08:00–09:30 and lunchtime.
- After 17:30: voicemail only; "half don't leave a message".
- Call mix: booking or moving check-ups and hygiene about 60%; "are you taking NHS patients?" about 15%; emergencies or toothache about 10%; other about 15%.
- Appointments in Dentally. Website 8 years old, not mobile-friendly, no online booking link.

## Goals
1. Every call answered, including peaks, lunch and after 17:30.
2. Check-ups and hygiene appointments booked or moved without reception.
3. Emergencies routed to the emergency slot list quickly and safely.
4. A modern, mobile-friendly website with online booking.
5. Before the January rush.

## Must-haves
| # | Must-have | Covered by |
|---|---|---|
| M1 | Answer calls when reception is busy, at lunch and out of hours, in a natural voice ("mustn't sound like a robot") | Factory: AI receptionist |
| M2 | Answer common questions, including "we're not taking NHS patients right now" (wording controlled by the practice, easy to change) | Factory: AI receptionist (knowledge base) |
| M3 | Book and move check-ups and hygiene appointments in Dentally | AI receptionist factory for the booking conversation; **Dentally integration is custom** (C1) |
| M4 | Emergencies/toothache sent to the emergency slot list or to a human | Factory: AI receptionist covers "transfer or urgent message"; **the triage questions and rules are custom** (C2) |
| M5 | Modern, mobile-friendly website with an online booking link | Factory: Websites (new `clinic` config needed; only `salon` exists) |
| M6 | Patient health information protected | All factories (UK GDPR, DPA) plus the extra controls in "Data involved" below |
| M7 | Website and call scripts compliant with GDC advertising guidance | Websites + AI receptionist content; practice to confirm (see "Compliance") |

## Nice-to-haves
- N1 Missed-call / voicemail follow-up text or email (Automation factory: Lead follow-up).
- N2 Weekly calls report for Marcus: calls handled, bookings made, emergencies (Automation factory: Weekly report).
- N3 Staff onboarding session to reduce resistance (custom, C3).
- N4 New-patient enquiry capture for private patients (worth about £400/yr each).

## Systems they use
- Dentally (appointments, patient records). API access and which appointment types/slots can be booked by a third party: **to confirm** with Dentally and the practice.
- Existing phone line and provider: **to confirm** (call forwarding on busy/no-answer/out of hours).
- Existing website and domain: built by a family member; domain ownership and login **to confirm**.

## Data involved (flag: health data)
- **Special category data (health) under UK GDPR Article 9.** Callers will describe symptoms, pain, treatment history; bookings link a name to dental care. Call recordings, transcripts and summaries will contain health data.
- Personal data: patient names, phone numbers, dates of birth (if used to find the patient in Dentally), NHS/private status.
- Needed before build on real data: data processing agreement; a DPIA (the practice is the controller; we support it); decide whether to record calls at all, and retention period; summaries sent only to a practice-controlled mailbox; no health data in Gabrion logs or outside the client vault and the practice's own tools; no use for training.
- The AI receptionist must not give clinical advice or diagnose; emergency rules must be written and signed off by the principal dentist.

## Compliance (flag: GDC)
- GDC guidance on advertising and the Standards for the Dental Team apply to the website and anything the receptionist says about services. To check with the practice: registrants' names, GDC numbers and qualifications shown correctly; no misleading claims, guarantees or unverifiable "best" claims; prices, if shown, clear and accurate; NHS/private status clear; complaints procedure and practice details shown. CQC registration and rating display may also apply. ASA/CAP code applies to marketing.
- Gabrion does not give legal or regulatory advice: the practice (Dr Amira Hassan as registrant) signs off all wording.

## Decision makers and timing
- Marcus Reid (practice manager) and Dr Amira Hassan (principal dentist). Timing: live before the January rush.
- Budget band stated: "a few thousand to set up, a couple of hundred a month is fine if it works".

## Success measures (agree in proposal)
- Unanswered calls cut from 30–40 a week to near zero (all calls answered by a person or the AI).
- Share of check-up/hygiene bookings made without reception.
- Emergencies reaching the emergency list the same day.
- Website passes the factory checklist (mobile, Lighthouse ≥ 85) and online bookings start arriving.
- Value check: one new private patient (~£400/yr) or roughly 7 recovered check-ups (£55) a month.
