# DRAFT credit note CN-0001 · Willow & Rose · DEMO · NOT ISSUED (needs approval A-0901)

- Against: INV-0007 (issued 2026-10-20, due 2026-11-03, £135, unpaid)
- Amount: £40.00 credit (removes the "extra changes 1h" line in full)
- Revised amount due on INV-0007: £95.00 (managed website, November 2026)
- Why a credit note, not a refund: INV-0007 has not been paid (no paid_on date in invoices.csv), so no money goes back out of Gabrion's accounts. Nothing to refund; the balance is simply reduced.

## Facts checked (D008)
- Contract (clients/willow-rose/README.md): managed £95/month includes 1 hour of changes a month. Extra changes £40/hour, only when the client asks in writing.
- Changes in October 2026 (clients/willow-rose/changes-log.md):
  - 2026-10-03 balayage price change, 15 min (requested by email)
  - 2026-10-21 gift voucher line, 20 min (requested by email); log says it was "logged by mistake as 1 hour extra (£40) on invoice INV-0007"
  - Total: 35 min, inside the 1 hour included. Extra chargeable time: 0. Correct extra charge: £0.
- Also odd: INV-0007 is dated 2026-10-20, a day before the 2026-10-21 change it charges for. Worth checking how the line was added.
- Priya says "we only asked for one change"; the log shows two written requests. Either way the total is within the included hour, so the £40 is wrong regardless.

## If approved
1. Mark CN-0001 issued; record in invoices.csv as `CN-0001,willow-rose,Credit note against INV-0007: extra changes line charged in error,-40,<date>,,issued,`
2. Send the reply/reminder in memory/outbox/finance-reminder-INV-0007-willow-rose.md (approval A-0902).
