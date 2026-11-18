"""Small JSON HTTP API on http.server.

Endpoints
  GET   /health                 -> {"status": "ok"}
  POST  /requests               -> 201, the created request (tenant form)
  GET   /requests[?status=new]  -> list, urgent first then oldest first (staff view)
  GET   /requests/<id>          -> one request
  PATCH /requests/<id>          -> body {"status": "booked"|"done"}; 409 if not allowed

Configuration (environment variables): REPAIRS_DB (SQLite path, default repairs.db),
REPAIRS_HOST (default 127.0.0.1), REPAIRS_PORT (default 8080).

Phase 1 has NO authentication: bind to localhost / staging only. Staff login is phase 2.
"""

from __future__ import annotations

import json
import os
import re
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

from .models import RepairRequest, ValidationError, TransitionError
from .store import Store, NotFound

MAX_BODY = 64 * 1024
_ITEM_RE = re.compile(r"^/requests/(\d{1,12})$")
_FAILED = object()  # sentinel: an error response has already been sent


class Handler(BaseHTTPRequestHandler):
    server_version = "BrightsideRepairs/0.1"
    sys_version = ""
    store: Store  # set by make_server

    # Log method, path and status only: never request bodies (they hold personal data).
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.log_date_time_string(), fmt % args))

    def _send(self, status: int, payload) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, message: str, **extra) -> None:
        self._send(status, {"error": message, **extra})

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if length < 0:
            self._error(HTTPStatus.BAD_REQUEST, "invalid Content-Length")
            return _FAILED
        if length > MAX_BODY:
            self.close_connection = True  # do not read the oversized body
            self._error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "body too large")
            return _FAILED
        raw = self.rfile.read(length) if length else b""
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._error(HTTPStatus.BAD_REQUEST, "body must be valid JSON")
            return _FAILED

    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path == "/health":
            return self._send(HTTPStatus.OK, {"status": "ok"})
        if parts.path == "/requests":
            status = parse_qs(parts.query).get("status", [None])[0]
            try:
                reqs = self.store.list(status)
            except ValueError as exc:
                return self._error(HTTPStatus.BAD_REQUEST, str(exc))
            return self._send(HTTPStatus.OK, {"requests": [r.to_dict() for r in reqs]})
        m = _ITEM_RE.match(parts.path)
        if m:
            try:
                return self._send(HTTPStatus.OK, self.store.get(int(m.group(1))).to_dict())
            except NotFound:
                return self._error(HTTPStatus.NOT_FOUND, "request not found")
        self._error(HTTPStatus.NOT_FOUND, "not found")

    def do_POST(self):
        if urlsplit(self.path).path != "/requests":
            return self._error(HTTPStatus.NOT_FOUND, "not found")
        data = self._read_json()
        if data is _FAILED:
            return
        try:
            req = RepairRequest.create(data)
        except ValidationError as exc:
            return self._error(HTTPStatus.BAD_REQUEST, "validation failed", fields=exc.errors)
        self._send(HTTPStatus.CREATED, self.store.add(req).to_dict())

    def do_PATCH(self):
        m = _ITEM_RE.match(urlsplit(self.path).path)
        if not m:
            return self._error(HTTPStatus.NOT_FOUND, "not found")
        data = self._read_json()
        if data is _FAILED:
            return
        if not isinstance(data, dict) or set(data) != {"status"}:
            return self._error(HTTPStatus.BAD_REQUEST, 'body must be {"status": "<new status>"}')
        try:
            req = self.store.set_status(int(m.group(1)), data["status"])
        except NotFound:
            return self._error(HTTPStatus.NOT_FOUND, "request not found")
        except TransitionError as exc:
            return self._error(HTTPStatus.CONFLICT, str(exc))
        self._send(HTTPStatus.OK, req.to_dict())


def make_server(store: Store, host: str = "127.0.0.1", port: int = 8080,
                quiet: bool = False) -> ThreadingHTTPServer:
    attrs = {"store": store}
    if quiet:
        attrs["log_message"] = lambda self, fmt, *args: None
    handler = type("BoundHandler", (Handler,), attrs)
    return ThreadingHTTPServer((host, port), handler)


def main() -> None:
    db = os.environ.get("REPAIRS_DB", "repairs.db")
    host = os.environ.get("REPAIRS_HOST", "127.0.0.1")
    port = int(os.environ.get("REPAIRS_PORT", "8080"))
    store = Store(db)
    server = make_server(store, host, port)
    print(f"Brightside repairs API on http://{host}:{port} (db: {db})", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        store.close()


if __name__ == "__main__":
    main()
