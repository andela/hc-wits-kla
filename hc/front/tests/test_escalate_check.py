from hc.api.models import Check
from hc.accounts.models import Member
from hc.test import BaseTestCase


class EscalateCheckTestCase(BaseTestCase):

    def setUp(self):
        super(EscalateCheckTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        bob = Member.objects.get(user=self.bob)
        bob.assigned_jobs.add(self.check)
        bob.save()
        url = "/checks/escalate"
        payload = {
            'check_status': [str(bob.id) + ' ' + str(self.check.code)],
            'code': [str(self.check.code)]
        }
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)

        self.assertRedirects(r, "/checks/")

    def test_missing_check_status(self):
        check = Check(user=self.alice)
        check.save()
        url = "/checks/escalate"
        payload = {
            'code': [str(check.code)]
        }
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)

        self.assertRedirects(r, "/checks/")

    def test_request_not_post(self):
        url = "/checks/escalate"

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(url)

        self.assertEqual(403, r.status_code)

