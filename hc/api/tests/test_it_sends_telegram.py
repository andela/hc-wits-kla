from hc.test import BaseTestCase
from datetime import timedelta as td
import time
from hc.api.models import Channel, Check, Notification
from hc.api.transports import Sms, Telegram
from django.core import mail
from django.utils import timezone

class SmsTelegramTestCase(BaseTestCase):

    def _setup_data(self, kind, value, status="down", email_verified=True):
        self.check = Check()
        self.check.status = "up"
        self.check.user = self.alice
        self.check.last_ping = timezone.now()
        self.check.timeout = td(minutes=2)
        self.check.grace = td(minutes=1)
        self.check.save()

        self.channel = Channel(user=self.alice)
        self.channel.kind = "telegram"
        self.channel.value = "Nabaasa"
        self.channel.email_verified = email_verified
        self.channel.user_id = self.alice.id
        self.channel.save()
        self.channel.checks.add(self.check)

    def test_it_sends_telegram_notifications(self):
        self._setup_data("kind", "telegram","value",True)
        # Expect not exception here, method on the class is invoked and message sent
        self.channel.notify(self.check)
        
        





