# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 08:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_priority'),
    ]

    operations = [
        migrations.RenameField(
            model_name='priority',
            old_name='user',
            new_name='member',
        ),
    ]
