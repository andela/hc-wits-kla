from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check

class TestAssignedJobsTestCase(BaseTestCase):
    """
    Test Team owner can view and assign jobs to teammates
    """

    def setUp(self):
        super(TestAssignedJobsTestCase, self).setUp()
        self.check1 = Check.objects.create(user = self.alice, name="wits1")
        self.check2 = Check.objects.create(user = self.alice, name="wits2")


    def test_can_assign_job_to_team_member(self):
        """
        Test can assign jobs to a team mate
        """
        url = "/allocate_jobs/"
        #get team member
        bob =  Member.objects.get(user=self.bob)
        payload = {"member_id": bob.id,
        "checks-"+str(self.check1.id): 'on'
        }
        self.client.login(username="alice@example.org", password= "password")
        res = self.client.post(url,data=payload)
        self.assertRedirects(res, "/accounts/profile/")


    def test_method_is_get(self):
        "Test if redirects when request  method is get"
        url = "/allocate_jobs/"
        #login user team owner alice
        self.client.login(username="alice@example.org", password= "password")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


    def test_can_view_jobs_assigned(self):
        """
        Test can assign jobs to a team mate
        """
        url = "/view_assigned_jobs/"
        #get bob who is on alice's team
        bob = Member.objects.get(user=self.bob)
        #get team checks
        team_checks = Check.objects.filter(user=self.alice)
        payload = {
            "member_id": bob.id,
            "checks": team_checks
        }
        self.client.login(username="alice@example.org", password= "password")
        res = self.client.post(url,data=payload)
        self.assertEqual(res.status_code, 200)
