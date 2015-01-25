# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20150125_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('course_id', models.IntegerField(max_length=11)),
                ('user_id', models.IntegerField(max_length=11)),
            ],
            options={
                'db_table': 'at_course_enrollments',
            },
            bases=(models.Model,),
        ),
    ]
