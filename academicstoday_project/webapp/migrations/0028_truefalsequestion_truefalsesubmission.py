# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_auto_20150227_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('question_num', models.SmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('true_choice', models.CharField(max_length=127, null=True)),
                ('false_choice', models.CharField(max_length=127, null=True)),
                ('answer', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_true_false_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('question_num', models.SmallIntegerField(default=0)),
                ('answer', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now=True, null=True, auto_now_add=True)),
            ],
            options={
                'db_table': 'at_true_false_submissions',
            },
            bases=(models.Model,),
        ),
    ]
