# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-14 17:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webform', '0011_auto_20170614_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/documents')),
            ],
        ),
        migrations.AlterField(
            model_name='state',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 17, 48, 12, 930873, tzinfo=utc)),
        ),
    ]
