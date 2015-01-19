# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePreivew',
            fields=[
                ('id', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=63)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
            ],
            options={
                'db_table': 'at_course_previews',
            },
            bases=(models.Model,),
        ),
    ]
