from hc.api.models import DatabaseBackupTask
from django.urls import reverse
from hc.test import BaseTestCase


class DatabaseBackupTestCase(BaseTestCase):
    def setUp(self):
        super(DatabaseBackupTestCase, self).setUp()
        self.client.login(username="alice@example.org", password="password")
        self.form = {
            "database_kind": "mysql",
            "database_name": "test_db",
            "username": "admin",
            "ip_address": "127.0.0.1",
            "password": "",
            "backups_period": "Daily"
        }

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

    def test_creates_db_backup_task(self):
        res = self.client.post(reverse("hc-scheduled-tasks"), self.form)
        self.assertContains(res, self.form.get("database_name"))

    def test_it_removes_backup_task(self):
        res = self.client.delete(
            reverse("hc-db-task-delete", kwargs={"task_id": self.task.id}))
        self.assertEqual(res.status_code, 200)

    def test_downloads_backup(self):
        res = self.client.get(
            reverse("hc-db-backup", kwargs={"task_id": self.task.id}))
        self.assertEqual(res.status_code, 302)
