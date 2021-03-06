# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-05 10:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0027_check_nag'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='last_nag',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='check',
            name='nag_mode',
            field=models.CharField(choices=[(b'on', b'On'), (b'off', b'Off')], default=b'off', max_length=4),
        ),
        migrations.AlterIndexTogether(
            name='check',
            index_together=set([('status', 'user', 'alert_after', 'nag_mode')]),
        ),
    ]
