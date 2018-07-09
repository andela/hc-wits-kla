from hc.test import BaseTestCase
from datetime import timedelta as td
import time
from hc.api.models import Channel, Check, Notification
from django.core import mail

class NagTestCase(BaseTestCase):

    def _setup_data(self, kind, value, status="down", email_verified=True):
        self.check = Check()
        self.check.status = status
        self.check.user = self.alice
        self.check.nag_mode = "on"
        self.check.nag = td(seconds=60)
        self.check.save()

        self.channel = Channel(user=self.alice)
        self.channel.kind = kind
        self.channel.value = value
        self.channel.email_verified = email_verified
        self.channel.save()
        self.channel.checks.add(self.check)

    def test_it_sends_notification(self):
        #after 60 seconds, it should send a notification
        # test that a user has been notified
        time.sleep(60)
        self._setup_data("email", "alice@example.org")
        self.channel.notify(self.check)

        n = Notification.objects.get()
        self.assertEqual(n.error, "")

        # And email should have been sent
        self.assertEqual(len(mail.outbox), 1)
