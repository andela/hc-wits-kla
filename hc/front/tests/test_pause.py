from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def setUp(self):
        super(PauseTestCase, self).setUp()
        self.check = Check(user=self.alice, status="up")
        self.check.save()

    def test_it_pauses(self):
        url = "/checks/%s/pause/" % self.check.code

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")

        self.check.refresh_from_db()
        self.assertEqual(self.check.status, "paused")

    def test_it_does_not_pause(self):
        url = "/checks/%s/pause/" % self.check.code

        # Login using charlie who doesn't have team access
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url)

        self.assertEqual(403, r.status_code)

