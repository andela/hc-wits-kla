from hc.api.models import Check
from hc.test import BaseTestCase


class ViewEscalateCheckTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice)
        check.save()
        url = "/checks/{}/escalate/form".format(check.code)

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)

        self.assertEqual(200, r.status_code)

