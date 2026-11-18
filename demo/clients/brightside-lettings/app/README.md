# Brightside Lettings repair-request portal (phase 1)

Branch: `feature/repair-requests` · Factory: `factories/software.md` · Task: D014

Phase 1 is the core: repair request model with validation, urgency rules, status
workflow, SQLite store and a small JSON HTTP API. Python 3.10+ standard library only:
no third-party, paid or external dependencies. No tenant web form or staff login yet.

## Rules implemented
- **Fields:** `property_ref`, `category`, `description`, `tenant_name`, `tenant_email`
  (required), `urgency` (optional: `urgent` or `routine`). Unknown fields are rejected.
- **Categories:** urgent: `no_heat`, `water_leak`, `no_power`, `security`.
  Routine: `plumbing`, `electrical`, `appliance`, `heating`, `damp_mould`,
  `doors_windows`, `pests`, `structural`, `other`.
- **Urgency:** the four urgent categories are always `urgent` (a tenant cannot lower
  them). A tenant may mark any other category `urgent`; otherwise it is `routine`.
- **Sorting:** staff list is urgent first, then oldest first.
- **Status:** `new` -> `booked` -> `done` only. Anything else returns 409.

## Run locally
```
cd app
python3 -m unittest discover -s tests -t . -v     # run the tests
REPAIRS_DB=./repairs.db REPAIRS_PORT=8080 python3 -m repairs
```
Environment variables: `REPAIRS_DB` (SQLite file, default `repairs.db`),
`REPAIRS_HOST` (default `127.0.0.1`), `REPAIRS_PORT` (default `8080`). No secrets are needed
in phase 1; if any are added later they come from the password manager as environment
variables at run time and are never committed.

## API
| Method | Path | Body | Result |
|---|---|---|---|
| GET | `/health` | | 200 `{"status":"ok"}` |
| POST | `/requests` | request fields | 201 created request; 400 with `fields` on validation errors |
| GET | `/requests[?status=new\|booked\|done]` | | 200 `{"requests":[...]}` urgent first |
| GET | `/requests/<id>` | | 200 or 404 |
| PATCH | `/requests/<id>` | `{"status":"booked"}` | 200; 409 if the move is not allowed; 404 |

Bodies over 64 KB get 413. Example:
```
curl -X POST localhost:8080/requests -H 'Content-Type: application/json' \
  -d '{"property_ref":"BL-TEST-1","category":"water_leak","description":"Water through ceiling","tenant_name":"Test Tenant","tenant_email":"t@example.test"}'
```

## Deploy (staging only until approved)
Hosting is not decided yet (must be UK/EU, per intake). Until it is:
1. Deploy to a Gabrion staging host only, bound to `127.0.0.1` behind a reverse proxy with
   HTTPS and access restricted (phase 1 has **no authentication**).
2. Copy the `repairs/` package, set `REPAIRS_DB` to a path outside the code folder,
   run `python3 -m repairs` under a process supervisor (e.g. systemd).
3. Check `GET /health` returns 200, then run the factory checklist.

Production deploy and merge need the founder's approval in the approval queue, plus
staff authentication, backups and error tracking (factory checklist).

## Roll back
- **Code:** redeploy the previous release tag (or `git revert` the merge commit) and
  restart the service. Phase 1 is a new service, so rollback = stop the service and
  remove the proxy route; nothing else depends on it.
- **Data:** the schema is created with `CREATE TABLE IF NOT EXISTS` and is additive. Take a
  copy of the SQLite file before every deploy (`sqlite3 repairs.db ".backup pre-deploy.db"`)
  and restore that copy if a release must be undone.

## Layout
- `repairs/models.py` validation, urgency, transitions, sorting
- `repairs/store.py` SQLite store (parameterised SQL)
- `repairs/api.py` HTTP API (`http.server`)
- `tests/` unittest suites (synthetic data only); `test-output.txt` last run
