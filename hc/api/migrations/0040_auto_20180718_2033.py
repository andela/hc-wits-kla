# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 20:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_emailtask_socialmediatask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailtask',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='socialmediatask',
            name='owner',
        ),
    ]