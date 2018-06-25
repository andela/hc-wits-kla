from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)

        self.assertRedirects(r, "/checks/")
        self.assertEqual(1, Check.objects.count())

    ### Test that team access works
    def test_team_acess_works(self):

        # create a check using alice
        check = Check(user=self.alice)
        check.save()

        url = "/checks/%s/name/" % check.code

        # Logging in as bob, not charlie because Bob has team access so this
        self.client.login(username="bob@example.org", password="password")
        r = self.client.post(url)

        self.assertEqual(302, r.status_code)

