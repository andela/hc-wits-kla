# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='priority',
            name='job',
        ),
        migrations.RemoveField(
            model_name='priority',
            name='member',
        ),
        migrations.DeleteModel(
            name='Priority',
        ),
    ]
