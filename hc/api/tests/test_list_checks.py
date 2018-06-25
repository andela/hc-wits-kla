import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        ### Assert the response status code
        self.assertEqual(200, r.status_code)

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}

        ### Assert the expected length of checks
        self.assertEqual(len(checks), 2)

        ### Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status, --- DONE
        self.assertEqual(3600, doc["checks"][1]["timeout"])
        self.assertEqual(900, doc["checks"][1]["grace"])
        self.assertEqual("new", doc["checks"][1]["status"])
        self.assertEqual(self.a1.url(), doc["checks"][1]["ping_url"])

        self.assertEqual(86400, doc["checks"][0]["timeout"])
        self.assertEqual(3600, doc["checks"][0]["grace"])
        self.assertEqual("up", doc["checks"][0]["status"])
        self.assertEqual(self.a2.url(), doc["checks"][0]["ping_url"])

        ### last_ping, n_pings and pause_url
        self.assertEqual(1, doc["checks"][1]["n_pings"])
        self.assertEqual(0, doc["checks"][0]["n_pings"])
        self.assertEqual(self.a1.last_ping.isoformat(), doc["checks"][1]["last_ping"])
        self.assertEqual(self.a2.last_ping.isoformat(), doc["checks"][0]["last_ping"])

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    ### Test that it accepts an api_key in the request
    def test_it_accepts_api_key_in_request(self):
        payload = {"api_key": "abc"}
        url = "/api/v1/checks/"
        r = self.client.put(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(405, r.status_code)
