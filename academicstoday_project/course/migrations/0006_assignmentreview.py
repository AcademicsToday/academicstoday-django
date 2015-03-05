# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20150303_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentReview',
            fields=[
                ('id', models.AutoField(serialize=False, max_length=11, primary_key=True)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=31)),
                ('comment', models.TextField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('post_date', models.DateField(auto_now_add=True, null=True, auto_now=True)),
            ],
            options={
                'db_table': 'at_assignment_reviews',
            },
            bases=(models.Model,),
        ),
    ]
