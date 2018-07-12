from hc.test import BaseTestCase


class OnboardingTestCase(BaseTestCase):
    def setUp(self):
        super(OnboardingTestCase, self).setUp()

    def test_faqs_works(self):
        self.client.login(username="alice@example.org", password="password")
        url = "/faqs/"
        r = self.client.post(url)

    def test_tutorials_work(self):
        self.client.login(username="alice@example.org", password="password")
        url = "/tutorials/"
        r = self.client.post(url)
