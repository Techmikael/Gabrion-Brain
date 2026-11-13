# Playbook: Website build

**Owner:** web-builder · **Factory:** `factories/websites.md` · **Approval:** going live

1. **Intake.** Check the intake form in `clients/<slug>/intake.md` is complete: business name, industry, services and prices to show, opening hours, address, phone, email, booking link, logo, colours, photos, domain.
2. **Template.** Copy the closest industry config from `templates/website/configs/` to `clients/<slug>/site/config.json` and fill it from the intake. Do not copy another client's config.
3. **Build on staging.** `python3 templates/website/build.py clients/<slug>/site/config.json --out clients/<slug>/site/dist`, then deploy `dist/` to the staging URL.
4. **Checklist.** Run every item in `factories/websites.md` → Checklist. Record pass/fail in `clients/<slug>/site/checklist.md`.
5. **Client review.** Send the staging link via the founder or Front Desk; up to two rounds of changes are included.
6. **Approval.** Add an approval item: type `go-live`, prepared work = staging link + checklist.
7. **Launch.** After APPROVED: point the domain, enable HTTPS, add uptime monitoring, hand to operations-support.
8. **Close.** Task to `done`; Finance raises the launch invoice.
