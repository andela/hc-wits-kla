from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.db.models import Q
from django.utils import timezone
from celery.utils.log import get_task_logger
from .models import DatabaseBackupTask, SocialMediaTask, EmailTask

logger = get_task_logger(__name__)

# command to run: celery -A hc worker -l info --beat


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="backup_databases",
    max_retries=5,
    ignore_result=False
)
def backup_databases():
    now = timezone.now()
    task_due = Q(next_run_date__lt=now)
    task_not_scheduled = Q(next_run_date__isnull=True)
    dbs = DatabaseBackupTask.objects.filter(task_due | task_not_scheduled)
    for db in dbs:
        db.backup()


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="post_social_media",
    max_retries=5,
    ignore_result=False
)
def post_social_media():
    task_not_run = Q(run_date__isnull=True)
    tasks = SocialMediaTask.objects.filter(task_not_run)
    for task in tasks:
        task.tweet()


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="send_emails",
    max_retries=5,
    ignore_result=False
)
def send_emails():
    task_not_run = Q(run_date__isnull=True)
    tasks = EmailTask.objects.filter(task_not_run)
    for task in tasks:
        task.run()
