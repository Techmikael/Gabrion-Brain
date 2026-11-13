# Playbook: Discovery call

**Owner:** founder on the call, solutions-architect prepares and writes up · **Client journey:** step 3 · **Approval:** none (the proposal that follows needs one)

## Before the call (solutions-architect, the day before)
1. Read the lead row in `memory/crm/leads.csv` and Sales' research notes.
2. Look at the prospect's website, Google reviews and booking or contact flow. Note 3 visible problems (missed calls, no online booking, slow site, manual admin).
3. Pick the 1–2 factories most likely to fit and the demo to show (website template, AI receptionist test number).
4. Write a one-page brief in `clients/<slug>/discovery/brief.md` (copy `clients/_template/`).

## On the call (30 minutes, founder)
| Minutes | Do |
|---|---|
| 0–3 | Thank them, agree the agenda and the 30-minute end time |
| 3–15 | Their business today: what takes the most time, what loses money, what they have tried |
| 15–20 | Numbers: calls or enquiries a week, how many are missed, staff hours on admin, average sale value |
| 20–25 | Show the matching demo for 5 minutes, no more |
| 25–30 | Budget band, who decides, timing; agree next step: "I'll send a proposal by <date>" |

Good questions: "Walk me through what happens when a new customer gets in touch." · "What happens to calls after 6pm?" · "If this worked perfectly, what would be different in 3 months?"

Do not quote a price on the call. Say: "I'll send a fixed price with the proposal by <date>."

## After the call (solutions-architect, same day)
1. Save the transcript or notes in `clients/<slug>/discovery/`.
2. Write `requirements.md`: goals, must-haves, nice-to-haves, systems they use, data involved (flag any personal or health data), success measure.
3. Update the lead: stage `proposal`, factory, next action "proposal", next date within 3 working days.
4. Start `playbooks/proposal.md`.
