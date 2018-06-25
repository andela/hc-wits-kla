from hc.api.models import Channel
from hc.test import BaseTestCase


class RemoveChannelTestCase(BaseTestCase):

    def setUp(self):
        super(RemoveChannelTestCase, self).setUp()
        self.channel = Channel(user=self.alice, kind="email")
        self.channel.value = "alice@example.org"
        self.channel.save()

    def test_it_works(self):
        url = "/integrations/%s/remove/" % self.channel.code

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/integrations/")

        self.assertEqual(0, Channel.objects.count())

    def test_team_access_works(self):
        url = "/integrations/%s/remove/" % self.channel.code

        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        self.assertEqual(0, Channel.objects.count())

    def test_it_handles_bad_uuid(self):
        url = "/integrations/not-uuid/remove/"

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(400, r.status_code)

    def test_it_checks_owner(self):
        url = "/integrations/%s/remove/" % self.channel.code

        self.client.login(username="charlie@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(403, r.status_code)

    def test_it_handles_missing_uuid(self):
        # Valid UUID but there is no channel for it:
        url = "/integrations/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/remove/"

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertEqual(302, r.status_code)
