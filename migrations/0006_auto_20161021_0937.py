# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_auto_20161004_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.CharField(default='child', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='studyid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

















