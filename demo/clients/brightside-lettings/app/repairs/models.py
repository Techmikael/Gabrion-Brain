"""Repair request model: validation, urgency rules and status transitions.

Python 3 standard library only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Iterable

# Categories a tenant can choose. The first four are always urgent.
URGENT_CATEGORIES = frozenset({"no_heat", "water_leak", "no_power", "security"})
ROUTINE_CATEGORIES = frozenset(
    {"plumbing", "electrical", "appliance", "heating", "damp_mould",
     "doors_windows", "pests", "structural", "other"}
)
CATEGORIES = URGENT_CATEGORIES | ROUTINE_CATEGORIES

URGENCY_LEVELS = ("urgent", "routine")

# Allowed status moves: new -> booked -> done, nothing else.
STATUSES = ("new", "booked", "done")
TRANSITIONS = {"new": frozenset({"booked"}), "booked": frozenset({"done"}), "done": frozenset()}

MAX_LEN = {
    "property_ref": 100,
    "tenant_name": 100,
    "tenant_email": 254,
    "description": 2000,
}
MIN_DESCRIPTION = 10

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_INPUT_FIELDS = ("property_ref", "category", "urgency", "description",
                 "tenant_name", "tenant_email")


class ValidationError(ValueError):
    """Raised when request data is invalid. `errors` maps field -> message."""

    def __init__(self, errors: dict[str, str]):
        super().__init__("; ".join(f"{k}: {v}" for k, v in errors.items()))
        self.errors = errors


class TransitionError(ValueError):
    """Raised when a status change is not allowed."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def resolve_urgency(category: str, requested: str | None) -> str:
    """Urgent categories are always urgent; otherwise honour the tenant's choice
    (default routine). A tenant can raise urgency but never lower it below the rule."""
    if category in URGENT_CATEGORIES:
        return "urgent"
    return requested if requested in URGENCY_LEVELS else "routine"


def validate_new(data: Any) -> dict[str, str]:
    """Validate and normalise tenant input. Returns clean fields or raises ValidationError."""
    if not isinstance(data, dict):
        raise ValidationError({"_body": "must be a JSON object"})

    errors: dict[str, str] = {}
    unknown = sorted(set(data) - set(_INPUT_FIELDS))
    if unknown:
        errors["_body"] = "unknown fields: " + ", ".join(unknown)

    clean: dict[str, str] = {}
    for name in ("property_ref", "description", "tenant_name", "tenant_email", "category"):
        value = data.get(name)
        if not isinstance(value, str) or not value.strip():
            errors[name] = "required"
            continue
        value = value.strip()
        if name in MAX_LEN and len(value) > MAX_LEN[name]:
            errors[name] = f"must be at most {MAX_LEN[name]} characters"
            continue
        clean[name] = value

    if "category" in clean:
        clean["category"] = clean["category"].lower()
        if clean["category"] not in CATEGORIES:
            errors["category"] = "must be one of: " + ", ".join(sorted(CATEGORIES))
    if "description" in clean and len(clean["description"]) < MIN_DESCRIPTION:
        errors["description"] = f"must be at least {MIN_DESCRIPTION} characters"
    if "tenant_email" in clean:
        clean["tenant_email"] = clean["tenant_email"].lower()
        if not _EMAIL_RE.match(clean["tenant_email"]):
            errors["tenant_email"] = "must be a valid email address"

    urgency = data.get("urgency")
    if urgency is not None and urgency not in URGENCY_LEVELS:
        errors["urgency"] = "must be 'urgent' or 'routine'"

    if errors:
        raise ValidationError(errors)

    clean["urgency"] = resolve_urgency(clean["category"], urgency)
    return clean


@dataclass
class RepairRequest:
    property_ref: str
    category: str
    urgency: str
    description: str
    tenant_name: str
    tenant_email: str
    status: str = "new"
    id: int | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    @classmethod
    def create(cls, data: Any) -> "RepairRequest":
        return cls(**validate_new(data))

    @property
    def is_urgent(self) -> bool:
        return self.urgency == "urgent"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["is_urgent"] = self.is_urgent
        return d


def check_transition(current: str, new: Any) -> str:
    """Return the new status if the move is allowed, else raise TransitionError."""
    if new not in STATUSES:
        raise TransitionError(f"unknown status {new!r}; must be one of {', '.join(STATUSES)}")
    if new not in TRANSITIONS.get(current, frozenset()):
        raise TransitionError(f"cannot move from {current!r} to {new!r}")
    return new


def apply_transition(req: RepairRequest, new: Any) -> RepairRequest:
    req.status = check_transition(req.status, new)
    req.updated_at = utc_now()
    return req


def sort_key(req: RepairRequest) -> tuple:
    """Urgent first, then oldest first, then id."""
    return (0 if req.is_urgent else 1, req.created_at, req.id or 0)


def sort_requests(reqs: Iterable[RepairRequest]) -> list[RepairRequest]:
    return sorted(reqs, key=sort_key)
