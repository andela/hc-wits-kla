import logging
import time
from datetime import timedelta as td
import datetime

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check
from django.db.models import DateTimeField, ExpressionWrapper, F

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down = query.filter(alert_after__lt=now, status="up")
        going_up = query.filter(alert_after__gt=now, status="down")

        nag = query.annotate(
            time_to_ping=ExpressionWrapper(
                F('last_ping') + F('timeout') + F('grace'),
                output_field=DateTimeField()
            ),
            time_to_nag = ExpressionWrapper(
                F('last_nag') + F('nag'),
                output_field=DateTimeField()
            )
        ).filter(time_to_ping__lt = now, time_to_nag__lte = now)

        nag_last_nag_null = query.annotate(
            time_to_ping=ExpressionWrapper(
                F('last_ping') + F('timeout') + F('grace'),
                output_field=DateTimeField()
            )
        ).filter(time_to_ping__lt = now, last_nag__isnull=True)

        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down.iterator()) + list(going_up.iterator()) + list(nag.iterator()) + list(nag_last_nag_null.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()
        return True

    def handle_one(self, check):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """


        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        check.save()

        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert()
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" % (ch.kind, ch.value, error))

        # Turning a Job to  Nag Mode if its specified time has elapsed
        # time_to_nag = check.nag
        # if check.last_nag:
        #     time_to_nag = time_to_nag + check.last_nag

        if check.nag_mode == 'off':
            check.nag_mode = 'on'
        check.last_nag = timezone.now()
        check.save()

        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)
                # self.nag_user()
