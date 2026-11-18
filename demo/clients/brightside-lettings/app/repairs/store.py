"""SQLite store for repair requests (standard library sqlite3, parameterised SQL only)."""

from __future__ import annotations

import sqlite3
import threading

from .models import RepairRequest, apply_transition, sort_requests, STATUSES

SCHEMA = """
CREATE TABLE IF NOT EXISTS repair_requests (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    property_ref TEXT NOT NULL,
    category     TEXT NOT NULL,
    urgency      TEXT NOT NULL CHECK (urgency IN ('urgent', 'routine')),
    description  TEXT NOT NULL,
    tenant_name  TEXT NOT NULL,
    tenant_email TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'booked', 'done')),
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_repair_status ON repair_requests (status);
"""

_COLUMNS = ("id", "property_ref", "category", "urgency", "description",
            "tenant_name", "tenant_email", "status", "created_at", "updated_at")


class NotFound(KeyError):
    pass


class Store:
    def __init__(self, path: str = ":memory:"):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        with self._lock, self._conn:
            self._conn.executescript(SCHEMA)

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    @staticmethod
    def _row(row: sqlite3.Row) -> RepairRequest:
        return RepairRequest(**{k: row[k] for k in _COLUMNS})

    def add(self, req: RepairRequest) -> RepairRequest:
        with self._lock, self._conn:
            cur = self._conn.execute(
                "INSERT INTO repair_requests (property_ref, category, urgency, description,"
                " tenant_name, tenant_email, status, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (req.property_ref, req.category, req.urgency, req.description,
                 req.tenant_name, req.tenant_email, req.status, req.created_at, req.updated_at),
            )
            req.id = cur.lastrowid
        return req

    def get(self, req_id: int) -> RepairRequest:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM repair_requests WHERE id = ?", (req_id,)).fetchone()
        if row is None:
            raise NotFound(req_id)
        return self._row(row)

    def list(self, status: str | None = None) -> list[RepairRequest]:
        """All requests, urgent first then oldest first. Optional status filter."""
        sql, args = "SELECT * FROM repair_requests", ()
        if status is not None:
            if status not in STATUSES:
                raise ValueError(f"unknown status {status!r}")
            sql, args = sql + " WHERE status = ?", (status,)
        with self._lock:
            rows = self._conn.execute(sql, args).fetchall()
        return sort_requests(self._row(r) for r in rows)

    def set_status(self, req_id: int, new_status: str) -> RepairRequest:
        """Change status, enforcing new -> booked -> done. Raises NotFound / TransitionError."""
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT * FROM repair_requests WHERE id = ?", (req_id,)).fetchone()
            if row is None:
                raise NotFound(req_id)
            req = apply_transition(self._row(row), new_status)
            self._conn.execute(
                "UPDATE repair_requests SET status = ?, updated_at = ? WHERE id = ?",
                (req.status, req.updated_at, req.id))
        return req
