from datetime import timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse
from hc.test import BaseTestCase
from hc.api.models import Check


class MyReportsTestCase(BaseTestCase):
    def setUp(self):
        super(MyReportsTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Test check")
        self.check.last_ping = timezone.now()
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get(reverse("hc-reports"))
            self.assertContains(r, "Test check", status_code=200)

    def test_daily_reports(self):
        self.check.last_ping = timezone.now()
        self.alice.profile.reports_period = "Daily"
        self.alice.profile.save()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(reverse("hc-reports"))
        self.assertContains(r, "Test check", status_code=200)

        # should not contain checks last pinged days ago
        self.check.last_ping = timezone.now() - timedelta(days=3)
        self.check.save()
        res = self.client.get(reverse("hc-reports"))
        self.assertNotContains(res, "Test check")

    def test_weekly_reports(self):
        self.check.last_ping = timezone.now() - timedelta(days=6)
        self.alice.profile.reports_period = "Weekly"
        self.alice.profile.save()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(reverse("hc-reports"))
        self.assertContains(r, "Test check", status_code=200)

        # should not contain checks last pinged a month ago
        self.check.last_ping = timezone.now() - timedelta(days=10)
        self.check.save()
        res = self.client.get(reverse("hc-reports"))
        self.assertNotContains(res, "Test check")

    def test_monthly_reports(self):
        self.check.last_ping = timezone.now() - timedelta(days=20)
        self.alice.profile.reports_period = "Monthly"
        self.alice.profile.save()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get(reverse("hc-reports"))
        self.assertContains(r, "Test check", status_code=200)
