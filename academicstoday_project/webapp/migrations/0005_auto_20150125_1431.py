# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150125_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEnrollmentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, max_length=11, serialize=False)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=63)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
                ('paragraph_one', models.CharField(max_length=255)),
                ('paragraph_two', models.CharField(max_length=255)),
                ('paragraph_three', models.CharField(max_length=255)),
                ('paragraph_four', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
            ],
            options={
                'db_table': 'at_course_entrollment_infos',
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
