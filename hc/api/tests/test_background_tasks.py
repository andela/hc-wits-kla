from hc.api.models import DatabaseBackupTask, EmailTask, SocialMediaTask
from mock import patch
from hc.test import BaseTestCase
from hc.api.tasks import backup_databases, send_emails, post_social_media


class BackgroundTasksTest(BaseTestCase):
    def setUp(self):
        super(BackgroundTasksTest, self).setUp()
        self.task = DatabaseBackupTask(
            owner=self.alice,
            username="admin",
            password="",
            ip_address="127.0.0.1",
            database_kind="mysql",
            backups_period="Daily",
            database_name="db_test"
        )
        self.task.save()

        self.email_task = EmailTask(subject="test", body="test")
        self.email_task.save()

        self.post_task = SocialMediaTask(post="test")
        self.post_task.save()

    @patch("hc.api.tasks.backup_databases")
    def test_backups_database(self, backup):
        backup()
        backup_databases()
        backup.assert_called()

    @patch("hc.api.tasks.send_emails")
    def test_it_sends_emails(self, send_mail):
        send_mail()
        send_emails()
        send_mail.assert_called()

    @patch("hc.api.tasks.post_social_media")
    def test_it_posts_to_twitter(self, post_to_media):
        post_to_media()
        post_social_media()
        post_to_media.assert_called()
