import os
import tempfile
import unittest

from repairs.models import RepairRequest, TransitionError
from repairs.store import Store, NotFound
from tests.fixtures import valid


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")

    def tearDown(self):
        self.store.close()

    def test_add_and_get(self):
        r = self.store.add(RepairRequest.create(valid()))
        self.assertIsNotNone(r.id)
        self.assertEqual(self.store.get(r.id).to_dict(), r.to_dict())

    def test_get_missing(self):
        with self.assertRaises(NotFound):
            self.store.get(999)

    def test_list_sorted_urgent_first(self):
        a = self.store.add(RepairRequest.create(valid(category="plumbing")))
        b = self.store.add(RepairRequest.create(valid(category="no_power")))
        c = self.store.add(RepairRequest.create(valid(category="other")))
        d = self.store.add(RepairRequest.create(valid(category="security")))
        self.assertEqual([r.id for r in self.store.list()], [b.id, d.id, a.id, c.id])

    def test_status_filter(self):
        a = self.store.add(RepairRequest.create(valid()))
        self.store.add(RepairRequest.create(valid()))
        self.store.set_status(a.id, "booked")
        self.assertEqual([r.id for r in self.store.list("booked")], [a.id])
        with self.assertRaises(ValueError):
            self.store.list("bogus")

    def test_invalid_transition_not_persisted(self):
        r = self.store.add(RepairRequest.create(valid()))
        with self.assertRaises(TransitionError):
            self.store.set_status(r.id, "done")
        self.assertEqual(self.store.get(r.id).status, "new")
        self.store.set_status(r.id, "booked")
        self.store.set_status(r.id, "done")
        with self.assertRaises(TransitionError):
            self.store.set_status(r.id, "booked")
        self.assertEqual(self.store.get(r.id).status, "done")

    def test_set_status_missing(self):
        with self.assertRaises(NotFound):
            self.store.set_status(42, "booked")

    def test_sql_injection_text_stored_literally(self):
        nasty = "Flat 1'); DROP TABLE repair_requests;--"
        r = self.store.add(RepairRequest.create(valid(property_ref=nasty)))
        self.assertEqual(self.store.get(r.id).property_ref, nasty)
        self.assertEqual(len(self.store.list()), 1)

    def test_persists_to_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "repairs.db")
            s1 = Store(path)
            r = s1.add(RepairRequest.create(valid(category="water_leak")))
            s1.close()
            s2 = Store(path)
            self.assertEqual(s2.get(r.id).urgency, "urgent")
            s2.close()


if __name__ == "__main__":
    unittest.main()
