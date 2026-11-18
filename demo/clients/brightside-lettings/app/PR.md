# PR: Brightside repair-request portal, phase 1 (core model, store, API)

Branch: `feature/repair-requests` -> `main` · Client: brightside-lettings · Task: D014 ·
Factory: `factories/software.md` · **Do not merge without founder approval (queue A-0701).**

## What changed
New Python 3 standard-library service in `app/` (no dependencies added, none paid):
- `repairs/models.py`: `RepairRequest` model; validation of required fields, lengths,
  category list, email format and unknown fields (all errors returned together); urgency
  rules (no_heat, water_leak, no_power, security always urgent and cannot be downgraded);
  sorting urgent first then oldest; status transitions `new -> booked -> done` only.
- `repairs/store.py`: SQLite store with CHECK constraints, parameterised SQL, thread lock,
  transition enforced inside a transaction so a refused change is never saved.
- `repairs/api.py`: JSON API on `http.server` (`/health`, `POST/GET /requests`,
  `GET/PATCH /requests/<id>`); 400 validation, 404, 409 bad transition, 413 body over 64 KB;
  access log records method, path and status only (no bodies).
- `tests/`: 36 unittest tests (validation, urgency and sorting, invalid transitions,
  store, API end to end over a real socket). `README.md`: run, deploy, roll back.

## How it was tested
`python3 -m unittest discover -s tests -t . -v` on Python 3.13.18, 2026-11-18. Result:
**Ran 36 tests ... OK**. Also a manual smoke test of `python3 -m repairs` with curl
(POST a water_leak request -> 201 urgent; GET list -> 200). Full output:

```
test_body_too_large (tests.test_api.ApiTests.test_body_too_large) ... ok
test_create_and_get (tests.test_api.ApiTests.test_create_and_get) ... ok
test_create_validation_error (tests.test_api.ApiTests.test_create_validation_error) ... ok
test_health (tests.test_api.ApiTests.test_health) ... ok
test_invalid_json_and_non_object (tests.test_api.ApiTests.test_invalid_json_and_non_object) ... ok
test_list_sorted_urgent_first (tests.test_api.ApiTests.test_list_sorted_urgent_first) ... ok
test_list_status_filter (tests.test_api.ApiTests.test_list_status_filter) ... ok
test_not_found (tests.test_api.ApiTests.test_not_found) ... ok
test_patch_bad_body (tests.test_api.ApiTests.test_patch_bad_body) ... ok
test_status_transitions (tests.test_api.ApiTests.test_status_transitions) ... ok
test_failed_transition_leaves_request_unchanged (tests.test_models.TransitionTests.test_failed_transition_leaves_request_unchanged) ... ok
test_invalid_transitions (tests.test_models.TransitionTests.test_invalid_transitions) ... ok
test_unknown_status (tests.test_models.TransitionTests.test_unknown_status) ... ok
test_valid_path (tests.test_models.TransitionTests.test_valid_path) ... ok
test_sort_urgent_first_then_oldest (tests.test_models.UrgencyTests.test_sort_urgent_first_then_oldest) ... ok
test_tenant_can_flag_routine_category_urgent (tests.test_models.UrgencyTests.test_tenant_can_flag_routine_category_urgent) ... ok
test_urgent_categories (tests.test_models.UrgencyTests.test_urgent_categories) ... ok
test_urgent_category_cannot_be_downgraded (tests.test_models.UrgencyTests.test_urgent_category_cannot_be_downgraded) ... ok
test_all_errors_reported_together (tests.test_models.ValidationTests.test_all_errors_reported_together) ... ok
test_bad_email (tests.test_models.ValidationTests.test_bad_email) ... ok
test_bad_urgency_value (tests.test_models.ValidationTests.test_bad_urgency_value) ... ok
test_blank_and_non_string_rejected (tests.test_models.ValidationTests.test_blank_and_non_string_rejected) ... ok
test_body_must_be_object (tests.test_models.ValidationTests.test_body_must_be_object) ... ok
test_description_length_limits (tests.test_models.ValidationTests.test_description_length_limits) ... ok
test_required_fields (tests.test_models.ValidationTests.test_required_fields) ... ok
test_unknown_category (tests.test_models.ValidationTests.test_unknown_category) ... ok
test_unknown_fields_rejected (tests.test_models.ValidationTests.test_unknown_fields_rejected) ... ok
test_valid_request_is_normalised (tests.test_models.ValidationTests.test_valid_request_is_normalised) ... ok
test_add_and_get (tests.test_store.StoreTests.test_add_and_get) ... ok
test_get_missing (tests.test_store.StoreTests.test_get_missing) ... ok
test_invalid_transition_not_persisted (tests.test_store.StoreTests.test_invalid_transition_not_persisted) ... ok
test_list_sorted_urgent_first (tests.test_store.StoreTests.test_list_sorted_urgent_first) ... ok
test_persists_to_file (tests.test_store.StoreTests.test_persists_to_file) ... ok
test_set_status_missing (tests.test_store.StoreTests.test_set_status_missing) ... ok
test_sql_injection_text_stored_literally (tests.test_store.StoreTests.test_sql_injection_text_stored_literally) ... ok
test_status_filter (tests.test_store.StoreTests.test_status_filter) ... ok

----------------------------------------------------------------------
Ran 36 tests in 0.539s

OK
```

Secret scan (grep for api keys, secrets, passwords, tokens, private keys, Stripe/AWS/
GitHub/Slack/Google key patterns, and real-domain email addresses) over `app/`: no matches.

## Factory checklist (`factories/software.md`)
- [x] Tests pass; new code has tests (locally; no CI configured on this repo yet)
- [x] No secrets in the repository (grep scan, no matches)
- [x] Dependencies have no known critical vulnerabilities (none: standard library only)
- [ ] Staging deploy reviewed by the client (hosting not decided; to do)
- [x] README: how to run, deploy and roll back
- [ ] Backups and error tracking for production (to do before go-live)

Checklist is **not fully passed**, so this PR is for review/merge to the main branch only;
it is not a production go-live.

## Rollback
New, self-contained service with no consumers yet. Revert the merge commit
(`git revert -m 1 <merge-sha>`); if deployed anywhere, stop the service and remove its proxy
route. The schema is additive; restore the pre-deploy SQLite backup if data must be undone.

## Data and privacy notes
- Stores personal data (tenant name, email, property reference/address) as the intake says.
  No payment data. Hosting must be UK/EU; decision pending.
- **No authentication in phase 1**: `GET /requests` returns all tenants' details. Must not be
  exposed to the internet; bind to localhost / restricted staging only. Staff login and a
  tenant-only submit route are needed before go-live.
- Tests and fixtures use synthetic data only (`example.test`); no client data in the repo.
  `*.db` files are git-ignored. Logs do not contain request bodies.
- Still to decide with the client before production: retention period for done requests,
  backups and encryption at rest, privacy notice wording.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01FAPrNe9eGp1i58FSPngqA2
