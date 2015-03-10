# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0005_auto_20150310_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSubmission',
            fields=[
                ('review_id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=2)),
                ('review', models.TextField()),
                ('review_date', models.DateField(null=True, auto_now=True)),
                ('submission_date', models.DateField(null=True, auto_now_add=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='coursereviewsubmission',
            name='course',
        ),
        migrations.DeleteModel(
            name='CourseReviewSubmission',
        ),
    ]
