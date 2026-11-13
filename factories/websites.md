# Factory: Websites
Owner: web-builder · Run: managed monthly, or handed over
Stages: intake form → template → build on staging → checklist test → approved launch

## Templates
`templates/website/configs/`: salon (built). To add: restaurant, trades, clinic, corporate — copy salon.json and change sections and copy.

## Checklist (all must pass before go-live approval)
- [ ] Business name, phone, email, address and hours match the intake form exactly
- [ ] Every link and button works; booking link opens the right calendar
- [ ] Looks right on a phone (375px wide) and a desktop; no sideways scrolling
- [ ] Page title and description set; one H1 per page
- [ ] Images have alt text; colour contrast passes (WCAG AA)
- [ ] Privacy notice and cookie notice present; no tracking before consent
- [ ] Contact form (if any) delivers to the client and to nobody else
- [ ] Lighthouse performance ≥ 85 on mobile
- [ ] Only the client's own or licensed images and text
- [ ] Uptime monitor set up for the live URL

## Run-book (known fixes)
- Site down: check hosting status, redeploy last approved build.
- Wrong opening hours: update config, rebuild, redeploy (routine change, no approval if it matches the client's written request).
