# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 17:37
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
                ('int_response', models.IntegerField(blank=True, null=True)),
                ('float_response', models.FloatField(blank=True, null=True)),
                ('date_response', models.DateField(blank=True, null=True)),
                ('boolean_response', models.NullBooleanField()),
                ('text_response', models.CharField(blank=True, max_length=60, null=True)),
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
                ('datatype', models.CharField(max_length=20)),
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
                ('role', models.CharField(max_length=20)),
                ('studyid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('prompt', models.CharField(max_length=200)),
                ('allow_multiple_responses', models.BooleanField()),
                ('missing_value_int', models.IntegerField(blank=True, default=999, null=True)),
                ('missing_value_float', models.FloatField(blank=True, null=True)),
                ('missing_value_boolean', models.NullBooleanField()),
                ('missing_value_date', models.DateField(blank=True, null=True)),
                ('missing_value_text', models.CharField(blank=True, max_length=60, null=True)),
                ('choice_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Choice_Group')),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(max_length=20)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='db.Person')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='db.Person')),
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
                ('unit_of_measure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.Measure')),
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
