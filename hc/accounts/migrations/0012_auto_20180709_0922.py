# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-09 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_merge_20180709_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reports_period',
            field=models.CharField(default='Monthly', max_length=10),
        ),
    ]
