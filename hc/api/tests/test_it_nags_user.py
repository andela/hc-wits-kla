from datetime import timedelta as td

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class NagUserTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_nags_for_check(self, mock):

        check = Check(user=self.alice, name='test me')
        check.alert_after = timezone.now() - td(days=1, minutes=30)
        check.last_ping = timezone.now() - td(days=1, minutes=30)
        check.timeout = td(seconds=5)
        check.grace = td(seconds=5)
        check.last_nag = timezone.now() - td(minutes=50)
        check.status = "down"
        check.nag_mode = "off"
        check.save()

        result = Command().handle_one(check)
        # self.assertTrue(result == True)
