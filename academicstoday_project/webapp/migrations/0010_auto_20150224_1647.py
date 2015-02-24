# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20150223_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('course_id', models.IntegerField(max_length=11)),
                ('type', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'at_assignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('question_num', models.SmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_essay_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('user_id', models.BigIntegerField()),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('file_path', models.FilePathField()),
            ],
            options={
                'db_table': 'at_essay_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('selected', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'at_multiple_choice_answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceOption',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('choice', models.CharField(max_length=1)),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_multiple_choice_options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('question_num', models.SmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_multiple_choice_question',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('user_id', models.BigIntegerField()),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('selected', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'at_multiple_choice_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseQuestion',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('question_num', models.SmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_response_question',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseSubmission',
            fields=[
                ('id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('user_id', models.BigIntegerField()),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('response', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_response_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='courseenrollment',
            name='user_id',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
    ]
