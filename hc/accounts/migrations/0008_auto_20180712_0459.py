# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-12 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_reports_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reports_period',
            field=models.CharField(default=b'Monthly', max_length=10),
        ),
    ]
