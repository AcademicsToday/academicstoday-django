# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150125_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, max_length=11, primary_key=True)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=63)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
                ('paragraph_one', models.CharField(max_length=255)),
                ('paragraph_two', models.CharField(max_length=255)),
                ('paragraph_three', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
            ],
            options={
                'db_table': 'at_course',
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='CourseEnrollmentInfo',
        ),
    ]
