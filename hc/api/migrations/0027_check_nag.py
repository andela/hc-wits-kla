# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-03 12:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag',
            field=models.DurationField(default=datetime.timedelta(0, 600)),
        ),
    ]