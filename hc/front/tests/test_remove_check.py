from hc.api.models import Check
from hc.test import BaseTestCase


class RemoveCheckTestCase(BaseTestCase):

    def setUp(self):
        super(RemoveCheckTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/remove/" % self.check.code

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")

        self.assertEqual(0, Check.objects.count())

    def test_team_access_works(self):
        url = "/checks/%s/remove/" % self.check.code

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        self.assertEqual(0, Check.objects.count())

    def test_it_handles_bad_uuid(self):
        url = "/checks/not-uuid/remove/"

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(400, r.status_code)

    def test_it_checks_owner(self):
        url = "/checks/%s/remove/" % self.check.code

        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(403, r.status_code)

    def test_it_handles_missing_uuid(self):
        # Valid UUID but there is no check for it:
        url = "/checks/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/remove/"

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(404, r.status_code)
