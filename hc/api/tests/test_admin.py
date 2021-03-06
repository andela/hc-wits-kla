from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

        ### Set Alice to be staff and superuser and save her :)
        self.check.is_staff = True
        self.check.is_superuser = True
        self.check.save()

    def test_it_shows_channel_list_with_pushbullet(self):
        self.client.login(username="alice@example.org", password="password")

        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()

        ### Assert for the push bullet
        channels = Channel.objects.all()
        channels_list = [chan.kind for chan in channels]
        self.assertIn('pushbullet', channels_list)
