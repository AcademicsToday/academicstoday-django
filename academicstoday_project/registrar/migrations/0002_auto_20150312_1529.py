# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EssaySubmissionReview',
            fields=[
                ('review_id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('marks', models.PositiveSmallIntegerField(choices=[(0, '0 Star'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=0)),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True, auto_now_add=True)),
                ('assignment', models.ForeignKey(null=True, to='registrar.Assignment')),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('exam', models.ForeignKey(null=True, to='registrar.Exam')),
                ('question', models.ForeignKey(to='registrar.EssayQuestion')),
                ('quiz', models.ForeignKey(null=True, to='registrar.Quiz')),
                ('student', models.ForeignKey(to='registrar.Student')),
                ('submission', models.ForeignKey(to='registrar.EssaySubmission')),
            ],
            options={
                'db_table': 'at_essay_submission_reviews',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='assignmentreview',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='assignmentreview',
            name='course',
        ),
        migrations.RemoveField(
            model_name='assignmentreview',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='assignmentreview',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='assignmentreview',
            name='student',
        ),
        migrations.DeleteModel(
            name='AssignmentReview',
        ),
    ]
