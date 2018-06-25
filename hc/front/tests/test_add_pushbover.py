from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def test_it_adds_channel(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(302, r.status_code)

        channels = list(Channel.objects.all())
        self.assertEqual(1, len(channels))
        self.assertEqual("a|0", channels[0].value)

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/integrations/add_pushover/")
        self.assertEqual(404, r.status_code)

    def test_it_validates_nonce(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(403, r.status_code)

    ### Test that pushover validates priority
    def test_pushover_validates_priority(self):
        self.client.login(username='alice@example.org', password='password')

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # Note that priority is set an invalid value of 3
        params = "pushover_user_key=a&nonce=INVALID&prio='3'"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(403, r.status_code)

    def test_initiate_subscription(self):
        self.client.login(username='alice@example.org', password='password')

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # Note that priority is set an invalid value of 3
        params = "pushover_user_key=a&nonce=INVALID&prio=2"

        # r = self.client.post("/integrations/add_pushover/?%s" % params)
        r = self.client.post("/integrations/add_pushover")
        print('post', r)

        self.assertEqual(301, r.status_code)



