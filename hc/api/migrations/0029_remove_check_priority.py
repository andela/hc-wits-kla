# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-04 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20180704_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='priority',
        ),
    ]