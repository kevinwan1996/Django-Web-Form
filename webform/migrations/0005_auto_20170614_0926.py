# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-14 13:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webform', '0004_auto_20170613_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 13, 26, 29, 496448, tzinfo=utc)),
        ),
    ]