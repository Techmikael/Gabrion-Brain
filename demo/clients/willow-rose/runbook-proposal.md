# PROPOSED run-book entries for factories/websites.md (DRAFT, DEMO)
Status: draft from incident 2026-11-18 (D006). Not added to `factories/websites.md`; the founder decides whether to adopt it. No client details below, so it is safe to copy into the factory file.

## Run-book (known fixes): proposed additions
- **Contact form or form endpoint failing (HTTP 5xx) while homepage is up:**
  1. Rebuild the last approved config locally and check whether it contains a form at all (`grep -c '<form' dist/index.html`).
  2. If the live site has a form the approved build does not: the live site has drifted. Roll back to the last approved build (allowed without approval: rollback to last approved version). Log it in the client's `changes-log.md`.
  3. If the form is part of the approved build: check hosting status and the form handler's status page; redeploy the last approved build.
  4. Any failed submissions are client data: do not open, export or re-send them without founder approval (client-data). Do not tell the client enquiries were lost without the founder.
  5. Anything beyond steps 1 to 3 is a new fix: approval (new-fix).
- **Monitor alert on a path the approved build does not have:** correct the monitor to match the approved build (internal, no approval), note it in the incident file.

## Prevention: proposed checklist and process additions
- Checklist: "Uptime monitor checks only pages and endpoints that exist in the approved build."
- Process: no change reaches a live site except by rebuilding the approved config; every change is recorded in `clients/<slug>/changes-log.md` with date and who asked.
- Process: when a contact form is added, the checklist line "Contact form delivers to the client and to nobody else" also requires a test that a failure alerts us and the submission is not lost (e.g. form also emails a copy).
