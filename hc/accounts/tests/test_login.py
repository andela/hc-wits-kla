from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from hc.api.models import Check, User


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302

        # Assert that a user was created
        user = User.objects.filter(email=form.get("email")).first()
        self.assertEqual(user.email, form.get('email'))

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')

        # Assert contents of the email body
        self.assertIn("To log into healthchecks.io, please open the link below:",
                      mail.outbox[0].body)

        # Assert that check is associated with the new user

        # find check associated  to the user
        associated_check = Check.objects.filter(
            user__email__contains=user.email).first()

        self.assertEqual(check, associated_check)

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        # Any other tests?

    def test_login_it_redirects(self):
        """
        tests that a succcessfully logged in user is redirected to hc-hecks route
        """
        email = "alice@example.org"
        password = "password"
        user = User(email=email)
        user.set_password(password)
        user.save()

        form = {'email': email, 'password': password}
        r = self.client.post(reverse('hc-login'), form)
        self.assertRedirects(r, reverse("hc-checks"))
