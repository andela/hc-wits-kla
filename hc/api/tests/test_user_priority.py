from hc.test import BaseTestCase
from hc.accounts.models import Member, Priority
from hc.api.models import Check


class TestUserPriorityListTestCase(BaseTestCase):
    """
    Test check can have a priority user's list to be notified according to priority
    """
    def setUp(self):
        super(TestUserPriorityListTestCase, self).setUp()
        self.check1 = Check.objects.create(user=self.alice, name="check1")
        self.check2 = Check.objects.create(user=self.alice, name="check2")
        pass