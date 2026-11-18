# Website checklist: The Copper Pot (DEMO)
- Date: 2026-11-18 · Agent: web-builder · Task: D011
- Factory: factories/websites.md · Build: demo/clients/copper-pot/site/dist/index.html (sha256 da1ea3b5…b03b9c1)
- Config: demo/clients/copper-pot/site/config.json (salon.json used for its structure only; no salon text kept)
- Staging: local folder only (no staging host in this demo)

**Overall: NOT READY FOR GO-LIVE.** 1 item failing, 2 pending client confirmation, 4 need a real host.

| # | Checklist item | Result | Evidence |
|---|---|---|---|
| 1 | Name, phone, email, address, hours match intake exactly | PASS (email needs client confirmation) | Grep of index.html: "The Copper Pot" x6, "01632 960371" x2 (+ tel:01632960371), "tom@copperpot.example.com" x3, "14 Fossgate, York YO1 9TA" x2; hours Monday Closed, Tuesday – Thursday 12:00–22:00, Friday – Saturday 12:00–23:00, Sunday 12:00–17:00 (intake's day abbreviations written out; times identical). The intake gives the owner's contact email, not a public business email; confirm with Tom before launch. |
| 2 | Every link and button works; booking link opens right calendar | PARTIAL: internal links PASS; external links pending | Anchors #top, #services, #about, #contact all have matching ids. 3 buttons go to https://booking.example.com/copperpot (matches intake). mailto/tel links correct. Booking calendar and the Google Maps directions link not checked online: pending, tested separately by Brain. Minor: Maps href has unencoded spaces (template behaviour; browsers accept it). |
| 3 | Phone (375px) and desktop; no sideways scrolling | Pending: tested separately by Brain | Needs a browser render. Template has a viewport meta tag and a 720px mobile breakpoint. |
| 4 | Page title and description; one H1 | PASS | Title "The Copper Pot · Bistro on Fossgate, York"; meta description set; 1 H1. |
| 5 | Images have alt text; contrast WCAG AA | PASS | 0 img tags (text logo until the client sends one; no photos supplied). Contrast: white on copper #b25c2a 4.71:1, copper on white 4.71:1, body text 16.8:1, muted text 5.5 to 6.1:1. Fixed during build: the secondary "ghost" button (copper text on #f6f5f2 hero) was 4.32:1, below 4.5; removed from config (menu is still in the nav). |
| 6 | Privacy notice and cookie notice; no tracking before consent | **FAIL** (privacy/cookie notice) · PASS (no tracking) | 0 script tags, no analytics, pixel or tag manager, no cookies set. But the page has no privacy notice and no cookie notice: the template has no slot for them. Needs a template addition (footer privacy link/page) and a privacy notice text naming the client as controller. |
| 7 | Contact form delivers to client only | Not applicable | No contact form on the page (contact is phone, email, booking link). |
| 8 | Lighthouse performance ≥ 85 on mobile | Pending: tested separately by Brain | Needs a real host. Page is a single static HTML file, no images or scripts. |
| 9 | Only client's own or licensed images and text | PASS (copy pending client review) | No images. All text written from the intake only; grep for salon/hair/stylist/Willow/Rose/receptionist/Example Street returns nothing. Copy goes to Tom in the client review (playbook step 5). |
| 10 | Uptime monitor for the live URL | Not possible until live | Set up at launch (playbook step 7). |

## Intake gaps (do not block staging)
- Logo "to follow": text logo used. Photos: none supplied, so no images; no stock or other clients' images used.
- "Cream" has no hex value; template default backgrounds used.
- Dish-level menu not supplied; only the prices the intake says to show.

## To do before go-live
1. Add privacy and cookie notice (template change plus client-specific privacy text), then rebuild and recheck item 6.
2. Tom confirms public email and approves copy (client review via founder or Front Desk).
3. Brain runs mobile/desktop render, link check (booking calendar) and Lighthouse on a real staging host.
