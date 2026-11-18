# Money report · November 2026 (to 2026-11-18) · DEMO, fictional

Prepared by finance-admin for the founder · tasks D010, D008 · nothing sent

## Cash
- Bank balance 2026-11-17: **£6,420** (demo/memory/finance/cash.csv). No money in or out recorded since.
- November costs booked so far: **£86.69** (£46.19 Gabrion overhead, £40.50 attributed to clients).

## Unpaid invoices
| Invoice | Client | Amount | Due | Status |
|---|---|---|---|---|
| INV-0007 | willow-rose | £135 (£95 after credit note) | 2026-11-03 | **15 days overdue**; £40 line disputed and wrong |
| INV-0008 | copper-pot | £750 (50% deposit of £1,500) | 2026-12-02 | draft |
| INV-0009 | fenwick-physio | £450 (50% deposit of £900) | terms not in contract | draft |
| INV-0010 | northfield-accountants | £750 (100% on signature) | 2026-12-02 | draft |
| INV-0011 | brightside-lettings | £1,600 (50% deposit of £3,200) | terms not in contract | draft |

Drafts total **£3,550**; with the £95 from Willow & Rose, **£3,645** is due to come in. Under the onboarding playbook, work starts once the deposit is paid, but builds D011 to D014 are already on the board (D014 is in progress). Founder to decide whether to wait for deposits.

## Willow & Rose £40 query (D008)
The £40 line was wrong. The plan includes 1 hour of changes a month. October had two changes by email, 15 min and 20 min, 35 min in total, so no extra time was chargeable. The changes log says the 20 min was "logged by mistake as 1 hour extra". INV-0007 is unpaid, so the fix is a **£40 credit note, not a refund**: no money goes out. Waiting on approval A-0901. The 14-day reminder for the remaining £95 is drafted but waits on A-0902. No approved reminder template exists yet, and no 7-day reminder was recorded.

## Cost per client, November (AI + tools + hosting vs monthly fee)
| Client | Nov cost | Monthly fee | Cost / fee | Fee status |
|---|---|---|---|---|
| willow-rose | £7.10 (hosting £4.00, chat AI £3.10) | £95 | 7.5% | live since 2026-09-01 |
| fenwick-physio | £11.40 (voice test number + minutes) | £180 | 6.3% | **not started**, from launch |
| northfield-accountants | £22.00 (n8n instance share, sandbox) | £60 | **36.7%, FLAG** | **not started**, from switch-on |
| copper-pot | £0.00 | £95 | 0% | **not started**, from launch |
| brightside-lettings | £0.00 | £150 | 0% | **not started**, from launch |

- **Flag: Northfield Accountants.** Its £22 n8n share is above 30% of the £60 fee, even in a partial month and while still only a sandbox. Until switch-on there is no fee, so the cost is being absorbed now. If the instance share stays at £22 once live, this client is above the threshold. Options for the founder: a cheaper or shared instance, or reviewing the fee. Any price change needs approval.
- Fenwick: the £180 fee includes 600 platform minutes. Watch per-minute cost once live.
- Only Willow & Rose is actually paying a monthly fee in November. The other four fees have not started.
- Gabrion overhead (not per client): Anthropic API £38.20, 1Password £7.99.

## Founder decisions waiting
1. **A-0901**: £40 credit note on INV-0007 (refund type).
2. **A-0902**: send the reply and £95 reminder to Willow & Rose.
3. **A-0903**: send INV-0008 to INV-0011, and set payment terms for Fenwick and Brightside. VAT treatment is not stated in the contract summaries.
