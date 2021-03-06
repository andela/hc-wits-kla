from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
        ### Repeat above test for when check is an empty string

        empty_check = Check()
        self.assertEquals(empty_check.tags, "")
        self.assertEquals(empty_check.name, "")

    def test_status_works_with_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())
        self.assertEqual("up", check.get_status())
        #Assertions are already passing
        ### The above 2 asserts fail. Make them pass

    def test_paused_check_is_not_in_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    ### Test that when a new check is created, it is not in the grace period
    def test_check_is_not_in_grace_period(self):
        check = Check()
        self.assertTrue(check.in_grace_period)
        #A NEW CHECK IS IN THE GRACE PERIOD
