from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    # Login and test it redirects already logged in
    def test_logged_in_user_is_redirected(self):
        # login user for the first time
        self.client.login(username="alice@example.org", password="password")

        # login user again
        r = self.client.post("/accounts/check_token/alice/secret-token/")

        # assert that it redirects to hc-checks when already logged in
        self.assertRedirects(r, reverse("hc-checks"))

    # Login with a bad token and check that it redirects
    def test_login_with_bad_token_redirects(self):
        r = self.client.post("/accounts/check_token/alice/bad-token/")
        self.assertRedirects(r, reverse("hc-login"))

    # Any other tests?
