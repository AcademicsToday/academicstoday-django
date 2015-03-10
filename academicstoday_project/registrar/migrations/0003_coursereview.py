# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150310_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField()),
                ('review', models.TextField()),
                ('review_date', models.DateField(auto_now=True, null=True)),
                ('submission_date', models.DateField(null=True, auto_now_add=True)),
                ('courses', models.ManyToManyField(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_reviews',
            },
            bases=(models.Model,),
        ),
    ]
