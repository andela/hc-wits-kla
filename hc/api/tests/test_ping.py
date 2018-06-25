from django.test import Client, TestCase

from hc.api.models import Check, Ping


class PingTestCase(TestCase):

    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertEqual(200, r.status_code)

        self.check.refresh_from_db()
        self.assertEqual("up", self.check.status)

        ping = Ping.objects.latest("id")
        self.assertEqual("http", ping.scheme)

    def test_it_handles_bad_uuid(self):
        r = self.client.get("/ping/not-uuid/")
        self.assertEqual(400, r.status_code)

    def test_it_handles_120_char_ua(self):
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/44.0.2403.89 Safari/537.36")

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        self.assertEqual(200, r.status_code)

        ping = Ping.objects.latest("id")
        self.assertEqual(ua, ping.ua)

    def test_it_truncates_long_ua(self):
        ua = "01234567890" * 30

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)

        self.assertEqual(200, r.status_code)

        ping = Ping.objects.latest("id")
        self.assertEqual(200, len(ping.ua))
        self.assertTrue(ua.startswith(ping.ua))

    def test_it_reads_forwarded_ip(self):
        ip = "1.1.1.1"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's remote address
        self.assertEqual(200, r.status_code)
        self.assertEqual("1.1.1.1", ping.remote_addr)

        ip = "1.1.1.1, 2.2.2.2"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        self.assertEqual(200, r.status_code)
        self.assertEqual("1.1.1.1", ping.remote_addr)

    def test_it_reads_forwarded_protocol(self):
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's scheme
        self.assertEqual(200, r.status_code)
        ping = Ping.objects.latest("id")
        self.assertEqual("https", ping.scheme)

    def test_it_never_caches(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        assert "no-cache" in r.get("Cache-Control")

    ### Test that when a ping is made a check with a paused status changes status
    def test_ping_check_changes_status(self):
        self.check.status = "paused"
        r = self.client.post("/ping/%s/" % self.check.code)
        self.assertEqual(200, r.status_code)
        self.check.refresh_from_db()
        self.assertEqual("up", self.check.status)

    ### Test that a post to a ping works
    def test_post_to_ping_works(self):
        r = self.client.post("/ping/%s/" % self.check.code)
        self.assertEqual(200, r.status_code)
        self.check.refresh_from_db()

        ping = Ping.objects.latest("id")
        self.assertEqual("http", ping.scheme)

    ### Test that the csrf_client head works
    def test_csrf_client(self):
        # cross-site request fogery
        csrt_client = Client(enforce_csrf_checks=True)

        r = csrt_client.get("/ping/%s/" % self.check.code)
        self.assertEqual(200, r.status_code)

        self.check.refresh_from_db()
        self.assertEqual("up", self.check.status)

        ping = Ping.objects.latest("id")
        self.assertEqual("http", ping.scheme)
