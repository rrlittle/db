# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice_group',
            name='datatype',
            field=models.CharField(default='radio', max_length=20),
            preserve_default=False,
        ),
    ]