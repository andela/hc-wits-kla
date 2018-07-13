from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        self.assertTrue(result == True)
        assert result, "handle_many should return True"

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        self.assertTrue(set(names) == set(handled_names))
        self.assertEquals(set(names), set(handled_names))
        ### The above assert fails. Make it pass
        # Assertion is already passing

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

    ### Assert when Command's handle many that when handle_many should return True


    def test_it_checks_for_pinging_many_times(self):
        check = Check(user=self.alice,last_ping="2018-07-11 16:50:20.720677+03")
        check.status="up"
        check.timeout = "00:02:00"
        check.grace = "00:01:00"
        check.ping_before_last_ping = "2018-07-11 16:50:20.120677+03"
        check.save()
        
        # Expect no exceptions here, after running invoking the method--
        Command().pinged_often()






