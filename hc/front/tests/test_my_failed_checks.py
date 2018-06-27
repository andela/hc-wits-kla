from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class UserFailedChecksTestCase(BaseTestCase):

    def setUp(self):
        super(UserFailedChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alices Failed Checks")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/unresolved/")
            self.assertEqual(r.status_code, 200)

    def test_check_shows_red_check(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "down"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/unresolved/")

        # Desktop
        self.assertContains(r, "icon-down")

        # Mobile
        self.assertContains(r, "label-danger")

        self.assertContains(r, "Alices Failed Checks")

        self.assertEqual("down", self.check.status)

    def test_failing_checks_without_tag_are_displayed(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "down"
        self.check.tags = "tests productions   "
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/unresolved/")
        self.assertIn("tests", self.check.tags)
