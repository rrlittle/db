# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 18:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_response', models.DateField(default=datetime.datetime.now)),
                ('boolean_response', models.NullBooleanField()),
                ('date_response', models.DateField(blank=True, null=True)),
                ('text_response', models.CharField(blank=True, max_length=60, null=True)),
                ('int_response', models.IntegerField(blank=True, null=True)),
                ('float_response', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('default_boolean_resp', models.NullBooleanField()),
                ('default_date_resp', models.DateField(blank=True, null=True)),
                ('default_text_resp', models.CharField(blank=True, max_length=60, null=True)),
                ('default_int_resp', models.IntegerField(blank=True, null=True)),
                ('default_float_resp', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('ui', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=60)),
                ('lastName', models.CharField(max_length=60)),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('prompt', models.CharField(max_length=200)),
                ('choice_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Choice_Group')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Survey_Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_order', models.PositiveIntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Question')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Survey')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Measure')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Choice_Group'),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Choice'),
        ),
        migrations.AddField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Person'),
        ),
        migrations.AddField(
            model_name='answer',
            name='survey_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Survey_Question'),
        ),
        migrations.AlterUniqueTogether(
            name='survey_question',
            unique_together=set([('survey', 'question_order')]),
        ),
    ]
