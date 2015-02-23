# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('week_num', models.IntegerField(max_length=7)),
                ('title', models.CharField(max_length=31)),
                ('description', models.TextField()),
                ('youtube_url', models.URLField(default='')),
                ('vimeo_url', models.URLField(default='')),
                ('bliptv_url', models.URLField(default='')),
                ('preferred_service', models.CharField(max_length=31)),
            ],
            options={
                'db_table': 'at_lectures',
            },
            bases=(models.Model,),
        ),
    ]
