# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-01 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20160923_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='allow_multiple_responses',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
