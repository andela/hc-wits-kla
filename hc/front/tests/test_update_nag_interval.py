from hc.test import BaseTestCase
from hc.api.models import Check


class ConfigureNagInterval(BaseTestCase):

    def setUp(self):
        super(ConfigureNagInterval, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/nag/" % self.check.code
        payload = {"nagging": 400}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEqual(400, check.nag.total_seconds())
