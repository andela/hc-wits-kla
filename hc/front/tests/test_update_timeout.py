from hc.api.models import Check
from hc.test import BaseTestCase


class UpdateTimeoutTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateTimeoutTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEqual(3600, check.timeout.total_seconds())
        self.assertEqual(60, check.grace.total_seconds())

    def test_team_access_works(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 7200, "grace": 60}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, data=payload)

        check = Check.objects.get(code=self.check.code)
        self.assertEqual(7200, check.timeout.total_seconds())

    def test_it_handles_bad_uuid(self):
        url = "/checks/not-uuid/timeout/"
        payload = {"timeout": 3600, "grace": 60}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertEqual(400, r.status_code)

    def test_it_handles_missing_uuid(self):
        # Valid UUID but there is no check for it:
        url = "/checks/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/timeout/"
        payload = {"timeout": 3600, "grace": 60}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertEqual(404, r.status_code)

    def test_it_checks_ownership(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 3600, "grace": 60}

        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertEqual(403, r.status_code)

