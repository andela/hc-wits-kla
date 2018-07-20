from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendOverPingAlertsTestCase(BaseTestCase):

    def test_it_checks_for_pinging_many_times(self):
            check = Check(user=self.alice,last_ping="2018-07-11 16:50:20.720677+03")
            check.status="up"
            check.timeout = "00:02:00"
            check.grace = "00:01:00"
            check.ping_before_last_ping = "2018-07-11 16:50:20.120677+03"
            check.save()
            
            # Expect no exceptions here, after invoking the method--
            Command().pinged_often()