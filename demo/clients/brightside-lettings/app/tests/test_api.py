import http.client
import json
import threading
import unittest

from repairs.api import make_server, MAX_BODY
from repairs.store import Store
from tests.fixtures import valid


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")
        self.server = make_server(self.store, "127.0.0.1", 0, quiet=True)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.store.close()

    def call(self, method, path, body=None, raw=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        payload = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        hdrs = {"Content-Type": "application/json"}
        hdrs.update(headers or {})
        conn.request(method, path, body=payload, headers=hdrs)
        resp = conn.getresponse()
        data = json.loads(resp.read() or b"null")
        ctype = resp.getheader("Content-Type")
        conn.close()
        return resp.status, data, ctype

    def test_health(self):
        status, data, ctype = self.call("GET", "/health")
        self.assertEqual((status, data), (200, {"status": "ok"}))
        self.assertTrue(ctype.startswith("application/json"))

    def test_create_and_get(self):
        status, created, _ = self.call("POST", "/requests", valid(category="no_heat"))
        self.assertEqual(status, 201)
        self.assertEqual(created["status"], "new")
        self.assertEqual(created["urgency"], "urgent")
        self.assertTrue(created["is_urgent"])
        status, got, _ = self.call("GET", f"/requests/{created['id']}")
        self.assertEqual((status, got), (200, created))

    def test_create_validation_error(self):
        status, data, _ = self.call("POST", "/requests", valid(tenant_email="bad", category="x"))
        self.assertEqual(status, 400)
        self.assertIn("tenant_email", data["fields"])
        self.assertIn("category", data["fields"])
        self.assertEqual(self.store.list(), [])

    def test_invalid_json_and_non_object(self):
        status, data, _ = self.call("POST", "/requests", raw=b"{not json")
        self.assertEqual(status, 400)
        status, _, _ = self.call("POST", "/requests", raw=b"null")
        self.assertEqual(status, 400)
        status, _, _ = self.call("POST", "/requests", body=[1, 2])
        self.assertEqual(status, 400)

    def test_body_too_large(self):
        status, _, _ = self.call("POST", "/requests", raw=b"x" * (MAX_BODY + 1))
        self.assertEqual(status, 413)

    def test_list_sorted_urgent_first(self):
        ids = {}
        for cat in ("plumbing", "water_leak", "pests", "security"):
            ids[cat] = self.call("POST", "/requests", valid(category=cat))[1]["id"]
        status, data, _ = self.call("GET", "/requests")
        self.assertEqual(status, 200)
        self.assertEqual([r["id"] for r in data["requests"]],
                         [ids["water_leak"], ids["security"], ids["plumbing"], ids["pests"]])

    def test_list_status_filter(self):
        rid = self.call("POST", "/requests", valid())[1]["id"]
        self.call("POST", "/requests", valid())
        self.call("PATCH", f"/requests/{rid}", {"status": "booked"})
        _, data, _ = self.call("GET", "/requests?status=booked")
        self.assertEqual([r["id"] for r in data["requests"]], [rid])
        status, _, _ = self.call("GET", "/requests?status=bogus")
        self.assertEqual(status, 400)

    def test_status_transitions(self):
        rid = self.call("POST", "/requests", valid())[1]["id"]
        status, data, _ = self.call("PATCH", f"/requests/{rid}", {"status": "done"})
        self.assertEqual(status, 409)
        self.assertIn("cannot move", data["error"])
        status, data, _ = self.call("PATCH", f"/requests/{rid}", {"status": "booked"})
        self.assertEqual((status, data["status"]), (200, "booked"))
        status, _, _ = self.call("PATCH", f"/requests/{rid}", {"status": "new"})
        self.assertEqual(status, 409)
        status, data, _ = self.call("PATCH", f"/requests/{rid}", {"status": "done"})
        self.assertEqual((status, data["status"]), (200, "done"))
        status, _, _ = self.call("PATCH", f"/requests/{rid}", {"status": "booked"})
        self.assertEqual(status, 409)
        self.assertEqual(self.store.get(rid).status, "done")

    def test_patch_bad_body(self):
        rid = self.call("POST", "/requests", valid())[1]["id"]
        for body in ({}, {"status": "booked", "urgency": "routine"}, ["booked"]):
            status, _, _ = self.call("PATCH", f"/requests/{rid}", body)
            self.assertEqual(status, 400, body)
        status, _, _ = self.call("PATCH", f"/requests/{rid}", {"status": "cancelled"})
        self.assertEqual(status, 409)

    def test_not_found(self):
        self.assertEqual(self.call("GET", "/requests/999")[0], 404)
        self.assertEqual(self.call("PATCH", "/requests/999", {"status": "booked"})[0], 404)
        self.assertEqual(self.call("GET", "/nope")[0], 404)
        self.assertEqual(self.call("POST", "/requests/1", valid())[0], 404)
        self.assertEqual(self.call("GET", "/requests/abc")[0], 404)


if __name__ == "__main__":
    unittest.main()
