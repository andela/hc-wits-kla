from hc.api.models import Check
from hc.test import BaseTestCase


class UpdatePriorityTestCase(BaseTestCase):

    def setUp(self):
        super(UpdatePriorityTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works_high_priority(self):
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": "High"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEquals("High", check.priority)

    def test_it_works_low_priority(self):
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": "Low"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEquals("Low", check.priority)

    def test_invalid_check_code(self):
        url = "/checks/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/priority/"
        payload = {"priority": "Low"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)

        self.assertEquals(404, r.status_code)
