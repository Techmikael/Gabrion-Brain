import unittest

from repairs.models import (
    RepairRequest, ValidationError, TransitionError, URGENT_CATEGORIES,
    validate_new, resolve_urgency, check_transition, apply_transition, sort_requests,
)
from tests.fixtures import valid


class ValidationTests(unittest.TestCase):
    def test_valid_request_is_normalised(self):
        clean = validate_new(valid(category=" Plumbing ", tenant_email="Tenant@Example.TEST"))
        self.assertEqual(clean["category"], "plumbing")
        self.assertEqual(clean["tenant_email"], "tenant@example.test")
        self.assertEqual(clean["urgency"], "routine")

    def test_body_must_be_object(self):
        for body in (None, [], "text", 3):
            with self.assertRaises(ValidationError) as ctx:
                validate_new(body)
            self.assertIn("_body", ctx.exception.errors)

    def test_required_fields(self):
        for name in ("property_ref", "category", "description", "tenant_name", "tenant_email"):
            data = valid()
            del data[name]
            with self.assertRaises(ValidationError) as ctx:
                validate_new(data)
            self.assertEqual(ctx.exception.errors[name], "required")

    def test_blank_and_non_string_rejected(self):
        for bad in ("", "   ", 123, None):
            with self.assertRaises(ValidationError) as ctx:
                validate_new(valid(property_ref=bad))
            self.assertIn("property_ref", ctx.exception.errors)

    def test_unknown_category(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_new(valid(category="gardening"))
        self.assertIn("category", ctx.exception.errors)

    def test_bad_email(self):
        for bad in ("no-at-sign", "a@b", "a b@example.test", "@example.test"):
            with self.assertRaises(ValidationError) as ctx:
                validate_new(valid(tenant_email=bad))
            self.assertIn("tenant_email", ctx.exception.errors)

    def test_description_length_limits(self):
        with self.assertRaises(ValidationError):
            validate_new(valid(description="short"))
        with self.assertRaises(ValidationError):
            validate_new(valid(description="x" * 2001))
        validate_new(valid(description="x" * 2000))

    def test_bad_urgency_value(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_new(valid(urgency="asap"))
        self.assertIn("urgency", ctx.exception.errors)

    def test_unknown_fields_rejected(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_new(valid(status="done"))
        self.assertIn("_body", ctx.exception.errors)

    def test_all_errors_reported_together(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_new({"category": "nope", "tenant_email": "bad"})
        self.assertGreaterEqual(len(ctx.exception.errors), 4)


class UrgencyTests(unittest.TestCase):
    def test_urgent_categories(self):
        self.assertEqual(URGENT_CATEGORIES, {"no_heat", "water_leak", "no_power", "security"})
        for cat in URGENT_CATEGORIES:
            self.assertEqual(validate_new(valid(category=cat))["urgency"], "urgent", cat)

    def test_urgent_category_cannot_be_downgraded(self):
        self.assertEqual(resolve_urgency("water_leak", "routine"), "urgent")

    def test_tenant_can_flag_routine_category_urgent(self):
        self.assertEqual(resolve_urgency("plumbing", "urgent"), "urgent")
        self.assertEqual(resolve_urgency("plumbing", None), "routine")

    def test_sort_urgent_first_then_oldest(self):
        def make(i, cat, ts):
            r = RepairRequest.create(valid(category=cat))
            r.id, r.created_at = i, ts
            return r
        reqs = [
            make(1, "plumbing", "2026-11-01T09:00:00.000000Z"),
            make(2, "no_heat", "2026-11-03T09:00:00.000000Z"),
            make(3, "pests", "2026-11-02T09:00:00.000000Z"),
            make(4, "security", "2026-11-02T09:00:00.000000Z"),
            make(5, "water_leak", "2026-11-02T09:00:00.000000Z"),
        ]
        self.assertEqual([r.id for r in sort_requests(reqs)], [4, 5, 2, 1, 3])


class TransitionTests(unittest.TestCase):
    def test_valid_path(self):
        r = RepairRequest.create(valid())
        apply_transition(r, "booked")
        self.assertEqual(r.status, "booked")
        apply_transition(r, "done")
        self.assertEqual(r.status, "done")

    def test_invalid_transitions(self):
        bad = [("new", "done"), ("new", "new"), ("booked", "new"), ("booked", "booked"),
               ("done", "new"), ("done", "booked"), ("done", "done")]
        for current, new in bad:
            with self.assertRaises(TransitionError, msg=f"{current}->{new}"):
                check_transition(current, new)

    def test_unknown_status(self):
        for new in ("cancelled", "", None, 1):
            with self.assertRaises(TransitionError):
                check_transition("new", new)

    def test_failed_transition_leaves_request_unchanged(self):
        r = RepairRequest.create(valid())
        with self.assertRaises(TransitionError):
            apply_transition(r, "done")
        self.assertEqual(r.status, "new")


if __name__ == "__main__":
    unittest.main()
