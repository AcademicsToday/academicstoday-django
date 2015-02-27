# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20150227_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('due_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('quiz_id', models.PositiveIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_quiz_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='truefalsequestion',
            name='quiz_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='truefalsesubmission',
            name='quiz_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='truefalsequestion',
            name='assignment_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='truefalsesubmission',
            name='assignment_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
